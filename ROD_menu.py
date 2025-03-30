
from sl_utils.logger import log_function_call, streamlit_logger


@log_function_call(streamlit_logger)
def pagesetup():
    # Description: This is the main file to set up the menu
    # from app_pages import introduction
    from sl_app_pages.multi_page import MultiPage
    from sl_app_pages.introduction import introduction_body
    from sl_app_pages.notesondataprep import notesondataprep_body
    from sl_app_pages.ML_page import run as machinelearning
    from sl_app_pages.wordclouds_original import wordcloud_explorer
    from sl_app_pages.mod_page_calls import (
         mp1_intro,
         mp2_dataex,
         mp3_datapre,
         # mp3_map,
         loginpage,
         logoutpage,
        )

    # Create an instance of the MultiPage class
    app = MultiPage(app_name="UK Political Donations")  # Create an instance

    # Add your app pages here using .add_page()

    app.add_page("Introduction", introduction_body)
    app.add_page("Objective and Requirements", mp1_intro)
    app.add_page("Articles by Character Counts\n and initial Classifications",
                 mp2_dataex)
    app.add_page("Sentiment Analysis", mp3_datapre)
    app.add_page("WordCloud Explorer", wordcloud_explorer)
    app.add_page("Real or Dubious Article Checker", machinelearning)
    # app.add_page("Map of Analysed Articles", mp3_map)
    app.add_page("Notes on Data\n and Manipulations", notesondataprep_body)
    app.add_page("Login", loginpage)
    app.add_page("Logout", logoutpage)

    # app.add_page("Regulated Entities", regulatedentitypage_body)
    app.run()  # Run the  app
    # End of PoliticalPartyAnalysisDashboard.py
# Path: sl_app_pages/ROD_dashboard.py
# end of ROD_dashboard.py
