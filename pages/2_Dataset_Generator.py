import streamlit as st
import re
from packages.dataset_generator.datagen import generate_dataset
from packages.utils.utils import load_session_state, hide_streamlit_style

DATASET = 0
CAPACITY = 1
DIFFICULTY = 2

PATTERN = r'[0-9\s]'  # Pattern to check if the dataset name contains spaces or numbers

def run_app():
    # Main content
    with st.container():
        if st.session_state.datasets:      # Datasets exist
            st.header("Available Datasets")

            st.markdown("##")

            # Disable the number input so the user cant change the number of employees if datasets are available
            st.session_state.disabled = True

            dataset_names = list(st.session_state.datasets.keys())
            dataset_to_display = st.selectbox("Select Dataset", dataset_names, index=dataset_names.index(st.session_state.selected_dataset),
                                              key="dataset_selectbox")
            st.session_state.selected_dataset = dataset_to_display  # Update the selected dataset

            st.markdown("##")

            left_column, right_column = st.columns(2)

            with left_column:
                st.subheader("Dataset Information")
                st.markdown(f"**Number of Employees:** {st.session_state.number_of_employees}")

            with right_column:
                st.subheader("Dataset Settings")
                st.markdown(f"**Capacity:** {st.session_state.datasets[st.session_state.selected_dataset][CAPACITY]} hours")
                st.markdown(f"**Difficulty:** {':star:'* st.session_state.datasets[st.session_state.selected_dataset][DIFFICULTY]}")

            st.markdown("##")

            st.dataframe(st.session_state.datasets[st.session_state.selected_dataset][DATASET], use_container_width=True)   # Display the selected dataset

        else:
            # No datasets available
            st.info("No datasets available. Please generate a dataset.")
            st.session_state.disabled = False

    
    # Sidebar content
    with st.sidebar:
        st.header("Productivity Dataset Generator")

        left_column, right_column = st.columns(2)

        with left_column:
            # Used so that the page remembers the number of employees if datasets were generated before
            default_value = st.session_state.number_of_employees if st.session_state.datasets else 5 

            number_of_employees = st.number_input("Number of Employees", min_value=5, value=default_value, disabled=st.session_state.disabled)
        
        with right_column:
            capacity = st.number_input("Capacity (hrs)", min_value=1, value=600)

        dataset_name = st.text_input("Dataset Name", "printing")  # User-defined dataset name

        difficulty = st.slider("Difficulty", min_value=1, max_value=10, value=5, step=1)

        generate_button = st.button("Generate Dataset", use_container_width=True)

        left_column, right_column = st.columns(2)
        
        with left_column:
            delete_selected_button = st.button("Delete Selected", use_container_width=True)

        with right_column:
            delete_all_button = st.button("Delete All", use_container_width=True)


        if generate_button:  # Handle the click event of the "Generate Dataset" button
            if re.search(PATTERN, dataset_name):    # Check if the dataset name contains spaces or numbers
                st.error("Dataset name cannot contain spaces or numbers.")
                
            else:
                dataset = generate_dataset(number_of_employees)
                st.session_state.number_of_employees = number_of_employees
                st.session_state.datasets[dataset_name] = (dataset, capacity, difficulty)
                st.session_state.selected_dataset = dataset_name  # Update the selected dataset
                st.session_state.lp_changed = True
                st.experimental_rerun()  # Rerun the app to update the dataset selectbox


        if delete_selected_button:  # Handle the click event of the "Delete Selected Dataset" button
            if not st.session_state.datasets:   # Check if there are datasets to delete
                st.warning("No datasets to delete.")
            else:
                del st.session_state.datasets[st.session_state.selected_dataset]

                if st.session_state.datasets:   # Check if there are still datasets left
                    # Update the selected dataset to the first dataset in the dictionary
                    st.session_state.selected_dataset = list(st.session_state.datasets.keys())[0]
                    
                    st.sessions_state.lp_changed = True

                else:
                    st.session_state.selected_dataset = None
            
                st.experimental_rerun()  # Rerun the app to update the dataset selectbox

        if delete_all_button:  # Handle the click event of the "Delete All Datasets" button
            if not st.session_state.datasets:   # Check if there are datasets to delete
                st.warning("No datasets to delete.")
            else:  
                st.session_state.datasets.clear()  # Clear the datasets dictionary
                st.session_state.selected_dataset = None  # Reset the selected dataset
                st.experimental_rerun()  # Rerun the app to update the dataset selectbox


        



if __name__ == "__main__":
    st.set_page_config(page_title="Dataset Generator", page_icon=":chart_with_upwards_trend:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()

    run_app()
