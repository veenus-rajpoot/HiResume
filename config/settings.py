"""
Centralized configuration.

Every other module reads settings from here instead of calling
os.getenv() directly — this keeps the .env contract in one place.
"""
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv


# Load .env from the project root regardless of the current working directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _get_bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


class Settings:
    # --- Groq / LLM ---
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))

    # --- Embeddings ---
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # --- Storage paths (all relative to project root unless absolute) ---
    VECTOR_DB_DIR: Path = PROJECT_ROOT / os.getenv("VECTOR_DB_DIR", "data/vector_db")
    PROFILE_DIR: Path = PROJECT_ROOT / os.getenv("PROFILE_DIR", "data/profiles")
    OUTPUT_DIR: Path = PROJECT_ROOT / os.getenv("OUTPUT_DIR", "outputs")

    # --- RAG tuning ---
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "800"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    RETRIEVAL_TOP_K: int = int(os.getenv("RETRIEVAL_TOP_K", "12"))

    @classmethod
    def validate(cls) -> list[str]:
        """Returns a list of human-readable problems, empty if config is OK."""
        problems = []
        if not cls.GROQ_API_KEY:
            problems.append(
                "GROQ_API_KEY is missing. Add it to your .env file "
                "(get one at https://console.groq.com/keys)."
            )
        return problems

    @classmethod
    def ensure_dirs(cls) -> None:
        for d in (cls.VECTOR_DB_DIR, cls.PROFILE_DIR, cls.OUTPUT_DIR):
            d.mkdir(parents=True, exist_ok=True)


settings = Settings()
