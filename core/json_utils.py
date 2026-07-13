"""
LLMs occasionally wrap JSON in markdown fences or add stray text even
when told not to. This helper extracts and parses JSON defensively so
a single formatting hiccup doesn't crash the whole graph.
"""
from __future__ import annotations

import json
import re


def parse_json_response(raw: str, default: dict | None = None) -> dict:
    if default is None:
        default = {}

    text = raw.strip()
    # Strip ```json ... ``` or ``` ... ``` fences if present
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Last resort: grab the outermost {...} block
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    return default
