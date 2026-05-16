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
                    st.write(result.get("risk_assessment", "No risk assessment returned."))

                    st.subheader("🧠 Explanation")
                    explanation = result.get("explanation", {})
                    if isinstance(explanation, dict):
                        st.write(explanation.get("summary", "No summary returned."))
                    else:
                        st.write(explanation)

                    # Show full result in expander for debugging
                    with st.expander("Full response (debug)"):
                        st.json(result)

                else:
                    # run_pipeline returned a plain string
                    st.success("Analysis complete.")
                    st.write(result)

            except ImportError as e:
                st.error("Could not import the AI pipeline. Check your `rag/generator.py` file.")
                st.exception(e)
            except Exception as e:
                st.error("Pipeline crashed. See details below.")
                st.exception(e)