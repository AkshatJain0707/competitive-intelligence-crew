import json
import re


def extract_json_from_text(text: str) -> dict | None:
    """Extract JSON from text, handling common formatting issues."""
    text = text.strip()
    
    if text.startswith('{'):
        end = text.rfind('}')
        if end != -1:
            text = text[:end+1]
    
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    
    return None


def validate_competitor_profile(data: dict) -> bool:
    """Check if data has all required CompetitorProfile fields."""
    required = {'company_name', 'url', 'messaging_analysis', 'visual_analysis'}
    return all(field in data for field in required)


def validate_brand_analysis(data: dict) -> bool:
    """Check if data has all required BrandAnalysis fields."""
    required = {'primary_colors', 'secondary_colors', 'design_style', 'emotional_tone', 'logo_analysis'}
    return all(field in data for field in required)


def validate_strategic_report(data: dict) -> bool:
    """Check if data has all required StrategicReport fields."""
    required = {'report_title', 'competitor_profiles', 'comparative_summary', 
                'identified_gaps_and_opportunities', 'strategic_recommendations'}
    return all(field in data for field in required)
