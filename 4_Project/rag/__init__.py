"""
RAG (Retrieval-Augmented Generation) module for PDF document processing.

Exposes:
    - build_vectorstore(pdf_path): ingest a PDF and return a FAISS vector store
    - search_vectorstore(query, k): search the persisted FAISS index
"""

from rag.ingest import build_vectorstore
from rag.retriever import search_vectorstore

__all__ = ["build_vectorstore", "search_vectorstore"]
