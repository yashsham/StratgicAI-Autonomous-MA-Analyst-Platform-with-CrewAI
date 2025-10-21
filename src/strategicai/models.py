# In src/strategicai/models.py
from pydantic import BaseModel, Field

class ScreeningDecision(BaseModel):
    """
    Represents the decision and justification from the initial company screening.
    """
    recommendation: str = Field(description="The final recommendation, either 'Go' or 'No-Go'.")
    justification: str = Field(description="A brief, one-sentence justification for the recommendation.")