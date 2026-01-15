import pandas as pd
from collections import Counter

# Load processed data
jobs = pd.read_csv("data/jobs_processed.csv")

# Convert skills column from string to list
jobs["skills"] = jobs["skills"].apply(lambda x: x.strip("[]").replace("'", "").split(", "))

# Count all skills
all_skills = []
for skills in jobs["skills"]:
    all_skills.extend(skills)

skill_counts = Counter(all_skills)

# Convert to DataFrame
skill_demand = pd.DataFrame(
    skill_counts.items(),
    columns=["skill", "count"]
).sort_values(by="count", ascending=False)

print(skill_demand)
