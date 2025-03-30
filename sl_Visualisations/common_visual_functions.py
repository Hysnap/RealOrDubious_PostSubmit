import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from sl_utils.logger import log_function_call, streamlit_logger
import numpy as np
import pandas as pd
from sl_components.filters import filter_by_date
from nltk.corpus import stopwords
from wordcloud import WordCloud
import plotly.express as px


# ================= General Helpers =====================

def get_dataset_or_error(required_columns=None, dataflag=None):
    """
    Retrieve and validate the dataset from session_state.

    if no flag present load data from session_state else load preprocessed_wordcloud_data
    """
    if dataflag == "text":
        df = st.session_state.get("wordcount_data", None)
        if df is None:
            df= df.from_csv("sl_data_for_dashboard//preprocessed_wordcloud.zip")
            st.session_state["preprocessed_wordcloud_data"] = df
        return df
    elif dataflag is None:
        df = st.session_state.get("data_clean", None)
        if df is None:
            st.error("No data found. Please upload a dataset.")
            return None

        if required_columns:
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                st.error(f"Dataset missing required columns: {', '.join(missing)}")
                return None
        return df
    else:
        st.error("Invalid data flag.")
        return None



def apply_date_filter(df,
                      date_col="date_clean",
                      pageref_label=""):
    df[date_col] = pd.to_datetime(df[date_col])
    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()

    show_slider = st.checkbox("Show Date Slider",
                              value=False,
                              key=f"{pageref_label}_slider")
    if show_slider:
        start_date, end_date = st.slider(
            "Select Date Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD",
            key=pageref_label
        )
    else:
        start_date, end_date = min_date, max_date

    return filter_by_date(df,
                          pd.to_datetime(start_date),
                          pd.to_datetime(end_date), date_col)


# ================ Display Type Selector ================

@log_function_call(streamlit_logger)
def select_display_type(key):
    return st.radio("Select Display Type",
                    options=["Count", "Percentage"],
                    index=1,
                    key=key)


def prepare_counts(df, group_by, display_type):
    counts = df.groupby(group_by).agg(article_count=("article_count", "sum")).reset_index()

    if display_type == "Percentage":
        counts["percentage"] = counts["article_count"] / counts.groupby(group_by[0])["article_count"].transform("sum") * 100
        return counts, "percentage", "Percentage of Articles"

    return counts, "article_count", "Sum of Article Counts"


# ====================== Plotting =======================

def plot_bar(data, x, y, hue, title, xlabel,
             ylabel, order=None, rotate_xticks=True):
    my_pal = {0: "green", 1: "red"}
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.barplot(data=data, x=x, y=y, hue=hue,
                palette=my_pal, alpha=0.7, ax=ax, order=order)

    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles, title="Label",
              labels=["Dubious (0)", "Real (1)"], fontsize=8)
    if rotate_xticks:
        plt.xticks(rotation=45)
    st.pyplot(fig)


def plot_line(data, x, y, hue, title, xlabel, ylabel):
    my_pal = {0: "green", 1: "red"}
    fig, ax = plt.subplots(figsize=(12, 3))
    sns.lineplot(data=data, x=x, y=y, hue=hue,
                 palette=my_pal, alpha=0.7, ax=ax)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles, title="Label",
              labels=["Dubious (0)", "Real (1)"], fontsize=10)
    plt.xticks(rotation=45)
    st.pyplot(fig)


def plot_scatter(df, x_col, y_col, hue_col,
                 title, xlabel, ylabel, palette=None):
    if df.empty:
        st.warning("No data available for the selected date range.")
        return

    palette = palette or {0: "green", 1: "red"}
    fig, ax = plt.subplots(figsize=(3, 3))
    sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col,
                    palette=palette, alpha=0.7, ax=ax)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.legend(title="Label", labels=["Dubious (0)", "Real (1)"], fontsize=10)
    st.pyplot(fig)


def plot_violin(ax, df, x, y, title, xlabel,
                ylabel, log_scale=False, color_map=None):
    sns.violinplot(data=df, x=x, y=y, ax=ax,
                   hue=x, legend=False, palette=color_map)
    ax.set_title(title, fontsize=8)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Dubious (0)", "Real (1)"])
    ax.set_xlabel(xlabel, fontsize=6)
    ax.set_ylabel(ylabel, fontsize=6)
    if log_scale:
        ax.set_yscale("log")
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)


def plot_boxplot(df, x_col, y_col, title, xlabel, ylabel, palette=None):
    fig, ax = plt.subplots(figsize=(3, 3))
    palette = palette or {1: "green", 0: "red"}
    sns.boxplot(data=df, x=x_col, y=y_col, palette=palette, ax=ax)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.set_xticklabels(["Dubious (0)", "Real (1)"])
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    st.pyplot(fig)


def plot_hexbin_grid(df,
                     x_col,
                     y_col,
                     label_col,
                     title,
                     xlabel,
                     ylabel,
                     cmap="coolwarm",
                     xlim=None,
                     ylim=None,
                     threshold=None,
                     marginal_bins=30,
                     grid_size=30):
    if threshold:
        df.loc[df[x_col].abs() < threshold, x_col] = None
        df.loc[df[y_col].abs() < threshold, y_col] = None
    df = df.dropna(subset=[x_col, y_col])
    df[label_col] = df[label_col].astype(int)

    fig = plt.figure(figsize=(8, 8))
    grid = sns.jointplot(data=df, x=x_col, y=y_col, kind="hex",
                         cmap=cmap, gridsize=grid_size, marginal_ticks=True)

    hexbin = grid.ax_joint.hexbin(df[x_col],
                                  df[y_col],
                                  C=df[label_col],
                                  reduce_C_function=np.mean,
                                  gridsize=grid_size,
                                  cmap=cmap)

    cbar = fig.colorbar(hexbin, ax=grid.ax_joint)
    cbar.set_label("Proportion of Real Articles", fontsize=10)

    sns.histplot(df[x_col], bins=marginal_bins,
                 ax=grid.ax_marg_x, color="gray", kde=True)
    sns.histplot(df[y_col], bins=marginal_bins,
                 ax=grid.ax_marg_y, color="gray", kde=True)

    grid.figure.suptitle(title, fontsize=12)
    grid.figure.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make space for the title
    grid.ax_joint.set_xlabel(xlabel, fontsize=10)
    grid.ax_joint.set_ylabel(ylabel, fontsize=10)

    if xlim:
        grid.ax_joint.set_xlim(*xlim)
    if ylim:
        grid.ax_joint.set_ylim(*ylim)

    st.pyplot(grid.fig)


def plotly_weighted_scatter(df, x, y, size, label_col,
                            title, xlabel, ylabel,
                            mode="ratio", max_size=40):
    if df.empty:
        st.warning("No data available to display.")
        return

    df = df.copy()

    if mode == "binary":
        df[label_col] = df[label_col].astype(str)
        df = df.sort_values(by=label_col)

        fig = px.scatter(
            df,
            x=x,
            y=y,
            size=size,
            color=label_col,
            color_discrete_map={"0": "red", "1": "green"},
            size_max=max_size,
            opacity=0.7,
            title=title,
            hover_data={x: True, y: True, size: True, label_col: True}
        )

    elif mode == "ratio":
        # Pivot the data to combine label 0 and 1 counts at each x/y point
        grouped = df.groupby([x, y, label_col])[size].sum().unstack(fill_value=0).reset_index()
        grouped.columns.name = None  # remove MultiIndex name

        grouped["real_ratio"] = grouped.get(1, 0) / (grouped.get(1, 0) + grouped.get(0, 0))
        grouped["real_ratio"] = grouped["real_ratio"].fillna(0.5)
        grouped["article_count"] = grouped.get(1, 0) + grouped.get(0, 0)

        fig = px.scatter(
            grouped,
            x=x,
            y=y,
            size="article_count",
            color="real_ratio",
            color_continuous_scale=["red", "purple", "green"],
            size_max=max_size,
            opacity=0.7,
            title=title,
            hover_data={x: True, y: True, "article_count": True, "real_ratio": True}
        )

    else:
        st.error(f"Unknown mode '{mode}' for plotly_weighted_scatter.")
        return

    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        legend_title="Label" if mode == "binary" else "Realness Ratio",
        margin=dict(l=20, r=20, t=40, b=20),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

# =============== Wordcloud Helpers ====================

# def get_cleaned_text(df, label=None):
#     if label is not None:
#         df = df[df["label"] == label]
#     return " ".join(df["text"].astype(str).str.lower().str.split().sum())


# def generate_wordcloud(text, stop_words):
#     return WordCloud(width=800, height=400,
#                      background_color="white",
#                      stopwords=stop_words).generate(text)


# def display_wordcloud(wordcloud):
#     fig, ax = plt.subplots(figsize=(8, 4))
#     ax.imshow(wordcloud, interpolation="bilinear")
#     ax.axis("off")
#     st.pyplot(fig)


# def get_stopwords():
#     return set(stopwords.words("english"))

# end of common_visual_functions.py
# Path: sl_visualisations/common_visual_functions.py