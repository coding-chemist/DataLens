import matplotlib.cm as cm
import matplotlib.pyplot as plt


def plot_histogram(df, column):
    """Plot a histogram for a numerical column."""
    fig, ax = plt.subplots()
    df[column].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
    ax.set_title(f"Histogram of {column}")
    ax.grid(False)
    return fig


def plot_bar_chart(df, column):
    """Plot a bar chart for a categorical column."""
    fig, ax = plt.subplots()
    df[column].value_counts().head(10).plot(kind="bar", ax=ax, color="coral")
    ax.set_title(f"Bar Chart of {column}")
    return fig


def plot_time_series(df, column):
    """Plot a time series for a datetime column."""
    fig, ax = plt.subplots(figsize=(6, 5))
    df[column].value_counts().sort_index().plot(ax=ax)
    ax.set_title(f"Time Series Plot of {column}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Frequency")
    return fig


def plot_data_type_distribution(summary_df):
    """Generate a pie chart for the distribution of data types."""
    data_type_counts = summary_df["Data Type"].value_counts()
    colormap = cm.get_cmap("Paired", len(data_type_counts))
    colors = [colormap(i) for i in range(len(data_type_counts))]

    fig, ax = plt.subplots()
    ax.pie(
        data_type_counts,
        labels=data_type_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
    )
    ax.set_title("Distribution of Data Types")
    return fig


def plot_top_missing_values(summary_df):
    """Generate a bar chart for the top 5 columns with the most missing values."""
    top_missing = summary_df.nlargest(5, "Missing Values")
    fig, ax = plt.subplots()
    ax.bar(
        top_missing["Column Name"],
        top_missing["Missing Values"],
        color="skyblue",
        edgecolor="black",
    )
    ax.set_title("Top 5 Columns with Missing Values")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Missing Values")
    ax.set_xticks(range(len(top_missing["Column Name"])))
    ax.set_xticklabels(top_missing["Column Name"], rotation=90)
    return fig


def plot_top_unique_values(summary_df):
    """Generate a bar chart for the top 5 columns with the most unique values."""
    top_unique = summary_df.nlargest(5, "Unique Values")  # Sort and select top 5
    fig, ax = plt.subplots()
    ax.bar(
        top_unique["Column Name"],
        top_unique["Unique Values"],
        color="lightgreen",
        edgecolor="black",
    )
    ax.set_title("Top 5 Columns with Unique Values")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Unique Values")
    ax.set_xticks(range(len(top_unique["Column Name"])))
    ax.set_xticklabels(top_unique["Column Name"], rotation=90, ha="right")
    return fig


def plot_most_frequent_words(word_counts):
    """Plot the most frequent words in a text column."""
    # Unzip the word counts into separate lists for words and their frequencies
    words, counts = zip(*word_counts)

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(words, counts, color="lightcoral")
    ax.set_title("Most Frequent Words")
    ax.set_xlabel("Words")
    ax.set_ylabel("Frequency")
    ax.set_xticklabels(words, rotation=90, ha="right")
    return fig
