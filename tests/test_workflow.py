"""
Lightweight tests for the deterministic parts of the pipeline (no Groq
API calls required). Run with: pytest tests/
"""
from core.chunking import chunk_text
from core.json_utils import parse_json_response
from services.ats_optimizer import score_resume
from services.resume_assembler import assemble_resume
from core.schemas import StaticProfile


def test_chunk_text_basic():
    chunks = chunk_text("A" * 2000, source="unit_test")
    assert len(chunks) > 1
    assert all(c["source"] == "unit_test" for c in chunks)


def test_chunk_text_empty():
    assert chunk_text("") == []


def test_parse_json_response_with_fences():
    raw = '```json\n{"a": 1}\n```'
    assert parse_json_response(raw) == {"a": 1}


def test_parse_json_response_invalid_falls_back():
    assert parse_json_response("not json at all", default={"x": []}) == {"x": []}


def test_score_resume_basic():
    jd = "Looking for a Python developer with experience in FastAPI and Docker."
    resume = "Built backend services in Python using FastAPI and deployed with Docker."
    score, matched, missing = score_resume(jd, resume)
    assert score > 50
    assert "python" in matched
    assert "fastapi" in matched


def test_assemble_resume_includes_static_profile_even_with_no_generated_content():
    profile = StaticProfile(
        full_name="Jane Doe", email="jane@example.com",
        college_name="State University", branch="Computer Science",
        graduation_year="2025", linkedin_url="linkedin.com/in/janedoe",
    )
    resume = assemble_resume(
        jd_text="Looking for a data engineer with Spark experience.",
        profile=profile, generated={}, gaps=[],
    )
    assert resume.profile.full_name == "Jane Doe"
    assert any("State University" in e for e in resume.sections.education)
