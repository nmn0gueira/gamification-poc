import streamlit as st
from streamlit_lottie import st_lottie
from packages.utils.utils import load_session_state, hide_streamlit_style, load_lottieurl



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
        
        st.write("Get started by exploring the options below.")


    # ---- WHAT I DO ----
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("What I do")
            st.write("##")
            st.write(
                """
                On my YouTube channel I am creating tutorials for people who:
                - are looking for a way to leverage the power of Python in their day-to-day work.
                - are struggling with repetitive tasks in Excel and are looking for a way to use Python and VBA.
                - want to learn Data Analysis & Data Science to perform meaningful and impactful analyses.
                - are working with Excel and found themselves thinking - "there has to be a better way."

                If this sounds interesting to you, consider subscribing and turning on the notifications, so you don’t miss any content.
                """
            )
            st.write("[YouTube Channel >](https://youtube.com/c/CodingIsFun)")
        with right_column:
            st_lottie(lottie_coding, height=300, key="coding")

    # ---- PROJECTS ----
    with st.container():
        st.write("---")
        st.header("My Projects")
        st.write("##")
        image_column, text_column = st.columns((1, 2))
        with image_column:
            st.empty()
        with text_column:
            st.subheader("Integrate Lottie Animations Inside Your Streamlit App")
            st.write(
                """
                Learn how to use Lottie Files in Streamlit!
                Animations make our web app more engaging and fun, and Lottie Files are the easiest way to do it!
                In this tutorial, I'll show you exactly how to do it
                """
            )
            st.markdown("[Watch Video...](https://youtu.be/TXSOitGoINE)")
    with st.container():
        image_column, text_column = st.columns((1, 2))
        with image_column:
            st.empty()
        with text_column:
            st.subheader("How To Add A Contact Form To Your Streamlit App")
            st.write(
                """
                Want to add a contact form to your Streamlit website?
                In this video, I'm going to show you how to implement a contact form in your Streamlit app using the free service ‘Form Submit’.
                """
            )
            st.markdown("[Watch Video...](https://youtu.be/FOULV9Xij_8)")

    # ---- CONTACT ----
    with st.container():
        st.write("---")
        st.header("Get In Touch With Me!")
        st.write("##")

        # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
        contact_form = """
        <form action="https://formsubmit.co/YOUR@MAIL.COM" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit">Send</button>
        </form>
        """
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
            st.empty()

    st.markdown("##")

    st.markdown("### What is Productivity?")

    st.markdown("Productivity describes various measures of the efficiency of production. A productivity measure is expressed as the ratio of output to inputs used in a production process, i.e. output per unit of input. Productivity is a crucial factor in production performance of firms and nations. Increasing national productivity can raise living standards because more real income improves people's ability to purchase goods and services, enjoy leisure, improve housing and education and contribute to social and environmental programs. Productivity growth also helps businesses to be more profitable.")





    st.header("Gamification")

    st.markdown("##")

    st.markdown("### What is Gamification?")
    st.markdown("Gamification is the application of game-design elements and game principles in non-game contexts. It can also be defined as a set of activities and processes to solve problems by using or applying the characteristics of game elements. Gamification commonly employs game design elements to improve user engagement, organizational productivity, flow, learning, crowdsourcing, employee recruitment and evaluation, ease of use, usefulness of systems, physical exercise, traffic violations, voter apathy, and more. A collection of research on gamification shows that a majority of studies on gamification find it has positive effects on individuals. However, individual and contextual differences exist.")
    st.markdown("### Why Gamification?")
    st.markdown("Gamification is a powerful tool to engage people. It is a way to motivate people to change their behavior, develop skills and drive innovation. It is a way to inspire people to do things they otherwise would not do, such as completing boring or difficult tasks, or learning new things. Gamification is a way to make people feel good about themselves and their accomplishments. It is a way to make people feel like they are part of something bigger than themselves. It is a way to make people feel like they are part of a community. It is a way to make people feel like they are part of a team. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause. It is a way to make people feel like they are part of a movement. It is a way to make people feel like they are part of a cause.")


    with st.sidebar:
        st.header("About the project")
        st.write("This project was created by [Nuno Nogueira] during an internship at [INOV INESC](https://www.inov.pt/sobre-nos/index.html) as part of FCT/UNL Internship Program.")
        
        st.markdown("---")
        st.header("Source Code")
        st.write("The source code is available on [GitHub]")



if __name__ == "__main__":
    st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")

    lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

    # Load session state
    load_session_state()

    # Hide the Streamlit branding
    hide_streamlit_style()
    
    run_app()
