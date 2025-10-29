# app.py (Streamlit Frontend for Competitor Intelligence Engine)
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ✅ FastAPI backend URL
API_URL = "http://localhost:8000/analyze_competitor"

# 🎨 Streamlit page configuration
st.set_page_config(
    page_title="Competitor Intelligence Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar Section ---
st.sidebar.title("⚙️ Configuration")
st.sidebar.info(
    "This app uses a multi-agent CrewAI backend to analyze competitor websites "
    "using **Gemini LLM**, **visual intelligence**, and **strategic synthesis**."
)
st.sidebar.markdown("---")
st.sidebar.write("Developed by [Akshat Sunil Jain](#) 🌟")

# --- Header Section ---
st.markdown(
    """
    <div style='text-align: center; padding: 10px 0;'>
        <h1 style='color: #2E86C1;'>🏁 Competitor Intelligence Engine</h1>
        <p style='font-size:18px; color: #5D6D7E;'>Unleash multi-agent intelligence to decode your competitors’ strategy, design, and market position.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Input Form ---
st.markdown("### 🔍 Enter Competitor Details")
col1, col2 = st.columns([1, 2])

with col1:
    company_name = st.text_input("**Company Name**", placeholder="e.g., OpenAI")
with col2:
    company_url = st.text_input("**Website URL**", placeholder="e.g., https://openai.com")

analyze_btn = st.button("🚀 Start Analysis", use_container_width=True)

# --- On Button Click ---
if analyze_btn:
    if not company_name or not company_url:
        st.warning("⚠️ Please enter both company name and website URL.")
    else:
        with st.spinner("⏳ Running full competitor analysis using CrewAI agents..."):
            try:
                # Simple retry/backoff for transient connection errors
                from requests.adapters import HTTPAdapter
                from urllib3.util.retry import Retry

                session = requests.Session()
                retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
                session.mount("http://", HTTPAdapter(max_retries=retries))

                response = session.post(API_URL, json={"company_name": company_name, "company_url": company_url}, timeout=30)
                if response.status_code == 200:
                    result = response.json()

                    if result["status"] == "success":
                        st.success(f"✅ Analysis Completed: {company_name}")
                        report = result["report"]

                        # --- Display Structured Report ---
                        st.markdown("## 📊 Strategic Report Summary")
                        st.markdown(f"**{report.get('report_title', 'Untitled Report')}**")
                        st.markdown(f"_{report.get('comparative_summary', 'No summary available.')}_")

                        st.markdown("### 🧩 Identified Gaps & Opportunities")
                        st.info(report.get("identified_gaps_and_opportunities", "N/A"))

                        st.markdown("### 🎯 Strategic Recommendations")
                        st.success(report.get("strategic_recommendations", "N/A"))

                        # --- Competitor Profiles Section ---
                        st.markdown("---")
                        st.markdown("## 🏢 Competitor Profiles")

                        competitors = report.get("competitor_profiles", [])
                        for comp in competitors:
                            with st.expander(f"**{comp['company_name']}** ({comp['url']})", expanded=False):
                                st.markdown("#### 🗣 Messaging Analysis")
                                st.write(comp.get("messaging_analysis", "N/A"))

                                visual = comp.get("visual_analysis", {})
                                st.markdown("#### 🎨 Visual Brand Analysis")

                                # Display colors beautifully
                                primary_colors = visual.get("primary_colors", [])
                                secondary_colors = visual.get("secondary_colors", [])
                                if primary_colors:
                                    st.write("**Primary Colors:**")
                                    cols = st.columns(len(primary_colors))
                                    for i, color in enumerate(primary_colors):
                                        cols[i].markdown(
                                            f"<div style='background-color:{color}; width:100%; height:40px; border-radius:5px;'></div>",
                                            unsafe_allow_html=True,
                                        )

                                if secondary_colors:
                                    st.write("**Secondary Colors:**")
                                    cols = st.columns(len(secondary_colors))
                                    for i, color in enumerate(secondary_colors):
                                        cols[i].markdown(
                                            f"<div style='background-color:{color}; width:100%; height:40px; border-radius:5px;'></div>",
                                            unsafe_allow_html=True,
                                        )

                                st.markdown("**Design Style:** " + visual.get("design_style", "N/A"))
                                st.markdown("**Emotional Tone:** " + visual.get("emotional_tone", "N/A"))
                                st.markdown("**Logo Analysis:** " + visual.get("logo_analysis", "N/A"))

                    else:
                        st.error(result.get("message", "Failed to generate report."))

                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "🚨 Could not connect to the backend at http://localhost:8000.\n"
                    "Make sure the FastAPI server is running (run `python main.py` or `uvicorn main:app --reload --port 8000`)"
                )
            except requests.exceptions.Timeout:
                st.error("🚨 Request timed out. The backend might be busy. Try again or increase the timeout.")
            except Exception as e:
                st.error(f"🚨 Unexpected Error: {e}")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#7F8C8D; font-size:14px;'>"
    "Made with ❤️ using CrewAI, Gemini, and Streamlit."
    "</div>",
    unsafe_allow_html=True,
)
