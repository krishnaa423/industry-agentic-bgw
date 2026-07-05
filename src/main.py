import argparse

from stage1 import run_stage1_check, run_stage1_fetch
from stage2 import run_stage2_check, run_stage2_extract
from stage3 import run_stage3_check, run_stage3_generate
from stage4 import run_stage4_check, run_stage4_generate
from stage5 import run_stage5_check, run_stage5_generate


COMMAND_HANDLERS = {
    "stage1-fetch": run_stage1_fetch,
    "stage1-check": run_stage1_check,
    "stage2-extract": run_stage2_extract,
    "stage2-check": run_stage2_check,
    "stage3-generate": run_stage3_generate,
    "stage3-check": run_stage3_check,
    "stage4-generate": run_stage4_generate,
    "stage4-check": run_stage4_check,
    "stage5-generate": run_stage5_generate,
    "stage5-check": run_stage5_check,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage-by-stage retrieval and starter-input pipeline for QE, EPW, and BerkeleyGW."
    )
    parser.add_argument("command", choices=sorted(COMMAND_HANDLERS), help="Stage action to run.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    COMMAND_HANDLERS[args.command]()


if __name__ == "__main__":
    main()
