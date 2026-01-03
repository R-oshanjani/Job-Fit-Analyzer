# app/semantic_matcher.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.memory import memory

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def _get_embedding(text: str):
    cached = memory.get_embedding(text)
    if cached is not None:
        return cached

    embedding = model.encode(text)
    memory.store_embedding(text, embedding)
    return embedding


def semantic_similarity(resume_text: str, job_text: str) -> float:
    resume_emb = _get_embedding(resume_text)
    job_emb = _get_embedding(job_text)

    return float(
        cosine_similarity([resume_emb], [job_emb])[0][0]
    )
