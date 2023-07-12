import streamlit as st
import pandas as pd
from packages.linear_programming.lp_solver import solve_linear_programming, Status
from packages.utils.utils import load_session_state, hide_streamlit_style


def display_model():
    # Display the objective function
    st.header("Objective Function")
    st.write(str(st.session_state.lp_model.objective))

    # Display the variables and their values in a table
    st.header("Variables")
    variables_table = []

    for variable in st.session_state.lp_model.variables():
        variables_table.append([variable.name, variable.varValue])
    st.table(variables_table)

    # Display the constraints
    st.header("Constraints")
    for constraint in st.session_state.lp_model.constraints.values():
        st.write(str(constraint))

    st.header("Pieces produced")
    # The total number of pieces produced is the value of the objective function divided by the number of tasks
    st.write(st.session_state.lp_model.objective.value()/len(st.session_state.lp_dataframe))


def run_app():
    st.title("Linear Programming")

    with st.container():
        if st.session_state.lp_dataframe is not None:  
            st.dataframe(st.session_state.lp_dataframe)

            # Make check to verify if datasets have been changed without loading again
            # If so, warn the user

            if st.session_state.lp_model is not None:
                # {0: 'Not Solved', 1: 'Optimal', -1: 'Infeasible', -2: 'Unbounded', -3: 'Undefined'}
                status = st.session_state.lp_model.status

                match status:
                    case Status.OPTIMAL:
                        st.success("Optimal Solution Found")
                        display_model()
                    case Status.INFEASIBLE:
                        st.error("Infeasible Problem")
                        st.info("Make sure the minimum hours worked is not too high.")
                    case Status.UNBOUNDED:
                        st.error("Unbounded Problem")
                    case Status.UNDEFINED:
                        st.error("Undefined Problem")
                    case _:
                        st.warning("No Solution Found")


        else:
            st.info("Linear programming data frame not built. Please build the data frame first, make sure you have generated datasets.")


    with st.sidebar:
        st.header("Linear Programming Model Solver")

        min_hours_worked = st.number_input("Minimum hours of work required", min_value=1, value=100)

        left_column, right_column = st.columns(2)

        with left_column:
            build_button = st.button("Build dataframe")

        with right_column:
            solve_button = st.button("Solve LP problem")

        if build_button:
            if len(st.session_state.datasets) == 0:
                st.warning("No datasets to use. Please generate a dataset.")
                
            else:
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
                st.session_state.lp_model = None
                st.experimental_rerun()

        if solve_button:
            if st.session_state.lp_dataframe is None:
                st.warning("No problem to solve. Please build the dataframe first.")

            else:
                st.session_state.lp_model = solve_linear_programming(st.session_state.lp_dataframe, min_hours_worked)
                st.experimental_rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="Linear Programming", page_icon=":books:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
