from __future__ import annotations

from core.schemas import FinalResume


def resume_to_markdown(resume: FinalResume) -> str:
    p = resume.profile
    s = resume.sections
    lines: list[str] = []

    lines.append(f"# {p.full_name or 'Your Name'}")
    contact_bits = [b for b in [p.email, p.phone, p.location] if b]
    if contact_bits:
        lines.append(" | ".join(contact_bits))
    link_bits = [b for b in [p.linkedin_url, p.github_url, p.portfolio_url, *p.other_links] if b]
    if link_bits:
        lines.append(" | ".join(link_bits))
    lines.append("")

    if s.professional_summary:
        lines += ["## Professional Summary", s.professional_summary, ""]

    if s.skills:
        lines += ["## Skills", ", ".join(s.skills), ""]

    if s.experience:
        lines.append("## Experience")
        lines += [f"- {b}" for b in s.experience]
        lines.append("")

    if s.projects:
        lines.append("## Projects")
        lines += [f"- {b}" for b in s.projects]
        lines.append("")

    if s.education:
        lines.append("## Education")
        lines += [f"- {b}" for b in s.education]
        lines.append("")

    if s.certifications:
        lines.append("## Certifications")
        lines += [f"- {b}" for b in s.certifications]
        lines.append("")

    if s.achievements:
        lines.append("## Achievements")
        lines += [f"- {b}" for b in s.achievements]
        lines.append("")

    return "\n".join(lines).strip() + "\n"
