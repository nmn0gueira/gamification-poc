import streamlit as st
import pandas as pd

def run_app():
    st.title("Linear Programming")

    with st.container():
        if st.session_state.lp_dataframe:  
            number_of_employees = len(st.session_state.datasets[st.session_state.selected_dataset][0]) # Each employee is a row in the dataset

            dataframe = pd.DataFrame(columns=["Person " + str(i+1) for i in range(number_of_employees)])
            capacities = []

            # Create complete dataframe with unit processing times
            # Load from datasets
            for task_name, (dataset, capacity) in st.session_state.datasets.items():
                unit_processing_times = dataset['unit_processing_time'].values
                dataframe.loc[task_name] = unit_processing_times

                capacities.append(capacity)
        
            dataframe['Capacity'] = capacities

            st.dataframe(dataframe)

        else:
            st.write("Upload a dataset to start")


    with st.sidebar:
        st.header("Upload dataset")
        st.write("Upload a dataset to start")

        file = st.file_uploader("Upload dataset", type=["csv", "xlsx"])

        if file:
            dataset = pd.read_csv(file) if file.type == "csv" else pd.read_excel(file)

            st.session_state.lp_dataframe = dataset

            st.session_state.datasets = {file.name: (dataset, 100)}



if __name__ == "__main__":
    st.set_page_config(page_title="Linear Programming", page_icon=":books:", layout="wide")

    if "lp_dataframe" not in st.session_state:
        st.session_state.lp_dataframe = None  # Dataframe with the unit processing times

    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)  # Hide the Streamlit footer and menu button
    run_app()
