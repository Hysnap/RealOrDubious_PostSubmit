import pandas as pd
import streamlit as st
from sl_components.filters import apply_filters
from sl_utils.logger import logger


# Convert placeholder date to datetime once

def count_unique_records(df, column, filters=None):
    """Counts unique donors based on a specific DonationType."""
    df = apply_filters(df, filters)
    return df[column].nunique()


def count_missing_values(df, column, missing_value, filters=None):
    """Counts donations where a specific column has a given missing value."""
    df = apply_filters(df, filters)
    return df[df[column].eq(missing_value)].shape[0]


def count_null_values(df, column, filters=None):
    """Counts donations where a specific column has null (NaN) values."""
    df = apply_filters(df, filters)
    return df[column].isna().sum()


def get_top_or_bottom_entity_by_column(df,
                                       column,
                                       value_column,
                                       top=True,
                                       filters=None):
    """
    Returns the name and value of the entity with the
    greatest or smallest value
    in the specified column.

    Parameters:
        df (pd.DataFrame): The dataset.
        column (str): The column to group by.
        value_column (str): The column to sum for the value.
        top (bool, optional): If True, returns the top entity.
        If False, returns the bottom entity.
        filters (dict, optional): Dictionary where keys are column names
        and values are filter conditions.

    Returns:
        tuple: (EntityName, Value)
    """
    df = apply_filters(df, filters)
    grouped = df.groupby(column)[value_column].sum()
    if top:
        entity = grouped.idxmax()
        value = grouped.max()
    else:
        entity = grouped.idxmin()
        value = grouped.min()
    return entity, value


def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:,.1f}M"
    elif value >= 10_000:
        return f"{value / 1_000:,.1f}k"
    else:
        return f"{value:,.0f}"


def calculate_percentage(numerator=0, denominator=0):
    """Calculate the percentage of a numerator to a denominator"""
    try:
        numerator = float(numerator)
        denominator = float(denominator)
    except (ValueError, TypeError):
        return 0
    return (numerator / denominator) * 100 if denominator > 0 else 0


def calculate_agg_by_variable(
    datafile=st.session_state.get("data_clean"),
    groupby_variable="PartyName",
    groupby_name="Party",
    agg_variable="Value",
    agg_type="mean",
    agg_name="AverageDonation"
        ):
    """
    Calculate aggregate measures by group.

    Parameters:
    datafile (pd.DataFrame): DataFrame containing entity and measure columns.
    groupby_variable (str): Column name representing the entity.
    agg_variable (str): Column name representing the numeric measure.
    agg_type (str): Aggregation function to use (e.g., 'mean', 'sum').
    agg_name (str): Name for the aggregated measure.

    Returns:
    pd.DataFrame: DataFrame containing aggregated measures by group.
    """
    if datafile is None:
        return pd.DataFrame()

    # Calculate aggregate measures by allocated entity
    if agg_type == "mean":
        agg_df = datafile.groupby(groupby_variable,
                                  as_index=False)[agg_variable].mean()
    elif agg_type == "sum":
        agg_df = datafile.groupby(groupby_variable,
                                  as_index=False)[agg_variable].sum()
    elif agg_type == "count":
        agg_df = datafile.groupby(groupby_variable,
                                  as_index=False)[agg_variable].count()
    elif agg_type == "nunique":
        agg_df = datafile.groupby(groupby_variable,
                                  as_index=False)[agg_variable].nunique()
    else:
        raise ValueError(f"Unsupported aggregation type: {agg_type}")

    agg_df.rename(columns={agg_variable: agg_name,
                           groupby_variable: groupby_name}, inplace=True)

    return agg_df
