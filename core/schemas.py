"""
Shared data models used across the app (UI, graph nodes, services).
Keeping these in one place avoids circular imports and keeps every
module talking about "a profile" or "a resume" in the same shape.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class StaticProfile(BaseModel):
    """
    Information that is JD-independent and must ALWAYS appear on the
    resume verbatim (or lightly formatted), regardless of retrieval.
    """
    full_name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    college_name: str = ""
    branch: str = ""
    graduation_year: str = ""
    linkedin_url: str = ""
    github_url: str = ""
    portfolio_url: str = ""
    other_links: list[str] = Field(default_factory=list)
    summary_seed: str = ""  # a few free-text lines the user wrote about themselves

    def is_complete_enough(self) -> bool:
        return bool(self.full_name and (self.email or self.phone))


class RetrievedChunk(BaseModel):
    text: str
    source: str = ""
    score: float = 0.0


class GapItem(BaseModel):
    requirement: str
    covered: bool
    closest_match: str = ""  # best transferable evidence found in the profile, if any


class ResumeSections(BaseModel):
    professional_summary: str = ""
    skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    achievements: list[str] = Field(default_factory=list)


class FinalResume(BaseModel):
    profile: StaticProfile
    sections: ResumeSections
    ats_score: float = 0.0
    matched_keywords: list[str] = Field(default_factory=list)
    missing_keywords: list[str] = Field(default_factory=list)
    notes: str = ""  # transparency note about any gap-filling that happened
