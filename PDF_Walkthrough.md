# Résumé — RAG PDF avec CrewAI

## Ce qu'on a construit

Un pipeline **RAG complet** piloté par **3 agents CrewAI**, qui reproduit exactement le parcours enseigné en cours : du PDF brut jusqu'à la réponse vérifiée.

---

## Le pipeline, étape par étape

```
PDF
 │
 ▼
[1] PyPDFLoader                     → charge le PDF page par page
 │
 ▼
[2] RecursiveCharacterTextSplitter  → découpe en chunks (1000 tokens, overlap 200)
 │                                    = le "splitter" du cours
 ▼
[3] GoogleGenerativeAIEmbeddings    → transforme chaque chunk en vecteur
 │   model: gemini-embedding-001     = "embedding / vector translation" du cours
 ▼
[4] FAISS vectorstore               → stocke les vecteurs sur disque
 │                                    = la base de données vectorielle
 ▼
[5] similarity_search(query, k=4)   → retrouve les 4 chunks les plus proches
 │                                    = le "retrieval" du RAG
 ▼
[6] CrewAI — 3 agents séquentiels
     ├── pdf_retriever  → formule la requête vectorielle + restitue les chunks
     ├── analyst        → raisonne sur les chunks, effectue les calculs
     └── verifier       → vérifie les sources, score de confiance
 │
 ▼
Réponse sourcée + VALIDÉE
```

---

## Les 3 concepts du cours, implémentés

| Concept cours | Implémentation |
|---|---|
| **Splitter / Tokenisation** | `RecursiveCharacterTextSplitter(chunk_size=1000, overlap=200)` dans `rag/ingest.py` |
| **Embedding / Vector translation** | `GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")` |
| **Vector Store / Retrieval** | `FAISS.from_documents()` + `similarity_search_with_score()` dans `rag/retriever.py` |

---

## Ce que CrewAI apporte en plus du simple RAG

| RAG seul | RAG + CrewAI |
|---|---|
| 1 pipeline, 1 réponse | 3 agents avec rôles distincts |
| Pas de contrôle qualité | Agent **verifier** qui valide les sources |
| Pas de raisonnement explicite | Agent **analyst** qui montre son calcul |
| Black box | Chaque étape est **traçable et loggée** |

---

## Preuve que ça fonctionne

Question posée :
> *"Quel est le total des dépenses pour le Produit A en T1 2024 ?"*

Réponse du pipeline :
```
Analyst  → 2 100 000 + 3 400 000 + 1 800 000 = 7 300 000 EUR
           Sources : Page 2 (détail mensuel), Page 4 (tableau comparatif)

Verifier → STATUT : VALIDÉ
           Traçabilité    : CONFORME
           Calculs        : CONFORME
           Hallucinations : AUCUNE
           Score de confiance : ÉLEVÉ
```

---

## Architecture des fichiers

```
4_Project/
├── rag/
│   ├── ingest.py       ← PDF → chunks → embeddings → FAISS
│   └── retriever.py    ← requête vectorielle → chunks + scores
├── tools/
│   └── rag_tools.py    ← @tool CrewAI : index_pdf, search_pdf
├── config/
│   ├── rag_agents.yaml ← définition des 3 agents
│   └── rag_tasks.yaml  ← instructions des 3 tâches
├── rag_crew.py         ← orchestration CrewAI
└── main.py             ← point d'entrée (--mode pdf / --mode mail)
```

---

## Commande pour lancer

```bash
cd /Users/tom/Desktop/IG/S8/AI_orchestration

uv run 4_Project/main.py --mode pdf \
  --pdf data/example.pdf \
  --question "Quel est le total des depenses pour le Produit A en T1 2024 ?"
```

---

## Angle pour l'oral

> **"Quand suffit-il d'un simple RAG, et quand faut-il de l'orchestration multi-agents ?"**

- Un RAG seul répond — mais ne se vérifie pas lui-même.
- CrewAI permet de **séparer les responsabilités** : chercher ≠ analyser ≠ vérifier.
- Le **verifier agent** est la vraie valeur ajoutée : il garantit qu'aucune hallucination ne passe.
