"""
Chat route — main entry point for the LangGraph waste assistant.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
import uuid
import logging

from app.models.schemas import ChatRequest, ChatResponse, WasteSummary, WasteCategory
from app.nodes.graph import waste_graph
from app.utils.session_store import create_session, get_session, update_session
from app.utils.classifier import DISPOSAL_GUIDE

router = APIRouter(prefix="/api", tags=["chat"])
logger = logging.getLogger(__name__)


def _get_or_create_state(session_id: Optional[str], user_input: str) -> tuple[str, dict]:
    """Return (session_id, state_dict) — create new session if needed."""
    if not session_id:
        session_id = create_session()

    state = get_session(session_id)
    if not state:
        session_id = create_session()
        state = get_session(session_id)

    state["user_input"] = user_input
    return session_id, state


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Main conversational endpoint.
    Drives the LangGraph flow step by step based on session state.
    """
    session_id, state = _get_or_create_state(req.session_id, req.message)

    try:
        result = await waste_graph.ainvoke(state)
    except Exception as e:
        logger.error(f"Graph error: {e}")
        raise HTTPException(status_code=500, detail="AI workflow error. Please try again.")

    # Persist updated state
    update_session(session_id, result)

    # Build waste summary card if classification is done
    waste_summary = None
    if result.get("waste_type") and result.get("waste_type") != "Unknown" and result.get("stage") == "complete":
        wt = result["waste_type"]
        guide = DISPOSAL_GUIDE.get(wt, DISPOSAL_GUIDE["Unknown"])
        waste_summary = WasteSummary(
            waste_item=result.get("waste_item", ""),
            waste_type=WasteCategory(wt),
            disposal_instructions=result.get("disposal_instructions", []),
            reward_points=result.get("reward_points", 0),
            color_code=result.get("color_code", "#6B7280"),
        )

    return ChatResponse(
        reply=result.get("reply", ""),
        session_id=session_id,
        waste_summary=waste_summary,
        stage=result.get("stage", "greeting"),
    )


@router.post("/chat/image", response_model=ChatResponse)
async def chat_with_image(
    session_id: Optional[str] = Form(None),
    message: Optional[str] = Form(""),
    file: UploadFile = File(...),
):
    """
    Image upload endpoint — placeholder for vision-based classification.
    Currently extracts filename as a hint for classification.
    """
    filename = file.filename or ""
    # Use filename stem as waste item hint (placeholder)
    hint = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ")
    combined_message = f"{message} {hint}".strip() if message else hint

    req = ChatRequest(message=combined_message, session_id=session_id)
    return await chat(req)


@router.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Return current session state (for debugging / reward display)."""
    state = get_session(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session_id,
        "stage": state.get("stage"),
        "user_name": state.get("user_name"),
        "reward_points": state.get("reward_points", 0),
        "waste_type": state.get("waste_type"),
    }


@router.delete("/session/{session_id}")
async def reset_session(session_id: str):
    """Reset session to start a fresh conversation."""
    from app.utils.session_store import delete_session
    delete_session(session_id)
    return {"message": "Session reset. Start a new conversation!"}
