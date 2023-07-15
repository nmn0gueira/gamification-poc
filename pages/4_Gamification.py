import streamlit as st
from packages.utils.utils import load_session_state, hide_streamlit_style
import plotly.express as px
import pandas as pd
from pandas.api.types import CategoricalDtype

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


def build_productivity_df(points_per_star):
    number_of_players = len(st.session_state.datasets[st.session_state.selected_dataset][0])
    placements = [i for i in range(number_of_players)]
    tasks = [task_name for task_name in st.session_state.datasets.keys()]
    df = pd.DataFrame(index=placements, columns=["Player"] + tasks)
    df.index.name = "Placement"

    total_points = [0] * number_of_players # Initialized list to store the total points for each player

    for task_name, (dataset, _, task_difficulty) in st.session_state.datasets.items():
        max_points = points_per_star * task_difficulty

        # The calculated formula gives the most points to the faster employees who worked on the task (regardless of the number of tasks executed)
        # List with only the employees that worked on this task
        task_workers_info = [index for index, value in enumerate(st.session_state.lp_model_info[VARIABLES][task_name]) if value > 0]

        # Sort the list by the processing time
        task_workers_info.sort(key=lambda x: dataset["unit_processing_time"][x])  # Sort the list by the processing time

        # Distribute the points to the players
        for i in range(len(task_workers_info)):
            points = int(max_points/(i+1))  # The points are distributed in a decreasing fashion
            df.loc[task_workers_info[i], task_name] = points
            total_points[task_workers_info[i]] += points


    df["Player"] = df.index.copy() + 1  # Add the player column
    
    df["Total Points"] = total_points      # Add the total points column

    # Sort the dataframe by the total points column
    df.sort_values(by="Total Points", ascending=False, inplace=True)

    df.reset_index(drop=True, inplace=True)  # Reset the index

    # Convert the index to Ordinal type with the defined suffixes
    df.index = (df.index+1).to_series().astype(CategoricalDtype(ordered=True)).map(lambda x: f"{x}{ORDINAL_SUFFIXES[x-1]}")

    return df

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

                # Display the dataframe as a table when the user clicks the button
                with left_column.expander("Display Chart", expanded=False):
                    st.dataframe(st.session_state.leaderboards[PRODUCTIVITY], use_container_width=True)


                fig = px.bar(st.session_state.leaderboards[PRODUCTIVITY], x="Total Points", y=st.session_state.leaderboards[PRODUCTIVITY].index, orientation="h", text_auto=True, labels={"Total Points": "Points", "index": "Player"})
                
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                
                # Update the y-axis labels using the mapping
                fig.update_yaxes(tickvals=[y for y in fig.data[0].y], ticktext=[st.session_state.leaderboards[PRODUCTIVITY]["Player"][i] for i in range(len(fig.data[0].y))])
                
                st.plotly_chart(fig, use_container_width=True)

                

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

                st.experimental_rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="Gamification", page_icon=":trophy:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
