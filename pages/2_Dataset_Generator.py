import streamlit as st
from packages.dataset_generator.datagen import generate_dataset

def run_app():
    
    # Main content
    with st.container():
        if st.session_state.datasets:
            # Datasets exist
            st.subheader("Available Datasets")
            st.session_state.disabled = True

            dataset_names = list(st.session_state.datasets.keys())
            dataset_to_display = st.selectbox("Select Dataset", dataset_names, index=dataset_names.index(st.session_state.selected_dataset),
                                              key="dataset_selectbox")
            st.session_state.selected_dataset = dataset_to_display  # Update the selected dataset
            st.dataframe(st.session_state.datasets[st.session_state.selected_dataset][0])

        else:
            # No datasets available
            st.info("No datasets available. Please generate a dataset.")
            st.session_state.disabled = False

    
    # Sidebar content
    with st.sidebar:
        st.header("Generate Dataset")

        left_column, right_column = st.columns(2)

        with left_column:
            number_of_employees = st.number_input("Number of Employees", min_value=1, value=5, disabled=st.session_state.disabled)
        with right_column:
            capacity = st.number_input("Capacity", min_value=1, value=500)

        dataset_name = st.text_input("Dataset Name", "Dataset 1")  # User-defined dataset name

        generate_button = st.button("Generate Dataset")
        delete_button = st.button("Delete All Datasets")


        if generate_button:  # Handle the click event of the "Generate Dataset" button
            dataset = generate_dataset(number_of_employees)
            st.session_state.datasets[dataset_name] = (dataset, capacity)
            st.session_state.selected_dataset = dataset_name  # Update the selected dataset
            st.experimental_rerun()  # Rerun the app to update the dataset selectbox


        if delete_button:  # Handle the click event of the "Delete All Datasets" button
            if not st.session_state.datasets:
                st.warning("No datasets to delete.")
            else:  
                st.session_state.datasets.clear()  # Clear the datasets dictionary
                st.session_state.selected_dataset = None  # Reset the selected dataset
                st.experimental_rerun()  # Rerun the app to update the dataset selectbox


        



if __name__ == "__main__":
    st.set_page_config(page_title="Dataset Generator", page_icon=":chart_with_upwards_trend:", layout="wide")

    if "datasets" not in st.session_state:
        st.session_state.datasets = {}  # Create the datasets dictionary in session_state

    if "selected_dataset" not in st.session_state:
        st.session_state.selected_dataset = None  # Initialize the selected dataset

    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    
    st.markdown(hide_st_style, unsafe_allow_html=True)  # Hide the Streamlit footer and menu button

    run_app()
