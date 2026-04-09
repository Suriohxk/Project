"""
In-memory session store. Replace with Redis for production.
"""
from typing import Dict, Optional
import uuid
from app.models.schemas import UserSession

_sessions: Dict[str, dict] = {}


def create_session() -> str:
    sid = str(uuid.uuid4())
    _sessions[sid] = {
        "session_id": sid,
        "stage": "greeting",
        "user_name": None,
        "user_age": None,
        "waste_item": None,
        "waste_type": None,
        "disposal_instructions": None,
        "color_code": None,
        "reward_points": 0,
        "reply": None,
        "webhook_fired": False,
        "user_input": "",
    }
    return sid


def get_session(session_id: str) -> Optional[dict]:
    return _sessions.get(session_id)


def update_session(session_id: str, data: dict) -> dict:
    if session_id not in _sessions:
        _sessions[session_id] = data
    else:
        _sessions[session_id].update(data)
    return _sessions[session_id]


def delete_session(session_id: str):
    _sessions.pop(session_id, None)
