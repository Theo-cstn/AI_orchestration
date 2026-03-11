from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew
import os
from dotenv import load_dotenv

load_dotenv()
llm = LLM(
    model="gemini-3-flash-preview",
    provider="google",
    api_key=os.getenv("GOOGLE_API_KEY")
)


@CrewBase
class PartnershipCrew():
    """Crew pour le tri de mails de partenariats"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'], llm=llm,verbose=True)

    @agent
    def classifier(self) -> Agent:
        return Agent(config=self.agents_config['classifier'], llm=llm, verbose=True)

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def classification_task(self) -> Task:
        return Task(config=self.tasks_config['classification_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
        