"""
Splits long career-history text into overlapping chunks suitable for
embedding. Kept as its own module so chunk strategy can evolve
independently of loading / storing.
"""
from __future__ import annotations

from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings


def chunk_text(text: str, source: str = "uploaded_document") -> list[dict]:
    """
    Returns a list of {"text": ..., "source": ...} dicts ready to be
    embedded and stored in the vector database.
    """
    if not text or not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    pieces = splitter.split_text(text)
    return [{"text": piece, "source": source} for piece in pieces if piece.strip()]
