# crew.py (FINAL, FULLY INTEGRATED & OPTIMIZED)
import os
import traceback
from crewai import Crew, Process
from agents import CompetitorAnalysisAgents
from tasks import CompetitorAnalysisTasks


class CompetitorAnalysisCrew:
    """
    The orchestrator that manages all agents and tasks for end-to-end competitor analysis.
    Workflow:
      1. Web Recon Agent → Scrapes site text + hero image
      2. Visual Brand Analyst → Interprets brand design
      3. Content Strategist → Extracts key messaging
      4. Strategic Insights Agent → Synthesizes full report
    """

    def __init__(self):
        try:
            # Instantiate all agents and tasks
            self.agents = CompetitorAnalysisAgents()
            self.tasks = CompetitorAnalysisTasks()

            print("Agents and Tasks initialized successfully.")
        except Exception as e:
            print(f"Initialization error: {e}")
            traceback.print_exc()

    def build_crew(self, company_name: str, company_url: str) -> Crew:
        """
        Assembles the complete crew pipeline for a given competitor website.
        """
        try:
            # --- Initialize individual agents ---
            web_recon = self.agents.web_recon_agent()
            visual_analyst = self.agents.visual_brand_analyst_agent()
            content_strategist = self.agents.content_strategist_agent()
            strategist = self.agents.strategic_insights_agent()

            # --- Define task flow ---
            scrape_task = self.tasks.scrape_website_task(web_recon, company_url)
            analyze_visuals_task = self.tasks.analyze_visuals_task(visual_analyst)
            analyze_messaging_task = self.tasks.analyze_messaging_task(content_strategist)
            compile_profile_task = self.tasks.compile_profile_task(
                strategist, company_name, company_url
            )
            report_task = self.tasks.generate_report_task(strategist)

            # --- Create Crew ---
            crew = Crew(
                agents=[web_recon, visual_analyst, content_strategist, strategist],
                tasks=[
                    scrape_task,
                    analyze_visuals_task,
                    analyze_messaging_task,
                    compile_profile_task,
                    report_task,
                ],
                process=Process.sequential,  # Each agent runs in order
                verbose=True,
            )

            print(f"Crew for {company_name} built successfully.")
            return crew

        except Exception as e:
            print(f"Crew build error: {e}")
            traceback.print_exc()
            raise

    def run(self, company_name: str, company_url: str):
        """
        Executes the end-to-end competitor analysis pipeline.
        Returns the final StrategicReport object.
        """
        try:
            crew = self.build_crew(company_name, company_url)
            print(f"Running CrewAI pipeline for {company_name} ...\n")

            result = crew.kickoff()

            print("\nCrew Execution Completed Successfully.")
            return result

        except Exception as e:
            print(f"Crew execution failed: {e}")
            traceback.print_exc()
            return None


# --- CLI TESTING ENTRY POINT ---
if __name__ == "__main__":
    try:
        company_name = "OpenAI"
        company_url = "https://openai.com"

        print("Starting Competitor Analysis Crew...")
        crew_instance = CompetitorAnalysisCrew()
        final_report = crew_instance.run(company_name, company_url)

        if final_report:
            print("\nFinal Strategic Report:")
            print(final_report)
        else:
            print("\nNo report generated. Check logs for errors.")

    except Exception as e:
        print(f"Fatal Error: {e}")
        traceback.print_exc()
