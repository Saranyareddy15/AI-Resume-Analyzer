"""
Stage 1 of the "AI": simple, explainable keyword-overlap scoring.

This is intentionally NOT deep NLP yet — it's a solid, honest
baseline you can explain in an interview ("I started with keyword
matching, then upgraded to semantic similarity"). Swap this module
out later for a TensorFlow/embedding-based version without touching
the rest of the app.
"""

import re
import nltk
from nltk.corpus import stopwords

# Download once, quietly, if not already present.
try:
    STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords", quiet=True)
    STOPWORDS = set(stopwords.words("english"))

# A small curated skill vocabulary. In a real ATS tool you'd load a
# much bigger list (or a skills taxonomy). Extend this freely.
COMMON_SKILLS = {
    "python", "flask", "django", "java", "javascript", "html", "css",
    "sql", "mysql", "postgresql", "mongodb", "git", "github", "docker",
    "kubernetes", "aws", "azure", "gcp", "rest", "api", "tensorflow",
    "pytorch", "nlp", "machine learning", "deep learning", "pandas",
    "numpy", "scikit-learn", "react", "node", "linux", "agile", "scrum",
    "opencv", "keras", "excel", "communication", "leadership",
    "problem solving", "teamwork", "project management",
}


def _tokenize(text):
    text = text.lower()
    words = re.findall(r"[a-zA-Z][a-zA-Z+.#]*", text)
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def extract_keywords(text):
    """Return the set of known skills found in the text."""
    text_lower = text.lower()
    found = set()
    for skill in COMMON_SKILLS:
        # word-boundary match so "java" doesn't match inside "javascript"
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def compute_ats_score(resume_text, jd_text):
    """
    Returns a dict with:
      - score: 0-100 float
      - matched: skills present in both resume and JD
      - missing: skills in the JD but not in the resume
    """
    resume_skills = extract_keywords(resume_text)
    jd_skills = extract_keywords(jd_text)

    if not jd_skills:
        return {"score": 0.0, "matched": [], "missing": [], "jd_skills": []}

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    score = round((len(matched) / len(jd_skills)) * 100, 1)

    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing),
        "jd_skills": sorted(jd_skills),
    }
