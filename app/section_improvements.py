# app/section_improvements.py

def improve_sections(sections: dict, missing_skills: list) -> dict:
    improvements = {}

    # SKILLS
    if missing_skills:
        improvements["Skills"] = [
            f"If applicable, add {skill} to the skills section."
            for skill in missing_skills
        ]

    # PROJECTS
    if not sections.get("projects", "").strip():
        improvements["Projects"] = [
            "If applicable, add 1–2 projects demonstrating relevant technical skills."
        ]

    # EXPERIENCE
    if not sections.get("experience", "").strip():
        improvements["Experience"] = [
            "If applicable, include internships or work experience with measurable impact."
        ]

    # EDUCATION
    if not sections.get("education", "").strip():
        improvements["Education"] = [
            "Add education details including degree, institution, and graduation year."
        ]

    return improvements
