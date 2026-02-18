# 3_Messages/messages_chat.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

messages = [
    SystemMessage(content="You explain concepts briefly."),
    HumanMessage(content="What is a vector database?")
]

response = llm.invoke(messages)
print(response.content)
