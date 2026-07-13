"""
Single place that talks to Groq. Every service/node asks this module
for an LLM instance instead of instantiating ChatGroq directly, so the
model name / temperature / key handling stays consistent everywhere.
"""
from __future__ import annotations

from functools import lru_cache
from langchain_groq import ChatGroq
from config.settings import settings


@lru_cache(maxsize=4)
def get_llm(temperature: float | None = None) -> ChatGroq:
    if not settings.GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to your .env file before running the app."
        )
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        temperature=settings.LLM_TEMPERATURE if temperature is None else temperature,
    )


def invoke_text(prompt: str, *, system: str | None = None, temperature: float | None = None) -> str:
    """Convenience helper for simple prompt -> text calls."""
    llm = get_llm(temperature)
    messages = []
    if system:
        messages.append(("system", system))
    messages.append(("human", prompt))
    response = llm.invoke(messages)
    return response.content
