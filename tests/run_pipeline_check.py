import subprocess
import sys
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]
MAIN = REPO_DIR / "src" / "main.py"

COMMANDS = [
    "stage1-fetch",
    "stage1-check",
    "stage2-extract",
    "stage2-check",
    "stage3-generate",
    "stage3-check",
    "stage4-generate",
    "stage4-check",
    "stage5-generate",
    "stage5-check",
]


EXPECTED_MARKERS = {
    REPO_DIR / "docs" / "stage3_outputs" / "scf.in": ["ecutwfc=100.0", "conv_thr=1.0d-12"],
    REPO_DIR / "docs" / "stage3_outputs" / "epsilon.inp": ["epsilon_cutoff 10.0", "number_bands 200"],
    REPO_DIR / "docs" / "stage3_outputs" / "sigma.inp": ["number_bands 200", "screening_semiconductor"],
    REPO_DIR / "docs" / "stage4_outputs" / "dfpt.in": ["tr2_ph=1.0d-14", "nq1=8, nq2=8, nq3=8"],
    REPO_DIR / "docs" / "stage4_outputs" / "kernel.inp": ["number_val_bands 3", "number_cond_bands 7"],
    REPO_DIR / "docs" / "stage4_outputs" / "absorption.inp": ["polarization 1 0 0", "number_cond_bands_fine 7"],
    REPO_DIR / "docs" / "stage5_outputs" / "epw.in": ["wannierize  = .true.", "proj(1)     = 'random'"],
}


def run_command(command: str) -> None:
    subprocess.run(
        [sys.executable, str(MAIN), command],
        cwd=REPO_DIR,
        check=True,
    )


def assert_expected_files() -> None:
    for path, markers in EXPECTED_MARKERS.items():
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                raise AssertionError(f"Missing marker {marker!r} in {path}")


def main() -> None:
    for command in COMMANDS:
        run_command(command)
    assert_expected_files()
    print("Pipeline smoke test passed.")


if __name__ == "__main__":
    main()
