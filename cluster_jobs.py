import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load processed data
jobs = pd.read_csv("data/jobs_processed.csv")

# Convert skill lists to text
jobs["skills_text"] = jobs["skills"].apply(lambda x: " ".join(x.strip("[]").replace("'", "").split(", ")))

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(jobs["skills_text"])

# K-Means clustering
kmeans = KMeans(n_clusters=2, random_state=42)
jobs["cluster"] = kmeans.fit_predict(X)

# Display results
print(jobs[["title", "skills_text", "cluster"]])
