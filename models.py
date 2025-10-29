# models.py (The data backbone of our application)
from pydantic import BaseModel, Field
from typing import List

class BrandAnalysis(BaseModel):
    """Data model for the visual analysis of a brand's website."""
    primary_colors: List[str] = Field(..., description="List of 2-3 primary hex color codes identified.")
    secondary_colors: List[str] = Field(..., description="List of 2-3 secondary hex color codes identified.")
    design_style: str = Field(..., description="A concise description of the overall design style.")
    emotional_tone: str = Field(..., description="The perceived emotional tone conveyed by the visuals.")
    logo_analysis: str = Field(..., description="A brief analysis of the company logo's design and impact.")

class CompetitorProfile(BaseModel):
    """A comprehensive, structured profile of a single competitor."""
    company_name: str = Field(..., description="Official name of the competitor company.")
    url: str = Field(..., description="Homepage URL of the competitor's website.")
    messaging_analysis: str = Field(..., description="Detailed analysis of key messaging, value propositions, and positioning.")
    visual_analysis: BrandAnalysis = Field(..., description="The complete visual brand analysis.")

class StrategicReport(BaseModel):
    """The final strategic report with actionable insights."""
    report_title: str = Field(..., description="A compelling title for the final report.")
    competitor_profiles: List[CompetitorProfile] = Field(..., description="A list of detailed profiles for each competitor.")
    comparative_summary: str = Field(..., description="A high-level summary comparing the competitors.")
    identified_gaps_and_opportunities: str = Field(..., description="Identified market gaps and strategic opportunities.")
    strategic_recommendations: str = Field(..., description="Actionable strategic recommendations for our brand.")