# PATH: sl_visualisations/subjectivity_refactor.py

from sl_utils.logger import log_function_call, streamlit_logger
import streamlit as st
from sl_utils.common_visual_functions import (
    get_dataset_or_error,
    apply_date_filter,
    plotly_weighted_scatter
)


@log_function_call(streamlit_logger)
def plot_article_vs_title_subjectivity(
    target_label="Article vs Title Subjectivity",
    pageref_label="subjectivity_scatter"):
    df = get_dataset_or_error([
        "article_subjectivity", "title_subjectivity",
        "label", "article_count", "date_clean"])
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
        df=df,
        x="article_subjectivity",
        y="title_subjectivity",
        size="article_count",
        label_col="label",
        title="Scatter Plot of Subjectivity: Articles vs Titles",
        xlabel="Article Subjectivity",
        ylabel="Title Subjectivity",
        mode=mode
    )


@log_function_call(streamlit_logger)
def plot_article_subjectivity_vs_polarity(
    target_label="Article Subjectivity vs Polarity",
    pageref_label="Article_S_V_P_scatter"):
    df = get_dataset_or_error([
        "article_subjectivity", "article_polarity",
        "label", "article_count", "date_clean"])
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
        df=df,
        x="article_polarity",
        y="article_subjectivity",
        size="article_count",
        label_col="label",
        title="Scatter Plot of Article Subjectivity vs Polarity",
        xlabel="Article Polarity",
        ylabel="Article Subjectivity",
        mode=mode
    )


@log_function_call(streamlit_logger)
def plot_title_subjectivity_vs_polarity(
    target_label="Title Subjectivity vs Polarity",
    pageref_label="Title_S_V_P_scatter"):
    df = get_dataset_or_error([
        "title_subjectivity", "title_polarity",
        "label", "article_count", "date_clean"])
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
        df=df,
        x="title_polarity",
        y="title_subjectivity",
        size="article_count",
        label_col="label",
        title="Scatter Plot of Title Subjectivity vs Polarity",
        xlabel="Title Polarity",
        ylabel="Title Subjectivity",
        mode=mode
    )


@log_function_call(streamlit_logger)
def plot_article_vs_title_subjectivity_scat(
    target_label="Article vs Title Subjectivity (Alt)",
    pageref_label="subjectivity_scatter_alt"):
    df = get_dataset_or_error([
        "article_subjectivity", "title_subjectivity",
        "label", "article_count", "date_clean"])
    if df is None:
        return

    mode = st.radio(
        "Select Coloring Mode:",
        options=["binary", "ratio"],
        index=1,
        key=f"{pageref_label}_mode"
        )

    df = apply_date_filter(df, "date_clean", pageref_label)

    # Drop rows where both subjectivity columns are missing
    df.dropna(subset=["title_subjectivity", "article_subjectivity"],
              how="all", inplace=True)

    plotly_weighted_scatter(
        df=df,
        x="article_subjectivity",
        y="title_subjectivity",
        size="article_count",
        label_col="label",
        title="Scatter Plot of Subjectivity: Articles vs Titles",
        xlabel="Article Subjectivity",
        ylabel="Title Subjectivity",
        mode=mode,
    )


@log_function_call(streamlit_logger)
def plot_subjectivity_contrad_variations(
    target_label="Subjectivity Contradiction vs Variations",
    pageref_label="Sub_con_var_scatter"):
    df = get_dataset_or_error([
        "contradiction_subjectivity", "subjectivity_variations",
        "label", "article_count", "date_clean"])
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
        df=df,
        x="subjectivity_variations",
        y="contradiction_subjectivity",
        size="article_count",
        label_col="label",
        title="Scatter Plot of Subjectivity Variations and Contradictions",
        xlabel="Subjectivity Variations",
        ylabel="Subjectivity Contradictions",
        mode=mode
    )
