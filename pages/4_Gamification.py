import streamlit as st
from packages.utils.utils import load_session_state, hide_streamlit_style
import plotly.express as px
import pandas as pd


# Leaderboards
PRODUCTIVITY = "Productivity"
QUALITATIVE = "Qualitative"
COMBINED = "Combined"


def build_productivity_df(points_per_star):
    df = pd.DataFrame(columns=[task_name for task_name in st.session_state.datasets.keys()] + ["Total Points"])


def build_qualitative_df():
    pass

def build_combined_df(productivity_df, qualitative_df, productivity_weight, qualitative_weight):
    pass


def run_app():
    with st.container():

        if st.session_state.leaderboards is not None:
            # Combined leaderboard goes here
            st.header("Leaderboards")

            left_column, right_column = st.columns(2)

            with left_column:
                st.subheader("Productivity Leaderboard")


                st.dataframe(st.session_state.leaderboards[PRODUCTIVITY])
                

            with right_column:
                st.subheader("Qualitative Leaderboard")
                
                pass

        else:
            st.info("No leaderboards available. Please create the leaderboards.")

        





    with st.sidebar:
        st.header("Gamification")

        points_per_star = st.number_input("Points per Star", min_value=1, value=10
                                          , help="The points to distribute per star for each task")
        

        left_column, right_column = st.columns(2)

        with left_column:
            productivity_weight = st.number_input("Productivity Weight", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

        with right_column:
            qualitative_weight = st.number_input("Qualitative Weight", value=1-productivity_weight, disabled=True)


        leaderboards_button = st.button("Create Leaderboards", use_container_width=True)


        if leaderboards_button:

            if st.session_state.lp_model_info is None:
                st.error("Please generate a Linear Programming model first.")
                return
                
            else:

                productivity_df = build_productivity_df(points_per_star)

                qualitative_df = build_qualitative_df()

                combined_df = build_combined_df(productivity_df, qualitative_df, productivity_weight, qualitative_weight)

                st.session_state.leaderboards = {PRODUCTIVITY: productivity_df, QUALITATIVE: qualitative_df, COMBINED: combined_df}


if __name__ == "__main__":
    st.set_page_config(page_title="Gamification", page_icon=":trophy:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
