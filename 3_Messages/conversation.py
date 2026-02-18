# 3_Messages/conversation.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

conversation = [
    HumanMessage(content="What is RAG?"),
    AIMessage(content="RAG combines retrieval with generation."),
    HumanMessage(content="Why is it useful?")
]

response = llm.invoke(conversation)
print(response.content)
