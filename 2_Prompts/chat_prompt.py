from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM with CrewAI's native Google support
llm = LLM(
    model="gemini-3-flash-preview",
    provider="google",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Initialize Google Search tool
search_tool = SerperDevTool()

# Create Agent
research_agent = Agent(
    role=" Helpful teaching assistant.",
    goal="Find accurate and up-to-date information from the web",
    backstory=(
        "You are an expert researcher skilled at using search engines "
        "to gather reliable, current information."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True
)

# Create Task
research_task = Task(
    description=(
        "Explain prompt engineering."
    ),
    expected_output="A clear summary of what you've seen.",
    agent=research_agent
)

# Create Crew
crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    process=Process.sequential,
    verbose=True
)

# Run Crew
result = crew.kickoff()
print(result)