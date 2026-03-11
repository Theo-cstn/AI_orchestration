"""
PDF Ingestion Pipeline
======================
PDF → pages → chunks → embeddings → FAISS vector store

Steps:
    1. Load PDF (PyPDFLoader)
    2. Split into chunks (RecursiveCharacterTextSplitter)
    3. Create embeddings (GoogleGenerativeAIEmbeddings)
    4. Store in FAISS (persisted to disk)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Path where the FAISS index is persisted
FAISS_INDEX_PATH = Path(__file__).parent.parent / "data" / "faiss_index"

# Embedding model
EMBEDDING_MODEL = "models/gemini-embedding-001"

# Chunking parameters (can be tuned — good topic for oral demo)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def build_vectorstore(pdf_path: str) -> FAISS:
    """
    Full ingestion pipeline:
      1. Load PDF
      2. Split into chunks
      3. Embed with Google Generative AI
      4. Store in FAISS (also saved to disk)

    Args:
        pdf_path: Absolute or relative path to the PDF file.

    Returns:
        FAISS vector store (in-memory, also persisted to disk).
    """
    pdf_path = str(Path(pdf_path).resolve())

    # ── 1. Load PDF ────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"📄 [RAG Ingestion] Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"   ✅ Pages loaded: {len(documents)}")

    # ── 2. Split into chunks ───────────────────────────────────────────────────
    print(f"\n✂️  [RAG Ingestion] Splitting into chunks...")
    print(f"   chunk_size={CHUNK_SIZE}, chunk_overlap={CHUNK_OVERLAP}")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    docs = splitter.split_documents(documents)
    print(f"   ✅ Chunks created: {len(docs)}")

    # Preview first chunk
    if docs:
        preview = docs[0].page_content[:150].replace("\n", " ")
        print(f"   📝 First chunk preview: '{preview}...'")

    # ── 3. Create embeddings ───────────────────────────────────────────────────
    print(f"\n🔢 [RAG Ingestion] Creating embeddings...")
    print(f"   Model: {EMBEDDING_MODEL}")
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    # ── 4. Build FAISS vector store ────────────────────────────────────────────
    print(f"\n🗄️  [RAG Ingestion] Building FAISS vector store...")
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Persist to disk
    FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(FAISS_INDEX_PATH))
    print(f"   ✅ Vector store saved to: {FAISS_INDEX_PATH}")
    print(f"{'='*60}\n")

    return vectorstore
