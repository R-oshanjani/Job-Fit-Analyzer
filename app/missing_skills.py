# app/missing_skills.py

from app.resume_parser import extract_skills


def find_missing_skills(resume_text: str, job_text: str) -> list:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)
    return sorted(job_skills - resume_skills)
