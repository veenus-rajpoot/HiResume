"""
Renders the FinalResume into a clean, single-column, ATS-friendly PDF.
Single column + standard fonts + no tables/text-boxes = maximum
compatibility with resume-parsing ATS software.
"""
from __future__ import annotations

import io

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, HRFlowable,
)

from core.schemas import FinalResume

_INK = "#1B2A4A"
_ACCENT = "#B8722E"
_MUTED = "#5A6472"


def _styles():
    base = getSampleStyleSheet()
    name = ParagraphStyle(
        "NameStyle", parent=base["Title"], fontName="Helvetica-Bold",
        fontSize=20, textColor=_INK, alignment=TA_LEFT, spaceAfter=2,
    )
    contact = ParagraphStyle(
        "ContactStyle", parent=base["Normal"], fontSize=9.5,
        textColor=_MUTED, spaceAfter=10,
    )
    heading = ParagraphStyle(
        "SectionHeading", parent=base["Heading2"], fontName="Helvetica-Bold",
        fontSize=11.5, textColor=_ACCENT, spaceBefore=12, spaceAfter=4,
        letterSpacing=0.6,
    )
    body = ParagraphStyle(
        "Body", parent=base["Normal"], fontSize=10, leading=14, textColor=_INK,
    )
    bullet = ParagraphStyle(
        "Bullet", parent=body, leftIndent=10,
    )
    return name, contact, heading, body, bullet


def build_resume_pdf(resume: FinalResume) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=LETTER,
        topMargin=0.55 * inch, bottomMargin=0.55 * inch,
        leftMargin=0.65 * inch, rightMargin=0.65 * inch,
    )
    name_style, contact_style, heading_style, body_style, bullet_style = _styles()

    p, s = resume.profile, resume.sections
    story = []

    story.append(Paragraph(p.full_name or "Your Name", name_style))
    contact_line = " &nbsp;|&nbsp; ".join(
        x for x in [p.email, p.phone, p.location] if x
    )
    if contact_line:
        story.append(Paragraph(contact_line, contact_style))
    links_line = " &nbsp;|&nbsp; ".join(
        x for x in [p.linkedin_url, p.github_url, p.portfolio_url, *p.other_links] if x
    )
    if links_line:
        story.append(Paragraph(links_line, contact_style))

    story.append(HRFlowable(width="100%", color=_ACCENT, thickness=1.1, spaceAfter=6))

    def add_bullets(title: str, items: list[str]):
        if not items:
            return
        story.append(Paragraph(title.upper(), heading_style))
        story.append(
            ListFlowable(
                [ListItem(Paragraph(item, bullet_style), leftIndent=10) for item in items],
                bulletType="bullet", start="•", leftIndent=10,
            )
        )

    if s.professional_summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
        story.append(Paragraph(s.professional_summary, body_style))

    if s.skills:
        story.append(Paragraph("SKILLS", heading_style))
        story.append(Paragraph(", ".join(s.skills), body_style))

    add_bullets("Experience", s.experience)
    add_bullets("Projects", s.projects)
    add_bullets("Education", s.education)
    add_bullets("Certifications", s.certifications)
    add_bullets("Achievements", s.achievements)

    story.append(Spacer(1, 0.1 * inch))

    doc.build(story)
    return buf.getvalue()
