# app/safe_rewrite.py

from app.resume_parser import extract_facts


class UnsafeRewriteError(Exception):
    pass


def validate_rewrite(original_facts: dict, rewritten_text: str):
    new_facts = extract_facts(rewritten_text)

    for key in original_facts:
        if not new_facts[key].issubset(original_facts[key]):
            raise UnsafeRewriteError(
                f"New {key} introduced: {new_facts[key] - original_facts[key]}"
            )


def safe_rewrite_resume(
    resume_text: str,
    rewrite_fn
) -> str:
    """
    rewrite_fn: callable that performs the rewrite (LLM or rule-based)
    """

    original_facts = extract_facts(resume_text)

    rewritten = rewrite_fn(resume_text)

    validate_rewrite(original_facts, rewritten)

    return rewritten
