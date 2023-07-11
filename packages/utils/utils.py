import streamlit as st
import requests

def load_session_state():
    """
    Load the session state variables
    """
    if not st.session_state:
        st.session_state.datasets = {}
        st.session_state.selected_dataset = None
        st.session_state.disabled = False
        st.session_state.lp_dataframe = None
        st.session_state.lp_model = None


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
