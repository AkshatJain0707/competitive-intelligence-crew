# tasks.py (Optimized and Final)
from crewai import Task
from models import BrandAnalysis, CompetitorProfile, StrategicReport

class CompetitorAnalysisTasks:
    """
    Defines structured CrewAI tasks that coordinate multi-agent collaboration
    for automated competitor intelligence gathering and strategic synthesis.
    """

    def scrape_website_task(self, agent, url: str):
        return Task(
            name=f"Scrape-{url}",
            description=f"Scrape the website at {url} to extract text content and hero image URL.",
            agent=agent,
            expected_output="A dictionary with 'text_content' and 'hero_image_url'."
        )

    def analyze_visuals_task(self, agent):
        return Task(
            name="VisualAnalysis",
            description=(
                "Analyze the website's visual branding elements. Return a valid JSON object with these fields:\n"
                "- primary_colors: [list of 2-3 hex color codes]\n"
                "- secondary_colors: [list of 2-3 hex color codes]\n"
                "- design_style: <description of overall design style>\n"
                "- emotional_tone: <perceived emotional tone>\n"
                "- logo_analysis: <analysis of the company logo>"
            ),
            agent=agent,
            output_pydantic=BrandAnalysis,
            expected_output="A fully populated BrandAnalysis Pydantic object."
        )

    def analyze_messaging_task(self, agent):
        return Task(
            name="MessagingAnalysis",
            description=(
                "Analyze the scraped text content for the website’s core messaging strategy, "
                "brand voice, and value propositions."
            ),
            agent=agent,
            expected_output="A comprehensive text-based messaging analysis."
        )

    def compile_profile_task(self, agent, company_name: str, url: str):
        return Task(
            name=f"CompileProfile-{company_name}",
            description=(
                f"Combine both visual and textual analyses to compile a comprehensive "
                f"CompetitorProfile for {company_name} ({url}). "
                f"\n\nReturn a valid JSON object with these exact fields:\n"
                f"- company_name: '{company_name}'\n"
                f"- url: '{url}'\n"
                f"- messaging_analysis: <detailed text analysis of messaging>\n"
                f"- visual_analysis: <object with primary_colors, secondary_colors, design_style, emotional_tone, logo_analysis>"
            ),
            agent=agent,
            output_pydantic=CompetitorProfile,
            expected_output=f"A validated CompetitorProfile Pydantic object for {company_name}."
        )

    def generate_report_task(self, agent):
        return Task(
            name="GenerateStrategicReport",
            description=(
                "Synthesize all competitor profiles into a final strategic report. "
                "Return a valid JSON object with these exact fields:\n"
                "- report_title: <compelling report title>\n"
                "- competitor_profiles: [array of CompetitorProfile objects]\n"
                "- comparative_summary: <high-level summary comparing competitors>\n"
                "- identified_gaps_and_opportunities: <identified market gaps and opportunities>\n"
                "- strategic_recommendations: <actionable strategic recommendations>"
            ),
            agent=agent,
            output_pydantic=StrategicReport,
            expected_output="A complete StrategicReport Pydantic object with insights and recommendations."
        )
