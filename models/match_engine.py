import pandas as pd   # 🔥 THIS WAS MISSING

# -----------------------------
# Skill Weights
# -----------------------------
CORE_SKILLS = {
    "python": 2,
    "machine learning": 3,
    "deep learning": 3,
    "nlp": 3,
    "data science": 3,
    "sql": 2,
}

TOOL_SKILLS = {
    "docker": 1,
    "kubernetes": 1,
    "aws": 1,
    "azure": 1,
    "gcp": 1,
    "pytorch": 1,
    "tensorflow": 1,
    "spark": 1,
}

# -----------------------------
# Helpers
# -----------------------------
def normalize_skills(skill_string):
    if pd.isna(skill_string) or not skill_string.strip():
        return set()
    return set(s.strip().lower() for s in skill_string.split(","))


def compute_score(user_skills, job_skills):
    score = 0
    max_score = 0

    for skill, weight in CORE_SKILLS.items():
        max_score += weight
        if skill in job_skills and skill in user_skills:
            score += weight

    for skill, weight in TOOL_SKILLS.items():
        max_score += weight
        if skill in job_skills and skill in user_skills:
            score += weight

    return round((score / max_score) * 100, 2) if max_score else 0

# -----------------------------
# Matching Engine
# -----------------------------
def match_jobs(user_skills):
    jobs = pd.read_csv("data/jobs_enriched.csv")
    user_skills = set(s.lower().strip() for s in user_skills)

    columns = [
        "title",
        "location",
        "match_score",
        "matched_skills",
        "missing_skills"
    ]

    results = []

    for _, row in jobs.iterrows():
        job_skills = normalize_skills(row.get("skills", ""))
        if not job_skills:
            continue

        score = compute_score(user_skills, job_skills)

        if score < 10:
            continue

        matched = user_skills & job_skills
        missing = job_skills - user_skills

        results.append({
            "title": row.get("title", ""),
            "location": row.get("location", ""),
            "match_score": score,
            "matched_skills": ", ".join(sorted(matched)),
            "missing_skills": ", ".join(sorted(missing)),
        })

    if not results:
        return pd.DataFrame(columns=columns)

    return pd.DataFrame(results, columns=columns).sort_values(
        "match_score", ascending=False
    )
