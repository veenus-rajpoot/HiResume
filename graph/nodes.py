"""
Each function here is one LangGraph node. Nodes only do I/O + call a
service function — the actual logic (prompts, parsing, scoring) lives
in core/ and services/, keeping nodes thin and easy to reorder/test.
"""
from __future__ import annotations

from core.vector_store import retrieve_relevant_chunks
from services.classifier import classify_chunks
from services.gap_analyzer import analyze_gaps
from services.section_generator import generate_sections
from services.resume_assembler import assemble_resume
from graph.state import ResumeState


def retrieve_node(state: ResumeState) -> ResumeState:
    chunks = retrieve_relevant_chunks(state["user_id"], state["jd_text"])
    warnings = list(state.get("warnings", []))
    if not chunks:
        warnings.append(
            "No stored career history matched this job description — the resume "
            "will rely primarily on your profile details. Consider uploading more "
            "detail about your experience/projects."
        )
    return {**state, "retrieved_chunks": chunks, "warnings": warnings}


def classify_node(state: ResumeState) -> ResumeState:
    classified = classify_chunks(state["jd_text"], state.get("retrieved_chunks", []))
    return {**state, "classified_facts": classified}


def gap_analysis_node(state: ResumeState) -> ResumeState:
    gaps = analyze_gaps(state["jd_text"], state.get("classified_facts", {}))
    return {**state, "gaps": gaps}


def generate_sections_node(state: ResumeState) -> ResumeState:
    generated = generate_sections(
        state["jd_text"], state.get("classified_facts", {}), state.get("gaps", [])
    )
    return {**state, "generated_sections": generated}


def assemble_node(state: ResumeState) -> ResumeState:
    final_resume = assemble_resume(
        jd_text=state["jd_text"],
        profile=state["static_profile"],
        generated=state.get("generated_sections", {}),
        gaps=state.get("gaps", []),
    )
    return {**state, "final_resume": final_resume}
