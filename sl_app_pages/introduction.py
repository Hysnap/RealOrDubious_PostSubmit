import streamlit as st


def introduction_body():
    """
    This function displays the content of Page one.
    """
    dataset1 = (
        "https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset"
    )
    dataset2 = (
        "https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset"
    )
    codeinstitute = "https://codeinstitute.net/"
    wmca = "https://www.wmca.org.uk/"

    # format text
    st.subheader('Welcome to the Real or Dubious News Dashboard')
    st.markdown(
        """
        * This dashboard is designed to share learnings from analysis undertaken on identifying **Real** or **Dubious News**.  
        * The data used in this analysis is sourced from the [Fake News Corpus]({dataset1}).  
        * The analysis is based on a dataset that contains news articles from various sources.  
        * The dataset was then enhanced with further records from the [Fake News Corpus]({dataset2}).  
        * For more details on the data, please see the **Notes on Data Preparation** page.
        """
    )
    st.markdown("### Key Findings\n\n- **Less Hyperbolic Articles**: Articles with less hyperbolic language are more likely to be **Real**.\n- **Objectivity**: The more **objective** an article is, the more likely it is to be **Real**.\n- **Character Count**:\n  - Titles with **more characters** are more likely to be **Dubious**.\n  - Articles with **more characters** are more likely to be **Dubious**.\n- **Source Credibility**: Articles mentioning a **recognized source** are more likely to be **Real**.\n- **Media Mentions**: Articles referencing **videos or pictures** in the title are more likely to be **Dubious**.\n- **Social Media References**: Articles referencing **key social media outlets** are more likely to be **Real**.")
    st.write("---")
    st.subheader("Notes Reason Created")
    st.markdown(
        """
        This dashboard was created as a **Capstone project** for the 
        **Data Analytics and AI bootcamp** provided by 
        [Code Institute]({codeinstitute}).  
        The course was funded by the 
        [West Midlands Combined Authority]({wmca}).
        """
    )
    st.write("---")
    st.write("* The login and logout are for admin purposes only.")
    github_repo = "https://github.com/yourusername/CapStoneProject_2025-1"
    st.write(f"* You can access the code through this [GitHub repository]({github_repo})")
    st.write("---")
