
# StratēgicAI: An Autonomous M&A Analyst Platform

StratēgicAI is a sophisticated, multi-agent platform that automates the complex process of Merger & Acquisition (M&A) target analysis. It deploys a team of autonomous AI agents powered by **CrewAI** and **Google's Gemini** to perform a comprehensive evaluation, moving from high-level screening to in-depth financial and market analysis.

This project demonstrates a complete, end-to-end AI pipeline that solves a real-world business problem, showcasing advanced concepts in autonomous systems, hierarchical agent collaboration, and data-driven decision-making.

---

## 🚀 Key Features

* **Multi-Crew Pipeline:** Utilizes two distinct crews—a fast, sequential **Screening Crew** and a comprehensive, hierarchical **Deep Dive Crew**—orchestrated to work in sequence.
* **Hierarchical Agent Collaboration:** A "Deal Lead" manager agent delegates tasks to a team of specialists (`Financial Analyst`, `Market Analyst`), demonstrating a sophisticated command structure.
* **Structured Data Outputs:** Agents use Pydantic models to return reliable, structured JSON data, ensuring robust and predictable logic between steps.
* **Dynamic Decision-Making:** The pipeline uses a router to autonomously decide whether to proceed with a deep-dive analysis based on the initial screening results.
* **Custom Tool Integration:** Agents are equipped with custom-built tools to fetch real-time data from financial APIs (Alpha Vantage) and official SEC filings (SEC-API).
* **Intelligent Memory:** The Deep Dive Crew is equipped with memory (`memory=True`) to share context and findings between agents, leading to a more cohesive final report.
* **Interactive Web Interface:** A user-friendly web UI built with Streamlit allows for easy interaction and demonstration.

---

## 🛠️ Tech Stack

* **AI Framework:** [CrewAI](https://www.crewai.com/)
* **Language Models (LLM):** Google Gemini Pro
* **Web UI:** Streamlit
* **Data Sources:** [Alpha Vantage API](https://www.alphavantage.co/), [SEC-API.io](https://sec-api.io/), [Serper.dev](https://serper.dev/)
* **Core Libraries:** Pydantic, Requests, PyYAML

---

## ⚙️ Setup & How to Run

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/strategicai.git](https://github.com/your-username/strategicai.git)
    cd strategicai
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    The project uses `uv` for fast package management.
    ```bash
    pip install uv
    uv pip install -r requirements.txt
    ```
    *(Note: If you don't have a `requirements.txt`, you can create one with `uv pip freeze > requirements.txt` or instruct users to install one by one.)*

4.  **Set Up API Keys:**
    Create a `.env` file in the root directory and add your API keys:
    ```
    GOOGLE_API_KEY="your_gemini_api_key"
    SERPER_API_KEY="your_serper_api_key"
    SEC_API_KEY="your_sec_api_key"
    ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key"
    ```

5.  **Run the Application:**
    Launch the Streamlit web interface.
    ```bash
    streamlit run app.py
    ```
    Open your browser to `http://localhost:8501` to use the application.