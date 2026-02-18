# 5_Vector_Databases/retrieval.py
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

texts = ["LLMs generate text.", "Vector DBs store embeddings."]

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

db = FAISS.from_texts(texts, embeddings)

# Retrieval
query = "What stores embeddings?"
docs = db.similarity_search(query, k=1)

print(f"Query: {query}")
print(f"Most relevant document: {docs[0].page_content}")
