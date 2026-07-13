"""
AI Resume Studio — Streamlit entry point.

Run with:
    streamlit run app.py

This file only wires UI <-> services/graph together. All real logic
lives in core/, services/, and graph/.
"""
from __future__ import annotations

import streamlit as st
from config.settings import settings
from core.schemas import StaticProfile
from services.ingestion import ingest_uploaded_files, ingest_pasted_text
from services.profile_store import save_profile, load_profile
from services.markdown_exporter import resume_to_markdown
from services.pdf_exporter import build_resume_pdf
from graph.workflow import run_resume_pipeline
from ui.styles import CUSTOM_CSS
from ui.components import (
    masthead, profile_form, match_meter, keyword_chips,
    resume_preview, gap_transparency_note,
)

st.set_page_config(page_title="AI Resume Studio", page_icon="🖋️", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------- session --
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "final_resume" not in st.session_state:
    st.session_state.final_resume = None
if "warnings" not in st.session_state:
    st.session_state.warnings = []

masthead()

config_problems = settings.validate()
if config_problems:
    for p in config_problems:
        st.error(p)
    st.stop()

# --------------------------------------------------------------- sidebar --
with st.sidebar:
    st.markdown("### 1 — Identify yourself")
    user_id = st.text_input(
        "Profile ID (any unique name/email)",
        value=st.session_state.user_id,
        help="Used to keep your uploaded background separate from other users.",
    )
    st.session_state.user_id = user_id.strip()

    if st.session_state.user_id:
        existing_profile = load_profile(st.session_state.user_id)

        st.markdown("---")
        updated_profile = profile_form(existing_profile)
        if st.button("💾 Save profile", use_container_width=True):
            save_profile(st.session_state.user_id, updated_profile)
            st.success("Profile saved.")

        st.markdown("---")
        st.markdown("### 2 — Add your career history")
        st.caption("Upload resumes/notes or paste free text: past roles, projects, "
                    "achievements, skills. This gets chunked & embedded for retrieval.")
        uploaded = st.file_uploader(
            "Upload files (.pdf, .docx, .txt, .md)",
            type=["pdf", "docx", "txt", "md"],
            accept_multiple_files=True,
        )
        pasted = st.text_area("...or paste text directly", height=120)
        replace_existing = st.checkbox(
            "Replace previously indexed data", value=False,
            help="Turn on if you're re-uploading a corrected version of your background."
        )

        if st.button("📥 Index my background", use_container_width=True):
            with st.spinner("Chunking and embedding your background..."):
                count = 0
                if uploaded:
                    files = [(f.name, f.read()) for f in uploaded]
                    count += ingest_uploaded_files(
                        st.session_state.user_id, files, replace=replace_existing
                    )
                if pasted.strip():
                    count += ingest_pasted_text(
                        st.session_state.user_id, pasted,
                        replace=replace_existing and not uploaded,
                    )
                if count:
                    st.success(f"Indexed {count} chunks.")
                else:
                    st.warning("Nothing to index — upload a file or paste some text.")
    else:
        st.info("Enter a profile ID above to begin.")

# ----------------------------------------------------------------- main --
if not st.session_state.user_id:
    st.stop()

st.markdown("### 3 — Paste the job description")
jd_text = st.text_area(
    "Job description",
    height=220,
    placeholder="Paste the full job description here...",
)

generate = st.button("✨ Generate tailored resume", type="primary")

if generate:
    if not jd_text.strip():
        st.warning("Paste a job description first.")
    else:
        profile = load_profile(st.session_state.user_id)
        if not profile.is_complete_enough():
            st.warning(
                "Your profile is missing basics (name/contact) — save your profile "
                "in the sidebar first for the best result."
            )
        with st.spinner("Retrieving relevant background, analyzing gaps, and drafting your resume..."):
            try:
                final_resume, warnings = run_resume_pipeline(
                    st.session_state.user_id, jd_text, profile
                )
                st.session_state.final_resume = final_resume
                st.session_state.warnings = warnings
            except Exception as e:
                st.error(f"Something went wrong generating your resume: {e}")

st.markdown('<hr class="desk-rule">', unsafe_allow_html=True)

resume = st.session_state.final_resume
if resume:
    for w in st.session_state.warnings:
        st.info(w)

    tab_preview, tab_ats, tab_download = st.tabs(["📄 Preview", "🎯 ATS Match", "⬇️ Download"])

    with tab_preview:
        gap_transparency_note(resume.notes)
        resume_preview(resume)

    with tab_ats:
        st.markdown('<div class="desk-card">', unsafe_allow_html=True)
        match_meter(resume.ats_score)
        st.markdown("</div>", unsafe_allow_html=True)
        keyword_chips(resume.matched_keywords, resume.missing_keywords)

    with tab_download:
        md_text = resume_to_markdown(resume)
        pdf_bytes = build_resume_pdf(resume)
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "Download as PDF", data=pdf_bytes,
                file_name=f"{(resume.profile.full_name or 'resume').replace(' ', '_')}_resume.pdf",
                mime="application/pdf", use_container_width=True,
            )
        with col2:
            st.download_button(
                "Download as Markdown", data=md_text,
                file_name=f"{(resume.profile.full_name or 'resume').replace(' ', '_')}_resume.md",
                mime="text/markdown", use_container_width=True,
            )
else:
    st.caption("Your generated resume will appear here.")
