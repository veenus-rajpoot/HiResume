"""
Embedding model wrapper. Uses a local sentence-transformers model so
the app doesn't need a separate embeddings API key — only Groq (which
is chat/completion only) is required from the user.
"""
from __future__ import annotations

from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> HuggingFaceEmbeddings:
    """Cached so the model is loaded into memory only once per process."""
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    )
