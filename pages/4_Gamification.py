import streamlit as st
from packages.utils.utils import load_session_state, hide_streamlit_style

def run_app():
    with st.container():
        st.header("Gamification")

        st.markdown("##")

        left_column, right_column = st.columns(2)

        with left_column:
            pass


    with st.sidebar:
        st.header("Gamification")

        points_per_star = st.number_input("Points per Star", min_value=1, value=10
                                          , help="The points to distribute per star for each task")

        left_column, right_column = st.columns(2)

        with left_column:
            pass    # Button to build the playerbase and the leaderboard
        with right_column:
            pass    # Button to randomize the qualitative factors


if __name__ == "__main__":
    st.set_page_config(page_title="Gamification", page_icon=":trophy:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
