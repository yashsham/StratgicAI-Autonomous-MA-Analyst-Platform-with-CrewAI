import os
from crewai.tools import tool
from alpha_vantage.fundamentaldata import FundamentalData

@tool("Company Overview Tool")
def get_company_overview(ticker: str) -> str:
    """
    Fetches a comprehensive overview of a public company, including its business description, industry,
    and key financial metrics like P/E Ratio and Market Capitalization.
    Useful for gaining a foundational understanding of the company.
    """
    try:
        # Initialize the FundamentalData client with your API key
        fd = FundamentalData(key=os.getenv("ALPHA_VANTAGE_API_KEY"), output_format='json')

        # Fetch the company overview data
        data, _ = fd.get_company_overview(symbol=ticker)

        # We can format this later, for now, returning the raw data is fine
        return str(data)
    except Exception as e:
        return f"An error occurred while fetching company overview: {e}"