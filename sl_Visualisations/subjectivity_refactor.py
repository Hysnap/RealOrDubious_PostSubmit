from sl_utils.logger import log_function_call, streamlit_logger
from sl_visualisations.common_visual_functions import (get_dataset_or_error,
                                                       apply_date_filter,
                                                       plot_scatter)


@log_function_call(streamlit_logger)
def plot_article_vs_title_subjectivity(
    target_label="Article vs Title Subjectivity",
    pageref_label="subjectivity_scatter"):
    df = get_dataset_or_error(["article_subjectivity",
                               "title_subjectivity",
                               "label",
                               "date_clean"])
    if df is None:
        return

    filtered_df = apply_date_filter(df,
                                    "date_clean",
                                    pageref_label)

    plot_scatter(
        df=filtered_df,
        x_col="article_subjectivity",
        y_col="title_subjectivity",
        hue_col="label",
        title="Scatter Plot of Subjectivity: Articles vs Titles",
        xlabel="Article Subjectivity",
        ylabel="Title Subjectivity"
    )


@log_function_call(streamlit_logger)
def plot_article_subjectivity_vs_polarity(
    target_label="Article Subjectivity vs Polarity",
    pageref_label="Article_S_V_P_scatter"):
    df = get_dataset_or_error(["article_subjectivity",
                               "article_polarity",
                               "label",
                               "date_clean"])
    if df is None:
        return

    filtered_df = apply_date_filter(df,
                                    "date_clean",
                                    pageref_label)

    plot_scatter(
        df=filtered_df,
        x_col="article_polarity",
        y_col="article_subjectivity",
        hue_col="label",
        title="Scatter Plot of Article Subjectivity vs Polarity",
        xlabel="Article Polarity",
        ylabel="Article Subjectivity"
    )


@log_function_call(streamlit_logger)
def plot_title_subjectivity_vs_polarity(
    target_label="Title Subjectivity vs Polarity",
    pageref_label="Title_S_V_P_scatter"):
    df = get_dataset_or_error(["title_subjectivity",
                               "title_polarity",
                               "label",
                               "date_clean"])
    if df is None:
        return

    filtered_df = apply_date_filter(df,
                                    "date_clean",
                                    pageref_label)

    plot_scatter(
        df=filtered_df,
        x_col="title_polarity",
        y_col="title_subjectivity",
        hue_col="label",
        title="Scatter Plot of Title Subjectivity vs Polarity",
        xlabel="Title Polarity",
        ylabel="Title Subjectivity"
    )


@log_function_call(streamlit_logger)
def plot_article_vs_title_subjectivity_scat(
    target_label="Article vs Title Subjectivity (Alt)",
    pageref_label="subjectivity_scatter_alt"):
    df = get_dataset_or_error(["article_subjectivity",
                               "title_subjectivity",
                               "label",
                               "date_clean"])
    if df is None:
        return

    filtered_df = apply_date_filter(df,
                                    "date_clean",
                                    pageref_label)

    # Drop rows where both subjectivity columns are missing
    filtered_df.dropna(subset=["title_subjectivity",
                               "article_subjectivity"],
                       how="all",
                       inplace=True)

    plot_scatter(
        df=filtered_df,
        x_col="article_subjectivity",
        y_col="title_subjectivity",
        hue_col="label",
        title="Scatter Plot of Subjectivity: Articles vs Titles",
        xlabel="Article Subjectivity",
        ylabel="Title Subjectivity"
    )


@log_function_call(streamlit_logger)
def plot_subjectivity_contrad_variations(
    target_label="Subjectivity Contradiction vs Variations",
    pageref_label="Sub_con_var_scatter"):
    df = get_dataset_or_error(["contradiction_subjectivity",
                               "subjectivity_variations",
                               "label",
                               "date_clean"])
    if df is None:
        return

    filtered_df = apply_date_filter(df,
                                    "date_clean",
                                    pageref_label)

    plot_scatter(
        df=filtered_df,
        x_col="subjectivity_variations",
        y_col="contradiction_subjectivity",
        hue_col="label",
        title="Scatter Plot of Subjectivity Variations and Contradictions",
        xlabel="Subjectivity Variations",
        ylabel="Subjectivity Contradictions"
    )


# End of subjectivity_refactor.py
# PATH: sl_visualisations/original_visualisations/subjectivity_refactor.py