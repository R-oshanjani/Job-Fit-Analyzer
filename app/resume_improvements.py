# app/resume_improvements.py

def generate_resume_improvements(missing_skills: list) -> list:
    improvements = []

    for skill in missing_skills:
        improvements.append(
            f"If applicable, add projects, coursework, or experience related to {skill}."
        )

    return improvements
