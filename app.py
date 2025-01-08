import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict
import numpy as np

from src.utils.pdf_loader import parse_pdf
from src.llm.llm_config import get_llm
from src.resume_analyzer import ResumeAnalysisSystem
from src.utils.chart_builder import create_radar_chart, create_bar_charts

# Initialize session state variables if they don't exist
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "results" not in st.session_state:
    st.session_state.results = []
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

# Set page configuration
st.set_page_config(layout="wide", page_title="Resume Analyzer")

# Custom CSS for better styling
st.markdown(
    """
    <style>
        .main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
        }
        .css-1d391kg {
            padding: 2rem;
        }
        .stProgress > div > div > div > div {
            background-color: #4CAF50;
        }
        /* Center the upload box */
        .css-1v0mbdj.etr89bj1 {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 150px;
            max-width: 1200px;
        }
        /* Center text in columns */
        .st-emotion-cache-1v0mbdj {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        /* Adjust container width */
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 2rem;
            margin: 0 auto;
        }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def get_resume_system():
    llm = get_llm()
    resume_system = ResumeAnalysisSystem(llm)
    return resume_system


@st.cache_resource
def analyze_resume(resume_text, job_description):
    resume_system = get_resume_system()
    result = resume_system.analyze_resume(resume_text, job_description)
    return result


def clear_session_state():
    st.session_state.job_description = ""
    st.session_state.results = []
    st.session_state.analysis_complete = False
    # Clear all full_result keys
    keys_to_remove = [
        key for key in st.session_state.keys() if key.startswith("full_result_")
    ]
    for key in keys_to_remove:
        del st.session_state[key]


@st.cache_data()
def adjusted_score(component, score):
    weights = {"skills": 0.4, "experience": 0.3, "education": 0.2, "other": 0.1}

    return score / weights[component]


def main():
    st.title("🎯 Advanced Resume Matching System")

    st.markdown("### 📝 Input Details")
    job_description = st.text_area(
        "Enter Job Description",
        value=st.session_state.job_description,
        height=200,
        key="job_description_input_1",
    )

    uploaded_files = st.file_uploader(
        "Upload Resume PDFs", type=["pdf"], accept_multiple_files=True
    )

    analyze_button = st.button("🔍 Analyze Resumes")
    clear_button = st.button("🗑️ Clear All")

    if clear_button:
        clear_session_state()
        st.experimental_rerun()

    if analyze_button:
        if not job_description:
            st.error("⚠️ Please provide a job description.")
            return

        if not uploaded_files:
            st.error("⚠️ Please upload at least one resume.")
            return

        with st.spinner("🔄 Analyzing resumes..."):
            # Store job description in session state
            st.session_state.job_description = job_description

            # Parse resumes and analyze
            results = []
            for idx, file in enumerate(uploaded_files):
                with st.status(f"📄 Processing {file.name}..."):
                    resume_text = parse_pdf(file)
                    result = analyze_resume(resume_text, job_description)

                    result_summary = {
                        # "name": file.name.replace(".pdf", ""),
                        "name": result["name"],
                        "total_score": result["total_score"],
                        "skills": result["component_scores"]["skills"]["score"],
                        "experience": result["component_scores"]["experience"]["score"],
                        "education": result["component_scores"]["education"]["score"],
                        "other": result["component_scores"]["other"]["score"],
                    }
                    results.append(result_summary)

                    # Store full result in session state
                    st.session_state[f"full_result_{idx}"] = result

            # Store results in session state
            st.session_state.results = results
            st.session_state.analysis_complete = True

    # Display results if analysis is complete (either from this run or previous)
    if st.session_state.analysis_complete and st.session_state.results:
        st.success("✅ Analysis Completed!")

        st.markdown("### 📊 Analysis Results")

        with st.container():
            chart_col1, chart_col2 = st.columns(2)
            bar_figs = create_bar_charts(st.session_state.results)

            with chart_col1:
                st.plotly_chart(bar_figs["total"])

            with chart_col2:
                st.plotly_chart(bar_figs["components"])

        with st.container():
            radar_fig = create_radar_chart(st.session_state.results)
            st.plotly_chart(radar_fig, use_container_width=True)

        st.markdown("### 📋 Detailed Results")
        for idx, res in enumerate(st.session_state.results):
            with st.expander(f"📄 {res['name']} (Score: {res['total_score']:.1f})"):
                full_result = st.session_state[f"full_result_{idx}"]

                det_col1, det_col2 = st.columns(2)

                with det_col1:
                    st.markdown("#### Component Scores")
                    for component, score in full_result["component_scores"].items():
                        raw_score = adjusted_score(component, score["score"])
                        weight_adjusted_score = score["score"]
                        st.progress(raw_score / 100)
                        st.markdown(f"**{component.title()}**: {raw_score:.1f}")
                        st.markdown(
                            f"**{component.title()} - Weight Adjusted**: {weight_adjusted_score:.1f}"
                        )
                        st.markdown(f"*{score['reason']}*")

                with det_col2:
                    st.markdown("#### 🎯 Matching Skills")
                    st.write(full_result["analysis"]["matching_skills"])

                st.markdown("#### 💡 Recommendations")
                recommendations = (
                    full_result["recommendations"].encode().decode("unicode_escape")
                )
                st.markdown(recommendations)


if __name__ == "__main__":
    main()
