from models import Stage2Plan, Stage4Artifacts
from paths import STAGE2_PLAN_PATH, STAGE4_OUTPUT_DIR, STAGE4_PAYLOAD_PATH, STAGE4_REPORT_PATH
from plan_helpers import parse_grid_triplet
from retrieval_store import format_documents, retrieve_context


def load_stage2_plan() -> Stage2Plan:
    return Stage2Plan.model_validate_json(STAGE2_PLAN_PATH.read_text(encoding="utf-8"))


def run_stage4_generate() -> None:
    plan = load_stage2_plan()
    q1, q2, q3 = parse_grid_triplet(plan.bse_k_grid.value)
    manual_queries = [
        "Quantum Espresso INPUT_PH tr2_ph ldisp nq1 nq2 nq3 fildyn verbosity",
        "BerkeleyGW kernel keywords number_val_bands number_cond_bands screening_semiconductor use_wfn_hdf5",
        "BerkeleyGW absorption keywords number_val_bands_fine number_cond_bands_fine polarization energy_resolution gaussian_broadening",
    ]
    retrieved_context = []
    for query in manual_queries:
        retrieved_context.append(f"[query] {query}")
        retrieved_context.extend(format_documents(retrieve_context("manual", query, limit=2)))

    dfpt_in = "\n".join(
        [
            "LiF DFPT starter calculation",
            "&INPUTPH",
            "  prefix='LiF',",
            "  outdir='tmp/',",
            "  tr2_ph=1.0d-14,",
            "  ldisp=.true.,",
            f"  nq1={q1}, nq2={q2}, nq3={q3},",
            "  fildyn='LiF.dyn',",
            "  verbosity='high'",
            "/",
        ]
    )

    kernel_inp = "\n".join(
        [
            "screening_semiconductor",
            f"number_val_bands {plan.kernel_valence_bands.value}",
            f"number_cond_bands {plan.kernel_conduction_bands.value}",
            "use_wfn_hdf5",
            "verbosity 1",
        ]
    )

    absorption_inp = "\n".join(
        [
            f"number_val_bands_fine {plan.kernel_valence_bands.value}",
            f"number_val_bands_coarse {plan.kernel_valence_bands.value}",
            f"number_cond_bands_fine {plan.kernel_conduction_bands.value}",
            f"number_cond_bands_coarse {plan.kernel_conduction_bands.value}",
            "eqp_corrections",
            "polarization 1 0 0",
            "energy_resolution 0.10",
            "gaussian_broadening",
            "use_wfn_hdf5",
            "verbosity 1",
        ]
    )

    artifacts = Stage4Artifacts(
        dfpt_in=dfpt_in,
        kernel_inp=kernel_inp,
        absorption_inp=absorption_inp,
        assumptions=[
            "The DFPT q-grid is set to 8x8x8 as a conservative carryover from the paper's converged BSE Brillouin-zone grid.",
            "The DFPT file omits material-specific masses and dielectric-response flags because the retrieved evidence does not pin down those exact settings.",
            "The kernel file uses the paper's 3 valence and 7 conduction bands directly.",
            "The absorption file uses the same 3/7 band window on both coarse and fine grids as a starter assumption.",
            "The absorption polarization is set to 1 0 0 as a placeholder because the paper does not specify polarization direction in input-file terms.",
            "The absorption energy_resolution value 0.10 is a heuristic, not a paper-derived value.",
        ],
        unresolved_items=[
            "The exact DFPT q-grid, irreducible-q setup, and whether epsil should be enabled still need confirmation from a trusted working example.",
            "The exact absorption polarization and broadening settings should be confirmed against the target spectrum setup.",
            "The exact kernel/absorption interpolation and exciton-Q settings still need confirmation from a trusted BerkeleyGW example.",
        ],
        doc_basis=[
            "QE INPUT_PH keywords: prefix, tr2_ph, fildyn, ldisp, nq1, nq2, nq3, verbosity.",
            "BerkeleyGW kernel keywords: number_val_bands, number_cond_bands, screening_semiconductor, use_wfn_hdf5, verbosity.",
            "BerkeleyGW absorption keywords: number_val_bands_fine/coarse, number_cond_bands_fine/coarse, eqp_corrections, polarization, energy_resolution, gaussian_broadening, use_wfn_hdf5, verbosity.",
            "Paper-derived values: DFPT threshold 10^-14 Ry^2, kernel bands 3/7, BSE convergence on an 8x8x8 Brillouin-zone grid.",
        ],
        retrieved_context=retrieved_context,
        overall_notes="Stage 4 uses manuals-store retrieval for keyword grounding and Stage 2 paper values for the quantitative starter choices.",
    )

    (STAGE4_OUTPUT_DIR / "dfpt.in").write_text(artifacts.dfpt_in.strip() + "\n", encoding="utf-8")
    (STAGE4_OUTPUT_DIR / "kernel.inp").write_text(artifacts.kernel_inp.strip() + "\n", encoding="utf-8")
    (STAGE4_OUTPUT_DIR / "absorption.inp").write_text(artifacts.absorption_inp.strip() + "\n", encoding="utf-8")
    STAGE4_PAYLOAD_PATH.write_text(artifacts.model_dump_json(indent=2), encoding="utf-8")
    print(f"Wrote payload: {STAGE4_PAYLOAD_PATH.name}")


def run_stage4_check() -> None:
    artifacts = Stage4Artifacts.model_validate_json(STAGE4_PAYLOAD_PATH.read_text(encoding="utf-8"))
    checks = {
        "dfpt.in": ["tr2_ph=1.0d-14", "ldisp=.true.", "nq1=8, nq2=8, nq3=8"],
        "kernel.inp": ["number_val_bands 3", "number_cond_bands 7", "screening_semiconductor"],
        "absorption.inp": ["number_val_bands_fine 3", "number_cond_bands_fine 7", "polarization 1 0 0"],
    }

    report_lines = [
        "# Stage 4 Report",
        "",
        "This report checks the starter-file generation stage for dfpt.in, kernel.inp, and absorption.inp.",
        "",
        "## File Checks",
        "",
    ]
    failed = []
    for filename, markers in checks.items():
        path = STAGE4_OUTPUT_DIR / filename
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
    STAGE4_REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote report: {STAGE4_REPORT_PATH.name}")
    if failed:
        print("Checks needing review:")
        for item in failed:
            print(f"- {item}")
    else:
        print("All Stage 4 checks passed.")

