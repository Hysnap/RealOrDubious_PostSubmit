# PATH: sl_visualisations/other_visuals_refactor.py

from sl_utils.logger import log_function_call, streamlit_logger
from sl_utils.common_visual_functions import (
    get_dataset_or_error,
    apply_date_filter,
    plotly_weighted_scatter,
    plot_boxplot,
    plot_hexbin_grid
)


@log_function_call(streamlit_logger)
def plot_article_vs_title_characters(
    target_label="Article vs Title Characters",
    pageref_label="char_scatter"):
    df = get_dataset_or_error([
        "text_length", "title_length", "label",
        "article_count", "date_clean"
    ])
    if df is None:
        return

    filtered_df = apply_date_filter(df, "date_clean", pageref_label)

    # Optional: filter extremely long texts
    filtered_df = filtered_df[
        (filtered_df["title_length"] < 1000) &
        (filtered_df["text_length"] < 25000)
    ]

    plotly_weighted_scatter(
        df=filtered_df,
        x="text_length",
        y="title_length",
        size="article_count",
        label_col="label",
        title="Scatter Plot of Character Counts: Articles vs Titles",
        xlabel="Article Character Count",
        ylabel="Title Character Count"
    )


@log_function_call(streamlit_logger)
def plot_article_text_count_distribution(
    target_label="Article Text Count Distribution",
    pageref_label="article_text_count_distribution"):
    df = get_dataset_or_error(["text_length", "label"])
    if df is None:
        return

    plot_boxplot(
        df=df,
        x_col="label",
        y_col="text_length",
        title="Article Text Count Distribution by Label",
        xlabel="Label",
        ylabel="Text Count"
    )


@log_function_call(streamlit_logger)
def plot_hex_subjectivity():
    df = get_dataset_or_error([
        "article_subjectivity", "title_subjectivity",
        "label", "date_clean"
    ])
    if df is None:
        return

    filtered_df = apply_date_filter(df, "date_clean", "hex_subjectivity")

    plot_hexbin_grid(
        df=filtered_df,
        x_col="article_subjectivity",
        y_col="title_subjectivity",
        label_col="label",
        title="Weighted Percentage of Real vs. Fake Articles (Subjectivity)",
        xlabel="Article Subjectivity",
        ylabel="Title Subjectivity",
        cmap="coolwarm",
        threshold=0.001,
        marginal_bins=30,
        grid_size=30
    )


@log_function_call(streamlit_logger)
def plot_hex_charcounts():
    df = get_dataset_or_error([
        "text_length", "title_length",
        "label", "date_clean"
    ])
    if df is None:
        return

    filtered_df = apply_date_filter(df, "date_clean", "hex_charcounts")

    # Filter character count extremes
    filtered_df = filtered_df[
        (filtered_df["title_length"] < 1000) &
        (filtered_df["text_length"] < 25000)
    ]

    plot_hexbin_grid(
        df=filtered_df,
        x_col="text_length",
        y_col="title_length",
        label_col="label",
        title="Weighted Percentage of Real vs. Fake Articles (Char Count)",
        xlabel="Article Size in Chars",
        ylabel="Title Size in Chars",
        cmap="coolwarm",
        threshold=10,
        xlim=(0, 25000),
        ylim=(0, 300),
        marginal_bins=25,
        grid_size=50
    )
