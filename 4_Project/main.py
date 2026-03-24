"""
Entry point for the AI Orchestration project.

Usage:
    # Mode mail (partenariats) — comportement original
    python main.py

    # Mode PDF — pipeline RAG + agents CrewAI
    python main.py --mode pdf
    python main.py --mode pdf --pdf data/my_report.pdf --question "Quel est le budget Q1 ?"
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Helpers ────────────────────────────────────────────────────────────────────

def run_mail_mode():
    """Mode original : classification de mails de partenariat."""
    from crew import PartnershipCrew

    print("\n" + "="*60)
    print("📧 MODE MAIL — PartnershipCrew")
    print("="*60)

    inputs = {
        "email_content": "Bonjour, je suis un bot qui veut vous vendre des chaussures pas chères."
    }
    PartnershipCrew().crew().kickoff(inputs=inputs)


def run_pdf_mode(pdf_path: str, question: str):
    """Mode PDF : RAG pipeline orchestré par agents CrewAI."""
    from rag.ingest import build_vectorstore
    from rag_crew import RAGDocumentCrew

    print("\n" + "="*60)
    print("📄 MODE PDF — RAGDocumentCrew")
    print(f"   PDF     : {pdf_path}")
    print(f"   Question: {question}")
    print("="*60)

    # Resolve path relative to this file's directory
    base_dir = Path(__file__).parent
    resolved_pdf = Path(pdf_path) if Path(pdf_path).is_absolute() else base_dir / pdf_path

    if not resolved_pdf.exists():
        print(f"\n❌ PDF not found: {resolved_pdf}")
        print("   Tip: run 'python create_demo_pdf.py' to generate a sample PDF.")
        sys.exit(1)

    # Step 1: Index the PDF (must be done BEFORE instantiating the crew)
    print(f"\n🚀 [Step 1/2] Indexing PDF...")
    build_vectorstore(str(resolved_pdf))

    # Step 2: Run the crew
    print(f"\n🤖 [Step 2/2] Starting RAG crew...")
    inputs = {
        "pdf_path": str(resolved_pdf),
        "question": question,
    }

    result = RAGDocumentCrew().crew().kickoff(inputs=inputs)

    print("\n" + "="*60)
    print("✅ RÉSULTAT FINAL")
    print("="*60)
    print(result)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AI Orchestration Project — CrewAI Demo",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["mail", "pdf"],
        default="mail",
        help=(
            "Mode d'exécution :\n"
            "  mail — classification de mails (défaut)\n"
            "  pdf  — analyse de document PDF via RAG"
        ),
    )
    parser.add_argument(
        "--pdf",
        default="data/example.pdf",
        help="Chemin vers le PDF à analyser (mode pdf uniquement). Défaut: data/example.pdf",
    )
    parser.add_argument(
        "--question",
        default="Quels sont les principaux points financiers de ce rapport ?",
        help="Question à poser sur le document (mode pdf uniquement).",
    )

    args = parser.parse_args()

    if args.mode == "mail":
        run_mail_mode()
    elif args.mode == "pdf":
        run_pdf_mode(args.pdf, args.question)


if __name__ == "__main__":
    main()