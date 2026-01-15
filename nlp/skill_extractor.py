import pandas as pd
import re

# --------------------------------------------------
# Skill normalization map (CRITICAL FIX)
# --------------------------------------------------
SKILL_MAP = {
    "python": ["python"],
    "java": ["java"],
    "sql": ["sql"],
    "machine learning": [
        "machine learning",
        "ml",
        "artificial intelligence",
        "ai"
    ],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "data science": ["data science"],
    "pytorch": ["pytorch", "torch"],
    "tensorflow": ["tensorflow", "tf"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "spark": ["spark"],
}

# --------------------------------------------------
# Skill extraction
# --------------------------------------------------
def extract_skills(text: str):
    if not text:
        return []

    text = text.lower()
    found = set()

    for canonical, variants in SKILL_MAP.items():
        for v in variants:
            if re.search(r"\b" + re.escape(v) + r"\b", text):
                found.add(canonical)

    return sorted(found)

# --------------------------------------------------
# Experience extraction
# --------------------------------------------------
def extract_experience(text: str):
    if not text:
        return "not specified"

    text = text.lower()

    patterns = [
        r"\d+\+?\s+years",
        r"\d+\+?\s+yrs",
        r"senior",
        r"junior",
        r"mid[- ]level",
        r"entry[- ]level"
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            return match.group()

    return "not specified"

# --------------------------------------------------
# Main enrichment pipeline
# --------------------------------------------------
def enrich_jobs_with_skills():
    jobs = pd.read_csv("data/jobs_raw.csv")

    skills_col = []
    experience_col = []

    for _, row in jobs.iterrows():
        title = str(row.get("title", ""))
        desc = str(row.get("description", ""))
        url = str(row.get("url", ""))

        combined_text = f"{title} {desc} {url}"

        skills_col.append(", ".join(extract_skills(combined_text)))
        experience_col.append(extract_experience(combined_text))

    jobs["skills"] = skills_col
    jobs["experience"] = experience_col

    jobs.to_csv("data/jobs_enriched.csv", index=False)
    print("✅ Skills & experience extracted → data/jobs_enriched.csv")

# --------------------------------------------------
# Entry point
# --------------------------------------------------
if __name__ == "__main__":
    enrich_jobs_with_skills()
