from models import Stage2Plan, Stage3Artifacts
from paths import STAGE2_PLAN_PATH, STAGE3_OUTPUT_DIR, STAGE3_PAYLOAD_PATH, STAGE3_REPORT_PATH
from plan_helpers import parse_grid_triplet, sigma_band_total
from retrieval_store import format_documents, retrieve_context


def load_stage2_plan() -> Stage2Plan:
    return Stage2Plan.model_validate_json(STAGE2_PLAN_PATH.read_text(encoding="utf-8"))


def run_stage3_generate() -> None:
    plan = load_stage2_plan()
    k1, k2, k3 = parse_grid_triplet(plan.bse_k_grid.value)
    total_bands = sigma_band_total(plan)
    manual_queries = [
        "Quantum Espresso INPUT_PW ecutwfc conv_thr prefix pseudo_dir K_POINTS",
        "BerkeleyGW epsilon keywords epsilon_cutoff number_bands frequency_dependence use_wfn_hdf5",
        "BerkeleyGW sigma keywords number_bands screening_semiconductor bare_coulomb_cutoff screened_coulomb_cutoff eqp_corrections",
    ]
    retrieved_context = []
    for query in manual_queries:
        retrieved_context.append(f"[query] {query}")
        retrieved_context.extend(format_documents(retrieve_context("manual", query, limit=2)))

    scf_in = "\n".join(
        [
            "&CONTROL",
            "  calculation='scf',",
            "  prefix='LiF',",
            "  outdir='tmp/',",
            "  pseudo_dir='pseudo/',",
            "  verbosity='high'",
            "/",
            "&SYSTEM",
            "  ibrav=0,",
            "  nat=2,",
            "  ntyp=2,",
            f"  ecutwfc={float(plan.pw_cutoff_ry.value.split()[0]):.1f},",
            "  occupations='fixed'",
            "/",
            "&ELECTRONS",
            "  conv_thr=1.0d-12",
            "/",
            "ATOMIC_SPECIES",
            "  Li 6.94 TODO_LI_PSEUDO",
            "  F  18.998 TODO_F_PSEUDO",
            "",
            "CELL_PARAMETERS angstrom",
            "  TODO_FILL_CELL_VECTOR_1",
            "  TODO_FILL_CELL_VECTOR_2",
            "  TODO_FILL_CELL_VECTOR_3",
            "",
            "ATOMIC_POSITIONS crystal",
            "  TODO_FILL_LI_POSITION",
            "  TODO_FILL_F_POSITION",
            "",
            "K_POINTS automatic",
            f"  {k1} {k2} {k3} 0 0 0",
        ]
    )

    epsilon_inp = "\n".join(
        [
            f"epsilon_cutoff {float(plan.dielectric_cutoff_ry.value.split()[0]):.1f}",
            f"number_bands {total_bands}",
            "frequency_dependence 0",
            "screening_semiconductor",
            "use_wfn_hdf5",
            "verbosity 1",
        ]
    )

    sigma_inp = "\n".join(
        [
            "screening_semiconductor",
            f"number_bands {total_bands}",
            "frequency_dependence 0",
            f"bare_coulomb_cutoff {float(plan.dielectric_cutoff_ry.value.split()[0]):.1f}",
            f"screened_coulomb_cutoff {float(plan.dielectric_cutoff_ry.value.split()[0]):.1f}",
            "eqp_corrections",
            "verbosity 1",
        ]
    )

    artifacts = Stage3Artifacts(
        scf_in=scf_in,
        epsilon_inp=epsilon_inp,
        sigma_inp=sigma_inp,
        assumptions=[
            "The SCF file keeps placeholder pseudopotential filenames because the paper does not specify exact pseudo files.",
            "The SCF file keeps placeholder cell vectors and atomic positions because the retrieved paper evidence does not provide a full crystal structure block.",
            "The SCF k-grid is set to the paper-derived 8x8x8 BSE grid as a conservative starter choice.",
            "The epsilon and sigma files both use 200 bands from the paper's 5 valence + 195 conduction GW setup.",
            "The sigma file uses frequency_dependence 0 as a conservative static/COHSEX-style starter assumption.",
        ],
        unresolved_items=[
            "Exact LiF lattice vectors and fractional coordinates should be supplied before using scf.in.",
            "Exact pseudopotential filenames for Li and F are still required.",
            "The exact BerkeleyGW mapping for the COHSEX choice should be verified against a trusted working example before production use.",
        ],
        doc_basis=[
            "QE INPUT_PW keywords: prefix, pseudo_dir, ecutwfc, conv_thr, K_POINTS.",
            "BerkeleyGW epsilon keywords: epsilon_cutoff, number_bands, frequency_dependence, use_wfn_hdf5.",
            "BerkeleyGW sigma keywords: number_bands, screening_semiconductor, bare_coulomb_cutoff, screened_coulomb_cutoff, frequency_dependence, eqp_corrections.",
            "Paper-derived values: 100 Ry cutoff, 10^-12 Ry SCF threshold, 10 Ry dielectric cutoff, 5 valence + 195 conduction bands, 8x8x8 BSE grid.",
        ],
        retrieved_context=retrieved_context,
        overall_notes="Stage 3 uses the manuals vector store for keyword grounding and the Stage 2 paper plan for exact numerical values, then renders deterministic starter templates.",
    )

    (STAGE3_OUTPUT_DIR / "scf.in").write_text(artifacts.scf_in.strip() + "\n", encoding="utf-8")
    (STAGE3_OUTPUT_DIR / "epsilon.inp").write_text(artifacts.epsilon_inp.strip() + "\n", encoding="utf-8")
    (STAGE3_OUTPUT_DIR / "sigma.inp").write_text(artifacts.sigma_inp.strip() + "\n", encoding="utf-8")
    STAGE3_PAYLOAD_PATH.write_text(artifacts.model_dump_json(indent=2), encoding="utf-8")
    print(f"Wrote payload: {STAGE3_PAYLOAD_PATH.name}")


def run_stage3_check() -> None:
    artifacts = Stage3Artifacts.model_validate_json(STAGE3_PAYLOAD_PATH.read_text(encoding="utf-8"))
    checks = {
        "scf.in": ["calculation='scf'", "ecutwfc=100", "conv_thr=1.0d-12", "K_POINTS automatic"],
        "epsilon.inp": ["epsilon_cutoff 10.0", "number_bands 200", "frequency_dependence 0"],
        "sigma.inp": ["number_bands 200", "screening_semiconductor", "screened_coulomb_cutoff 10.0"],
    }

    report_lines = [
        "# Stage 3 Report",
        "",
        "This report checks the starter-file generation stage for scf.in, epsilon.inp, and sigma.inp.",
        "",
        "## File Checks",
        "",
    ]
    failed = []
    for filename, markers in checks.items():
        path = STAGE3_OUTPUT_DIR / filename
        text = path.read_text(encoding="utf-8")
        missing_markers = [marker for marker in markers if marker not in text]
        status = "ok" if not missing_markers else "needs_review"
        if missing_markers:
            failed.append(f"{filename}: missing markers {missing_markers}")
        report_lines.extend(
            [
                f"### {filename}",
                f"- status: {status}",
                f"- missing_markers: {missing_markers if missing_markers else 'none'}",
                "- preview:",
                "```text",
                text,
                "```",
                "",
            ]
        )

    report_lines.extend(["## Retrieved Context", ""])
    report_lines.extend([f"- {line}" for line in artifacts.retrieved_context])
    report_lines.extend(["", "## Assumptions", ""])
    report_lines.extend([f"- {item}" for item in artifacts.assumptions])
    report_lines.extend(["", "## Unresolved Items", ""])
    report_lines.extend([f"- {item}" for item in artifacts.unresolved_items])
    report_lines.extend(["", "## Documentation Basis", ""])
    report_lines.extend([f"- {item}" for item in artifacts.doc_basis])
    report_lines.extend(["", "## Overall Notes", "", artifacts.overall_notes, ""])
    STAGE3_REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote report: {STAGE3_REPORT_PATH.name}")
    if failed:
        print("Checks needing review:")
        for item in failed:
            print(f"- {item}")
    else:
        print("All Stage 3 checks passed.")

