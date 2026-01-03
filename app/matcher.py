# app/matcher.py

def semantic_match(resume_skills, job_skills):
    """
    Simple semantic matcher (rule-based placeholder).
    Returns list of matched skill strings.
    """
    return [skill for skill in resume_skills if skill in job_skills]
