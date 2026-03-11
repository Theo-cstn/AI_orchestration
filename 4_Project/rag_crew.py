"""
RAG Document Crew
=================
A CrewAI crew that answers questions about a PDF document using a 3-agent pipeline:

  1. pdf_retriever  — finds relevant chunks in the vector store
  2. analyst        — reasons over chunks, performs calculations
  3. verifier       — validates sources and produces the final answer

Usage:
    inputs = {
        "pdf_path": "data/example.pdf",
        "question": "What is the total budget for Q1 2024?",
    }
    result = RAGDocumentCrew().crew().kickoff(inputs=inputs)
"""

import os
from dotenv import load_dotenv

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew

from tools.rag_tools import index_pdf_tool, search_pdf_tool

load_dotenv()

llm = LLM(
    model="gemini-3-flash-preview",
    provider="google",
    api_key=os.getenv("GOOGLE_API_KEY"),
)


@CrewBase
class RAGDocumentCrew:
    """
    Crew for answering questions about PDF documents using RAG + multi-agent orchestration.

    Pipeline:
        retrieval_task -> analysis_task -> verification_task

    Usage:
        # 1. Index the PDF first (done externally before kickoff)
        from rag.ingest import build_vectorstore
        build_vectorstore("path/to/doc.pdf")

        # 2. Run the crew
        RAGDocumentCrew().crew().kickoff(inputs={"question": "..."})
    """

    agents_config = "config/rag_agents.yaml"
    tasks_config = "config/rag_tasks.yaml"

    # ── Agents ─────────────────────────────────────────────────────────────────

    @agent
    def pdf_retriever(self) -> Agent:
        return Agent(
            config=self.agents_config["pdf_retriever"],
            tools=[search_pdf_tool],
            llm=llm,
            verbose=True,
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst"],
            llm=llm,
            verbose=True,
        )

    @agent
    def verifier(self) -> Agent:
        return Agent(
            config=self.agents_config["verifier"],
            llm=llm,
            verbose=True,
        )

    # ── Tasks ──────────────────────────────────────────────────────────────────

    @task
    def retrieval_task(self) -> Task:
        return Task(config=self.tasks_config["retrieval_task"])

    @task
    def analysis_task(self) -> Task:
        return Task(config=self.tasks_config["analysis_task"])

    @task
    def verification_task(self) -> Task:
        return Task(config=self.tasks_config["verification_task"])

    # ── Crew ───────────────────────────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
