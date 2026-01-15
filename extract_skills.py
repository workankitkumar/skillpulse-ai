import pandas as pd

# Load job data
jobs = pd.read_csv("data/jobs.csv")

# Define known skills
known_skills = [
    "python",
    "machine learning",
    "deep learning",
    "sql",
    "tensorflow",
    "docker",
    "pandas",
    "statistics"
]

# Function to extract skills from description
def extract_skills(description):
    description = description.lower()
    found = []
    for skill in known_skills:
        if skill in description:
            found.append(skill)
    return found

# Apply skill extraction
jobs["skills"] = jobs["description"].apply(extract_skills)

# Print results
print(jobs[["title", "skills"]])
