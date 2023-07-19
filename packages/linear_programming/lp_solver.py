from pulp import *

class Status:
    NOT_SOLVED = 0
    OPTIMAL = 1
    INFEASIBLE = -1
    UNBOUNDED = -2
    UNDEFINED = -3


def solve_linear_programming(dataframe, min_hours_worked, max_hours_worked):
    """
    Solves the linear programming problem
    :param dataframe: The dataframe with the unit processing times
    :param min_hours_worked: The minimum hours worked by an employee
    :param max_hours_worked: The maximum hours worked by an employee
    :return: The linear programming model
    """

    variables = {task_name : [] for task_name in dataframe.index} # Create a dictionary of lists to store the variables
    number_of_employees = len(dataframe.columns) - 1

    # Create model
    model = LpProblem("Maximize_Production", LpMaximize)

    
    # Create variables
    for key in variables:   # For each task
        for i in range(number_of_employees):    # For each employee
            variables[key].append(LpVariable("X" + key + str(i), lowBound=0, cat=LpInteger))   # Create variable


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
        
        sum = lpSum(aux_list)

        model += sum >= min_hours_worked # In total, the time spent by an employee must be greater than or equal to the minimum hours worked
        model += sum <= max_hours_worked # In total, the time spent by an employee must be less than or equal to the maximum hours worked


    # Solve model
    model.solve()

    return model
