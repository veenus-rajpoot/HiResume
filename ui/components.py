"""
Reusable, presentation-only Streamlit components. app.py wires these
together with state; these functions never touch the vector store or
LLM directly.
"""
from __future__ import annotations

import streamlit as st
from core.schemas import StaticProfile, FinalResume


def masthead():
    st.markdown(
        """
        <div class="masthead">
            <div class="eyebrow">AI Resume Studio</div>
            <h1>Draft a resume tailored to any job, from your real story</h1>
            <p>Keep one profile. Paste any job description. Get an ATS-friendly resume
            that always leads with your true background — never a blank page.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def profile_form(existing: StaticProfile) -> StaticProfile:
    st.markdown("#### Your profile")
    st.caption("These details are JD-independent and always appear on your resume.")

    full_name = st.text_input("Full name", value=existing.full_name)
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email", value=existing.email)
        college_name = st.text_input("College / University", value=existing.college_name)
        linkedin_url = st.text_input("LinkedIn URL", value=existing.linkedin_url)
        portfolio_url = st.text_input("Portfolio URL", value=existing.portfolio_url)
    with col2:
        phone = st.text_input("Phone", value=existing.phone)
        branch = st.text_input("Branch / Major", value=existing.branch)
        github_url = st.text_input("GitHub URL", value=existing.github_url)
        location = st.text_input("Location", value=existing.location)

    graduation_year = st.text_input("Graduation year", value=existing.graduation_year)
    other_links_raw = st.text_input(
        "Other platform links (comma-separated)",
        value=", ".join(existing.other_links),
        placeholder="e.g. LeetCode, Kaggle, personal blog",
    )
    summary_seed = st.text_area(
        "A few lines about yourself (optional, used as extra context)",
        value=existing.summary_seed,
        height=80,
    )

    other_links = [x.strip() for x in other_links_raw.split(",") if x.strip()]

    return StaticProfile(
        full_name=full_name, email=email, phone=phone, location=location,
        college_name=college_name, branch=branch, graduation_year=graduation_year,
        linkedin_url=linkedin_url, github_url=github_url, portfolio_url=portfolio_url,
        other_links=other_links, summary_seed=summary_seed,
    )


def match_meter(score: float):
    pct = max(0.0, min(100.0, score))
    st.markdown(
        f"""
        <div class="match-meter-wrap">
            <div class="match-meter-label">
                <span>ATS KEYWORD MATCH</span>
                <span class="match-meter-score">{pct:.1f}%</span>
            </div>
            <div class="match-meter-track">
                <div class="match-meter-fill" style="width:{pct}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def keyword_chips(matched: list[str], missing: list[str]):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Matched keywords**")
        chips = "".join(f'<span class="chip chip-matched">{k}</span>' for k in matched[:25])
        st.markdown(f'<div class="chip-row">{chips or "<em>none yet</em>"}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("**Missing keywords**")
        chips = "".join(f'<span class="chip chip-missing">{k}</span>' for k in missing[:25])
        st.markdown(f'<div class="chip-row">{chips or "<em>none — great coverage</em>"}</div>', unsafe_allow_html=True)


def resume_preview(resume: FinalResume):
    p, s = resume.profile, resume.sections
    html = ['<div class="resume-sheet">']
    html.append(f"<h1>{p.full_name or 'Your Name'}</h1>")

    contact_bits = [b for b in [p.email, p.phone, p.location] if b]
    if contact_bits:
        html.append(f'<div class="contact-line">{" &nbsp;|&nbsp; ".join(contact_bits)}</div>')
    link_bits = [b for b in [p.linkedin_url, p.github_url, p.portfolio_url, *p.other_links] if b]
    if link_bits:
        html.append(f'<div class="contact-line">{" &nbsp;|&nbsp; ".join(link_bits)}</div>')

    def bullet_section(title: str, items: list[str]):
        if not items:
            return ""
        lis = "".join(f"<li>{i}</li>" for i in items)
        return f"<h3>{title}</h3><ul>{lis}</ul>"

    if s.professional_summary:
        html.append(f"<h3>Professional Summary</h3><p>{s.professional_summary}</p>")
    if s.skills:
        html.append(f"<h3>Skills</h3><p>{', '.join(s.skills)}</p>")
    html.append(bullet_section("Experience", s.experience))
    html.append(bullet_section("Projects", s.projects))
    html.append(bullet_section("Education", s.education))
    html.append(bullet_section("Certifications", s.certifications))
    html.append(bullet_section("Achievements", s.achievements))
    html.append("</div>")

    st.markdown("\n".join(html), unsafe_allow_html=True)


def gap_transparency_note(notes: str):
    if notes:
        st.markdown(f'<div class="gap-note">ℹ️ {notes}</div>', unsafe_allow_html=True)
