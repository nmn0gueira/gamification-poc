import streamlit as st

def run_app():
    st.title("Linear Programming")

    number_of_employees = len(st.session_state.datasets[st.session_state.selected_dataset]) # Each employee is a row in the dataset

    dataframe = pd.DataFrame(columns=["Person " + str(i+1) for i in range(number_of_employees)])
    capacities = []
    variables = {}

    # Create complete dataframe with unit processing times
    # Load from datasets
    for task_name, dataset in st.session_state.datasets.items():
        capacity = int(input("Enter capacity: "))

        unit_processing_times = dataset['unit_processing_time'].values
        dataframe.loc[task_name] = unit_processing_times

        capacities.append(capacity)
        variables[task_name] = []
    
    dataframe['Capacity'] = capacities



  
if __name__ == '__main__':
    import sys
    import subprocess
    import pandas as pd
    from pulp import *


if __name__ == "__main__":
    st.set_page_config(page_title="Linear Programming", page_icon=":books:", layout="wide")

    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)  # Hide the Streamlit footer and menu button
    run_app()
