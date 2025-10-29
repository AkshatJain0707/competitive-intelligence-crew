# main.py (COMPLETE FASTAPI BACKEND)
import os
import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew import CompetitorAnalysisCrew
from fastapi.middleware.cors import CORSMiddleware
import sys

# Ensure stdout/stderr are UTF-8 on Windows so emoji/log messages don't raise encoding errors
if sys.stdout.encoding is None or sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        # reconfigure may not be available in older Pythons; ignore if it fails
        pass

# ✅ Initialize FastAPI app
app = FastAPI(
    title="Competitor Intelligence Engine",
    description="An autonomous multi-agent competitor analysis system powered by CrewAI",
    version="1.0.0",
)

# ✅ Enable CORS for frontend / testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request Schema
class CompetitorRequest(BaseModel):
    company_name: str
    company_url: str

# ✅ Response Schema
class AnalysisResponse(BaseModel):
    status: str
    message: str
    report: dict | None = None


@app.get("/")
async def root():
    """Basic health check"""
    return {"message": "Competitor Intelligence Engine is running successfully!"}


@app.post("/analyze_competitor", response_model=AnalysisResponse)
async def analyze_competitor(request: CompetitorRequest):
    """
    Trigger the complete multi-agent competitor analysis workflow.
    """
    try:
        company_name = request.company_name.strip()
        company_url = request.company_url.strip()

        if not company_name or not company_url:
            raise HTTPException(status_code=400, detail="Company name and URL are required.")

        print(f"\nInitiating analysis for: {company_name} ({company_url})")

        crew_instance = CompetitorAnalysisCrew()
        final_report = crew_instance.run(company_name, company_url)

        if not final_report:
            raise HTTPException(status_code=500, detail="Crew execution failed to produce a report.")

        return AnalysisResponse(
            status="success",
            message=f"Analysis for {company_name} completed successfully.",
            report=final_report if isinstance(final_report, dict) else {"output": str(final_report)},
        )

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        print(f"Internal Server Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# ✅ Optional: Local Testing Entry Point
if __name__ == "__main__":
    import uvicorn

    print("\nLaunching FastAPI Server for Competitor Analysis ...\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
