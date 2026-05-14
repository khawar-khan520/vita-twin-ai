import streamlit as st
from rag.generator import run_pipeline
from graph.graph_builder import MentalHealthGraph

st.set_page_config(page_title="VitaTwin Mind AI", layout="wide")

st.title("🧠 VitaTwin Mind AI – Mental Health Intelligence System")

st.write("Enter a query to analyze mental health patterns and risk signals.")

# Initialize graph
kg = MentalHealthGraph()

query = st.text_input("Ask about mental health state:")

if st.button("Analyze") and query:

    result = run_pipeline(query)

    st.subheader("📊 Risk Assessment")

    risk = result["risk_assessment"]

    st.write(f"**Risk Level:** {risk['risk_level']}")
    st.write(f"**Average Stress:** {risk['avg_stress']}")
    st.write(f"**Average Sleep:** {risk['avg_sleep']}")

    st.subheader("🧠 Explanation")

    for r in risk["reason"]:
        st.write("•", r)

    st.subheader("📌 AI Summary")
    st.success(result["explanation"]["summary"])