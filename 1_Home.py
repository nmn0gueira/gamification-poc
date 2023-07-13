import streamlit as st
from packages.utils.utils import load_session_state, hide_streamlit_style

def run_app():
    st.title("Home")



    st.header("Gamification")

    st.markdown("##")

    st.markdown("### What is Gamification?")
    st.markdown("Gamification is the application of game-design elements and game principles in non-game contexts. It can also be defined as a set of activities and processes to solve problems by using or applying the characteristics of game elements. Gamification commonly employs game design elements to improve user engagement, organizational productivity, flow, learning, crowdsourcing, employee recruitment and evaluation, ease of use, usefulness of systems, physical exercise, traffic violations, voter apathy, and more. A collection of research on gamification shows that a majority of studies on gamification find it has positive effects on individuals. However, individual and contextual differences exist.")
    st.markdown("### Why Gamification?")
    st.markdown("Gamification is a powerful tool to engage people. It is a way to motivate people to change their behavior, develop skills and drive innovation. It is a way to inspire people to do things they otherwise would not do, such as completing boring or difficult tasks, or learning new things. Gamification is a way to make people feel good about themselves and their accomplishments. It is a way to make people feel like they are part of something bigger than themselves. It is a way to make people feel like they are part of a community. It is a way to make people feel like they are part of a team. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause.")



if __name__ == "__main__":
    st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()
    
    run_app()
