from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
SOURCES_DIR = DOCS_DIR / "sources"
VECTOR_STORE_DIR = DOCS_DIR / "vector_store"
MANUALS_STORE_DIR = VECTOR_STORE_DIR / "manuals"
PAPERS_STORE_DIR = VECTOR_STORE_DIR / "papers"

STAGE1_MANIFEST_PATH = DOCS_DIR / "stage1_manifest.json"
STAGE1_REPORT_PATH = DOCS_DIR / "stage1_report.md"
STAGE2_PLAN_PATH = DOCS_DIR / "stage2_plan.json"
STAGE2_REPORT_PATH = DOCS_DIR / "stage2_report.md"
STAGE3_OUTPUT_DIR = DOCS_DIR / "stage3_outputs"
STAGE3_PAYLOAD_PATH = DOCS_DIR / "stage3_payload.json"
STAGE3_REPORT_PATH = DOCS_DIR / "stage3_report.md"
STAGE4_OUTPUT_DIR = DOCS_DIR / "stage4_outputs"
STAGE4_PAYLOAD_PATH = DOCS_DIR / "stage4_payload.json"
STAGE4_REPORT_PATH = DOCS_DIR / "stage4_report.md"
STAGE5_OUTPUT_DIR = DOCS_DIR / "stage5_outputs"
STAGE5_PAYLOAD_PATH = DOCS_DIR / "stage5_payload.json"
STAGE5_REPORT_PATH = DOCS_DIR / "stage5_report.md"

