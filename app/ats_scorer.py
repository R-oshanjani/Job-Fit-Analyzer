# app/ats_scorer.py

from app.resume_parser import extract_skills
from app.semantic_matcher import semantic_similarity
from app.section_parser import split_sections


def ats_score(resume_text: str, job_text: str) -> dict:
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    # Skill match
    skill_match_ratio = len(resume_skills & job_skills) / max(len(job_skills), 1)
    skill_score = skill_match_ratio * 40

    # Semantic similarity
    semantic_score = semantic_similarity(resume_text, job_text) * 30

    # Section coverage
    sections = split_sections(resume_text)
    filled_sections = sum(1 for v in sections.values() if v.strip())
    section_score = (filled_sections / len(sections)) * 20

    # Keyword density
    keyword_density = sum(resume_text.lower().count(skill) for skill in job_skills)
    keyword_score = min(keyword_density, 10)

    total = round(skill_score + semantic_score + section_score + keyword_score)

    return {
        "total_score": total,
        "breakdown": {
            "Skill Match (40%)": round(skill_score, 1),
            "Semantic Similarity (30%)": round(semantic_score, 1),
            "Section Coverage (20%)": round(section_score, 1),
            "Keyword Density (10%)": round(keyword_score, 1)
        }
    }
