"""
LangGraph workflow for Waste Classification and Smart Disposal Assistant.

Graph Flow:
  start → clarification → router → [plastic|organic|ewaste|hazardous|unknown] → final
"""
from typing import TypedDict, Optional, Annotated
import operator
import uuid
import logging

from langgraph.graph import StateGraph, END

from app.utils.classifier import classify_waste, DISPOSAL_GUIDE
from app.utils.webhook import trigger_webhook
from app.utils.supabase_client import upsert_user, save_waste_query, save_reward

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# State definition
# ─────────────────────────────────────────────
class WasteState(TypedDict):
    session_id: str
    user_input: str
    stage: str                       # greeting | collecting_name | collecting_age | collecting_waste | routing | complete
    user_name: Optional[str]
    user_age: Optional[str]
    waste_item: Optional[str]
    waste_type: Optional[str]
    disposal_instructions: Optional[list]
    color_code: Optional[str]
    reward_points: Optional[int]
    reply: Optional[str]
    webhook_fired: bool


# ─────────────────────────────────────────────
# Node: Start (greeting + collect name)
# ─────────────────────────────────────────────
def start_node(state: WasteState) -> WasteState:
    stage = state.get("stage", "greeting")

    if stage == "greeting":
        state["reply"] = (
            "🌿 Namaste! Welcome to the **Waste Classification Assistant**.\n\n"
            "I help you dispose of waste responsibly — the Indian way! ♻️\n\n"
            "May I know your **name** to get started?"
        )
        state["stage"] = "just_greeted"   # sentinel so clarification skips this turn
        return state

    return state


# ─────────────────────────────────────────────
# Node: Clarification (collect name → age → waste item)
# ─────────────────────────────────────────────
def clarification_node(state: WasteState) -> WasteState:
    stage = state.get("stage", "collecting_name")
    user_input = state.get("user_input", "").strip()

    # just_greeted means start_node already set the reply this turn — skip
    if stage == "just_greeted":
        state["stage"] = "collecting_name"
        return state

    if stage == "collecting_name":
        if not user_input:
            state["reply"] = "Please tell me your name so I can assist you better. 😊"
            return state
        state["user_name"] = user_input.title()
        state["stage"] = "collecting_age"
        state["reply"] = (
            f"Nice to meet you, **{state['user_name']}**! 🙏\n\n"
            "Could you please share your **age**?"
        )
        return state

    if stage == "collecting_age":
        age_str = user_input.strip()
        if not age_str.isdigit() or not (1 <= int(age_str) <= 120):
            state["reply"] = "Please enter a valid age (e.g., 25). 🧾"
            return state
        state["user_age"] = age_str
        state["stage"] = "collecting_waste"
        state["reply"] = (
            f"Thank you! Now, what **waste item** would you like help with?\n\n"
            "*(Examples: plastic bottle, banana peel, old phone, dead battery)*"
        )
        return state

    if stage == "collecting_waste":
        if not user_input:
            state["reply"] = "Please describe the waste item you want to dispose of. 🗑️"
            return state
        state["waste_item"] = user_input
        state["stage"] = "routing"
        return state

    return state


# ─────────────────────────────────────────────
# Node: Router (classify the waste type)
# ─────────────────────────────────────────────
def router_node(state: WasteState) -> WasteState:
    waste_item = state.get("waste_item", "")
    waste_type, instructions, color, points = classify_waste(waste_item)
    state["waste_type"] = waste_type
    state["disposal_instructions"] = instructions
    state["color_code"] = color
    state["reward_points"] = points
    return state


# ─────────────────────────────────────────────
# Conditional edge: route to specific waste node
# ─────────────────────────────────────────────
def route_by_waste_type(state: WasteState) -> str:
    wt = state.get("waste_type", "Unknown")
    mapping = {
        "Plastic": "plastic_node",
        "Organic": "organic_node",
        "E-Waste": "ewaste_node",
        "Hazardous": "hazardous_node",
    }
    return mapping.get(wt, "unknown_node")


# ─────────────────────────────────────────────
# Waste-specific nodes (build tailored reply)
# ─────────────────────────────────────────────
def _build_disposal_reply(state: WasteState, intro: str) -> WasteState:
    name = state.get("user_name", "Friend")
    item = state.get("waste_item", "your item")
    instructions = state.get("disposal_instructions", [])
    points = state.get("reward_points", 0)

    steps = "\n".join([f"  {i+1}. {step}" for i, step in enumerate(instructions)])
    state["reply"] = (
        f"{intro}\n\n"
        f"**Disposal Steps for '{item}':**\n{steps}\n\n"
        f"🌟 You've earned **{points} Eco Points** for responsible disposal!\n\n"
        f"Would you like to classify another waste item, {name}? Just type it!"
    )
    state["stage"] = "complete"
    return state


def plastic_node(state: WasteState) -> WasteState:
    return _build_disposal_reply(
        state,
        "♻️ This is **Plastic waste** — place it in the **Dry/Blue recycling bin**."
    )


def organic_node(state: WasteState) -> WasteState:
    return _build_disposal_reply(
        state,
        "🥬 This is **Organic waste** — goes into the **Wet/Green bin** or home compost!"
    )


def ewaste_node(state: WasteState) -> WasteState:
    return _build_disposal_reply(
        state,
        "💻 This is **E-Waste** — never throw it in regular trash. Use certified e-waste centers."
    )


def hazardous_node(state: WasteState) -> WasteState:
    return _build_disposal_reply(
        state,
        "⚠️ This is **Hazardous waste** — handle with care and use special disposal facilities."
    )


def unknown_node(state: WasteState) -> WasteState:
    return _build_disposal_reply(
        state,
        "🤔 I couldn't confidently classify this item. Here are some general guidelines:"
    )


# ─────────────────────────────────────────────
# Node: Final (trigger webhook + save to DB)
# ─────────────────────────────────────────────
async def final_node(state: WasteState) -> WasteState:
    if state.get("webhook_fired"):
        return state

    user_name = state.get("user_name")
    user_age = state.get("user_age")
    waste_item = state.get("waste_item")
    waste_type = state.get("waste_type")
    disposal = state.get("disposal_instructions", [])
    session_id = state.get("session_id", str(uuid.uuid4()))
    points = state.get("reward_points", 0)

    if all([user_name, user_age, waste_item, waste_type]):
        disposal_method = disposal[0] if disposal else "See disposal instructions"

        # Persist to Supabase (graceful failure)
        await upsert_user(session_id, user_name, user_age)
        await save_waste_query(session_id, waste_item, waste_type, disposal_method)
        await save_reward(session_id, points)

        # Fire webhook
        await trigger_webhook(user_name, user_age, waste_item, waste_type, disposal_method)
        state["webhook_fired"] = True

    return state


# ─────────────────────────────────────────────
# Conditional routing from clarification node
# ─────────────────────────────────────────────
def should_continue_or_route(state: WasteState) -> str:
    stage = state.get("stage", "")
    if stage == "routing":
        return "router_node"
    return END  # still collecting info — wait for next user message


# ─────────────────────────────────────────────
# Build the LangGraph
# ─────────────────────────────────────────────
def build_graph():
    g = StateGraph(WasteState)

    # Register nodes
    g.add_node("start_node", start_node)
    g.add_node("clarification_node", clarification_node)
    g.add_node("router_node", router_node)
    g.add_node("plastic_node", plastic_node)
    g.add_node("organic_node", organic_node)
    g.add_node("ewaste_node", ewaste_node)
    g.add_node("hazardous_node", hazardous_node)
    g.add_node("unknown_node", unknown_node)
    g.add_node("final_node", final_node)

    # Entry point
    g.set_entry_point("start_node")

    # start → clarification
    g.add_edge("start_node", "clarification_node")

    # clarification → router OR END (if still collecting)
    g.add_conditional_edges(
        "clarification_node",
        should_continue_or_route,
        {"router_node": "router_node", END: END}
    )

    # router → specific waste node
    g.add_conditional_edges(
        "router_node",
        route_by_waste_type,
        {
            "plastic_node": "plastic_node",
            "organic_node": "organic_node",
            "ewaste_node": "ewaste_node",
            "hazardous_node": "hazardous_node",
            "unknown_node": "unknown_node",
        }
    )

    # All waste nodes → final
    for node in ["plastic_node", "organic_node", "ewaste_node", "hazardous_node", "unknown_node"]:
        g.add_edge(node, "final_node")

    g.add_edge("final_node", END)

    return g.compile()


# Singleton compiled graph
waste_graph = build_graph()
