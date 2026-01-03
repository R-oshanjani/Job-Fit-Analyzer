# streamlit_app.py

import streamlit as st
import pandas as pd
from pypdf import PdfReader

from app.agent import evaluate_resume_job
from app.history import HistoryStore


# ================= FILE HELPERS =================
def read_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_text(file) -> str:
    return file.read().decode("utf-8", errors="ignore")


def resolve_input(uploaded_file, text_input) -> str:
    """
    Priority:
    1. Uploaded file
    2. Text area input
    """
    if uploaded_file:
        if uploaded_file.name.lower().endswith(".pdf"):
            return read_pdf(uploaded_file)
        elif uploaded_file.name.lower().endswith(".txt"):
            return read_text(uploaded_file)
    return text_input.strip()


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Resume–Job Match & ATS Analyzer",
    layout="centered"
)

st.title("🧠 Resume–Job Match & ATS Analyzer")
st.write(
    """
This system evaluates your resume against a job description using:
- Semantic similarity
- Skill gap analysis
- ATS-style scoring
- Section-wise resume improvements

No fabricated experience. No hallucinations.
"""
)

st.divider()

# ================= META INPUTS =================
job_id = st.text_input("Job ID", "job-001")

force_recheck = st.checkbox(
    "Force re-evaluation (ignore previous result)",
    value=False
)

# ================= RESUME INPUT =================
st.subheader("📄 Resume Input")

resume_file = st.file_uploader(
    "Upload Resume (.pdf or .txt)",
    type=["pdf", "txt"],
    key="resume_file"
)

resume_text = st.text_area(
    "Or paste resume text",
    height=160,
    placeholder="Paste resume text here if not uploading a file..."
)

# ================= JOB INPUT =================
st.subheader("💼 Job Description Input")

job_file = st.file_uploader(
    "Upload Job Description (.pdf or .txt)",
    type=["pdf", "txt"],
    key="job_file"
)

job_text = st.text_area(
    "Or paste job description text",
    height=160,
    placeholder="Paste job description text here if not uploading a file..."
)

# ================= ACTION =================
if st.button("Analyze Resume"):
    resume_content = resolve_input(resume_file, resume_text)
    job_content = resolve_input(job_file, job_text)

    if not resume_content or not job_content:
        st.warning("Please provide BOTH resume and job description.")
    else:
        result = evaluate_resume_job(
            resume_text=resume_content,
            job_text=job_content,
            job_id=job_id,
            force_recheck=force_recheck
        )

        # ================= RESULTS =================
        st.divider()
        st.subheader("📊 Match Decision")

        if result["decision"] == "MATCH":
            st.success("✅ MATCH")
        else:
            st.error("❌ NOT MATCH")

        st.subheader("📈 Semantic Match Score")
        st.write(f"{result['score']} / 100")

        # ================= ATS SCORE =================
        st.subheader("🤖 ATS Score")
        st.metric("Total ATS Score", result["ats"]["total_score"])

        st.subheader("🔍 ATS Breakdown")
        for k, v in result["ats"]["breakdown"].items():
            st.write(f"**{k}** : {v}")

        # ================= MISSING SKILLS =================
        st.subheader("❗ Missing Skills (from Job Description)")
        if result["missing_skills"]:
            st.write(", ".join(result["missing_skills"]))
        else:
            st.success("No critical skills missing.")

        # ================= SECTION-WISE IMPROVEMENTS =================
        st.subheader("🧩 Section-wise Resume Improvements")

        if result["section_improvements"]:
            for section, tips in result["section_improvements"].items():
                st.markdown(f"**{section}**")
                for tip in tips:
                    st.write("•", tip)
        else:
            st.success("All major resume sections are well covered.")

        # ================= EXPLANATION =================
        st.subheader("🧠 Explanation")
        st.write(result["explanation"])

# ================= HISTORY =================
st.divider()
st.subheader("📜 Evaluation History")

history = HistoryStore()
rows = history.fetch_all()

if rows:
    df = pd.DataFrame(
        rows,
        columns=["Job ID", "Decision", "Score", "Timestamp"]
    )
    st.dataframe(df, use_container_width=True)
else:
    st.info("No evaluations recorded yet.")
