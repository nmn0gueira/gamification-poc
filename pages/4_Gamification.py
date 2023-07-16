import streamlit as st
from packages.utils.utils import load_session_state, hide_streamlit_style
import plotly.express as px
import pandas as pd
import numpy as np
from packages.gamification.leaderboards import create_unordered_empty_leaderboard, finalize_leaderboard

# Linear Programming model information
# OBJECTIVE = 0
VARIABLES = 1
# CONSTRAINTS = 2
# STATUS = 3


# Leaderboards
PRODUCTIVITY = "Productivity"
QUALITATIVE = "Qualitative"
COMBINED = "Combined"

# Ordinal suffixes
ORDINAL_SUFFIXES = ['st', 'nd', 'rd'] + ['th'] * 17 + ['st', 'nd', 'rd'] + ['th'] * 7 + ['st']

# Colors
GOLD = "#ffd700"
SILVER = "#c0c0c0"
BRONZE = "#cd7f32"
DEFAULT = "#3d85c6"


def display_leaderboard(df):
    # Display the dataframe as a table
    with st.container():
        st.dataframe(df, use_container_width=True)

    # Display the dataframe as a bar chart
    with st.container():
        placements = df.index

        color_discrete_sequence = [DEFAULT] * len(df)  # Initialize the color list with the default color

        # Change the color of the first bar to gold
        color_discrete_sequence[0] = GOLD
        # Change the color of the second bar to silver
        color_discrete_sequence[1] = SILVER
        # Change the color of the third bar to bronze
        color_discrete_sequence[2] = BRONZE

        fig = px.bar(df,
                    x="Total Points",
                    y=placements,
                    color=placements,  # Use the placements as the color to get the same color for each bar
                    color_discrete_sequence=color_discrete_sequence,
                    orientation="h",
                    text_auto=True,
                    labels={"Total Points": "Points", "index": "Player"})

        for i in range(4, placements.size):  # Start from the 4th bar (index 3))):
            fig.data[i].showlegend = False  # Then, hide legends for the last 6 bars

        # Customize the label for the 4th bar's legend
        fig.data[3].name = '4th and below'
        
        # Update the y-axis labels using the mapping so that the player names are displayed instead of the index
        fig.update_yaxes(tickvals=[bar.y for bar in fig.data], ticktext=[df["Player"][i] for i in range(len(fig.data))])

        st.plotly_chart(fig, use_container_width=True)


def build_productivity_df(points_per_star):
    number_of_players = len(st.session_state.datasets[st.session_state.selected_dataset][0])
    tasks = [task_name for task_name in st.session_state.datasets.keys()]
    df = create_unordered_empty_leaderboard(number_of_players, tasks)

    for task_name, (dataset, _, task_difficulty) in st.session_state.datasets.items():
        max_points = points_per_star * task_difficulty

        # The calculated formula gives the most points to the faster employees who worked on the task (regardless of
        # the number of tasks executed) List with only the employees that worked on this task
        task_workers_info = [index for index, value in enumerate(st.session_state.lp_model_info[VARIABLES][task_name])
                             if value > 0]

        # Sort the list by the processing time
        task_workers_info.sort(key=lambda x: dataset["unit_processing_time"][x])  # Sort the list by the processing time

        # Distribute the points to the players
        for i in range(len(task_workers_info)):
            points = int(max_points / (i + 1))  # The points are distributed in a decreasing fashion
            df.loc[task_workers_info[i], task_name] = points
            df.loc[task_workers_info[i], "Total Points"] += points

    df = finalize_leaderboard(df)

    return df


def build_qualitative_df(min_qualitative_value, max_qualitative_value):
    # Randomly generate the qualitative values for each employee
    number_of_players = len(st.session_state.datasets[st.session_state.selected_dataset][0])

    qualitative_factors = ["Self-assessment", "Engagement"]

    df = create_unordered_empty_leaderboard(number_of_players, qualitative_factors)

    for qualitative_factor in qualitative_factors:
        df[qualitative_factor] = [np.random.randint(min_qualitative_value, max_qualitative_value) for _ in
                                  range(number_of_players)]
        df["Total Points"] += df[qualitative_factor]
        
    df = finalize_leaderboard(df)

    return df


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

                display_leaderboard(st.session_state.leaderboards[PRODUCTIVITY])

            with right_column:
                st.subheader("Qualitative Leaderboard")
       
                display_leaderboard(st.session_state.leaderboards[QUALITATIVE])

        else:
            st.info("No leaderboards available. Please create the leaderboards.")

    with st.sidebar:
        st.header("Gamification")

        st.subheader("Productivity", help="The productivity leaderboard is based on the points earned for each task")

        points_per_star = st.number_input("Points per Star", min_value=1, value=10
                                          , help="The points to distribute per star for each task")

        st.markdown("---")

        st.subheader("Qualitative",
                     help="The qualitative leaderboard is randomly generated for each employee based on the minimum and maximum values")

        left_column, right_column = st.columns(2)

        with left_column:
            min_qualitative_value = st.number_input("Minimum", min_value=0, max_value=100, value=0, step=1)

        with right_column:
            max_qualitative_value = st.number_input("Maximum", min_value=min_qualitative_value, max_value=100,
                                                    value=100, step=1)

        st.markdown("---")

        st.subheader("Combined",
                     help="The combined leaderboard is based on the weighted average of the productivity and qualitative values for each task")
        left_column, right_column = st.columns(2)

        with left_column:
            productivity_weight = st.number_input("Productivity Weight", min_value=0.0, max_value=1.0, value=0.5,
                                                  step=0.1)

        with right_column:
            qualitative_weight = st.number_input("Qualitative Weight", value=1 - productivity_weight, disabled=True)

        leaderboards_button = st.button("Create Leaderboards", use_container_width=True)

        if leaderboards_button:

            if st.session_state.lp_model_info is None:
                st.error("Please generate a Linear Programming model first.")
                return

            else:

                productivity_df = build_productivity_df(points_per_star)

                qualitative_df = build_qualitative_df(min_qualitative_value, max_qualitative_value)

                combined_df = build_combined_df(productivity_df, qualitative_df, productivity_weight,
                                                qualitative_weight)

                st.session_state.leaderboards = {PRODUCTIVITY: productivity_df, QUALITATIVE: qualitative_df,
                                                 COMBINED: combined_df}

                st.experimental_rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="Gamification", page_icon=":trophy:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
