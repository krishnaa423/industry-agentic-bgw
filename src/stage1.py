import json
from dataclasses import asdict

from io_utils import ensure_output_directories, fetch_text, html_to_text
from paths import STAGE1_MANIFEST_PATH, STAGE1_REPORT_PATH
from plan_helpers import preview_lines
from retrieval_store import source_path, vector_store_counts, build_vector_store
from source_registry import SOURCE_SPECS


def run_stage1_fetch() -> None:
    ensure_output_directories()
    manifest = []
    for source_spec in SOURCE_SPECS:
        print(f"Fetching {source_spec.name} ...", flush=True)
        path = source_path(source_spec.name)
        try:
            raw_text, status_code, final_url = fetch_text(source_spec.url)
            cleaned_text = html_to_text(raw_text)
            path.write_text(cleaned_text, encoding="utf-8")
            manifest.append(
                {
                    **asdict(source_spec),
                    "final_url": final_url,
                    "status_code": status_code,
                    "output_file": str(path),
                    "char_count": len(cleaned_text),
                    "line_count": len(cleaned_text.splitlines()),
                    "error": None,
                }
            )
            print(f"Saved {path.name}: {len(cleaned_text)} chars", flush=True)
        except Exception as exc:
            manifest.append(
                {
                    **asdict(source_spec),
                    "final_url": None,
                    "status_code": None,
                    "output_file": None,
                    "char_count": 0,
                    "line_count": 0,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            print(f"Failed {source_spec.name}: {type(exc).__name__}: {exc}", flush=True)

    STAGE1_MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote manifest: {STAGE1_MANIFEST_PATH.name}")

    manual_count = build_vector_store(SOURCE_SPECS, "manual")
    paper_count = build_vector_store(SOURCE_SPECS, "paper")
    print(f"Built manuals vector store with {manual_count} chunks")
    print(f"Built papers vector store with {paper_count} chunks")


def run_stage1_check() -> None:
    ensure_output_directories()
    rows = []
    missing_sources = []
    for source_spec in SOURCE_SPECS:
        path = source_path(source_spec.name)
        if not path.exists():
            missing_sources.append(source_spec.name)
            continue
        text = path.read_text(encoding="utf-8")
        rows.append(
            {
                "name": source_spec.name,
                "kind": source_spec.kind,
                "chars": len(text),
                "lines": len(text.splitlines()),
                "preview": preview_lines(text),
            }
        )

    store_counts = vector_store_counts()
    report_lines = [
        "# Stage 1 Report",
        "",
        "This report checks the curated local source corpus and the persistent vector stores.",
        "",
    ]

    if missing_sources:
        report_lines.extend(["## Missing Sources", ""])
        report_lines.extend([f"- {source_name}" for source_name in missing_sources])
        report_lines.append("")

    report_lines.extend(
        [
            "## Vector Stores",
            "",
            f"- manuals_store_chunks: {store_counts['manuals']}",
            f"- papers_store_chunks: {store_counts['papers']}",
            "",
            "## Source Summary",
            "",
        ]
    )

    for row in rows:
        report_lines.extend(
            [
                f"### {row['name']}",
                f"- kind: {row['kind']}",
                f"- chars: {row['chars']}",
                f"- lines: {row['lines']}",
                "- preview:",
                "```text",
                row["preview"],
                "```",
                "",
            ]
        )

    if STAGE1_MANIFEST_PATH.exists():
        manifest = json.loads(STAGE1_MANIFEST_PATH.read_text(encoding="utf-8"))
        failures = [item for item in manifest if item.get("error")]
        if failures:
            report_lines.extend(["## Fetch Failures", ""])
            for item in failures:
                report_lines.extend(
                    [
                        f"### {item['name']}",
                        f"- url: {item['url']}",
                        f"- error: {item['error']}",
                        "",
                    ]
                )

    STAGE1_REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote report: {STAGE1_REPORT_PATH.name}")
    if missing_sources:
        print(f"Missing sources: {', '.join(missing_sources)}")
    else:
        print(f"All {len(rows)} sources are present.")

