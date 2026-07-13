"""
Thin wrapper around a persistent Chroma vector store. Each user gets
their own collection (keyed by user_id) so profiles never mix.
"""
from __future__ import annotations

import uuid
from langchain_chroma import Chroma
from core.embeddings import get_embedding_model
from config.settings import settings


def _collection_name(user_id: str) -> str:
    safe = "".join(c for c in user_id if c.isalnum() or c in "-_") or "default"
    return f"profile_{safe}"


def get_vector_store(user_id: str) -> Chroma:
    settings.ensure_dirs()
    return Chroma(
        collection_name=_collection_name(user_id),
        embedding_function=get_embedding_model(),
        persist_directory=str(settings.VECTOR_DB_DIR),
    )


def index_chunks(user_id: str, chunks: list[dict]) -> int:
    """
    Embeds and stores chunks (each a {"text","source"} dict).
    Returns the number of chunks indexed.
    """
    if not chunks:
        return 0
    store = get_vector_store(user_id)
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c.get("source", "unknown")} for c in chunks]
    ids = [str(uuid.uuid4()) for _ in chunks]
    store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    return len(chunks)


def reset_user_data(user_id: str) -> None:
    """Wipes a user's vector collection, e.g. before a fresh re-upload."""
    store = get_vector_store(user_id)
    try:
        store.delete_collection()
    except Exception:
        pass


def retrieve_relevant_chunks(user_id: str, query: str, k: int | None = None) -> list[dict]:
    """
    RAG retrieval step: given a job description (or a query derived
    from it), return the top-k most relevant chunks from the user's
    stored career history, each with a similarity score.
    """
    store = get_vector_store(user_id)
    k = k or settings.RETRIEVAL_TOP_K
    try:
        results = store.similarity_search_with_relevance_scores(query, k=k)
    except Exception:
        # Empty collection or first-ever query can raise; treat as no data.
        return []

    return [
        {"text": doc.page_content, "source": doc.metadata.get("source", ""), "score": score}
        for doc, score in results
    ]
