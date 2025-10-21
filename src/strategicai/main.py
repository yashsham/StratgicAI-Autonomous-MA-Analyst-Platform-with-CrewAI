#!/usr/bin/env python

import yaml

from pathlib import Path

from crewai import Agent, Crew, Process, Task

from langchain_google_genai import ChatGoogleGenerativeAI



# Import tools and models

from .tools.sec_tools import search_sec_filings

from .tools.financial_data_tools import get_company_overview

from crewai_tools import SerperDevTool

from .models import ScreeningDecision





def safe_task(config_entry, agent, **kwargs):

    """

    Helper to safely create a Task ensuring YAML entries are dicts.

    """

    if not isinstance(config_entry, dict):

        raise TypeError(

            f"[ERROR] Expected a dict for Task config, got {type(config_entry)}. "

            "This usually means your tasks.yaml file has a formatting or indentation error."

        )

    return Task(config=config_entry, agent=agent, **kwargs)





def run(ticker: str):

    """

    Orchestrates the M&A analysis process:

    1. Loads configurations.

    2. Builds all agents and tasks manually.

    3. Runs the screening crew.

    4. Optionally runs the deep-dive crew if 'Go' is recommended.

    """

    # --- 1️⃣ Load YAML Configurations ---

    configs_path = Path(__file__).parent / 'config'

    agents_config_path = configs_path / 'agents.yaml'

    tasks_config_path = configs_path / 'tasks.yaml'



    with open(agents_config_path, 'r', encoding='utf-8') as f:

        agents_config = yaml.safe_load(f)



    with open(tasks_config_path, 'r', encoding='utf-8') as f:

        tasks_config = yaml.safe_load(f)



    # ✅ Debug check to make sure YAML parsed correctly

    print("\n[DEBUG] YAML type checks:")

    for key, value in tasks_config.items():

        print(f"  {key}: {type(value)}")



    # --- 2️⃣ Create Tools ---

    search_tool = SerperDevTool()



    # --- 3️⃣ Create Agents ---

    company_screener = Agent(

        config=agents_config['company_screener'],

        tools=[search_sec_filings, get_company_overview],

        allow_delegation=False,

        verbose=True

    )



    financial_analyst = Agent(

        config=agents_config['financial_analyst'],

        tools=[search_sec_filings, get_company_overview],

        verbose=True

    )



    market_analyst = Agent(

        config=agents_config['market_analyst'],

        tools=[search_tool],

        verbose=True

    )



    deal_lead = Agent(

        config=agents_config['deal_lead'],

        verbose=True

    )



    report_synthesizer = Agent(

        config=agents_config['report_synthesizer'],

        verbose=True

    )



    # --- 4️⃣ Create Tasks Safely ---

    screening_task = safe_task(

        tasks_config['screening_task'],

        agent=company_screener,

        output_pydantic=ScreeningDecision

    )



    financial_analysis_task = safe_task(

        tasks_config['financial_analysis_task'],

        agent=financial_analyst

    )



    market_analysis_task = safe_task(

        tasks_config['market_analysis_task'],

        agent=market_analyst

    )



    synthesis_task = safe_task(

        tasks_config['synthesis_task'],

        agent=report_synthesizer,

        context=[financial_analysis_task, market_analysis_task]

    )



    # --- 5️⃣ Screening Crew ---

    print("🚀 Kicking off the Screening Crew for an initial analysis...")

    screening_crew = Crew(

        agents=[company_screener],

        tasks=[screening_task],

        process=Process.sequential,

        verbose=True,

    )



    screening_result = screening_crew.kickoff(inputs={'ticker': ticker})



    print("\n\n########################")

    print("## 🏁 Screening Complete!")

    print("########################\n")

    print("Screening Crew Final Output:")

    print(screening_result)



    # --- 6️⃣ Deep Dive Crew Decision ---

    if (

        screening_result

        and hasattr(screening_result, "pydantic")

        and screening_result.pydantic

        and getattr(screening_result.pydantic, "recommendation", None) == "Go"

    ):

        print("\n- Decision: Screening resulted in a 'Go'. Proceeding to Deep Dive analysis.")

        print(f"- Justification: {screening_result.pydantic.justification}")



        # --- 7️⃣ Deep Dive Crew ---

        print("\n🚀 Kicking off the Deep Dive Crew... This will take a few minutes.")

        from crewai import LLM



        llm = LLM(

    model="gemini/gemini-2.0-flash",

    temperature=0.7,

)



        deep_dive_crew = Crew(

            agents=[financial_analyst, market_analyst, deal_lead, report_synthesizer],

            tasks=[financial_analysis_task, market_analysis_task, synthesis_task],

            process=Process.hierarchical,

            manager_llm=llm,

            memory=True,

            verbose=True,

            embedder={

    "provider": "google-generativeai",

    "config": {

        "model": "models/embedding-001",

        "task_type": "retrieval_document"

    }

}



        )



        deep_dive_result = deep_dive_crew.kickoff(inputs={'ticker': ticker})



        print("\n\n########################")

        print("## 🏁 Deep Dive Complete!")

        print("########################\n")

        print("Deep Dive Crew Final Investment Thesis:")

        print(deep_dive_result)

        return deep_dive_result



    else:

        print("\n- Decision: Screening resulted in a 'No-Go'. Halting analysis.")

        if screening_result and hasattr(screening_result, "pydantic") and screening_result.pydantic:

            print(f"- Justification: {screening_result.pydantic.justification}")

        else:

            print("- Justification: No valid structured output from screening crew.")

        return screening_result





# --- 8️⃣ Local Run (for debugging) ---

if __name__ == "__main__":

    final_report = run(ticker='TSLA')

    print("\n--- Main execution finished. Final Report: ---")

    print(final_report)

