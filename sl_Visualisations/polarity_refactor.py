# Description: Visualisations for polarity related data.
# Category: Visualisations

# PATH: sl_visualisations/polarity_refactor.py

from sl_utils.logger import log_function_call, streamlit_logger
import streamlit as st
from sl_visualisations.common_visual_functions import (
    get_dataset_or_error,
    apply_date_filter,
    plotly_weighted_scatter
)



@log_function_call(streamlit_logger)
def plot_article_vs_title_polarity(target_label="Article vs Title Polarity",
                                   pageref_label="polarity_scatter"):
    df = get_dataset_or_error(["title_polarity", "article_polarity", "label", "article_count", "date_clean"])
    if df is None:
        return

    mode = st.radio(
        "Select Coloring Mode:",
        options=["binary", "ratio"],
        index=1,
        key=f"{pageref_label}_mode"
        )

    df = apply_date_filter(df, "date_clean", pageref_label)

    plotly_weighted_scatter(
        df,
        x="title_polarity",
        y="article_polarity",
        size="article_count",
        label_col="label",
        title="Plot of Article Polarity vs Title Polarity",
        xlabel="Title Polarity",
        ylabel="Article Polarity",
        mode=mode
    )


@log_function_call(streamlit_logger)
def plot_title_vs_article_polarity(target_label="Title vs Article Polarity",
                                   pageref_label="title_article_polarity_scatter"):
    df = get_dataset_or_error(["title_polarity", "article_polarity", "label", "article_count", "date_clean"])
    if df is None:
        return

    mode = st.radio(
        "Select Coloring Mode:",
        options=["binary", "ratio"],
        index=1,
        key=f"{pageref_label}_mode"
        )

    df = apply_date_filter(df, "date_clean", pageref_label)

    plotly_weighted_scatter(
        df,
        x="article_polarity",
        y="title_polarity",
        size="article_count",
        label_col="label",
        title="Scatter Plot of Polarities: Articles vs Titles",
        xlabel="Article Polarity",
        ylabel="Title Polarity",
        mode=mode
    )


@log_function_call(streamlit_logger)
def plot_polarity_contrad_variations(target_label="Polarity Contradiction vs Variations",
                                     pageref_label="Pol_con_var_scatter"):
    df = get_dataset_or_error(["contradiction_polarity", "polarity_variations", "label", "article_count", "date_clean"])
    if df is None:
        return

    mode = st.radio(
        "Select Coloring Mode:",
        options=["binary", "ratio"],
        index=1,
        key=f"{pageref_label}_mode"
        )

    df = apply_date_filter(df, "date_clean", pageref_label)

    plotly_weighted_scatter(
        df,
        x="polarity_variations",
        y="contradiction_polarity",
        size="article_count",
        label_col="label",
        title="Scatter Plot of Polarity Variations and Contradictions",
        xlabel="Polarity Variations",
        ylabel="Polarity Contradictions",
        mode=mode
    )
