"""
Wires the nodes into a linear LangGraph pipeline:

  retrieve -> classify -> gap_analysis -> generate_sections -> assemble -> END

Exposed as a single `run_resume_pipeline()` function so the UI layer
never has to know about LangGraph internals.
"""
from __future__ import annotations

from functools import lru_cache
from langgraph.graph import StateGraph, END

from graph.state import ResumeState
from graph.nodes import (
    retrieve_node,
    classify_node,
    gap_analysis_node,
    generate_sections_node,
    assemble_node,
)
from core.schemas import StaticProfile, FinalResume


@lru_cache(maxsize=1)
def _compiled_graph():
    graph = StateGraph(ResumeState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("classify", classify_node)
    graph.add_node("gap_analysis", gap_analysis_node)
    graph.add_node("generate_sections", generate_sections_node)
    graph.add_node("assemble", assemble_node)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "classify")
    graph.add_edge("classify", "gap_analysis")
    graph.add_edge("gap_analysis", "generate_sections")
    graph.add_edge("generate_sections", "assemble")
    graph.add_edge("assemble", END)

    return graph.compile()


def run_resume_pipeline(
    user_id: str, jd_text: str, static_profile: StaticProfile
) -> tuple[FinalResume, list[str]]:
    """
    Runs the full pipeline and returns (final_resume, warnings).
    """
    initial_state: ResumeState = {
        "user_id": user_id,
        "jd_text": jd_text,
        "static_profile": static_profile,
        "warnings": [],
    }
    result: ResumeState = _compiled_graph().invoke(initial_state)
    return result["final_resume"], result.get("warnings", [])
