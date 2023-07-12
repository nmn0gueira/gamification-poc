import streamlit as st
import pandas as pd
import plotly.express as px
from packages.linear_programming.lp_solver import solve_linear_programming, Status
from packages.utils.utils import load_session_state, hide_streamlit_style


def display_model():
    # Display the objective function
    left_column, right_column = st.columns(2)

    with left_column:
        st.subheader("Production")
        # The total number of pieces produced is the value of the objective function divided by the number of tasks
        st.subheader(f"{int(st.session_state.lp_model.objective.value()/len(st.session_state.lp_dataframe))} pieces")

    with right_column:
        st.subheader("Total Hours Worked")
        # st.subheader(f"{st.session_state.lp_model.objective.value()} hours")


    # Por isto num somatorio
    st.subheader("Objective Function")
    st.write(str(st.session_state.lp_model.objective))

    # Display the variables and their values in a table
    st.subheader("Variables")
    variables_table = []

    # Por isto num bar chart selecionavel por tarefa
    for variable in st.session_state.lp_model.variables():
        variables_table.append([variable.name, variable.varValue])
    st.table(variables_table)

    # Display the constraints
    # Organizar isto ou por tipo de constraint ou por tarefa
    st.subheader("Constraints")
    for constraint in st.session_state.lp_model.constraints.values():
        st.write(str(constraint))



def run_app():

    # Main content
    with st.container():
        if st.session_state.lp_dataframe is not None:
            # Make check to verify if datasets have been changed without loading again
            # If so, warn the user
            if st.session_state.lp_changed:
                st.warning("Datasets have changed. Please build the dataframe again.")


            st.header("Model information")

            st.dataframe(st.session_state.lp_dataframe, use_container_width=True)


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
            solve_button = st.button("Solve LP model")

        
        if st.session_state.lp_dataframe is not None:
            st.subheader("Average Productivity per Task")
            st.markdown(f"**{round(st.session_state.average_productivity_per_task,4)}** hours per task")


        if build_button:
            if len(st.session_state.datasets) == 0:
                st.warning("No datasets to use. Please generate a dataset.")

            elif st.session_state.lp_changed == False:
                st.warning("Datasets have not changed.")
                
            else:
                st.session_state.lp_changed = False

                number_of_employees = len(st.session_state.datasets[st.session_state.selected_dataset][0]) # Each employee is a row in the dataset

                df = pd.DataFrame(columns=["Person " + str(i+1) for i in range(number_of_employees)])
                capacities = []

                average_productivity_per_task = 0

                # Create complete dataframe with unit processing times
                # Load from datasets
                for task_name, (dataset, capacity) in st.session_state.datasets.items():
                    unit_processing_times = dataset['unit_processing_time'].values
                    df.loc[task_name] = unit_processing_times
                    average_productivity_per_task += unit_processing_times.mean()
                    capacities.append(capacity)

                average_productivity_per_task /= len(st.session_state.datasets)
                st.session_state.average_productivity_per_task = average_productivity_per_task

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
    st.set_page_config(page_title="Linear Programming", page_icon=":bar_chart:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
