from crewai import Agent, Task, Crew, Process, LLM
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Initialisation du LLM avec le support natif Google (comme votre 1er script)
llm = LLM(
    model="gemini-3-flash-preview",
    provider="google",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# 2. Création de l'Agent vulgarisateur
explainer_agent = Agent(
    role="Tech Explainer",
    goal="Explain complex technical concepts clearly and simply",
    backstory=(
        "You are an expert teacher. You excel at taking advanced "
        "technology concepts and explaining them so that anyone can understand."
    ),
    llm=llm,
    verbose=True
)

# 3. Création de la Task AVEC variables dynamiques ({topic})
explanation_task = Task(
    description="Explain {topic} in simple terms.",
    expected_output="A clear, beginner-friendly explanation of {topic}.",
    agent=explainer_agent
)

# 4. Création du Crew
crew = Crew(
    agents=[explainer_agent],
    tasks=[explanation_task],
    process=Process.sequential,
    verbose=True
)

# 5. Définition des variables dynamiques et lancement
dynamic_inputs = {
    "topic": "vector databases"
}

result = crew.kickoff(inputs=dynamic_inputs)


print(result)