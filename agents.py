import os
from crewai import Agent
from crewai.llms.base_llm import BaseLLM

try:
    from tools.google_gemini_adapter import GoogleGeminiAdapter
except Exception:
    GoogleGeminiAdapter = None

try:
    from tools.scraper_tool import WebsiteScraperTool
except Exception as e:
    print(f"Warning: Could not import WebsiteScraperTool: {e}")
    WebsiteScraperTool = None

try:
    from tools.vision_tool import GeminiVisionTool
except Exception as e:
    print(f"Warning: Could not import GeminiVisionTool: {e}")
    GeminiVisionTool = None


def _get_gemini_llm():
    """Create a Gemini LLM if ENABLE_LLM=1 and GOOGLE_API_KEY is set."""
    if os.getenv("ENABLE_LLM", "0").lower() not in ("1", "true", "yes"):
        print("LLM disabled (set ENABLE_LLM=1 to enable LLM calls).")
        return None

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("No GOOGLE_API_KEY found in environment.")
        return None

    if GoogleGeminiAdapter is None:
        print("GoogleGeminiAdapter not available. Install google-generativeai package.")
        return None

    try:
        llm = GoogleGeminiAdapter(api_key=api_key, model="gemini-pro")
        print("✓ Gemini LLM initialized successfully")
        return llm
    except RuntimeError as e:
        if "not enabled" in str(e).lower():
            print(f"\n⚠️  {e}")
            print("Using NoOpLLM fallback for development mode...")
            return NoOpLLM()
        print(f"✗ Failed to initialize Gemini: {e}")
        return None
    except Exception as e:
        print(f"✗ Failed to initialize Gemini: {e}")
        return None


# Minimal NoOp / Mock LLM for development: provides deterministic responses and prevents
# the system from instantiating external LLM providers like OpenAI when not desired.
class NoOpLLM(BaseLLM):
    """A minimal BaseLLM-compatible no-op LLM for development and testing.

    This class prevents CrewAI from attempting to instantiate external LLM
    provider clients when LLMs are disabled or unavailable.
    """

    def __init__(self, model: str = "noop-model"):
        # Initialize BaseLLM with the model name
        super().__init__(model=model)

    def call(self, messages, tools: list[dict] | None = None, callbacks=None, available_functions=None, from_task=None, from_agent=None):
        # Normalize messages to text
        if isinstance(messages, list):
            try:
                text = "\n".join(m.get("content", "") for m in messages)
            except Exception:
                text = str(messages)
        else:
            text = str(messages)

        # If the system prompt is asking for valid JSON, try to return a minimal
        # but valid JSON structure matching the expected Pydantic models so
        # the converter can validate and the pipeline can continue in dev mode.
        lower_text = text.lower()

        import json

        # Detect if a full CompetitorProfile is being requested FIRST, before strategic report checks
        is_competitor_request = any(
            kw in lower_text
            for kw in (
                "competitorprofile",
                "compile profile",
                "competitor profile",
                "compile a comprehensive",
                "combine visual",
                "combine messaging",
                "combine both visual",
                "compile a comprehensive competitor",
            )
        ) or ("combine" in lower_text and ("visual" in lower_text or "messaging" in lower_text))

        if is_competitor_request:
            # Try to extract company name and url from prompt text
            company = None
            url = None
            for part in text.replace('(', ' ').replace(')', ' ').split():
                if part.startswith("http"):
                    url = part.strip('"')
                candidate = part.strip('"').strip(',').strip('.')
                if len(candidate) > 2 and candidate[0].isupper():
                    company = company or candidate

            result = {
                "company_name": company or "ExampleCo",
                "url": url or "https://example.com",
                "messaging_analysis": "Placeholder messaging analysis synthesized from earlier outputs.",
                "visual_analysis": {
                    "primary_colors": ["#112233", "#445566"],
                    "secondary_colors": ["#778899", "#aabbcc"],
                    "design_style": "Clean, modern layout with generous whitespace",
                    "emotional_tone": "Trustworthy and optimistic",
                    "logo_analysis": "Simple wordmark with subtle geometric tweak",
                },
            }
            return json.dumps(result)

        # Prefer StrategicReport if the prompt asks for a strategic report or
        # if the converter likely expects one. This should run after CompetitorProfile checks.
        strategic_keywords = (
            "strategicreport",
            "strategic report",
            "generate strategic report",
            "synthesize",
            "final strategic report",
            "synthesize all",
            "synthesize all competitor",
            "synthesize all competitor profiles",
            "StrategicReport",
        )
        if any(k in lower_text for k in strategic_keywords) or "competitor_profiles" in lower_text:
            # Extract 0-3 company candidates more conservatively
            STOPWORDS = {
                "the",
                "you",
                "your",
                "agent",
                "tool",
                "task",
                "analysis",
                "analysis:",
                "final",
                "report",
                "generate",
                "synthesize",
                "compile",
                "combine",
                "use",
                "only",
                "never",
                "name",
                "url",
                "important",
                "arguments",
            }
            companies = []
            for part in text.replace('(', ' ').replace(')', ' ').split():
                if part.startswith("http"):
                    url = part.strip('"').strip(',').strip('.')
                    if companies:
                        companies[-1].setdefault("url", url)
                    else:
                        companies.append({"company_name": "ExampleCo", "url": url})
                else:
                    candidate = part.strip('"').strip(',').strip('.')
                    # accept candidate if it's titlecased, alphabetic-ish and not a stopword
                    if (
                        len(candidate) > 2
                        and candidate[0].isupper()
                        and candidate.lower() not in STOPWORDS
                        and candidate.isalpha()
                    ):
                        # avoid duplicates and limit total captured companies
                        if candidate not in [c.get("company_name") for c in companies]:
                            companies.append({"company_name": candidate})
                        if len(companies) >= 3:
                            break

            if not companies:
                companies = [{"company_name": "ExampleCo", "url": "https://example.com"}]

            competitor_profiles = []
            for c in companies:
                name = c.get("company_name", "ExampleCo")
                url = c.get("url", "https://example.com")
                competitor_profiles.append(
                    {
                        "company_name": name,
                        "url": url,
                        "messaging_analysis": "Placeholder messaging analysis synthesized from earlier outputs.",
                        "visual_analysis": {
                            "primary_colors": ["#112233", "#445566"],
                            "secondary_colors": ["#778899", "#aabbcc"],
                            "design_style": "Clean, modern layout with generous whitespace",
                            "emotional_tone": "Trustworthy and optimistic",
                            "logo_analysis": "Simple wordmark with subtle geometric tweak",
                        },
                    }
                )

            result = {
                "report_title": "Competitor Landscape Overview",
                "competitor_profiles": competitor_profiles,
                "comparative_summary": "Placeholder comparative summary across competitors.",
                "identified_gaps_and_opportunities": "Placeholder gaps and opportunities.",
                "strategic_recommendations": "Placeholder strategic recommendations.",
            }
            return json.dumps(result)

        # If we see indicators of BrandAnalysis, fall back to returning BrandAnalysis.
        if "primary_colors" in lower_text and "logo_analysis" in lower_text or "visual analysis" in lower_text:
            result = {
                "primary_colors": ["#112233", "#445566"],
                "secondary_colors": ["#778899", "#aabbcc"],
                "design_style": "Clean, modern layout with generous whitespace",
                "emotional_tone": "Trustworthy and optimistic",
                "logo_analysis": "Simple wordmark with subtle geometric tweak",
            }
            return json.dumps(result)

        # If prompt contains evidence of both visual and messaging JSON blobs
        # (e.g., prior task outputs), try to synthesize a CompetitorProfile
        if "primary_colors" in lower_text and ("messaging" in lower_text or "messaging_analysis" in lower_text or "hero" in lower_text):
            result = {
                "company_name": company or "ExampleCo",
                "url": url or "https://example.com",
                "messaging_analysis": "Placeholder messaging analysis synthesized from earlier outputs.",
                "visual_analysis": {
                    "primary_colors": ["#112233", "#445566"],
                    "secondary_colors": ["#778899", "#aabbcc"],
                    "design_style": "Clean, modern layout with generous whitespace",
                    "emotional_tone": "Trustworthy and optimistic",
                    "logo_analysis": "Simple wordmark with subtle geometric tweak",
                },
            }
            return json.dumps(result)

        # Default: Return a simple text response that CrewAI can parse
        return f"[NoOpLLM response] Prompt received: {text[:500]}"

    def supports_function_calling(self) -> bool:
        """Indicate whether this LLM supports function-calling style outputs.

        NoOpLLM does not support function calling; return False so the
        converter uses the text-based fallback path.
        """
        return False


class CompetitorAnalysisAgents:
    def web_recon_agent(self):
        llm = _get_gemini_llm() or NoOpLLM()
        tools = []
        if WebsiteScraperTool is not None:
            tools.append(WebsiteScraperTool())
        return Agent(
            role="Web Reconnaissance Specialist",
            goal="Scrape competitor websites.",
            backstory="You are a master of the web...",
            tools=tools,
            llm=llm,
        )

    def visual_brand_analyst_agent(self):
        llm = _get_gemini_llm() or NoOpLLM()
        tools = []
        if GeminiVisionTool is not None:
            tools.append(GeminiVisionTool())
        return Agent(
            role="Visual Brand Analyst",
            goal="Analyze visual elements from competitor websites.",
            backstory="You are a seasoned brand strategist...",
            tools=tools,
            llm=llm,
        )

    def content_strategist_agent(self):
        llm = _get_gemini_llm() or NoOpLLM()
        return Agent(
            role="Content Strategist",
            goal="Analyze text content from competitor websites.",
            backstory="You are an expert in marketing...",
            tools=[],
            llm=llm,
        )

    def strategic_insights_agent(self):
        llm = _get_gemini_llm() or NoOpLLM()
        return Agent(
            role="Strategic Insights Agent",
            goal="Synthesize all gathered data into a comprehensive report.",
            backstory="You are a high-level business strategist...",
            tools=[],
            llm=llm,
        )
    