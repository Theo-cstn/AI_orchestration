"""
Script to generate a sample market analysis PDF for demo purposes.

Run this once to create data/example.pdf:
    python create_demo_pdf.py

Requires: fpdf2
    pip install fpdf2
    or: uv add fpdf2
"""

from pathlib import Path
from fpdf import FPDF


SCRIPT_DIR = Path(__file__).parent


def create_demo_pdf(output_path: str = "data/example.pdf"):
    """Generate a fictional market analysis report PDF."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ── Page 1: Cover ──────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.ln(30)
    pdf.cell(0, 15, "RAPPORT D'ANALYSE MARCHE", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "TechCorp Solutions - Exercice 2024", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Confidentiel - Usage interne uniquement", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 8, "Date : Mars 2024", new_x="LMARGIN", new_y="NEXT", align="C")

    # ── Page 2: Executive Summary ──────────────────────────────────────────────
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "1. Resume Executif", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)
    summary = (
        "Ce rapport présente l'analyse complète des performances commerciales de TechCorp Solutions "
        "pour l'exercice 2024. Les résultats démontrent une croissance solide sur l'ensemble des "
        "segments de marché, portée principalement par les Produits A et C. "
        "Le chiffre d'affaires total pour le premier trimestre 2024 s'élève à 18.3 millions d'euros, "
        "en hausse de 12% par rapport au T1 2023. "
        "Les dépenses marketing ont représenté 22% du budget total sur cette période."
    )
    pdf.multi_cell(0, 6, summary)

    # ── Page 3: Q1 2024 Details ────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "2. Detail des Depenses - T1 2024", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "2.1 Produit A - Logiciel de Gestion", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    product_a = (
        "Le Produit A (logiciel de gestion) a represente le poste de depense le plus "
        "important du T1 2024. Les investissements se repartissent comme suit :\n"
        "  - Janvier 2024 : 2 100 000 EUR (developpement fonctionnalites)\n"
        "  - Fevrier 2024 : 3 400 000 EUR (acquisition clients + marketing)\n"
        "  - Mars 2024    : 1 800 000 EUR (support et maintenance)\n\n"
        "Total Produit A - T1 2024 : 7 300 000 EUR\n\n"
        "Ces depenses ont permis d'acquerir 340 nouveaux clients entreprise, "
        "portant le total a 1 250 clients actifs pour ce segment."
    )
    pdf.multi_cell(0, 6, product_a)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "2.2 Produit B - Plateforme Cloud", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    product_b = (
        "Le Produit B (plateforme cloud) est en phase de lancement. Depenses T1 2024 :\n"
        "  - Janvier 2024 : 800 000 EUR (infrastructure cloud)\n"
        "  - Fevrier 2024 : 1 200 000 EUR (integration + tests)\n"
        "  - Mars 2024    : 950 000 EUR (lancement commercial)\n\n"
        "Total Produit B - T1 2024 : 2 950 000 EUR\n\n"
        "Le Produit B a atteint 85 clients en version beta a fin mars 2024."
    )
    pdf.multi_cell(0, 6, product_b)

    # ── Page 4: Q2 2024 ────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "3. Previsions - T2 2024", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "3.1 Produit A - Previsions T2 2024", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    q2_a = (
        "Sur la base des tendances observees, les previsions T2 2024 pour le Produit A :\n"
        "  - Avril 2024 : 2 200 000 EUR\n"
        "  - Mai 2024   : 2 500 000 EUR\n"
        "  - Juin 2024  : 2 800 000 EUR\n\n"
        "Prevision totale Produit A - T2 2024 : 7 500 000 EUR\n\n"
        "L'augmentation prevue est liee au lancement de la version 3.0 en mai 2024, "
        "ainsi qu'a une campagne marketing ciblee sur les PME."
    )
    pdf.multi_cell(0, 6, q2_a)

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 9, "3.2 Budget Marketing Global", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    marketing = (
        "Le budget marketing alloue pour 2024 est de 8 000 000 EUR, reparti comme suit :\n"
        "  - T1 2024 (realise)   : 1 800 000 EUR\n"
        "  - T2 2024 (prevu)     : 2 200 000 EUR\n"
        "  - T3 2024 (prevu)     : 2 100 000 EUR\n"
        "  - T4 2024 (prevu)     : 1 900 000 EUR\n\n"
        "Total marketing annuel prevu : 8 000 000 EUR\n\n"
        "Le ROI marketing estime pour 2024 est de 340%, calcule sur la base des nouveaux contrats "
        "signes directement attribuables aux campagnes marketing."
    )
    pdf.multi_cell(0, 6, marketing)

    # ── Page 5: Comparative Analysis ──────────────────────────────────────────
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "4. Comparaison 2023 vs 2024", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 11)
    comparison = (
        "Comparaison des dépenses T1 2023 vs T1 2024 :\n\n"
        "Produit A :\n"
        "  - T1 2023 : 6 100 000 EUR\n"
        "  - T1 2024 : 7 300 000 EUR\n"
        "  - Variation : +19.7%\n\n"
        "Produit B :\n"
        "  - T1 2023 : 0 EUR (produit non lancé)\n"
        "  - T1 2024 : 2 950 000 EUR\n"
        "  - Variation : N/A (nouveau produit)\n\n"
        "Budget Marketing :\n"
        "  - T1 2023 : 1 400 000 EUR\n"
        "  - T1 2024 : 1 800 000 EUR\n"
        "  - Variation : +28.6%\n\n"
        "La croissance globale des dépenses de T1 2023 à T1 2024 s'explique principalement par "
        "le lancement du Produit B et l'intensification des efforts marketing pour le Produit A."
    )
    pdf.multi_cell(0, 6, comparison)

    # ── Save ───────────────────────────────────────────────────────────────────
    output = SCRIPT_DIR / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output))
    print(f"PDF de demo cree: {output.resolve()}")
    print(f"   Pages: 5 | Contenu: rapport fictif TechCorp Solutions 2024")


if __name__ == "__main__":
    create_demo_pdf()
