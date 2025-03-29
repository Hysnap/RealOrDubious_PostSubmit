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
    df = pd.read_csv(
        "sl_data_for_dashboard//dashboard_data.zip",
        compression='zip',
        low_memory=False
    )

    # Rename columns for consistency
    df = df.rename(columns={
        "title_polarity_value": "title_polarity",
        "article_polarity_value": "article_polarity",
        "title_subjectivity_value": "title_subjectivity",
        "article_subjectivity_value": "article_subjectivity",
        "overall_polarity_value": "overall_polarity",
        "overall_subjectivity_value": "overall_subjectivity",
        "contradiction_polarity_value": "contradiction_polarity",
        "contradiction_subjectivity_value": "contradiction_subjectivity",
        "polarity_variations_value": "polarity_variations",
        "subjectivity_variations_value": "subjectivity_variations",
        "count_of_locations": "unique_location_count",
        "text_length_value": "text_length",
        "article_id": "article_count"
    })

    # Map full month names to numbers
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }

    # Map, then fill any unrecognized or missing months with April (4)
    df["month_num"] = df["month"].map(month_map).fillna(4).astype(int)

    # Format the date_clean field
    df["date_clean"] = pd.to_datetime(
        df["year"].astype(int).astype(str) + "-" +
        df["month_num"].astype(str).str.zfill(2) + "-01"
    )

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
