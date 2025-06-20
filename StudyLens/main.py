import streamlit as st
st.set_page_config(page_title="StudyLens", layout="wide")
import nest_asyncio
nest_asyncio.apply()
import nltk 
nltk.download('punkt_tab')
import importlib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Menu for page selection
def render_menu():
    PAGES = {
        "Upload Notes": "pages.upload",
        "Summary Generator": "pages.summary",
        "Mind Map": "pages.mindmap",
        "Flashcards": "pages.flashcards",
        "Quiz Generator": "pages.quiz",
    }
    
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Select a page:", list(PAGES.keys()))
    
    page = importlib.import_module(PAGES[choice])
    page.app()
    

if __name__ == "__main__":
    render_menu()
