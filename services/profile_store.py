from __future__ import annotations

import json
from pathlib import Path

from core.schemas import StaticProfile
from config.settings import settings


def _path_for(user_id: str) -> Path:
    settings.ensure_dirs()
    safe = "".join(c for c in user_id if c.isalnum() or c in "-_") or "default"
    return settings.PROFILE_DIR / f"{safe}.json"


def save_profile(user_id: str, profile: StaticProfile) -> None:
    path = _path_for(user_id)
    path.write_text(profile.model_dump_json(indent=2), encoding="utf-8")


def load_profile(user_id: str) -> StaticProfile:
    path = _path_for(user_id)
    if not path.exists():
        return StaticProfile()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return StaticProfile(**data)
    except Exception:
        return StaticProfile()
