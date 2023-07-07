import pandas as pd
from pulp import *

MIN_HOURS_WORKED = 100


def solve_linear_programming(dataframe: pd.DataFrame):

    variables = {task_name : [] for task_name in dataframe.index} # Create a dictionary of lists to store the variables
    number_of_employees = len(dataframe.columns) - 1

    # Create model
    model = LpProblem("Maximize_Production", LpMaximize)

    
    # Create variables
    for key in variables:   # For each task
        for i in range(number_of_employees):    # For each employee
            variables[key].append(LpVariable("X" + key + str(i+1), lowBound=0, cat="Integer"))   # Create variable


    # Define objective
    model += lpSum(variables.values()) # For example: (Xprinting1 + Xprinting2 + Xprinting3) + (Xcutting1 + Xcutting2 + Xcutting3) + ...
    

    # Add constraints
    # Related to the number of tasks executed being equal between machines
    values = list(variables.values())
    for i in range(1, len(values)):    # For each task
        model += lpSum(values[i]) == lpSum(values[0]) # Sum of each task's variables list must be equal to each other


    # Related to the unit processing times from the dataframe
    for key in variables:   # For each task
        aux_list = []

        for i in range(number_of_employees):    # For each employee
            aux_list.append(variables[key][i]*dataframe.loc[key][i])

        model += lpSum(aux_list) <= dataframe.loc[key]['Capacity'] # Sum of each task's variables list must be less than or equal to the task's capacity


    # Related to the employees' capacities
    for i in range(number_of_employees):    # For each employee
        aux_list = []

        for key in variables:   # For each task
            aux_list.append(variables[key][i]*dataframe.loc[key][i])
        
        model += lpSum(aux_list) >= MIN_HOURS_WORKED # In total, the time spent by an employee must be greater than or equal to the minimum hours worked

    # Solve model
    model.solve()


    # Show solution
    for v in model.variables():
        print(v.name, "=", v.varValue)

    return model
