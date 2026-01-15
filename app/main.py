import sys
import os
sys.path.append(os.path.abspath("."))

import streamlit as st
import pandas as pd

from models.match_engine import match_jobs
from nlp.resume_parser import extract_skills_from_resume
from app.chatbot import teach_skill

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="SkillPulse AI",
    page_icon="🚀",
    layout="centered"
)

# -------------------- SESSION STATE --------------------
if "results" not in st.session_state:
    st.session_state.results = None

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "lesson" not in st.session_state:
    st.session_state.lesson = None

# -------------------- HEADER --------------------
st.markdown(
    """
    <h1 style='text-align:center;'>🚀 SkillPulse AI</h1>
    <p style='text-align:center;color:gray;'>
    AI Job Matching • Skill Gap Analysis • AI Learning Assistant
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------- SKILL INPUT --------------------
st.subheader("🎯 Enter Your Skills")

user_skills = st.text_input(
    "Comma-separated skills",
    placeholder="e.g. python, machine learning, sql"
)

if st.button("🔍 Analyze Job Matches"):
    skills_list = [s.strip() for s in user_skills.split(",") if s.strip()]
    st.session_state.results = match_jobs(skills_list)

# -------------------- RESUME UPLOAD --------------------
st.divider()
st.subheader("📄 Upload Resume (PDF)")

uploaded_resume = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

if uploaded_resume:
    with st.spinner("Analyzing resume..."):
        st.session_state.resume_skills = extract_skills_from_resume(uploaded_resume)

    st.success("Resume analyzed successfully!")

    if st.session_state.resume_skills:
        st.markdown(
            f"**Extracted skills:** `{', '.join(st.session_state.resume_skills)}`"
        )

# -------------------- JOB RESULTS --------------------
if st.session_state.results is not None:

    results = st.session_state.results

    if results.empty:
        st.warning("No strong matches found. Try adding more skills.")
    else:
        st.subheader("📊 Job Match Results")
        st.dataframe(results, use_container_width=True)

        # -------------------- AI TEACHING --------------------
        st.divider()
        st.subheader("🧠 Learn Missing Skills with AI")

        for idx, row in results.iterrows():
            if row["missing_skills"]:
                with st.expander(f"📌 {row['title']} ({row['match_score']}%)"):
                    skills = [s.strip() for s in row["missing_skills"].split(",")]

                    selected = st.selectbox(
                        "Choose a skill to learn",
                        skills,
                        key=f"skill_{idx}"
                    )

                    if st.button("Teach me", key=f"teach_{idx}"):
                        with st.spinner("AI is preparing your lesson..."):
                            st.session_state.lesson = teach_skill(
                                selected,
                                row["title"]
                            )

        if st.session_state.lesson:
            st.markdown("### 📘 Your AI Lesson")
            st.markdown(st.session_state.lesson)

# -------------------- FOOTER --------------------
st.divider()
st.caption("SkillPulse AI • Built for learning-driven careers")
