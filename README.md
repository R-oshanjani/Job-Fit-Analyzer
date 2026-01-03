# Job-Fit-Analyzer
# Resume–Job Match & ATS Analyzer

A transparent, rule-based resume–job matching system that combines
semantic similarity, ATS-style scoring, skill gap analysis, and
section-wise resume improvement suggestions — without fabricating
experience.

This project is designed to be **explainable**, **safe**, and
**production-oriented**, unlike typical black-box “AI resume tools”.

---

## 🚀 Features

### 1. Resume–Job Semantic Matching
- Uses sentence embeddings to measure semantic similarity
- Cached embeddings to avoid recomputation and reduce cost
- Produces a clear match score (0–100)

### 2. ATS-Style Scoring (Explainable)
Final ATS score is calculated using a weighted breakdown:

| Component | Weight |
|--------|--------|
| Skill Match | 40% |
| Semantic Similarity | 30% |
| Section Coverage | 20% |
| Keyword Density | 10% |

Each component score is shown explicitly.

---

### 3. Missing Skills Detection
- Extracts skills from resume and job description
- Computes real gaps (Job − Resume)
- No hallucination, no guessing

---

### 4. Section-wise Resume Improvement
Provides **safe, conditional suggestions** for:
- Skills
- Projects
- Experience
- Education

All suggestions use **“If applicable…”** phrasing to avoid resume fraud.

---

### 5. File Upload + Text Input
Users can:
- Upload `.pdf` or `.txt` files
- Or paste resume / job description text
- Or mix both

File input takes priority if provided.

---

### 6. History Dashboard
- Stores past evaluations in SQLite
- Displays job ID, decision, ATS score, and timestamp
- Enables traceability and debugging

---

### 7. Safe LLM Integration (Optional)
- Uses Gemini only if API key is available
- Automatically falls back to deterministic explanations
- Never blocks the system if LLM is unavailable

---

## 🧠 Design Principles

- **Explainability over hype**
- **Rule-based safety over blind prompting**
- **No fabricated skills or experience**
- **Deterministic outputs where possible**
- **Modular, testable architecture**

---

## 🗂️ Project Structure

