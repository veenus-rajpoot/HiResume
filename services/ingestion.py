"""
Handles turning uploaded files / pasted text into indexed vector-store
chunks. This runs once per upload, separately from the per-JD LangGraph
pipeline (retrieval happens many times against data indexed once).
"""
from __future__ import annotations

from core.document_loader import extract_text
from core.chunking import chunk_text
from core.vector_store import index_chunks, reset_user_data


def ingest_uploaded_files(user_id: str, files: list[tuple[str, bytes]], replace: bool = False) -> int:
    """
    files: list of (filename, file_bytes) tuples.
    Returns the total number of chunks indexed.
    """
    if replace:
        reset_user_data(user_id)

    total = 0
    for filename, file_bytes in files:
        text = extract_text(filename, file_bytes)
        chunks = chunk_text(text, source=filename)
        total += index_chunks(user_id, chunks)
    return total


def ingest_pasted_text(user_id: str, text: str, source: str = "pasted_text", replace: bool = False) -> int:
    if replace:
        reset_user_data(user_id)
    chunks = chunk_text(text, source=source)
    return index_chunks(user_id, chunks)
