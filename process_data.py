import pandas as pd

# Load raw data
jobs = pd.read_csv("data/jobs_live.csv")

# Known skills list
known_skills = [
    "python", "machine learning", "deep learning",
    "sql", "tensorflow", "docker", "pandas", "statistics"
]

# Skill extraction function
def extract_skills(description):
    description = description.lower()
    return [skill for skill in known_skills if skill in description]

# Apply NLP processing
jobs["skills"] = jobs["description"].apply(extract_skills)

# Save processed data
jobs.to_csv("data/jobs_processed.csv", index=False)

print("✅ Processed data saved to data/jobs_processed.csv")
