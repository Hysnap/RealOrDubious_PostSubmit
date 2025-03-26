"""
Description: This module contains functions that load
and process data for the dashboard.
    The data is loaded from the data folder and processed
    to generate the required dataframes.
    The processed dataframes are then saved to the data
    folder for use in the dashboard.
    The functions in this module are used to load and process
    the data for the dashboard.
    The processed data is saved to the data folder for use in the dashboard.

    Functions:
    - mapdata: Loads the data required for the map visualization.
    - dashboarddata: Loads the data required for the dashboard visualization.
    - wordcountdata: Loads the data required for the wordcloud visualization.

    Returns:
        _type_: _description_
    """

import pandas as pd
from sl_utils.logger import log_function_call, datapipeline_logger as logger
import os


@log_function_call(logger)
def mapdata():
    # Check if articlesformap.csv exists
    file_path = "sl_data_for_dashboard//articlesformap.csv"
    if os.path.exists(file_path):
        logger.debug(f"{file_path} exists. Loading the file.")
        articles = pd.read_csv(file_path)
    else:
        logger.debug(f"{file_path} does not exist.")
        return RuntimeError(f"{file_path} does not exist.")

    return articles


@log_function_call(logger)
def dashboarddata():
    df = pd.read_csv("sl_data_for_dashboard//dashboard_data.zip",
                     usecols=None,  # Import all columns
                     dtype={
                        'index': int,
                        'title': str,
                        'subject': str,
                        'label': int,
                        'media_type': str,
                        'month': int,
                        'day': int,
                        'year': int,
                        'day_of_week': str,
                        'week_of_year': int,
                        'is_weekend': int,
                        'is_weekday': int,
                        'holiday': int,
                        'day_label': str,
                        'article_id': int,
                        'source_name': str,
                        'title_length': int,
                        'text_length': int,
                        'article_polarity': float,
                        'article_subjectivity': float,
                        'title_polarity': float,
                        'title_subjectivity': float,
                        'overall_polarity': float,
                        'overall_subjectivity': float,
                        'contradiction_polarity': float,
                        'contradiction_subjectivity': float,
                        'polarity_variations': float,
                        'subjectivity_variations': float,
                        'sentiment_article': str,
                        'sentiment_title': str,
                        'sentiment_overall': str,
                        'unique_location_count': int
                     },
                     compression='zip',
                     # Ensure date_clean is imported as a date
                     parse_dates=['date_clean']
                     )
    logger.debug("The shape of the data is: ", df.shape)
    logger.debug(df.head())

    # load data in to data_clean st.session_state
    return df


@log_function_call(logger)
def wordcountdata():
    # Use low_memory=False to avoid dtype inference issues
    df = pd.read_csv(
        "sl_data_for_dashboard//ngram_summary_v1.zip",
        compression='zip',
        low_memory=False
        )
    logger.debug("The shape of the data is: ", df.shape)
    logger.debug(df.head())

    # load data in to wordcountdata
    return df


# Path: f_dashboard/data_prep.py
# end of file