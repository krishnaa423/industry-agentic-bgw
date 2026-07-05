import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import SourceSpec
from paths import MANUALS_STORE_DIR, PAPERS_STORE_DIR, SOURCES_DIR


EMBEDDING_MODEL = "text-embedding-3-small"


def source_path(source_name: str) -> Path:
    return SOURCES_DIR / f"{source_name}.txt"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def reset_store_directory(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def build_documents(source_specs: list[SourceSpec], source_kind: str) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=180,
        separators=["\n\n", "\n", ". ", " "],
    )
    documents: list[Document] = []
    for spec in source_specs:
        if spec.kind != source_kind:
            continue
        path = source_path(spec.name)
        text = load_text(path)
        for chunk_index, chunk in enumerate(text_splitter.split_text(text)):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source_name": spec.name,
                        "source_kind": spec.kind,
                        "source_url": spec.url,
                        "chunk_index": chunk_index,
                    },
                )
            )
    return documents


def build_vector_store(source_specs: list[SourceSpec], source_kind: str) -> int:
    target_dir = MANUALS_STORE_DIR if source_kind == "manual" else PAPERS_STORE_DIR
    collection_name = "manuals" if source_kind == "manual" else "papers"
    reset_store_directory(target_dir)
    documents = build_documents(source_specs, source_kind)
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(target_dir),
        collection_name=collection_name,
    )
    return store._collection.count()


def load_vector_store(source_kind: str) -> Chroma:
    target_dir = MANUALS_STORE_DIR if source_kind == "manual" else PAPERS_STORE_DIR
    collection_name = "manuals" if source_kind == "manual" else "papers"
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=str(target_dir),
        collection_name=collection_name,
        embedding_function=embeddings,
    )


def retrieve_context(source_kind: str, query: str, limit: int = 4) -> list[Document]:
    store = load_vector_store(source_kind)
    return store.similarity_search(query, k=limit)


def format_documents(documents: list[Document]) -> list[str]:
    formatted = []
    for document in documents:
        source_name = document.metadata.get("source_name", "unknown")
        excerpt = document.page_content.strip()
        formatted.append(f"[{source_name}]\n{excerpt}")
    return formatted


def vector_store_counts() -> dict[str, int]:
    return {
        "manuals": load_vector_store("manual")._collection.count(),
        "papers": load_vector_store("paper")._collection.count(),
    }
