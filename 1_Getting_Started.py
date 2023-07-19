import streamlit as st
from streamlit_lottie import st_lottie
from packages.utils.utils import load_session_state, hide_streamlit_style, load_lottiefile



def run_app():
    # ---- HEADER SECTION ----
    with st.container():
        st.subheader("Introduction")
        st.title("Improving Productivity Through Gamification")
        st.markdown("##")
        st.write("This app was created to show how gamification can be used in a workplace environment to improve productivity.")
        
        st.write("""
                 It allows you to:
                 - generate datasets for workable employee data.
                 - solve linear programming models to see how to better organize employees between various tasks. 
                 - gamify the process by assigning points to each task and employee, and then displaying the results in leaderboards.""")
        
        st.write("Get started by exploring how the app works.")


    # ---- DATASET GENERATOR ----
    with st.container():
        st.write("---")
        
        st.header("Dataset Generator")
        st.markdown("##")
        st.write(
            """
            This component allows you to create, manage and delete datasets for workable employee data.
            Each dataset is meant to represent monthly data of a certain task of the workers, and it contains the following information:
            - Employee ID
            - Units processed
            - Hours worked
            - Efficiency factor (factors in time spent on breaks, lunch, etc.)
            - Unit processing time (time it takes to process one unit with no defects)
            """
        )

        st.write(
            """
            The formula used to calculate the unit processing time is the following:
            ```
            Unit Processing Time = Hours Worked * Efficiency Factor / (Units Processed - Number of Defects)
            ```
            """)

        st.markdown("##")

        left_column, right_column = st.columns((1.75,1))
        with left_column:
            st.write(
                """
                On the sidebar, you will find input elements to configure the dataset generation process:
                - "Number of Employees": The desired number of employees for the dataset. The minimum allowed value is 5.
                - "Capacity (hrs)": The desired capacity for the dataset. Represents the total number of hours available for the task.
                - "Dataset Name": Name for your dataset. Since each dataset is meant represents a task, it is recommended to use the name of the task as the dataset name.
                - "Task Difficulty": Use the slider to set the task difficulty, which ranges from 1 to 10, with 1 being the easiest and 10 being the hardest, this will affect the point system in the Gamification section.
                """
            )
            st.write("""After setting the parameters, click the "Generate Dataset" button. The app will create a new dataset based on the provided settings.""")
            
            
        with right_column:
            # Put other lottie file here
            st_lottie(lottie_datagen, speed=1, height=300, key="lottie_datagen")
            

    # ---- LINEAR PROGRAMMING ----
    with st.container():
        st.markdown("---")
        st.header("Linear Programming")

        st.info("Before you can solve an LP model, you need to have generated datasets")

        st.write(
            """
            This component allows you to solve linear programming models based on the unit processing times of the generated datasets.
            """
        )

        left_column, right_column = st.columns(2)

        with left_column:
            st.subheader("Build dataframe")
            st.write(
                """
                To solve an LP model, you need to build the dataframe that will be used to solve the model by clicking the "Build Dataframe" button.
                This dataframe displays the unit processing times of each employee for a given task and the capacity of said task.

                If you generate more datasets after building the dataframe, you will need to rebuild it to include the new datasets.
                """
            )

        with right_column:
            st.subheader("Solve LP model")

            st.write(
                """
                After building the dataframe, you can solve the LP model by clicking the "Solve LP Model" button.
                The input of minimum and maximum hours worked will be used for some of the constraints of the model.
                
                The app will display (if the model is solvable) the total number of units produced and the total number of hours worked by the employees as well the information of the model, including the objective function, variables and constraints.
                """
            )

        st.markdown("##")
        
        st.subheader("About the model info")

        # Model status
        st.write(
            """
            **Model status**: When the model is solvable, the status will be "Optimal" with a success message and the rest of the model info will be displayed. If the model is not solvable, its status will be displayed on screen with an error message.
            """
        )

        # Objective function
        st.write(
            """
            **Objective function**: The objective function is always to maximize the sum of all variables.
            """
        )

        # Variables
        st.write(
            """
            **Variables**: A variable represents the number of times a task was done by a certain employee. For example, the variable "Xprinting1" indicates the amount of times the task "printing" was done by the employee with ID 1.
            """
        )

        # Constraints
        st.write(
            """
            **Constraints**: The constraints are the rules that the model must follow. The constraints of this model are:
            - Equality constraints: A piece is produced only when all tasks for it are completed. There is no need to do aditional tasks for a piece that cannot be completed.
            - Unit processing time constraints: The total number of hours worked on a task cannot exceed its capacity.
            - Minimum hours worked constraints: The total number of hours worked by an employee must be equal to or greater than the minimum hours of work required.
            - Maximum hours worked constraints: The total number of hours worked by an employee must be equal to or lower than the maximum hours of work allowed.
            """
        )

        st.warning("Currently, the app uses a publicly available solver. The higher the number of employees and tasks, the longer it will take to solve the model.")

    # ---- GAMIFICATION ----
    with st.container():
        st.markdown("---")
        st.header("Gamification")
        st.info ("Before you can use the gamification component, you need to have a solved LP model")

        st.write(
            """
            This component allows you to create leaderboards with automatic point assignment based on how well the employees performed their tasks.
            """
        )

        left_column, right_column = st.columns((1.25,1))

        with left_column:
            st.subheader("How an employee gets his classification")
            st.write(
                """
                The final classification of an employee is based on aspects from the productivity
                and qualitative leaderboards. Their total score is equal to the following formula,
                with w1 being the weight of the productivity score and w2 being the weight of the
                qualitative score:
                ```
                Total Score = Productivity Score * w1 + Qualitative Score * w2
                ```
                """
            )
        
        with right_column:
            st.markdown("##")
            # Put other lottie file here
            st_lottie(lottie_gamification, speed=0.5, height=200, key="lottie_gamification")

        st.markdown("##")


        productivity_column, qualitative_column = st.columns(2)

        with productivity_column:
            st.subheader("Productivity leaderboard")
            st.write(
                """
                The productivity leaderboard takes the input of points per star to determine the 
                amount of points to distribute to each employee given a certain task's difficulty rating.

                The employees that worked on a given task will have points distributed to them based on
                their efficiency (unit processing time) and the task's difficulty rating.

                For example, if the task's difficulty rating is 5 and the points per star factor is 10, then
                the employee that worked the fastest will get 50 points, the second fastest will get 50/2 = 25 points,
                the third fastest will get 50/3 = 16.6 points which rounds to 17, and so on and so forth.

                The total score of each employee in this leaderboard is equal to the sum of all points they got from the tasks they worked on.

                """
            )

        with qualitative_column:
            st.subheader("Qualitative leaderboard")
            st.write(
                """
                The qualitative leaderboard is randomized and takes the input of the minimum and
                maximum qualitative values to determine the range of values to distribute to each employee.

                This leaderboard is meant to represent the qualitative aspects of the employees,
                such as their attitude, punctuality, etc. The qualitative aspects chosen for now were "Self-assessment" which
                represents how well the employee thinks he did versus how well he actually did (the lower the difference, the better),
                and "Engagement" which represents how engaged the employee was during the task (the higher the better).

                The total score of each employee in this leaderboard is equal to the sum of all qualitative values they got from the tasks they worked on.
                """
            )
        





    # ---- ABOUT ----
    with st.sidebar:
        for _ in range(8):
            st.markdown("##")
        st.markdown("---")
        st.header("About the project")
        st.write("This project was created by Nuno Nogueira during an internship at [INOV INESC](https://www.inov.pt/sobre-nos/index.html) as part of FCT/UNL Internship Program.")



if __name__ == "__main__":
    st.set_page_config(page_title="Getting Started", page_icon=":rocket:", layout="wide")

    lottie_datagen= load_lottiefile("lottiefiles/datagen1.json")

    lottie_gamification = load_lottiefile("lottiefiles/gamification2.json")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()
    
    run_app()
