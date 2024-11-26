import re
from collections import Counter

import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")


def clean_text(text):
    """Remove punctuation, stopwords, and convert to lowercase."""
    text = re.sub(r"[^a-zA-Z\s]", "", text.lower())
    stop_words = set(stopwords.words("english"))
    words = [word for word in text.split() if word not in stop_words]
    return words


def most_common_words(text_column, top_n=10):
    """Get the most common words in a text column."""
    all_words = []
    for text in text_column.dropna():
        all_words.extend(clean_text(str(text)))
    return Counter(all_words).most_common(top_n)
