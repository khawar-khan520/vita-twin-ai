import sys
import os

# Fix module imports for Render + local
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from rag.generator import run_pipeline

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="VitaTwin Mind AI",
    layout="wide"
)

# -----------------------------------
# Title
# -----------------------------------
st.title("🧠 VitaTwin Mind AI")
st.subheader("Mental Health Intelligence System")

st.write(
    "Analyze stress, burnout risk, sleep patterns, and emotional deterioration "
    "using RAG + Knowledge Graph reasoning."
)

# -----------------------------------
# User Input
# -----------------------------------
query = st.text_input(
    "Ask about mental health state:",
    placeholder="Example: high stress, low sleep, burnout"
)

# -----------------------------------
# Analyze Button
# -----------------------------------
if st.button("Analyze"):

    if not query:
        st.warning("Please enter a query.")
        st.stop()

    try:

        # -----------------------------------
        # Run AI Pipeline
        # -----------------------------------
        result = run_pipeline(query)

        # ===================================
        # 1. Retrieved Context (RAG)
        # ===================================
        st.subheader("📚 Retrieved Context (RAG)")

        retrieved_entries = result.get("retrieved_entries", [])

        if retrieved_entries:
            st.json(retrieved_entries)
        else:
            st.info("No retrieved context available.")

        # ===================================
        # 2. Risk Assessment
        # ===================================
        st.subheader("📊 Risk Assessment")

        risk = result.get("risk_assessment", {})

        risk_level = risk.get("risk_level", "UNKNOWN")

        # Colorized risk display
        if risk_level == "HIGH":
            st.error(f"Risk Level: {risk_level}")
        elif risk_level == "MEDIUM":
            st.warning(f"Risk Level: {risk_level}")
        else:
            st.success(f"Risk Level: {risk_level}")

        st.write(f"**Average Stress:** {risk.get('avg_stress', 'N/A')}")
        st.write(f"**Average Sleep:** {risk.get('avg_sleep', 'N/A')}")

        # Reasons
        st.markdown("### 🔍 Detected Factors")

        reasons = risk.get("reason", [])

        if reasons:
            for r in reasons:
                st.write("•", r)
        else:
            st.info("No risk factors detected.")

        # ===================================
        # 3. AI Explanation
        # ===================================
        st.subheader("🧠 AI Explanation")

        explanation = result.get("explanation", {})

        st.success(
            explanation.get(
                "summary",
                "No AI summary available."
            )
        )

        key_factors = explanation.get("key_factors", [])

        if key_factors:
            st.markdown("### Key Factors")

            for factor in key_factors:
                st.write("•", factor)

        # ===================================
        # 4. Knowledge Graph Insights
        # ===================================
        st.subheader("🔗 Knowledge Graph Insights")

        graph_edges = result.get("graph_edges", [])

        if graph_edges:

            for edge in graph_edges:
                st.write(f"• {edge}")

        else:
            st.info("No graph insights available.")

        # ===================================
        # 5. Input Evidence
        # ===================================
        st.subheader("🗂 Input Evidence")

        raw_logs = result.get("raw_logs", [])

        if raw_logs:
            st.json(raw_logs)
        else:
            st.info("No raw evidence available.")

    except Exception as e:

        st.error("Application Error")

        st.exception(e)