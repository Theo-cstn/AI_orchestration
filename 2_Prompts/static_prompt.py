import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Prompt fixe pour tester l'analyse d'un mail
prompt = """
Analyse le mail suivant et dis-moi s'il s'agit d'une demande de partenariat sérieuse (OUI ou NON) :
'Bonjour, je suis influenceur tech et j'aimerais tester votre produit pour en faire une vidéo.'
"""

response = llm.invoke(prompt)
print(f"Analyse du mail : {response.content}")