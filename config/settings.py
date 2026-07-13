"""
Centralized configuration.

Works in both:
1. Local development (.env)
2. Streamlit Cloud (st.secrets)
"""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


# ------------------------------------------------------------------
# Load local .env (ignored on Streamlit Cloud if secrets are provided)
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_setting(name: str, default=None):
    """
    Read configuration in the following order:

    1. Streamlit Secrets (deployment)
    2. .env / environment variables (local)
    3. Default value
    """
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return os.getenv(name, default)


def _get_bool(name: str, default: bool) -> bool:
    val = get_setting(name)
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------
    GROQ_API_KEY: str = get_setting("GROQ_API_KEY", "")
    GROQ_MODEL: str = get_setting(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )
    LLM_TEMPERATURE: float = float(
        get_setting("LLM_TEMPERATURE", "0.3")
    )

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------
    EMBEDDING_MODEL: str = get_setting(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    # ------------------------------------------------------------------
    # Storage
    # ------------------------------------------------------------------
    VECTOR_DB_DIR: Path = PROJECT_ROOT / get_setting(
        "VECTOR_DB_DIR",
        "data/vector_db"
    )

    PROFILE_DIR: Path = PROJECT_ROOT / get_setting(
        "PROFILE_DIR",
        "data/profiles"
    )

    OUTPUT_DIR: Path = PROJECT_ROOT / get_setting(
        "OUTPUT_DIR",
        "outputs"
    )

    # ------------------------------------------------------------------
    # RAG
    # ------------------------------------------------------------------
    CHUNK_SIZE: int = int(
        get_setting("CHUNK_SIZE", "800")
    )

    CHUNK_OVERLAP: int = int(
        get_setting("CHUNK_OVERLAP", "120")
    )

    RETRIEVAL_TOP_K: int = int(
        get_setting("RETRIEVAL_TOP_K", "12")
    )

    @classmethod
    def validate(cls) -> list[str]:
        problems = []

        if not cls.GROQ_API_KEY:
            problems.append(
                "GROQ_API_KEY is missing. "
                "Add it to Streamlit Secrets (deployment) "
                "or .env (local development)."
            )

        return problems

    @classmethod
    def ensure_dirs(cls):
        for d in (
            cls.VECTOR_DB_DIR,
            cls.PROFILE_DIR,
            cls.OUTPUT_DIR,
        ):
            d.mkdir(parents=True, exist_ok=True)


settings = Settings()