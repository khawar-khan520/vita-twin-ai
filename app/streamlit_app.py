import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="VitaTwin AI", layout="wide")

st.title("🧠 VitaTwin Mind AI")
st.caption("Mental Health Analysis System")

query = st.text_input("Ask about mental health state:")
clicked = st.button("Analyze")

if clicked:
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Running AI pipeline..."):
            try:
                from rag.generator import run_pipeline
                result = run_pipeline(query)

                # Handle result whether it's a dict or a plain string
                if isinstance(result, dict):
                    st.success("Analysis complete.")

                    st.subheader("📊 Risk Assessment")

                    risk = result["risk_assessment"]

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Risk Level", risk["risk_level"])

                    with col2:
                        st.metric("Avg Stress", risk["avg_stress"])

                    with col3:
                        st.metric("Avg Sleep", risk["avg_sleep"])

                    st.subheader("🧠 Explanation")

                    for reason in risk.get("reason", []):
                        st.write("•", reason)

                    st.success(result["explanation"]["summary"])

                    st.subheader("📚 Retrieved Entries")

                    for i, entry in enumerate(result["retrieved_entries"]):
                        st.markdown(f"### Entry {i + 1}")
                        st.write(f"User: {entry['user_id']}")
                        st.write(f"Date: {entry['date']}")
                        st.write(f"Mood: {entry['mood_score']}")
                        st.write(f"Stress: {entry['stress_level']}")
                        st.write("---")

            except ImportError as e:
                st.error("Could not import the AI pipeline. Check your `rag/generator.py` file.")
                st.exception(e)
            except Exception as e:
                st.error("Pipeline crashed. See details below.")
                st.exception(e)