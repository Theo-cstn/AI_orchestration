# 2_Prompts/static_prompt.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# On utilise le préfixe complet attendu par le nouveau SDK
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview", 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt = """
Analyse le mail suivant et dis-moi s'il s'agit d'une demande de partenariat sérieuse (OUI ou NON) :
'Bonjour, je suis influenceur tech et j'aimerais tester votre produit pour en faire une vidéo.'
"""

response = llm.invoke(prompt)
print(f"Analyse du mail : {response.content}")