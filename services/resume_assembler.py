from __future__ import annotations

from core.schemas import StaticProfile, ResumeSections, FinalResume
from services.ats_optimizer import score_resume


def _flatten_for_scoring(profile: StaticProfile, sections: ResumeSections) -> str:
    parts = [
        profile.summary_seed,
        sections.professional_summary,
        ", ".join(sections.skills),
        "\n".join(sections.experience),
        "\n".join(sections.projects),
        "\n".join(sections.education),
        "\n".join(sections.certifications),
        "\n".join(sections.achievements),
    ]
    return "\n".join(p for p in parts if p)


def assemble_resume(
    jd_text: str,
    profile: StaticProfile,
    generated: dict,
    gaps: list[dict],
) -> FinalResume:
    """
    Combines the always-present static profile with the JD-tailored
    generated content into one final resume object, and attaches an
    ATS score. Guarantees the profile fields (name, college, links...)
    are present regardless of what the RAG/generation steps produced.
    """
    education_lines = []
    if profile.college_name:
        line = profile.college_name
        if profile.branch:
            line += f" — {profile.branch}"
        if profile.graduation_year:
            line += f" ({profile.graduation_year})"
        education_lines.append(line)

    sections = ResumeSections(
        professional_summary=generated.get("professional_summary", "").strip(),
        skills=generated.get("skills", []),
        experience=generated.get("experience", []),
        projects=generated.get("projects", []),
        education=education_lines,
        certifications=generated.get("certifications", []),
        achievements=generated.get("achievements", []),
    )

    resume_text = _flatten_for_scoring(profile, sections)
    score, matched, missing = score_resume(jd_text, resume_text)

    uncovered = [g["requirement"] for g in gaps if not g.get("covered", True)]
    notes = ""
    if uncovered:
        notes = (
            "The candidate has no direct experience for: "
            + ", ".join(uncovered)
            + ". These were addressed by highlighting the closest transferable "
            "skills/projects rather than left blank."
        )

    return FinalResume(
        profile=profile,
        sections=sections,
        ats_score=score,
        matched_keywords=matched,
        missing_keywords=missing,
        notes=notes,
    )
