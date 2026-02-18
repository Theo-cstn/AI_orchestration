# 3_Messages/messages_basic.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

response = llm.invoke([
    HumanMessage(content="What is an embedding?")
])

print(response.content)
