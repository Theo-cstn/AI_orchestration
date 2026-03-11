"""
Vector Store Retriever
======================
Loads the persisted FAISS index and performs similarity search.

Returns chunks with text content + source metadata (page, file).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

FAISS_INDEX_PATH = Path(__file__).parent.parent / "data" / "faiss_index"
EMBEDDING_MODEL = "models/gemini-embedding-001"

# Global cached vectorstore (avoid reloading on every call)
_vectorstore: FAISS | None = None


def _load_vectorstore() -> FAISS:
    """Load the FAISS vector store from disk (cached after first call)."""
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    if not FAISS_INDEX_PATH.exists():
        raise FileNotFoundError(
            f"No FAISS index found at {FAISS_INDEX_PATH}. "
            "Please call build_vectorstore() first to index a PDF."
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    _vectorstore = FAISS.load_local(
        str(FAISS_INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )
    return _vectorstore


def reset_vectorstore_cache() -> None:
    """Force reload of the FAISS index on next call (e.g. after re-ingestion)."""
    global _vectorstore
    _vectorstore = None


def search_vectorstore(query: str, k: int = 4) -> list[dict]:
    """
    Search the vector store for the most relevant document chunks.

    Args:
        query: The question or search query.
        k: Number of top chunks to retrieve.

    Returns:
        List of dicts with keys:
            - "content": chunk text
            - "source": source PDF filename
            - "page": page number (0-indexed)
            - "score": similarity score (lower = more similar for L2)
    """
    print(f"\n🔍 [RAG Retriever] Searching for: '{query}'")
    print(f"   Retrieving top-{k} chunks...")

    vs = _load_vectorstore()
    results = vs.similarity_search_with_score(query, k=k)

    formatted = []
    for i, (doc, score) in enumerate(results):
        chunk = {
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page", "?"),
            "score": round(float(score), 4),
        }
        formatted.append(chunk)
        print(f"\n   ── Chunk {i+1} (score={chunk['score']}) ──")
        print(f"   Page: {chunk['page']} | Source: {Path(chunk['source']).name}")
        print(f"   '{chunk['content'][:120].strip()}...'")

    print(f"\n   ✅ {len(formatted)} chunks retrieved.\n")
    return formatted


def format_chunks_for_agent(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a single string block suitable as agent context.

    Args:
        chunks: Result from search_vectorstore().

    Returns:
        Formatted string with numbered chunks and metadata.
    """
    lines = []
    for i, chunk in enumerate(chunks, 1):
        lines.append(
            f"[Chunk {i} — Page {chunk['page']} | Source: {Path(chunk['source']).name}]"
        )
        lines.append(chunk["content"])
        lines.append("")
    return "\n".join(lines)
