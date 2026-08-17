"""
Decision trail, DE/PSO convergence, sentiment-tier breakdown.

Run with: streamlit run dashboard/app.py

Kept to Streamlit rather than a custom React app with websockets —
enough to demo the multi-agent decision-making clearly without taking
on real-time front-end infrastructure this project doesn't need.
"""
import streamlit as st

st.set_page_config(page_title="Agentic Financial Engine", layout="wide")
st.title("Agentic Neuro-Symbolic Financial Engine")

# TODO, roughly in priority order:
#  1. Decision trail table — read RiskDecision logs from orchestrator.run_pipeline
#  2. DE/PSO convergence plot — fitness vs. generation, from optimize.tune_signal_weights
#  3. Sentiment-tier breakdown — counts/scores from OracleOutput logs
#  4. Interpretability view — attention weights / Integrated Gradients for the
#     transformer, SHAP for the sentiment classifier only (see docs/future-work.md
#     for why not the whole pipeline)

st.info("Scaffold only — wire up sections above as each track's pieces land.")
