import pandas as pd


def load_data(file):
    """Load data from a CSV or Excel file."""
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")


def clean_data(df):
    """Clean the dataset by handling missing values and duplicates."""
    cleaned_df = df.copy()
    # Remove duplicates
    cleaned_df = cleaned_df.drop_duplicates()
    return cleaned_df


def get_data_summary(df):
    """Get a summary of the data: missing values, column data types, and shape."""
    summary = {
        "Column Name": df.columns,
        "Data Type": df.dtypes,
        "Missing Values": df.isnull().sum(),
        "Percentage Missing": (df.isnull().mean() * 100),
        "Unique Values": df.nunique(),
    }
    summary_df = pd.DataFrame(summary)
    summary_df["Data Type"] = summary_df["Data Type"].astype(
        str
    )  # Ensure compatibility with Streamlit
    return summary_df
