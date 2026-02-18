# 5_Vector_Databases/embeddings.py
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vector = embeddings.embed_query("What is a vector database?")

print(f"Vector length: {len(vector)}")
print(f"First 5 values: {vector[:5]}")
