import re

import requests
from bs4 import BeautifulSoup

from paths import (
    MANUALS_STORE_DIR,
    PAPERS_STORE_DIR,
    SOURCES_DIR,
    STAGE3_OUTPUT_DIR,
    STAGE4_OUTPUT_DIR,
    STAGE5_OUTPUT_DIR,
    VECTOR_STORE_DIR,
)


def ensure_output_directories() -> None:
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    MANUALS_STORE_DIR.mkdir(parents=True, exist_ok=True)
    PAPERS_STORE_DIR.mkdir(parents=True, exist_ok=True)
    STAGE3_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STAGE4_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STAGE5_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_text(text: str) -> str:
    cleaned = text.replace("\xa0", " ")
    cleaned = re.sub(r"\r\n?", "\n", cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return sanitize_text(soup.get_text("\n"))


def fetch_text(url: str) -> tuple[str, int, str]:
    response = requests.get(
        url,
        timeout=(5, 12),
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
    )
    response.raise_for_status()
    return response.text, response.status_code, response.url

