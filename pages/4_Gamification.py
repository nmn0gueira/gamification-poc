import streamlit as st
from packages.utils.utils import load_session_state, hide_streamlit_style

def run_app():
    st.title("Gamification")

if __name__ == "__main__":
    st.set_page_config(page_title="Gamification", page_icon=":trophy:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
