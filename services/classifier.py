from __future__ import annotations

from core.llm_client import invoke_text
from core.json_utils import parse_json_response
from services.prompts import CLASSIFY_SYSTEM, CLASSIFY_PROMPT

_EMPTY = {
    "experience": [],
    "projects": [],
    "skills": [],
    "certifications": [],
    "achievements": [],
}


def classify_chunks(jd_text: str, chunks: list[dict]) -> dict:
    """
    Classifies retrieved career-history chunks into resume sections.
    Returns a dict of raw (un-polished) facts per section.
    """
    if not chunks:
        return dict(_EMPTY)

    chunks_text = "\n---\n".join(c["text"] for c in chunks)
    prompt = CLASSIFY_PROMPT.format(jd_text=jd_text, chunks_text=chunks_text)
    raw = invoke_text(prompt, system=CLASSIFY_SYSTEM, temperature=0.1)
    parsed = parse_json_response(raw, default=dict(_EMPTY))

    for key in _EMPTY:
        parsed.setdefault(key, [])
    return parsed
