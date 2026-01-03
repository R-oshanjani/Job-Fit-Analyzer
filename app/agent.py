# app/agent.py

from app.semantic_matcher import semantic_similarity
from app.missing_skills import find_missing_skills
from app.resume_improvements import generate_resume_improvements
from app.section_parser import split_sections
from app.section_improvements import improve_sections
from app.ats_scorer import ats_score
from app.llm_reasoner import generate_reasoning
from app.history import HistoryStore

history = HistoryStore()


def evaluate_resume_job(resume_text, job_text, job_id, force_recheck=False):
    similarity = semantic_similarity(resume_text, job_text)
    score = int(similarity * 100)

    missing_skills = find_missing_skills(resume_text, job_text)
    base_improvements = generate_resume_improvements(missing_skills)

    sections = split_sections(resume_text)
    section_improvements = improve_sections(sections, missing_skills)

    ats = ats_score(resume_text, job_text)

    decision = "MATCH" if score >= 70 else "NOT MATCH"
    reasons = ["Semantic alignment score used for decision"]

    explanation = generate_reasoning(
        decision, score, resume_text, job_text, base_improvements
    )

    history.log(job_id, decision, ats["total_score"])

    return {
        "decision": decision,
        "score": score,
        "ats": ats,
        "missing_skills": missing_skills,
        "section_improvements": section_improvements,
        "explanation": explanation
    }
