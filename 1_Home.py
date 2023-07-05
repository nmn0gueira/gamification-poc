import streamlit as st

def run_app():
    st.title("Home")


if __name__ == "__main__":
    st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")

    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)  # Hide the Streamlit footer and menu button
    run_app()
