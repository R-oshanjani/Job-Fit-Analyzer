# app/resume_parser.py

SKILL_KEYWORDS = {
    "python", "java", "sql", "aws", "docker", "git",
    "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "scikit-learn", "tensorflow",
    "flask", "fastapi", "linux"
}


def extract_skills(text: str) -> set:
    text = text.lower()
    return {skill for skill in SKILL_KEYWORDS if skill in text}
