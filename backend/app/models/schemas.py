from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class WasteCategory(str, Enum):
    PLASTIC = "Plastic"
    ORGANIC = "Organic"
    E_WASTE = "E-Waste"
    HAZARDOUS = "Hazardous"
    UNKNOWN = "Unknown"


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List[ChatMessage]] = []


class WasteSummary(BaseModel):
    waste_item: str
    waste_type: WasteCategory
    disposal_instructions: List[str]
    reward_points: int
    color_code: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    waste_summary: Optional[WasteSummary] = None
    stage: str  # "collecting_name" | "collecting_age" | "collecting_waste" | "complete"


class WebhookPayload(BaseModel):
    user_name: str
    user_age: str
    waste_item: str
    waste_type: str
    disposal_method: str
    timestamp: str


class UserSession(BaseModel):
    session_id: str
    user_name: Optional[str] = None
    user_age: Optional[str] = None
    waste_item: Optional[str] = None
    waste_type: Optional[WasteCategory] = None
    disposal_method: Optional[str] = None
    stage: str = "greeting"
    reward_points: int = 0
