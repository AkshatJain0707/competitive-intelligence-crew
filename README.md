
# Competitive Intelligence Crew

An autonomous multi-agent competitor analysis system powered by **CrewAI** and **Google Gemini**.

## Features

- **Web Reconnaissance**: Scrapes competitor websites for text content and imagery
- **Visual Brand Analysis**: Analyzes design, colors, and visual elements
- **Content Strategy**: Extracts messaging, value propositions, and positioning
- **Strategic Report Generation**: Synthesizes insights into actionable recommendations

## Architecture

The system uses a multi-agent workflow:

1. **Web Reconnaissance Specialist** - Scrapes website content and hero images
2. **Visual Brand Analyst** - Analyzes visual branding elements
3. **Content Strategist** - Analyzes messaging and positioning
4. **Strategic Insights Agent** - Synthesizes all data into a comprehensive report

## Setup

### Prerequisites

- Python 3.9+
- Google API Key (for Gemini LLM)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/competitive-intelligence-crew.git
cd competitive-intelligence-crew

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
ENABLE_LLM=1
```

2. To enable Gemini LLM:
   - Set `ENABLE_LLM=1` in `.env`
   - Ensure the Generative Language API is enabled in your Google Cloud project
   - Visit: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com

## Usage

### Start the FastAPI Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
GET /
```

#### Analyze Competitor
```bash
POST /analyze_competitor
Content-Type: application/json

{
  "company_name": "OpenAI",
  "company_url": "https://openai.com"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Analysis for OpenAI completed successfully.",
  "report": {
    "report_title": "...",
    "competitor_profiles": [...],
    "comparative_summary": "...",
    "identified_gaps_and_opportunities": "...",
    "strategic_recommendations": "..."
  }
}
```

## Development

### Project Structure

```
competitive-intelligence-crew/
├── agents.py              # Agent definitions
├── crew.py                # Crew orchestration
├── tasks.py               # Task definitions
├── models.py              # Pydantic data models
├── main.py                # FastAPI application
├── frontend.py            # Streamlit frontend
├── json_validator.py      # JSON validation utilities
├── tools/
│   ├── google_gemini_adapter.py  # Gemini API adapter
│   ├── scraper_tool.py           # Web scraping
│   └── vision_tool.py            # Vision analysis
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (not in repo)
└── README.md              # This file
```

### Development Mode (NoOpLLM)

To run without Gemini API (development mode):

```env
ENABLE_LLM=0
```

The system will use `NoOpLLM` which returns deterministic mock responses for testing.

### Running Tests

```bash
python -m pytest
```

## Models

### BrandAnalysis
```python
{
  "primary_colors": ["#hex1", "#hex2"],
  "secondary_colors": ["#hex3", "#hex4"],
  "design_style": "description",
  "emotional_tone": "description",
  "logo_analysis": "description"
}
```

### CompetitorProfile
```python
{
  "company_name": "Company Name",
  "url": "https://example.com",
  "messaging_analysis": "detailed analysis",
  "visual_analysis": {...}  # BrandAnalysis object
}
```

### StrategicReport
```python
{
  "report_title": "Report Title",
  "competitor_profiles": [...],
  "comparative_summary": "summary",
  "identified_gaps_and_opportunities": "gaps",
  "strategic_recommendations": "recommendations"
}
```

## Troubleshooting

### Gemini API Not Found
If you see `404 models/gemini-pro not found`:
- Enable the Generative Language API in Google Cloud Console
- Ensure your API key has proper permissions
- Set `ENABLE_LLM=0` to use development mode

### Empty LLM Response
- Check that `ENABLE_LLM` is properly configured
- Verify API key in `.env`
- Check server logs for detailed error messages

## Contributing

Contributions are welcome! Please submit pull requests or open issues for bugs and feature requests.

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open a GitHub issue.
>>>>>>> master
