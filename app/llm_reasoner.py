# app/llm_reasoner.py

import os
import logging

USE_LLM = False
model = None

try:
    import google.generativeai as genai

    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-pro")
        USE_LLM = True
except Exception as e:
    USE_LLM = False


SYSTEM_INSTRUCTIONS = """
You are explaining a resume–job match result.

STRICT RULES:
- Do NOT invent skills, tools, experience, or metrics.
- Use ONLY information explicitly present in the resume or job description.
- Suggestions must be phrased conditionally using "if applicable".
- Do NOT exaggerate or assume missing information.
"""


def _format_suggestions(suggestions: list) -> str:
    if not suggestions:
        return "No suggestions."
    return "\n".join(f"- {s}" for s in suggestions)


def _fallback_explanation(
    decision: str,
    score: int,
    suggestions: list
) -> str:
    """
    Deterministic, safe explanation (NO LLM).
    """
    explanation = f"""
Decision: {decision}
Score: {score}/100

Reason:
The decision was computed using semantic similarity between the resume
and the job description.

Suggestions:
{_format_suggestions(suggestions)}
"""
    return explanation.strip()


def generate_reasoning(
    decision: str,
    score: int,
    resume_text: str,
    job_text: str,
    base_suggestions: list
) -> str:

    # ---------------- SILENT FALLBACK ----------------
    if not USE_LLM or model is None:
        return _fallback_explanation(decision, score, base_suggestions)

    # ---------------- LLM MODE ----------------
    prompt = f"""
{SYSTEM_INSTRUCTIONS}

Decision: {decision}
Score: {score}/100

Resume Content:
{resume_text}

Job Description:
{job_text}

Suggestions:
{_format_suggestions(base_suggestions)}

Explain the decision clearly and safely.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception:
        logging.exception("LLM generation failed")
        return _fallback_explanation(decision, score, base_suggestions)
