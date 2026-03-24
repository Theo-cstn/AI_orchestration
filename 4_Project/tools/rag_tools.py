"""
CrewAI RAG Tools
================
Exposes two tools for agents to use:
  - index_pdf_tool: ingest a PDF into the vector store
  - search_pdf_tool: search the vector store and return formatted results
"""

from crewai.tools import tool
from rag.ingest import build_vectorstore
from rag.retriever import search_vectorstore, format_chunks_for_agent, reset_vectorstore_cache


@tool("Index PDF Document")
def index_pdf_tool(pdf_path: str) -> str:
    """
    Load and index a PDF document into the vector store.
    This tool must be called before searching the document.

    Args:
        pdf_path: The absolute or relative path to the PDF file to index.

    Returns:
        A confirmation message with the number of chunks indexed.
    """
    try:
        reset_vectorstore_cache()
        build_vectorstore(pdf_path)
        return (
            f"✅ PDF successfully indexed: '{pdf_path}'. "
            "The vector store is ready for search queries."
        )
    except Exception as e:
        return f"❌ Error indexing PDF '{pdf_path}': {str(e)}"


@tool("Search PDF Vector Store")
def search_pdf_tool(query: str) -> str:
    """
    Search the indexed PDF vector store for the most relevant passages.

    Use this tool to retrieve text chunks that are semantically related
    to the query. Always cite the page numbers in your response.

    Args:
        query: The question or topic to search for in the document.

    Returns:
        Formatted text with the top retrieved chunks and their source pages.
    """
    try:
        chunks = search_vectorstore(query, k=4)
        if not chunks:
            return "No relevant content found for this query."

        result = format_chunks_for_agent(chunks)
        sources_summary = ", ".join(
            f"page {c['page']}" for c in chunks
        )
        return (
            f"Retrieved {len(chunks)} relevant chunks (from {sources_summary}):\n\n"
            f"{result}"
        )
    except FileNotFoundError as e:
        return f"❌ {str(e)} Please use the 'Index PDF Document' tool first."
    except Exception as e:
        return f"❌ Error searching vector store: {str(e)}"
