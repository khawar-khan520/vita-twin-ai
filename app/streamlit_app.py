import streamlit as st
from rag.generator import run_pipeline
from graph.graph_builder import MentalHealthGraph

st.set_page_config(page_title="VitaTwin Mind AI", layout="wide")

st.title("🧠 VitaTwin Mind AI – Mental Health Intelligence System")

st.write("Enter a query to analyze mental health patterns and risk signals.")

kg = MentalHealthGraph()

query = st.text_input("Ask about mental health state:")

if st.button("Analyze") and query:

    result = run_pipeline(query)

    # -----------------------------
    # 1. Retrieved Context (RAG)
    # -----------------------------
    st.subheader("📚 Retrieved Context (RAG)")

    retrieved = result.get("retrieved_entries", [])
    if retrieved:
        st.json(retrieved)
    else:
        st.info("No retrieved entries available.")

    # -----------------------------
    # 2. Risk Assessment
    # -----------------------------
    st.subheader("📊 Risk Assessment")

    risk = result.get("risk_assessment", {})

    st.write(f"**Risk Level:** {risk.get('risk_level', 'N/A')}")
    st.write(f"**Average Stress:** {risk.get('avg_stress', 'N/A')}")
    st.write(f"**Average Sleep:** {risk.get('avg_sleep', 'N/A')}")

    st.markdown("**Reasons:**")
    for r in risk.get("reason", []):
        st.write("•", r)

    # -----------------------------
    # 3. Explanation
    # -----------------------------
    st.subheader("🧠 Explanation")

    explanation = result.get("explanation", {})
    st.success(explanation.get("summary", "No summary available."))

    # -----------------------------
    # 4. Knowledge Graph
    # -----------------------------
    st.subheader("🔗 Knowledge Graph Insights")

    graph_edges = result.get("graph_edges", [])
    if graph_edges:
        st.write(graph_edges)
    else:
        st.info("Graph insights not available.")

    # -----------------------------
    # 5. Raw Evidence (optional)
    # -----------------------------
    st.subheader("🗂 Input Evidence")

    raw_logs = result.get("raw_logs", [])
    if raw_logs:
        st.json(raw_logs)