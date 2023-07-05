import streamlit as st

def run_app():
    st.title("Linear Programming")

if __name__ == "__main__":
    st.set_page_config(page_title="Linear Programming", page_icon=":books:", layout="wide")

    hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_st_style, unsafe_allow_html=True)  # Hide the Streamlit footer and menu button
    run_app()
