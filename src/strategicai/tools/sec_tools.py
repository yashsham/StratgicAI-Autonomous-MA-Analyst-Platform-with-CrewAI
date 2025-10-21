import os
import json
from crewai.tools import tool
from sec_api import QueryApi

@tool("SEC Filings Search Tool")
def search_sec_filings(query: str) -> str:
    """
    Searches for and retrieves the most recent 10-K and 10-Q filings for a given company ticker.
    This tool is essential for gathering official financial documents for analysis.
    """
    # Initialize the QueryApi with your API key from the .env file
    query_api = QueryApi(api_key=os.getenv("SEC_API_KEY"))

    # Define the search query for the API
    api_query = {
      "query": { "query_string": {
          "query": f"ticker:{query} AND formType:\"10-K\""
      }},
      "from": "0",
      "size": "1",
      "sort": [{ "filedAt": { "order": "desc" }}]
    }

    try:
        # Fetch the filings
        filings = query_api.get_filings(api_query)

        # We'll just return the metadata for now, not the full document URL
        return json.dumps(filings, indent=2)
    except Exception as e:
        return f"An error occurred while searching for SEC filings: {e}"