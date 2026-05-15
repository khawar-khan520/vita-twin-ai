import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from rag.generator import run_pipeline

st.set_page_config(page_title="VitaTwin Mind AI", layout="wide")

st.title("🧠 VitaTwin Mind AI")
st.write("Mental Health Intelligence System")

query = st.text_input("Ask about mental health state:")

if st.button("Analyze"):

    if query:

        result = run_pipeline(query)

        st.subheader("📊 Risk Assessment")

        risk = result.get("risk_assessment", {})

        st.write("Risk Level:", risk.get("risk_level"))

        st.subheader("🧠 Explanation")

        explanation = result.get("explanation", {})
        st.write(explanation.get("summary"))

    else:
        st.warning("Please enter a query.")