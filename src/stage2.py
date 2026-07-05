import re

from langchain_openai import ChatOpenAI

from models import Stage2Plan
from paths import STAGE2_PLAN_PATH, STAGE2_REPORT_PATH
from plan_helpers import make_missing_items, normalize_field, shorten_report_text
from retrieval_store import format_documents, retrieve_context, source_path, load_text


def build_paper_evidence_bundle() -> str:
    queries = [
        "LiF first-principles calculations Quantum Espresso EPW BerkeleyGW Wannier90",
        "100 Ry cutoff self-consistent threshold DFPT threshold dielectric matrix cutoff",
        "COHSEX 5 valence 195 conduction 14.7 eV band gap",
        "BSE kernel 3 valence 7 conduction 8x8x8 k-grid",
    ]
    sections = []
    for query in queries:
        documents = retrieve_context("paper", query, limit=3)
        sections.append(f"[query] {query}")
        sections.extend(format_documents(documents))
        sections.append("")
    return "\n".join(sections).strip()


def apply_regex_overrides(plan: Stage2Plan, paper_text: str) -> None:
    if "first-principles calculations of excitonic polarons for LiF" in paper_text:
        normalize_field(
            plan,
            "material",
            "LiF",
            "first-principles calculations of excitonic polarons for LiF",
            "Target material identified directly from the first-principles section.",
        )

    if "perform DFT and DFPT calculations using the Quantum Espresso package" in paper_text:
        normalize_field(
            plan,
            "dft_code",
            "Quantum Espresso",
            "perform DFT and DFPT calculations using the Quantum Espresso package",
            "DFT and DFPT software named explicitly in the paper.",
        )

    patterns = {
        "pw_cutoff_ry": (
            r"planewaves kinetic energy cutoff of\s+([0-9]+ Ry)",
            "Plane-wave cutoff parsed directly from the paper.",
        ),
        "scf_conv_thr_ry": (
            r"self-consistent calculations is\s+10\s*−\s*12.*?Ry",
            "SCF threshold parsed directly from the paper.",
        ),
        "dfpt_conv_thr_ry2": (
            r"DFPT the convergence threshold is\s+10\s*−\s*14.*?Ry\)\s*2",
            "DFPT threshold parsed directly from the paper.",
        ),
        "dielectric_cutoff_ry": (
            r"dielectric matrix to\s+([0-9]+ Ry)",
            "Dielectric cutoff parsed directly from the paper.",
        ),
        "quasiparticle_gap_ev": (
            r"band gap of\s+([0-9.]+ eV)",
            "Quasiparticle gap parsed directly from the paper.",
        ),
    }

    for field_name, (pattern, notes) in patterns.items():
        match = re.search(pattern, paper_text, flags=re.DOTALL)
        if not match:
            continue
        value = match.group(1) if match.lastindex else match.group(0)
        evidence = " ".join(match.group(0).split())
        if field_name == "scf_conv_thr_ry":
            value = "10^-12 Ry"
        elif field_name == "dfpt_conv_thr_ry2":
            value = "10^-14 Ry^2"
        normalize_field(plan, field_name, value, evidence, notes)

    sigma_match = re.search(
        r"include\s+([0-9]+)\s+valence bands and\s+([0-9]+)\s+conduction bands\..*?self-energy",
        paper_text,
        flags=re.DOTALL,
    )
    if sigma_match:
        normalize_field(
            plan,
            "sigma_valence_bands",
            sigma_match.group(1),
            " ".join(sigma_match.group(0).split()),
            "Sigma/GW valence band count parsed from the self-energy setup sentence.",
        )
        normalize_field(
            plan,
            "sigma_conduction_bands",
            sigma_match.group(2),
            " ".join(sigma_match.group(0).split()),
            "Sigma/GW conduction band count parsed from the self-energy setup sentence.",
        )

    kernel_match = re.search(
        r"BSE kernel is constructed using\s+([0-9]+)\s+valence bands and\s+([0-9]+)\s+conduction bands",
        paper_text,
        flags=re.DOTALL,
    )
    if kernel_match:
        normalize_field(
            plan,
            "kernel_valence_bands",
            kernel_match.group(1),
            " ".join(kernel_match.group(0).split()),
            "BSE kernel valence band count parsed directly from the paper.",
        )
        normalize_field(
            plan,
            "kernel_conduction_bands",
            kernel_match.group(2),
            " ".join(kernel_match.group(0).split()),
            "BSE kernel conduction band count parsed directly from the paper.",
        )

    supercell_match = re.search(
        r"lowest-energy free exciton state, rendered in an\s+([0-9]+\s*×\s*[0-9]+\s*×\s*[0-9]+)\s+supercell",
        paper_text,
        flags=re.DOTALL,
    )
    if supercell_match:
        supercell_value = supercell_match.group(1).replace(" ", "")
        normalize_field(
            plan,
            "supercell_hint",
            f"{supercell_value} supercell for exciton charge density visualization",
            " ".join(supercell_match.group(0).split()),
            "Supercell hint parsed from the exciton-density visualization discussion.",
        )

    bse_grid_match = re.search(
        r"lineshape converges when a\s+([0-9]+\s*×\s*[0-9]+\s*×\s*[0-9]+).*?k-grid is used",
        paper_text,
        flags=re.DOTALL,
    )
    if bse_grid_match:
        normalize_field(
            plan,
            "bse_k_grid",
            bse_grid_match.group(1).replace(" ", ""),
            " ".join(bse_grid_match.group(0).split()),
            "BSE k-grid parsed from the Brillouin-zone convergence discussion.",
        )


def run_stage2_extract() -> None:
    paper_text = load_text(source_path("paper_lif_excitonic_polarons_arxiv_html"))
    evidence_bundle = build_paper_evidence_bundle()
    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
    structured_model = model.with_structured_output(Stage2Plan)
    plan = structured_model.invoke(
        f"""
You are extracting a structured workflow summary from retrieved paper chunks.
Use only the supplied evidence.
Do not invent exact values that are not supported by the evidence.
If a field is not explicitly available, mark status="missing" and leave value null.
If a value is weakly implied but not exact, you may mark status="inferred" and explain why.
For status, use only: found, inferred, missing.
Keep evidence short and focused.

Interpretation guidance:
- material is the target material in the first-principles section
- study_goal is one sentence
- overall_notes should explicitly say this is a starter workflow summary, not a reproduction package

Retrieved paper evidence:
{evidence_bundle}
""".strip()
    )
    apply_regex_overrides(plan, paper_text)
    plan.missing_items = make_missing_items(plan)
    STAGE2_PLAN_PATH.write_text(plan.model_dump_json(indent=2), encoding="utf-8")
    print(f"Wrote plan: {STAGE2_PLAN_PATH.name}")


def run_stage2_check() -> None:
    plan = Stage2Plan.model_validate_json(STAGE2_PLAN_PATH.read_text(encoding="utf-8"))
    field_names = [
        "material",
        "study_goal",
        "dft_code",
        "xc_functional",
        "pseudopotentials",
        "pw_cutoff_ry",
        "scf_conv_thr_ry",
        "dfpt_conv_thr_ry2",
        "epw_code",
        "wannier_code",
        "gw_code",
        "dielectric_cutoff_ry",
        "sigma_valence_bands",
        "sigma_conduction_bands",
        "sigma_self_energy_method",
        "quasiparticle_gap_ev",
        "kernel_valence_bands",
        "kernel_conduction_bands",
        "bse_k_grid",
        "supercell_hint",
    ]

    report_lines = [
        "# Stage 2 Report",
        "",
        "This report checks the paper-store retrieval and structured extraction stage.",
        "",
        "## Workflow Flags",
        "",
        f"- uses_dft: {plan.uses_dft}",
        f"- uses_dfpt: {plan.uses_dfpt}",
        f"- uses_epw: {plan.uses_epw}",
        f"- uses_gw: {plan.uses_gw}",
        f"- uses_bse: {plan.uses_bse}",
        "",
        "## Extracted Fields",
        "",
    ]

    for field_name in field_names:
        field = getattr(plan, field_name)
        report_lines.extend(
            [
                f"### {field_name}",
                f"- status: {field.status}",
                f"- value: {field.value!r}",
                f"- notes: {field.notes or '(none)'}",
                "- evidence:",
                "```text",
                shorten_report_text(field.evidence or "(none)"),
                "```",
                "",
            ]
        )

    missing_lines = [f"- {item}" for item in plan.missing_items] if plan.missing_items else ["- none"]
    report_lines.extend(
        [
            "## Missing Items",
            "",
            *missing_lines,
            "",
            "## Overall Notes",
            "",
            plan.overall_notes,
            "",
        ]
    )
    STAGE2_REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote report: {STAGE2_REPORT_PATH.name}")
    print(f"Missing field count: {len(plan.missing_items)}")

