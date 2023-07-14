import streamlit as st
from packages.utils.utils import load_session_state, hide_streamlit_style
import plotly.express as px
import pandas as pd

def run_app():
    with st.container():
        st.header("Gamification")

        st.markdown("##")

        left_column, right_column = st.columns(2)

        with left_column:
            st.subheader("Productivity Leaderboard")
            if st.session_state.productivity_leaderboard is not None:
                st.dataframe(st.session_state.productivity_leaderboard)
            else:
                st.info("No leaderboard available. Please build the leaderboard.")

        with right_column:
            pass





    with st.sidebar:
        st.header("Gamification")

        points_per_star = st.number_input("Points per Star", min_value=1, value=10
                                          , help="The points to distribute per star for each task")

        left_column, right_column = st.columns(2)

        with left_column:
            prod_leaderboard_button = st.button("Build Productivity Leaderboard", use_container_width=True)
          

            pass    # Button to build the leaderboard (a dataframe with the employees and their points for each task and a total)
        with right_column:
            pass    # Button to randomize the qualitative factors


        if prod_leaderboard_button:

            if st.session_state.lp_model_info is None:
                st.error("Please generate a Linear Programming model first.")
                return
                
            else:
                df = pd.DataFrame(columns=[task_name for task_name in st.session_state.datasets.keys()] + ["Total Points"])

                st.session_state.productivity_leaderboard = df  


if __name__ == "__main__":
    st.set_page_config(page_title="Gamification", page_icon=":trophy:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
