import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.summarizer import summarize_text

def app():
    st.title("📄 Summary Generator")
    text = st.text_area("Enter or paste your academic content here:")

    if st.button("Generate Summary"):
        if text:
            summary = summarize_text(text)
            st.write(summary)
        else:
            st.error("Please enter some text.")
