import streamlit as st
from src.strategicai.main import run

st.title("🤖 StratēgicAI: Autonomous M&A Analyst")

st.write(
    "Welcome to StratēgicAI. Enter a company ticker to begin the analysis."
)

# Input box
ticker = st.text_input("Company Ticker", placeholder="e.g., MSFT, GOOGL")

# Only define and use `result` inside the button handler
if st.button("Run Analysis"):
    if ticker:
        st.write(f"Running analysis for {ticker}...")

        # Spinner while the crew runs
        with st.spinner("Agents are analyzing... Please wait."):
            result = run(ticker=ticker)

        st.success("✅ Analysis Complete!")

        st.write("## Final Report")

        # --- Display logic ---
        if hasattr(result, "pydantic") and result.pydantic:
            # Show structured decision (like ScreeningDecision)
            decision = result.pydantic
            st.json({
                "recommendation": decision.recommendation,
                "justification": decision.justification
            })

        elif isinstance(result, str):
            # Deep dive result returned as text/markdown
            st.markdown(result)

        elif hasattr(result, "tasks_output"):
            # CrewResult with multiple task outputs
            st.write("### Crew Task Summaries")
            for task_output in result.tasks_output:
                st.markdown(f"**{task_output.agent}** — {task_output.summary}")

        else:
            # Generic fallback
            st.write(result)

    else:
        st.error("❌ Please enter a company ticker before running the analysis.")

