from typing import Dict, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objects as go

import streamlit as st

weights = {"skills": 0.4, "experience": 0.3, "education": 0.2, "other": 0.1}


@st.cache_data()
def create_radar_chart(results: List[Dict]) -> go.Figure:
    """Create a radar chart to display the candidate scores across categories"""

    # Create a copy of the results to avoid modifying the original data
    results_copy = [result.copy() for result in results]

    categories = ["Skills", "Experience", "Education", "Other"]

    fig = go.Figure()

    for result in results_copy:
        weighted_scores = {
            "skills": result["skills"],
            "experience": result["experience"],
            "education": result["education"],
            "other": result["other"],
        }

        raw_scores = {
            key: weighted_scores[key] / weights[key] for key in weighted_scores
        }

        values = [
            raw_scores["skills"],
            raw_scores["experience"],
            raw_scores["education"],
            raw_scores["other"],
        ]

        values += values[:1]

        categories_plot = categories + [categories[0]]

        fig.add_trace(
            go.Scatterpolar(
                r=values, theta=categories_plot, name=result["name"], fill="toself"
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="Candidate Comparison Radar Chart",
    )

    return fig


@st.cache_data()
def create_bar_charts(results: List[Dict]) -> Dict[str, go.Figure]:
    """Create various bar charts comparing candidates"""

    # Create a copy of the results to avoid modifying the original data
    results_copy = [result.copy() for result in results]

    components = ["skills", "experience", "education", "other"]
    for result in results_copy:
        # converting the weighted scores to raw scores
        for component in components:
            result[component] = result[component] / weights[component]

    df = pd.DataFrame(results_copy)

    total_score_fig = go.Figure(
        data=[go.Bar(x=df["name"], y=df["total_score"], marker_color="#4CAF50")]
    )
    total_score_fig.update_layout(
        title="Total Score Comparison",
        yaxis_title="Total Score",
        xaxis_title="Candidates",
        yaxis_range=[0, 100],
    )

    components = ["skills", "experience", "education", "other"]
    comp_fig = go.Figure()

    for component in components:
        comp_fig.add_trace(
            go.Bar(
                name=component.capitalize(),
                x=df["name"],
                y=df[component],
            )
        )

    comp_fig.update_layout(
        barmode="group",
        title="Component-wise Score Comparison",
        yaxis_title="Score",
        xaxis_title="Candidates",
        yaxis_range=[0, 100],
    )

    return {"total": total_score_fig, "components": comp_fig}
