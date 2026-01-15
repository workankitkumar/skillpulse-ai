import pdfplumber
import re

# -------------------------------------------------
# Extract raw text from PDF
# -------------------------------------------------
def extract_resume_text(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.lower()


# -------------------------------------------------
# Skill vocabulary (same philosophy as job extractor)
# -------------------------------------------------
SKILL_MAP = {
    "python": ["python"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "nlp": ["nlp", "natural language processing"],
    "data science": ["data science"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "sql": ["sql"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws"],
    "azure": ["azure"],
    "gcp": ["gcp"],
    "java": ["java"],
    "javascript": ["javascript", "js"]
}

# -------------------------------------------------
# Extract skills from resume text
# -------------------------------------------------
def extract_skills_from_resume(text):
    found_skills = set()

    for skill, keywords in SKILL_MAP.items():
        for kw in keywords:
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, text):
                found_skills.add(skill)

    return sorted(found_skills)
