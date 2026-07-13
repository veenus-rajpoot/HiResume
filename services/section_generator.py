from __future__ import annotations

import json

from core.llm_client import invoke_text
from core.json_utils import parse_json_response
from services.prompts import GENERATE_SYSTEM, GENERATE_PROMPT

_EMPTY = {
    "professional_summary": "",
    "skills": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "achievements": [],
}


def generate_sections(jd_text: str, classified: dict, gaps: list[dict]) -> dict:
    """
    Turns raw classified facts + gap analysis into polished, ATS-optimized
    resume section content. This is the step that ensures the resume is
    never left blank/incomplete even when the JD asks for things the
    candidate hasn't directly done — it reframes the closest transferable
    evidence instead.
    """
    classified_text = json.dumps(classified, indent=2)
    gap_text = json.dumps(gaps, indent=2)

    prompt = GENERATE_PROMPT.format(
        jd_text=jd_text, classified_text=classified_text, gap_text=gap_text
    )
    raw = invoke_text(prompt, system=GENERATE_SYSTEM, temperature=0.4)
    parsed = parse_json_response(raw, default=dict(_EMPTY))

    for key in _EMPTY:
        parsed.setdefault(key, _EMPTY[key])
    return parsed
