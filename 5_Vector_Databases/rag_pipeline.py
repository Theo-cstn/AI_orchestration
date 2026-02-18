# 5_Vector_Databases/rag_pipeline.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Create vector store
texts = ["LLMs generate text.", "Vector DBs store embeddings.", "RAG combines retrieval and generation."]
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

db = FAISS.from_texts(texts, embeddings)

# RAG Pipeline
query = "Explain vector databases"
docs = db.similarity_search(query, k=2)
context = "\n".join([d.page_content for d in docs])

prompt = f"Use the context below to answer:\n{context}\n\nQuestion: {query}"
response = llm.invoke(prompt)

print(f"Query: {query}")
print(f"Context: {context}")
print(f"\nResponse: {response.content}")
