import os
import sys

import pandas as pd
import streamlit as st

# Dynamically add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import display_html

from src.data_insights import generate_statistics
from src.data_processing import clean_data
from src.data_processing import get_data_summary
from src.data_processing import load_data
from src.text_analysis import most_common_words
from src.visualization import plot_bar_chart
from src.visualization import plot_data_type_distribution
from src.visualization import plot_histogram
from src.visualization import plot_most_frequent_words
from src.visualization import plot_time_series
from src.visualization import plot_top_missing_values
from src.visualization import plot_top_unique_values


# Page Config
st.set_page_config(
    page_title="DataLens",
    page_icon="https://cdn.weasyl.com/~ley/submissions/524374/ca8423f69f9347a4943e373d5a2bf3cdede228ea8347e1fefcef0ef700934df2/ley-camera-lens-illustrator.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

display_html("app/app.html")

# App title
st.title("DataLens")

# Columns Layout
upload_col, data_col = st.columns([2, 4], gap="large")

# File Upload
with upload_col:
    uploaded_file = st.file_uploader("Upload your CSV/Excel file", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            # Load Data
            data = load_data(uploaded_file)
            new = st.container(height=80, border=False)
            head_col, tail_col = st.columns(2)
            with head_col:
                st.header("Data Preview")

            # Data Cleaning Toggle
            with tail_col:
                st.write("")
                clean_data_toggle = st.toggle("Remove duplicates")

            if clean_data_toggle:
                # Show cleaned data
                cleaned_data = clean_data(data)
                st.write("Data after Cleaning")
                st.write(cleaned_data.head())
            else:
                # Show original data
                st.write("Original Data")
                st.write(data.head())

            # Data Summary
            summary = get_data_summary(data)

            with data_col:
                columns_col, datatype_col, missing_values_col, unique_col = st.columns(
                    [0.7, 1, 1, 1]
                )

                with columns_col:
                    st.header("Columns")
                    st.header(len(data.columns.tolist()))

                with datatype_col:
                    st.header("Data Types")
                    pie_chart = plot_data_type_distribution(summary)
                    st.pyplot(pie_chart)

                with missing_values_col:
                    st.header("Missing Values")
                    missing_values_chart = plot_top_missing_values(summary)
                    st.pyplot(missing_values_chart)

                with unique_col:
                    st.header("Unique Values")
                    unique_values_chart = plot_top_unique_values(summary)
                    st.pyplot(unique_values_chart)

                # Column Selection
                st.write("## Column Insights")
                selected_column = st.selectbox(
                    "Select a Column for Analysis", data.columns
                )

                # Statistics and Visualizations
                table_col, plot_col = st.columns([1, 1], gap="small")
                # Handle different column types
                if data[selected_column].dtype == "object":
                    # Attempt to convert the column to datetime
                    try:
                        data[selected_column] = pd.to_datetime(
                            data[selected_column], errors="raise"
                        )
                        # If successful, treat it as a datetime column
                        with table_col:
                            st.write("DateTime Insights:")
                            st.write(
                                data[selected_column]
                                .value_counts()
                                .sort_index()
                                .head(10)
                            )
                        with plot_col:
                            st.pyplot(plot_time_series(data, selected_column))
                    except Exception as e:
                        # If not a datetime column, check if it's text or categorical
                        if (
                            data[selected_column]
                            .apply(lambda x: len(str(x).split()))
                            .mean()
                            > 8
                        ):
                            # Text Data (Sentence) - Plot Most Frequent Words
                            with table_col:
                                with st.expander("Most Frequent Words", expanded=True):
                                    word_counts = most_common_words(
                                        data[selected_column]
                                    )
                                    st.dataframe(word_counts)
                            with plot_col:
                                st.pyplot(plot_most_frequent_words(word_counts))
                        else:
                            # Categorical Data - Use the existing bar chart
                            with table_col:
                                st.write("Most Common Categories:")
                                st.write(data[selected_column].value_counts().head(10))
                            with plot_col:
                                st.pyplot(plot_bar_chart(data, selected_column))
                else:
                    # Handle numerical or datetime columns
                    if data[selected_column].dtype in ["int64", "float64"]:
                        stats = generate_statistics(data, selected_column)
                        with table_col:
                            with st.expander("Statistics", expanded=True):
                                st.write(stats)
                        with plot_col:
                            st.pyplot(plot_histogram(data, selected_column))
                    elif (
                        pd.to_datetime(data[selected_column], errors="coerce")
                        .notna()
                        .all()
                    ):
                        # Handle DateTime columns
                        with table_col:
                            st.write("DateTime Insights:")
                            st.write(
                                data[selected_column]
                                .value_counts()
                                .sort_index()
                                .head(10)
                            )
                        with plot_col:
                            st.pyplot(plot_time_series(data, selected_column))

        except Exception as e:
            # If there is an error during the file loading or processing, show an error message
            st.error(f"Error reading the file: {str(e)}")
