"""
Supabase client and database operations.
"""
import os
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

# Lazy init — only connect if env vars are present
_supabase = None


def get_supabase():
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
        if url and key:
            try:
                from supabase import create_client
                _supabase = create_client(url, key)
                logger.info("Supabase connected.")
            except Exception as e:
                logger.warning(f"Supabase init failed: {e}")
    return _supabase


async def upsert_user(session_id: str, name: str, age: str) -> Optional[dict]:
    """Insert or update user record."""
    db = get_supabase()
    if not db:
        return None
    try:
        result = db.table("users").upsert({
            "session_id": session_id,
            "name": name,
            "age": age,
            "created_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        return result.data
    except Exception as e:
        logger.error(f"upsert_user error: {e}")
        return None


async def save_waste_query(
    session_id: str,
    waste_item: str,
    waste_type: str,
    disposal_method: str,
) -> Optional[dict]:
    """Save a waste classification query."""
    db = get_supabase()
    if not db:
        return None
    try:
        result = db.table("waste_queries").insert({
            "session_id": session_id,
            "waste_item": waste_item,
            "waste_type": waste_type,
            "disposal_method": disposal_method,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }).execute()
        return result.data
    except Exception as e:
        logger.error(f"save_waste_query error: {e}")
        return None


async def save_reward(session_id: str, points: int) -> Optional[dict]:
    """Save or update reward points for a session."""
    db = get_supabase()
    if not db:
        return None
    try:
        result = db.table("rewards").upsert({
            "session_id": session_id,
            "points": points,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }).execute()
        return result.data
    except Exception as e:
        logger.error(f"save_reward error: {e}")
        return None


async def get_user_rewards(session_id: str) -> int:
    """Get total reward points for a session."""
    db = get_supabase()
    if not db:
        return 0
    try:
        result = db.table("rewards").select("points").eq("session_id", session_id).execute()
        if result.data:
            return result.data[0].get("points", 0)
    except Exception as e:
        logger.error(f"get_user_rewards error: {e}")
    return 0
