import streamlit as st
import json


def load_session_state():
    """
    Load the session state variables for the first time
    """
    if len(st.session_state) == 0:
        # Dataset Generator
        st.session_state.datasets = {}  # Datasets dictionary
        st.session_state.selected_dataset = None    # Selected dataset
        st.session_state.disabled = False   # Disabled state of the number input
        st.session_state.number_of_employees = 0 # Number of employees
        # Linear Programming
        st.session_state.lp_dataframe = None    # Dataframe with the unit processing times
        st.session_state.lp_model_info = None    # Linear Programming model
        st.session_state.lp_changed = True # Used to check if the LP model is no longer valid for current datasets
        st.session_state.total_pieces = 0 # Total number of pieces
        st.session_state.total_time = 0 # Total time
        # Gamification
        st.session_state.leaderboards= None # Leaderboards dictionary
        st.session_state.points_per_star = 0 # Points per star selected
        st.session_state.min_qualitative_value = 0 # Minimum qualitative value selected displayed
        st.session_state.max_qualitative_value = 0 # Maximum qualitative value selected displayed
        st.session_state.productivity_weight = 0 # Productivity weight selected displayed
        st.session_state.qualitative_weight = 0 # Qualitative weight selected displayed


@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def hide_streamlit_style():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
