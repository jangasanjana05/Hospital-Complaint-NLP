import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

DATA_FILE = "complaints.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)
df = df.dropna(subset=["complaint", "category", "priority"])

# Build category prediction model
category_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# Build priority prediction model
priority_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

category_model.fit(
    df["complaint"].astype(str),
    df["category"].astype(str)
)

priority_model.fit(
    df["complaint"].astype(str),
    df["priority"].astype(str)
)


def predict_complaint(complaint):
    complaint = complaint.strip()

    if not complaint:
        raise ValueError("Please enter a complaint.")

    category = category_model.predict([complaint])[0]
    priority = priority_model.predict([complaint])[0]

    return category, priority


def get_dashboard_data():
    return df.copy()


def get_category_counts():
    return df["category"].value_counts()


def get_priority_counts():
    return df["priority"].value_counts()
