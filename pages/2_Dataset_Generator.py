import streamlit as st
from packages.dataset_generator.datagen import generate_dataset

def run_app():
    st.sidebar.title("Employee Performance Dataset Generator")
    number_of_employees = st.sidebar.number_input("Number of Employees", min_value=1, value=100)
    dataset_name = st.sidebar.text_input("Dataset Name", "Dataset 1")  # User-defined dataset name

    if st.sidebar.button("Generate Dataset"):
        dataset = generate_dataset(number_of_employees)
        st.session_state.datasets[dataset_name] = dataset
        st.session_state.selected_dataset = dataset_name  # Update the selected dataset

    if not st.session_state.datasets:
        st.info("No datasets available. Please generate a dataset.")
    else:
        dataset_names = list(st.session_state.datasets.keys())
        dataset_to_display = st.selectbox("Select Dataset", dataset_names, index=dataset_names.index(st.session_state.selected_dataset),
                                          key="dataset_selectbox")
        st.session_state.selected_dataset = dataset_to_display  # Update the selected dataset
        st.dataframe(st.session_state.datasets[st.session_state.selected_dataset])


if __name__ == "__main__":
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
