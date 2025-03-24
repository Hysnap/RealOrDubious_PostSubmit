"""
A streamlist app to analyze political donations in the UK
Run this file first to start the app
"""
# import necessary modules
import streamlit as st
import os
import sys
# Set the page config at the very beginning of the script
st.set_page_config(page_title="Real or Dubious News",
                   layout="wide")

sys.path.append(os.path.abspath(os.getcwd())) 

# import local modules
try:
    import setup
    import ROD_menu
    from sl_utils.logger import streamlit_logger as logger
    from f_dashboard.data_prep import dashboarddata
    from f_dashboard.data_prep import mapdata
except ImportError as e:
    raise SystemExit(f"Error: Failed to import modules - {e}")


# log current working directory
if 'logger' in globals():
    # log current file and path
    logger.info("Streamlit App Starting...")
    current_file = os.path.abspath(__file__)
    current_path = os.path.dirname(current_file)
    logger.info(f"Current Working Directory: {os.getcwd()}")
    logger.info(f"running {current_path}, {current_file}")
else:
    # Run the setup function
    raise SystemExit("Error: Logger is not properly configured!")
# Run the setup function
logger.info("Running App setup...")
setup.setup_package()
logger.info("Setup completed successfully.")
# except Exception as e:
#     logger.critical(f"App setup crashed: {e}", exc_info=True)
#     st.error(f"App setup failed. Please check logs. {__name__}")
#     raise SystemExit("App setup failed. Exiting.")

# Run the first load function
try:
    with st.spinner('Please wait while the data sets are being calculated...'):
        @st.cache_data
        def load_mapdata():
            return mapdata()

        @st.cache_data
        def load_dashboard_data():
            return dashboarddata()
        
        # Store data in session state
        st.session_state['data_for_map'] = load_mapdata()
        st.session_state['data_clean'] = load_dashboard_data()
except Exception as e:
    logger.critical(f"First load crashed: {e}", exc_info=True)
    st.error(f"Data loading failed. Please check logs. {e}")
    raise SystemExit("Data loading failed. Exiting.")


try:
    logger.info("Running Menu setup...")
    ROD_menu.pagesetup()
    logger.info("Menu setup completed successfully.")
except Exception as e:
    logger.critical(f"Menu setup crashed: {e}", exc_info=True)
    st.error(f"Menu setup failed. Please check logs. {__name__}")
    raise SystemExit("Menu setup failed. Exiting.")


logger.info("App is fully loaded and ready!")
# The app is now ready to be run.
# To run the app, open a terminal and run:
#  "streamlit run PoliticalPartyAnalysisDashboard.py
# The app will open in a new tab in your default web browser.
