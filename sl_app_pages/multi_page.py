import streamlit as st
from sl_utils.version import get_git_version as get_git_version
from sl_utils.logger import streamlit_logger as logger  # Import the logger

# Define a class for managing multiple pages in a Streamlit app


class MultiPage:
    def __init__(self, app_name) -> None:
        self.pages = []  # List to store the pages
        self.app_name = app_name  # Name of the app


    # Method to add a new page to the app
    def add_page(self, title, func) -> None:
        self.pages.append({"title": title, "function": func})

    # Method to run the app
    def run(self):
        # Display the app title
        try:
            version = get_git_version()
            logger.info(f"App Version: {version}")
        except Exception as e:
            version = "1.0.0"
            logger.error(f"Error fetching version: {e}")
        st.text(f"Version: {version}")
        if not self.pages:
            if logger.level <= 20:
                st.warning("No pages have been added yet!")
            logger.warning("No pages have been added yet!")
            return

        # Log the selected page
        page = st.sidebar.radio(
            self.app_name,
            self.pages,
            format_func=lambda page: page["title"],
            key="menu_selection",
        )
        logger.info(f"Switched to page: {page['title']}")

        page["function"]()  # Run the selected page's function
