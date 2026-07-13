"""
The shared state object that flows through every LangGraph node.
TypedDict is used (rather than a Pydantic model) because that's what
LangGraph's StateGraph expects natively.
"""
from __future__ import annotations

from typing import TypedDict
from core.schemas import StaticProfile, FinalResume


class ResumeState(TypedDict, total=False):
    user_id: str
    jd_text: str
    static_profile: StaticProfile

    retrieved_chunks: list[dict]
    classified_facts: dict
    gaps: list[dict]
    generated_sections: dict

    final_resume: FinalResume

    # populated if a node hits a recoverable problem, surfaced in the UI
    warnings: list[str]
