import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="VitaTwin AI", layout="wide")

st.title("🧠 VitaTwin Mind AI")

st.write("Mental Health Analysis System")

# ALWAYS VISIBLE INPUT (IMPORTANT)
query = st.text_input("Ask about mental health state:")

# Button separate from input
clicked = st.button("Analyze")

if clicked:
    if query:
        st.success(f"Query received: {query}")
    else:
        st.warning("Please enter a query")