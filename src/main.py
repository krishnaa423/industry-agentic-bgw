from pathlib import Path

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"


@tool
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def build_vector_store() -> InMemoryVectorStore:
    documents = []
    for path in sorted(DOCS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        documents.append(Document(page_content=text, metadata={"source": path.name}))

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = InMemoryVectorStore(embedding=embeddings)
    vector_store.add_documents(documents)
    return vector_store


VECTOR_STORE = build_vector_store()


@tool
def retrieve_notes(query: str) -> str:
    """Retrieve relevant note snippets from the local text files."""
    docs = VECTOR_STORE.similarity_search(query, k=2)
    chunks = []
    for doc in docs:
        chunks.append(f"source={doc.metadata.get('source', 'unknown')}\n{doc.page_content}")
    return "\n\n".join(chunks)


def main() -> None:
    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0)
    agent = create_agent(
        model=model,
        tools=[add, retrieve_notes],
        system_prompt="Use the retrieval tool for note questions and the add tool for arithmetic.",
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "From the local notes, what toy k-grid and dielectric cutoff are recommended "
                        "for Silicon? Use the retrieval tool and answer briefly."
                    ),
                }
            ]
        }
    )

    for message in result["messages"]:
        content = getattr(message, "content", None)
        if isinstance(content, str) and content.strip():
            print(content)


if __name__ == "__main__":
    main()
