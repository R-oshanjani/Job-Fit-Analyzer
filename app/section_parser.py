# app/section_parser.py

import re

SECTION_HEADERS = {
    "skills": ["skills", "technical skills"],
    "projects": ["projects"],
    "experience": ["experience", "work experience", "internship"],
    "education": ["education"]
}


def split_sections(text: str) -> dict:
    text = text.lower()
    sections = {key: "" for key in SECTION_HEADERS}

    current = None
    for line in text.splitlines():
        line_clean = line.strip()

        for section, headers in SECTION_HEADERS.items():
            if any(line_clean.startswith(h) for h in headers):
                current = section
                break

        if current:
            sections[current] += line + "\n"

    return sections
