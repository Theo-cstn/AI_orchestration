# 2_Prompts/project.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

template = PromptTemplate(
    input_variables=["question"],
    template="Answer the following question clearly:\n{question}"
)

response = llm.invoke(template.format(question="What is RAG?"))
print(response.content)
