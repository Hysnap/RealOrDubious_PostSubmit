# PATH: sl_visualisations/boxplot_visuals.py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from sl_utils.logger import log_function_call, streamlit_logger
from sl_visualisations.common_visual_functions import (
    get_dataset_or_error,
    plot_violin
)

MAX_ROWS = 100000  # prevent memory overload for very large expansions


def expand_weighted_df(df, columns, weight_col="article_count"):
    """
    Expand the DataFrame according to article_count values for accurate violin plots.
    Clips total size to MAX_ROWS for memory safety.
    """
    df = df.copy()
    df = df.loc[df[weight_col] > 0]
    df = df.loc[:, columns + [weight_col]]

    # Repeat each row based on its article_count
    df_expanded = df.loc[df.index.repeat(df[weight_col])].drop(columns=weight_col)

    if len(df_expanded) > MAX_ROWS:
        df_expanded = df_expanded.sample(MAX_ROWS, random_state=42)

    return df_expanded


@log_function_call(streamlit_logger)
def plot_polarity_subjectivity_boxplots(
    target_label="Polarity and Subjectivity Boxplots",
    pageref_label="polarity_subjectivity_boxplots"
):
    """
    Plots a grid of violin plots showing various polarity and subjectivity metrics
    across real (1) and dubious (0) labels using weighted article_count expansion.
    """

    columns_required = [
        "title_polarity", "title_subjectivity",
        "article_polarity", "article_subjectivity",
        "contradiction_subjectivity", "subjectivity_variations",
        "contradiction_polarity", "polarity_variations",
        "overall_subjectivity", "overall_polarity",
        "text_length", "title_length", "label",
        "article_count"
    ]
    df = get_dataset_or_error(columns_required)
    if df is None:
        return

    my_pal = {"0": "r", "1": "g", 0: "r", 1: "g"}

    # Expand weighted rows for violin plotting
    expanded_df = expand_weighted_df(df, [
        "title_polarity", "title_subjectivity",
        "article_polarity", "article_subjectivity",
        "contradiction_subjectivity", "subjectivity_variations",
        "contradiction_polarity", "polarity_variations",
        "overall_subjectivity", "overall_polarity",
        "text_length", "title_length", "label"
    ])

    fig, ax = plt.subplots(3, 4, figsize=(12, 6))

    plots = [
        ("title_polarity", "Title Polarity by Label",
         "Label", "Polarity", False),
        ("title_subjectivity", "Title Subjectivity by Label",
         "Label", "Subjectivity", False),
        ("article_polarity", "Article Polarity by Label",
         "Label", "Polarity", False),
        ("article_subjectivity", "Article Subjectivity by Label",
         "Label", "Subjectivity", False),
        ("contradiction_polarity", "Polarity Contradictions",
         "Label", "Level of Contradictions", False),
        ("polarity_variations", "Polarity Variance",
         "Label", "Variance between Title and Text", False),
        ("contradiction_subjectivity", "Subjectivity Contradictions",
         "Label", "Level of Contradictions", False),
        ("subjectivity_variations", "Subjectivity Variance",
         "Label", "Variance between Title and Text", False),
        ("text_length", "Character Count Article",
         "Label", "Characters", True),
        ("overall_subjectivity", "Overall Subjectivity",
         "Label", "Subjectivity", False),
        ("overall_polarity", "Overall Polarity",
         "Label", "Polarity", False),
        ("title_length", "Character Count Title",
         "Label", "Characters", True),
    ]

    for i, (col, title, xlabel, ylabel, log_scale) in enumerate(plots):
        row, col_index = divmod(i, 4)
        plot_violin(
            ax[row, col_index], expanded_df, "label", col,
            title=title, xlabel=xlabel, ylabel=ylabel,
            log_scale=log_scale, color_map=my_pal
        )

    plt.tight_layout()
    st.pyplot(fig)

# End of boxplot_visuals.py
# Path: sl_visualisations/boxplot_visuals.py