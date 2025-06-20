# menu.py
import streamlit as st
import importlib

PAGES = {
    "Upload Notes": "pages.upload",
    "Summary Generator": "pages.summary",
    "Mind Map": "pages.mindmap",
    "Flashcards": "pages.flashcards",
    "Quiz Generator": "pages.quiz",
}

def render_menu():
    st.sidebar.title("📘 StudyLens")
    choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
    page = importlib.import_module(PAGES[choice])
    page.app()
