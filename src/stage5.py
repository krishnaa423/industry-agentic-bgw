from models import Stage2Plan, Stage5Artifacts
from paths import STAGE2_PLAN_PATH, STAGE5_OUTPUT_DIR, STAGE5_PAYLOAD_PATH, STAGE5_REPORT_PATH
from plan_helpers import parse_grid_triplet
from retrieval_store import format_documents, retrieve_context


def load_stage2_plan() -> Stage2Plan:
    return Stage2Plan.model_validate_json(STAGE2_PLAN_PATH.read_text(encoding="utf-8"))


def run_stage5_generate() -> None:
    plan = load_stage2_plan()
    k1, k2, k3 = parse_grid_triplet(plan.bse_k_grid.value)
    manual_queries = [
        "EPW inputs prefix outdir dvscf_dir elph epbwrite epwwrite wannierize kmaps",
        "EPW inputs nk1 nk2 nk3 nq1 nq2 nq3 nkf1 nkf2 nkf3 nqf1 nqf2 nqf3",
        "EPW inputs nbndsub nbndskip proj num_iter degaussw fsthick efermi_read",
    ]
    retrieved_context = []
    for query in manual_queries:
        retrieved_context.append(f"[query] {query}")
        retrieved_context.extend(format_documents(retrieve_context("manual", query, limit=2)))

    epw_in = "\n".join(
        [
            "&inputepw",
            "  prefix      = 'LiF'",
            "  outdir      = 'tmp/'",
            "  dvscf_dir   = 'tmp/'",
            "  elph        = .true.",
            "  epbwrite    = .true.",
            "  epwwrite    = .true.",
            "  wannierize  = .true.",
            "  kmaps       = .true.",
            f"  nk1         = {k1}",
            f"  nk2         = {k2}",
            f"  nk3         = {k3}",
            f"  nq1         = {k1}",
            f"  nq2         = {k2}",
            f"  nq3         = {k3}",
            f"  nkf1        = {k1}",
            f"  nkf2        = {k2}",
            f"  nkf3        = {k3}",
            f"  nqf1        = {k1}",
            f"  nqf2        = {k2}",
            f"  nqf3        = {k3}",
            "  nbndsub     = 10",
            "  nbndskip    = 0",
            "  proj(1)     = 'random'",
            "  num_iter    = 500",
            "  degaussw    = 0.01",
            "  fsthick     = 0.40",
            "  efermi_read = .false.",
            "/",
        ]
    )

    artifacts = Stage5Artifacts(
        epw_in=epw_in,
        assumptions=[
            "The EPW coarse and fine meshes are all set to 8x8x8 as a conservative carryover from the paper's reported 8x8x8 BSE convergence context.",
            "The EPW file enables elph, epbwrite, epwwrite, and wannierize because the paper explicitly uses EPW and Wannier90, but does not provide a ready-to-run EPW input block.",
            "The nbndsub value is set to 10 as a starter Wannier subspace placeholder based on the paper's 3 valence + 7 conduction BSE window.",
            "The proj(1) = 'random' setting is taken from the EPW input reference as the simplest starter projection choice.",
            "The degaussw and fsthick values are heuristic starter values, not paper-derived values.",
        ],
        unresolved_items=[
            "The actual EPW Wannier subspace, projections, and frozen-window choices still need to be chosen from a trusted LiF workflow or convergence study.",
            "The exact EPW coarse and fine meshes should be confirmed against the phonon and interpolation setup used for the excitonic-polaron workflow.",
            "The exact dvscf_dir layout and whether additional EPW read/write flags are needed depends on how the QE and PH outputs are organized in the real workflow.",
        ],
        doc_basis=[
            "EPW input keywords: prefix, outdir, dvscf_dir, elph, epbwrite, epwwrite, wannierize, kmaps, nk1/nk2/nk3, nq1/nq2/nq3, nkf1/nkf2/nkf3, nqf1/nqf2/nqf3, nbndsub, nbndskip, proj(:), num_iter, degaussw, fsthick, efermi_read.",
            "Paper-derived values: EPW and Wannier90 are used, and the broader workflow reports an 8x8x8 converged BSE k-grid that is reused here as a conservative mesh hint.",
        ],
        retrieved_context=retrieved_context,
        overall_notes="Stage 5 uses manuals-store retrieval to ground EPW keyword choices, but this remains the most assumption-heavy starter file in the pipeline.",
    )

    (STAGE5_OUTPUT_DIR / "epw.in").write_text(artifacts.epw_in.strip() + "\n", encoding="utf-8")
    STAGE5_PAYLOAD_PATH.write_text(artifacts.model_dump_json(indent=2), encoding="utf-8")
    print(f"Wrote payload: {STAGE5_PAYLOAD_PATH.name}")


def run_stage5_check() -> None:
    artifacts = Stage5Artifacts.model_validate_json(STAGE5_PAYLOAD_PATH.read_text(encoding="utf-8"))
    text = (STAGE5_OUTPUT_DIR / "epw.in").read_text(encoding="utf-8")
    markers = [
        "prefix      = 'LiF'",
        "wannierize  = .true.",
        "elph        = .true.",
        "epbwrite    = .true.",
        "nk1         = 8",
        "nq1         = 8",
        "proj(1)     = 'random'",
    ]
    missing_markers = [marker for marker in markers if marker not in text]
    status = "ok" if not missing_markers else "needs_review"

    report_lines = [
        "# Stage 5 Report",
        "",
        "This report checks the starter-file generation stage for epw.in.",
        "",
        "## File Check",
        "",
        "### epw.in",
        f"- status: {status}",
        f"- missing_markers: {missing_markers if missing_markers else 'none'}",
        "- preview:",
        "```text",
        text,
        "```",
        "",
        "## Retrieved Context",
        "",
    ]
    report_lines.extend([f"- {line}" for line in artifacts.retrieved_context])
    report_lines.extend(["", "## Assumptions", ""])
    report_lines.extend([f"- {item}" for item in artifacts.assumptions])
    report_lines.extend(["", "## Unresolved Items", ""])
    report_lines.extend([f"- {item}" for item in artifacts.unresolved_items])
    report_lines.extend(["", "## Documentation Basis", ""])
    report_lines.extend([f"- {item}" for item in artifacts.doc_basis])
    report_lines.extend(["", "## Overall Notes", "", artifacts.overall_notes, ""])
    STAGE5_REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote report: {STAGE5_REPORT_PATH.name}")
    if missing_markers:
        print(f"Checks needing review: {missing_markers}")
    else:
        print("All Stage 5 checks passed.")

