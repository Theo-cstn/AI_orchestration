# 2_Prompts/chat_prompt.py
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
    SystemMessage(content="You are a helpful teaching assistant."),
    HumanMessage(content="Explain prompt engineering.")
]

response = llm.invoke(messages)
print(response.content)
