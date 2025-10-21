from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from .tools.sec_tools import search_sec_filings
from .tools.financial_data_tools import get_company_overview
from .models import ScreeningDecision

search_tool = SerperDevTool()

@CrewBase
class StrategicAICrew:
    """StrategicAI crew for M&A analysis."""

    # ✅ Let CrewAI handle loading these YAMLs
    agents_config = Path(__file__).parent / 'config' / 'agents.yaml'
    tasks_config = Path(__file__).parent / 'config' / 'tasks.yaml'

    # ------ Agent Definitions ------ #
    @agent
    def company_screener(self) -> Agent:
        return Agent(
            config=self.agents_config['company_screener'],
            tools=[search_sec_filings, get_company_overview],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def financial_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            tools=[search_sec_filings, get_company_overview],
            verbose=True,
        )

    @agent
    def market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['market_analyst'],
            tools=[search_tool],
            verbose=True,
        )

    @agent
    def deal_lead(self) -> Agent:
        return Agent(config=self.agents_config['deal_lead'], verbose=True)

    @agent
    def report_synthesizer(self) -> Agent:
        return Agent(config=self.agents_config['report_synthesizer'], verbose=True)

    # ------ Task Definitions ------ #
    @task
    def screening_task(self) -> Task:
        return Task(
            config=self.tasks_config['screening_task'],
            agent=self.company_screener(),
            output_pydantic=ScreeningDecision,
        )

    @task
    def financial_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['financial_analysis_task'],
            agent=self.financial_analyst(),
        )

    @task
    def market_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['market_analysis_task'],
            agent=self.market_analyst(),
        )

    @task
    def synthesis_task(self) -> Task:
        return Task(
            config=self.tasks_config['synthesis_task'],
            agent=self.report_synthesizer(),
        )

    # ------ Crew Definitions ------ #
    @crew
    def screening_crew(self) -> Crew:
        return Crew(
            agents=[self.company_screener()],
            tasks=[self.screening_task()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def deep_dive_crew(self) -> Crew:
        from crewai import LLM
        llm = LLM(model="gemini/gemini-2.0-flash", temperature=0.7)

        return Crew(
            agents=[
                self.financial_analyst(),
                self.market_analyst(),
                self.deal_lead(),
                self.report_synthesizer(),
            ],
            tasks=[
                self.financial_analysis_task(),
                self.market_analysis_task(),
                self.synthesis_task(),
            ],
            process=Process.hierarchical,
            manager_llm=llm,
            memory=True,
            verbose=True,
            embedder={
                "provider": "google",
                "config": {
                    "model": "models/embedding-001",
                    "task_type": "retrieval_document",
                },
            },
        )
