import pandas as pd


def generate_statistics(df, column):
    """Generate basic statistics for a selected column."""
    if df[column].dtype in ["int64", "float64"]:
        stats = {
            "Mean": df[column].mean(),
            "Median": df[column].median(),
            "Std Dev": df[column].std(),
            "Min": df[column].min(),
            "Max": df[column].max(),
        }
    elif df[column].dtype == "object":
        stats = {
            "Most Common Value": df[column].mode()[0],
            "Unique Values Count": df[column].nunique(),
        }
    else:
        stats = {"Message": "Unsupported column type for detailed statistics."}
    return stats
