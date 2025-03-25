# Description: Visualisations for polarity related data.
# Category: Visualisations

from sl_utils.logger import log_function_call, streamlit_logger
from sl_visualisations.common_visual_functions import (get_dataset_or_error,
                                                       apply_date_filter,
                                                       plot_scatter,
                                                       
                                                       )


@log_function_call(streamlit_logger)
def plot_article_vs_title_polarity(target_label="Article vs Title Polarity",
                                   pageref_label="polarity_scatter"):
    """
    Scatter plot of article vs title polarity with label hue.
    """
    df = get_dataset_or_error(["title_polarity", "article_polarity", "label", "date_clean"])
    if df is None:
        return

    filtered_df = apply_date_filter(df, "date_clean", pageref_label)

    plot_scatter(
        df=filtered_df,
        x_col="title_polarity",
        y_col="article_polarity",
        hue_col="label",
        title="Plot of Article Polarity vs Title Polarity",
        xlabel="Title Polarity",
        ylabel="Article Polarity"
    )


@log_function_call(streamlit_logger)
def plot_title_vs_article_polarity(target_label="Title vs Article Polarity",
                                   pageref_label="title_article_polarity_scatter"):
    """
    Scatter plot of title vs article polarity (axes flipped).
    """
    df = get_dataset_or_error(["title_polarity", "article_polarity", "label", "date_clean"])
    if df is None:
        return

    filtered_df = apply_date_filter(df, "date_clean", pageref_label)

    plot_scatter(
        df=filtered_df,
        x_col="article_polarity",
        y_col="title_polarity",
        hue_col="label",
        title="Scatter Plot of Polarities Articles vs Titles",
        xlabel="Article Polarity",
        ylabel="Title Polarity"
    )


@log_function_call(streamlit_logger)
def plot_polarity_contrad_variations(target_label="Polarity Contradiction vs Variations",
                                     pageref_label="Pol_con_var_scatter"):
    """
    Scatter plot of polarity contradiction vs variation.
    """
    df = get_dataset_or_error(["contradiction_polarity", "polarity_variations", "label", "date_clean"])
    if df is None:
        return

    filtered_df = apply_date_filter(df, "date_clean", pageref_label)

    plot_scatter(
        df=filtered_df,
        x_col="polarity_variations",
        y_col="contradiction_polarity",
        hue_col="label",
        title="Scatter Plot of Polarity Variations and Contradictions",
        xlabel="Polarity\nVariations",
        ylabel="Polarity\nContradictions"
    )
