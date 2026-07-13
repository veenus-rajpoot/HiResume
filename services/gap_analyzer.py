from __future__ import annotations

import json

from core.llm_client import invoke_text
from core.json_utils import parse_json_response
from services.prompts import GAP_ANALYSIS_SYSTEM, GAP_ANALYSIS_PROMPT


def analyze_gaps(jd_text: str, classified: dict) -> list[dict]:
    """
    Returns a list of {"requirement", "covered", "closest_match"} dicts.
    This is what lets the generator honestly reframe transferable skills
    instead of leaving a section blank when the JD asks for something
    the candidate hasn't directly done.
    """
    classified_text = json.dumps(classified, indent=2)
    prompt = GAP_ANALYSIS_PROMPT.format(jd_text=jd_text, classified_text=classified_text)
    raw = invoke_text(prompt, system=GAP_ANALYSIS_SYSTEM, temperature=0.1)
    parsed = parse_json_response(raw, default={"requirements": []})
    return parsed.get("requirements", [])
