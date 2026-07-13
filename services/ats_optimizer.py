"""
A lightweight, deterministic ATS score: keyword overlap between the JD
and the final resume text. Deliberately not LLM-based so the score is
stable, explainable, and free to compute.
"""
from __future__ import annotations

import re

_STOPWORDS = {
    "the", "and", "a", "an", "to", "of", "in", "for", "with", "on", "is",
    "are", "as", "at", "by", "or", "be", "will", "we", "you", "your",
    "our", "this", "that", "from", "have", "has", "should", "must",
    "years", "year", "experience", "strong", "ability", "team", "work",
    "job", "role", "responsibilities", "requirements", "preferred",
    "using", "including", "etc", "such", "who", "their", "into",
}

_WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9+.#-]{1,}")


def _keywords(text: str, min_len: int = 3) -> set[str]:
    words = (w.lower() for w in _WORD_RE.findall(text))
    return {w for w in words if len(w) >= min_len and w not in _STOPWORDS}


def score_resume(jd_text: str, resume_text: str) -> tuple[float, list[str], list[str]]:
    """
    Returns (score_percent, matched_keywords, missing_keywords).
    """
    jd_keywords = _keywords(jd_text)
    resume_keywords = _keywords(resume_text)

    if not jd_keywords:
        return 0.0, [], []

    matched = sorted(jd_keywords & resume_keywords)
    missing = sorted(jd_keywords - resume_keywords)
    score = round(100 * len(matched) / len(jd_keywords), 1)
    return score, matched, missing
