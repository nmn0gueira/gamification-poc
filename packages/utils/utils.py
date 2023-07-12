import streamlit as st
import requests


def load_session_state():
    """
    Load the session state variables for the first time
    """
    if len(st.session_state) == 0:
        st.session_state.datasets = {}  # Datasets dictionary
        st.session_state.selected_dataset = None    # Selected dataset
        st.session_state.disabled = False   # Disabled state of the number input
        st.session_state.lp_dataframe = None    # Dataframe with the unit processing times
        st.session_state.lp_model = None    # Linear Programming model
        st.session_state.lp_changed = True # Used to check if the LP model is no longer valid for current datasets
        st.session_state.average_productivity_per_task = 0 # Average productivity per task

@st.cache_data
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def hide_streamlit_style():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
