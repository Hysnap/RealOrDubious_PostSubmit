import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from sl_components.filters import filter_by_date
from sl_utils.logger import log_function_call, streamlit_logger
from sl_visualisations.common_visual_functions import get_dataset_or_error, select_display_type, prepare_counts, plot_bar, plot_line

@log_function_call(streamlit_logger)
def plot_article_count_by_subject(target_label="Article Count by Subject",
                                  pageref_label="article_subject_count"):
    df = get_dataset_or_error(["subject", "label"])
    if df is None:
        return

    display_type = select_display_type(pageref_label)
    counts, y_value, y_label = prepare_counts(df, ["subject", "label"], display_type)

    plot_bar(
        data=counts,
        x="subject",
        y=y_value,
        hue="label",
        title="Article Count by Subject (Real vs Dubious)",
        xlabel="Subject",
        ylabel=y_label
    )


@log_function_call(streamlit_logger)
def plot_article_count_by_source(target_label="Article Count by Source",
                                 pageref_label="article_source_count"):
    df = get_dataset_or_error(["source_name", "label"])
    if df is None:
        return

    display_type = select_display_type(pageref_label)
    counts, y_value, y_label = prepare_counts(df, ["source_name", "label"], display_type)

    plot_bar(
        data=counts,
        x="source_name",
        y=y_value,
        hue="label",
        title="Article Count by Source (Real vs Dubious)",
        xlabel="Source",
        ylabel=y_label
    )


@log_function_call(streamlit_logger)
def plot_article_count_by_media(target_label="Article Count by Media",
                                pageref_label="article_media_count"):
    df = get_dataset_or_error(["media_type", "label"])
    if df is None:
        return

    display_type = select_display_type(pageref_label)
    counts, y_value, y_label = prepare_counts(df, ["media_type", "label"], display_type)
    sorted_order = counts.groupby("media_type")["count"].sum().sort_values(ascending=False).index

    plot_bar(
        data=counts,
        x="media_type",
        y=y_value,
        hue="label",
        title="Article Count by Media (Real vs Dubious)",
        xlabel="Media Type",
        ylabel=y_label,
        order=sorted_order
    )


@log_function_call(streamlit_logger)
def plot_article_count_by_day_label(target_label="Article Count by Day Label",
                                    pageref_label="article_day_count"):
    df = get_dataset_or_error(["day_label", "label"])
    if df is None:
        return

    display_type = select_display_type(pageref_label)
    counts, y_value, y_label = prepare_counts(df, ["day_label", "label"], display_type)

    plot_bar(
        data=counts,
        x="day_label",
        y=y_value,
        hue="label",
        title="Article Count by Day (Real vs Dubious)",
        xlabel="Day Label",
        ylabel=y_label,
        order=counts["day_label"].unique()[::-1]
    )


@log_function_call(streamlit_logger)
def plot_article_count_by_day(target_label="Article Count by Day",
                              pageref_label="article_day_count2"):
    df = get_dataset_or_error(["date_clean", "label"])
    if df is None:
        return
    df = df[df["date_clean"] >= '2015-01-01']

    display_type = select_display_type(pageref_label)
    counts, y_value, y_label = prepare_counts(df, ["date_clean", "label"], display_type)

    plot_line(
        data=counts,
        x="date_clean",
        y=y_value,
        hue="label",
        title="Article Count by Day (Real vs Dubious)",
        xlabel="Date",
        ylabel=y_label
    )


@log_function_call(streamlit_logger)
def plot_article_count_by_location(target_label="Article Count by Location",
                                   pageref_label="article_location_count"):
    df = get_dataset_or_error(["unique_location_count", "label"])
    if df is None:
        return

    display_type = select_display_type(pageref_label)
    counts, y_value, y_label = prepare_counts(df, ["unique_location_count", "label"], display_type)

    plot_bar(
        data=counts,
        x="unique_location_count",
        y=y_value,
        hue="label",
        title="Article Count by Location Count (Real vs Dubious)",
        xlabel="Location Count",
        ylabel=y_label,
        rotate_xticks=True
    )


# End of file
# PATH: sl_visualisations/article_count_refactor.py