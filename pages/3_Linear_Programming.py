import streamlit as st
import pandas as pd
import plotly.express as px
from packages.linear_programming.lp_solver import solve_linear_programming, Status
from packages.utils.utils import load_session_state, hide_streamlit_style

# Constraint types
EQUALITY = "equality"
UNIT_PROCESSING_TIME = "unit_processing_time"
MIN_EMPLOYEE_CAPACITY = "min_employee_capacity"
MAX_EMPLOYEE_CAPACITY = "max_employee_capacity"

# Linear Programming model information
OBJECTIVE = 0
VARIABLES = 1
CONSTRAINTS = 2
STATUS = 3


def get_model_info(lp_model):
    # Get the variables and their values
    variables = {task_name : [] for task_name in st.session_state.lp_dataframe.index} # Create a dictionary of lists to store the variables
    for variable in lp_model.variables():
        variables[variable.name[1:-1]].append(variable.value()) # Remove the "X" and the number from the variable name to obtain the task name


    constraints = list(lp_model.constraints.values())

    number_of_tasks = len(st.session_state.lp_dataframe)

    # Related to the number of tasks executed being equal between machines
    equality_constraints = constraints[0:number_of_tasks-1]

    # Related to the unit processing times from the dataframe
    unit_processing_time_constraints = constraints[number_of_tasks-1:number_of_tasks-1 + number_of_tasks]

    # Related to the employees' capacities (minimum hours required)
    min_employee_capacity_constraints = constraints[number_of_tasks-1 + number_of_tasks::2]

    # Related to the employees' capacities (maximum hours allowed)
    max_employee_capacity_constraints = constraints[number_of_tasks-1 + number_of_tasks + 1::2]

    # Create a dictionary of lists of constraints
    constraints = {EQUALITY : equality_constraints, UNIT_PROCESSING_TIME : unit_processing_time_constraints, MIN_EMPLOYEE_CAPACITY : min_employee_capacity_constraints, MAX_EMPLOYEE_CAPACITY : max_employee_capacity_constraints}

    return lp_model.objective, variables, constraints, lp_model.status



def display_model():
   
    with st.container():
        left_column, right_column = st.columns(2)

        with left_column:
            st.subheader("Production")
            # The total number of pieces produced is the value of the objective function divided by the number of tasks
            st.subheader(f"{int(st.session_state.lp_model_info[OBJECTIVE].value()/len(st.session_state.lp_dataframe))} pieces")

        with right_column:
            st.subheader("Total Hours Worked")
            hours_worked = 0
            for constraint in st.session_state.lp_model_info[CONSTRAINTS][MIN_EMPLOYEE_CAPACITY]:
                hours_worked += constraint.value() - constraint.constant

            st.subheader(f"{int(hours_worked)} hours")


    st.markdown("---")

    # Por isto num somatorio ou assim
    # Display the objective function
    with st.container():
        st.subheader("Objective Function")
        st.write(str(st.session_state.lp_model_info[OBJECTIVE]))

    st.markdown("##")
    
    # Display the variables and their values in a bar chart per task
    with st.container():
        st.subheader("Variables")

        variables = st.session_state.lp_model_info[VARIABLES]
        
        task = st.selectbox("Select a task", list(variables.keys()))
        variables_df = pd.DataFrame(variables[task], columns=["Value"])
        variables_df.index += 1    # Add 1 to the index to start at 1 instead of 0

        fig_variables = px.bar(
            variables_df,
            x=variables_df.index,
            y="Value",
            orientation="v",
            color_discrete_sequence=["#636EFA"] * len(variables_df),
            template="plotly_white",
            labels={"index": "Person", "Value": "Pieces processed"},
            )
        
        fig_variables.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, tickmode="linear", fixedrange=True),
            yaxis=dict(showgrid=False, zeroline=False, fixedrange=True),
            plot_bgcolor="rgba(0,0,0,0)"
            )
        
        st.plotly_chart(fig_variables, use_container_width=True)

        for i in range(len(variables[task])):
            st.markdown(f"**Person {i+1}** processed **{variables[task][i]}** pieces.")
        

    st.markdown("##")

    # Display the constraints
    with st.container():
        st.subheader("Constraints")
        
        equality_constraints_table = unit_processing_time_constraints_table = min_employees_capacity_constraints_table = max_employees_capacity_constraints_table = pd.DataFrame(columns=["Constraint", "Value"])
        equality_constraints = st.session_state.lp_model_info[CONSTRAINTS][EQUALITY]
        if equality_constraints != []:  # If there are no equality constraints, don't display the table
            st.write("Equality Constraints")
            for constraint in equality_constraints:
                equality_constraints_table = pd.concat([equality_constraints_table, pd.DataFrame([[str(constraint), constraint.value()-constraint.constant]], columns=["Constraint", "Value"])])   
            st.table(equality_constraints_table)
        
        unit_processing_time_constraints = st.session_state.lp_model_info[CONSTRAINTS][UNIT_PROCESSING_TIME]
        st.write("Unit Processing Time Constraints")
        for constraint in unit_processing_time_constraints:
            unit_processing_time_constraints_table = pd.concat([unit_processing_time_constraints_table, pd.DataFrame([[str(constraint), constraint.value()-constraint.constant]], columns=["Constraint", "Value"])])
        st.table(unit_processing_time_constraints_table)

        min_employee_capacity_constraints = st.session_state.lp_model_info[CONSTRAINTS][MIN_EMPLOYEE_CAPACITY]
        st.write("Employee Work Time Constraints (Minimum)")
        for constraint in min_employee_capacity_constraints:
            min_employees_capacity_constraints_table = pd.concat([min_employees_capacity_constraints_table, pd.DataFrame([[str(constraint), constraint.value()-constraint.constant]], columns=["Constraint", "Value"])])   
        st.table(min_employees_capacity_constraints_table)

        max_employee_capacity_constraints = st.session_state.lp_model_info[CONSTRAINTS][MAX_EMPLOYEE_CAPACITY]
        st.write("Employee Work Time Constraints (Maximum)")
        for constraint in max_employee_capacity_constraints:
            max_employees_capacity_constraints_table = pd.concat([max_employees_capacity_constraints_table, pd.DataFrame([[str(constraint), constraint.value()-constraint.constant]], columns=["Constraint", "Value"])])
        st.table(max_employees_capacity_constraints_table)


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

            if st.session_state.lp_model_info is not None:
                # {0: 'Not Solved', 1: 'Optimal', -1: 'Infeasible', -2: 'Unbounded', -3: 'Undefined'}
                status = st.session_state.lp_model_info[STATUS]

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

    # Sidebar content
    with st.sidebar:
        st.header("Linear Programming Model Solver")

        min_hours_worked = st.number_input("Minimum hours of work required", min_value=1, value=100)

        max_hours_worked = st.number_input("Maximum hours of work allowed", min_value=1, value=240)

        left_column, right_column = st.columns(2)

        with left_column:
            build_button = st.button("Build dataframe")

        with right_column:
            solve_button = st.button("Solve LP model")

        if st.session_state.lp_dataframe is not None:
            st.markdown("---")
            st.subheader("Average Productivity per Task")
            st.markdown(f"**{round(st.session_state.average_productivity_per_task,4)}** hours per task")

        if build_button:
            if len(st.session_state.datasets) == 0: # If there are no datasets, warn the user
                st.warning("No datasets to use. Please generate a dataset.")

            elif st.session_state.lp_changed == False:  # If the datasets have not changed, warn the user
                st.warning("Datasets have not changed.")
                
            else:
                st.session_state.lp_changed = False

                number_of_employees = len(st.session_state.datasets[st.session_state.selected_dataset][0]) # Each employee is a row in the dataset

                df = pd.DataFrame(columns=["Person " + str(i+1) for i in range(number_of_employees)])
                capacities = []

                average_productivity_per_task = 0

                # Create complete dataframe with unit processing times
                # Load from datasets
                for task_name, (dataset, capacity, _) in st.session_state.datasets.items():
                    unit_processing_times = dataset['unit_processing_time'].values
                    df.loc[task_name] = unit_processing_times
                    average_productivity_per_task += unit_processing_times.mean()
                    capacities.append(capacity)

                average_productivity_per_task /= len(st.session_state.datasets)
                st.session_state.average_productivity_per_task = average_productivity_per_task

                df['Capacity'] = capacities

                st.session_state.lp_dataframe = df
                st.session_state.lp_model_info = None
                st.experimental_rerun()

        if solve_button:
            if st.session_state.lp_dataframe is None:   # If the dataframe has not been built, warn the user
                st.warning("No problem to solve. Please build the dataframe first.")

            else:
                # This is a LpProblem object
                st.session_state.lp_model_info = get_model_info(solve_linear_programming(st.session_state.lp_dataframe, min_hours_worked, max_hours_worked))    
                st.experimental_rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="Linear Programming", page_icon=":bar_chart:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
