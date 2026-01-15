import pandas as pd
from collections import Counter

# Load processed data
jobs = pd.read_csv("data/jobs_processed.csv")

# Convert skills column to list
jobs["skills"] = jobs["skills"].apply(
    lambda x: x.strip("[]").replace("'", "").split(", ")
)

# Calculate market skill demand
all_skills = []
for skills in jobs["skills"]:
    all_skills.extend(skills)

skill_counts = Counter(all_skills)

# User input (can be replaced by UI later)
user_skills = ["python", "sql"]

# Recommendation logic
recommended = []
for skill, count in skill_counts.most_common():
    if skill not in user_skills:
        recommended.append(skill)

print("User skills:", user_skills)
print("Recommended skills to learn:", recommended)
