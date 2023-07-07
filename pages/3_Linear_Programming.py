import streamlit as st
import pandas as pd
from packages.linear_programming.lp_solver import solve_linear_programming

def run_app():
    st.title("Linear Programming")

    with st.container():
        if st.session_state.lp_dataframe is not None:  
            st.dataframe(st.session_state.lp_dataframe)

            # Make check to verify if datasets have been changed without loading again
            # If so, warn the user

            if st.session_state.lp_solution is not None:
                 # Display the objective function
                st.header("Objective Function")
                st.write(str(st.session_state.lp_solution.objective))

                # Display the variables and their values in a table
                st.header("Variables")
                variables_table = []

                for variable in st.session_state.lp_solution.variables():
                    variables_table.append([variable.name, variable.varValue])
                st.table(variables_table)

                # Display the constraints
                st.header("Constraints")
                for constraint in st.session_state.lp_solution.constraints.values():
                    st.write(str(constraint))

        else:
            st.write("Upload a dataset to start")

        


    with st.sidebar:
        st.header("LP Solver")
        load_button = st.button("Load Datasets")
        solve_button = st.button("Solve")

        if load_button:       
            number_of_employees = len(st.session_state.datasets[st.session_state.selected_dataset][0]) # Each employee is a row in the dataset

            df = pd.DataFrame(columns=["Person " + str(i+1) for i in range(number_of_employees)])
            capacities = []

            # Create complete dataframe with unit processing times
            # Load from datasets
            for task_name, (dataset, capacity) in st.session_state.datasets.items():
                unit_processing_times = dataset['unit_processing_time'].values
                df.loc[task_name] = unit_processing_times
                capacities.append(capacity)

            df['Capacity'] = capacities

            st.session_state.lp_dataframe = df
            st.session_state.lp_solution = None
            st.experimental_rerun()

        if solve_button:
            st.session_state.lp_solution = solve_linear_programming(st.session_state.lp_dataframe)
            st.experimental_rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="Linear Programming", page_icon=":books:", layout="wide")

    if "lp_dataframe" not in st.session_state:
        st.session_state.lp_dataframe = None  # Dataframe with the unit processing times

    if "lp_solution" not in st.session_state:
        st.session_state.lp_solution = None

    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)  # Hide the Streamlit footer and menu button
    run_app()
