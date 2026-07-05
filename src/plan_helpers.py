import re

from models import PaperField, Stage2Plan


def preview_lines(text: str, limit: int = 8) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:limit])


def shorten_report_text(text: str, width: int = 1200) -> str:
    if len(text) <= width:
        return text
    return text[: width - 4] + " ..."


def parse_grid_triplet(grid_text: str) -> tuple[int, int, int]:
    numbers = [int(number) for number in re.findall(r"\d+", grid_text)]
    if len(numbers) < 3:
        raise ValueError(f"Could not parse grid triplet from {grid_text!r}")
    return numbers[0], numbers[1], numbers[2]


def sigma_band_total(plan: Stage2Plan) -> int:
    return int(plan.sigma_valence_bands.value) + int(plan.sigma_conduction_bands.value)


def make_missing_items(plan: Stage2Plan) -> list[str]:
    missing = []
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
    for field_name in field_names:
        field = getattr(plan, field_name)
        if isinstance(field, PaperField) and field.status == "missing":
            missing.append(field_name)
    return missing


def normalize_field(
    plan: Stage2Plan,
    field_name: str,
    value: str,
    evidence: str,
    notes: str,
) -> None:
    field = getattr(plan, field_name)
    field.value = value
    field.status = "found"
    field.evidence = evidence
    field.notes = notes

