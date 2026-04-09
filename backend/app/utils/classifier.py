"""
Keyword-based waste classifier with LLM fallback.
"""
from typing import Tuple
import re

PLASTIC_KEYWORDS = [
    "plastic", "bottle", "bag", "wrapper", "straw", "container", "cup", "lid",
    "packaging", "polythene", "polybag", "PET", "HDPE", "PVC", "foam", "styrofoam",
    "tupperware", "jerry can", "sachet", "blister pack", "tetra pak"
]

ORGANIC_KEYWORDS = [
    "banana", "peel", "fruit", "vegetable", "food", "leftover", "waste",
    "leaf", "leaves", "grass", "flower", "compost", "kitchen", "rotten",
    "rice", "dal", "roti", "bread", "egg shell", "coffee grounds", "tea leaves",
    "onion", "potato", "tomato", "mango", "coconut", "garden", "plant"
]

EWASTE_KEYWORDS = [
    "phone", "mobile", "laptop", "computer", "tablet", "charger", "cable",
    "keyboard", "mouse", "printer", "monitor", "TV", "television", "hard disk",
    "USB", "circuit", "motherboard", "headphone", "earphone", "speaker", "camera",
    "remote", "wire", "electronic", "gadget", "device", "bulb", "CFL", "LED tube"
]

HAZARDOUS_KEYWORDS = [
    "battery", "batteries", "chemical", "paint", "solvent", "pesticide",
    "insecticide", "acid", "bleach", "detergent", "fertilizer", "medicine",
    "pill", "tablet", "syringe", "needle", "motor oil", "kerosene", "fuel",
    "gas cylinder", "aerosol", "spray can", "thermometer", "mercury", "asbestos"
]

DISPOSAL_GUIDE = {
    "Plastic": {
        "instructions": [
            "Rinse the plastic item to remove any residue.",
            "Flatten or compress to reduce volume.",
            "Place in the dry waste / blue recycling bin.",
            "Do NOT mix with wet/organic waste.",
            "Avoid burning plastic — it releases toxic fumes.",
            "Look for nearest Kabadiwala or recycling center in your area."
        ],
        "color": "#3B82F6",  # blue
        "points": 10
    },
    "Organic": {
        "instructions": [
            "Separate from dry and hazardous waste immediately.",
            "Place in the wet waste / green bin provided by your municipality.",
            "Consider home composting to create manure for plants.",
            "You can use a small compost bin or earthen pot at home.",
            "Do NOT throw in open areas or drains."
        ],
        "color": "#22C55E",  # green
        "points": 8
    },
    "E-Waste": {
        "instructions": [
            "Never throw e-waste in regular dustbins.",
            "Locate your nearest authorized e-waste collection center.",
            "Contact brands like Dell, HP, Samsung — many have take-back programs.",
            "Check Zelenium, E-Parisaraa, or municipal e-waste drives.",
            "Remove batteries (if detachable) and dispose separately as hazardous.",
            "Avoid breaking devices — it releases toxic materials."
        ],
        "color": "#F59E0B",  # amber
        "points": 15
    },
    "Hazardous": {
        "instructions": [
            "Never mix with household garbage.",
            "Store in original containers where possible.",
            "Take to authorized hazardous waste facility.",
            "For batteries: drop at electronics stores or municipal collection points.",
            "For medicines: return to pharmacy or use drug take-back programs.",
            "Contact your local municipality for hazardous waste collection day."
        ],
        "color": "#EF4444",  # red
        "points": 20
    },
    "Unknown": {
        "instructions": [
            "Unable to classify. Please describe the item more specifically.",
            "When in doubt, separate and ask your local waste collector.",
            "Contact your municipal corporation for guidance."
        ],
        "color": "#6B7280",  # gray
        "points": 5
    }
}


def classify_waste(item: str) -> Tuple[str, list, str, int]:
    """
    Returns: (waste_type, disposal_instructions, color_code, reward_points)
    Uses keyword matching first, then returns Unknown if no match.
    """
    item_lower = item.lower()

    def match(keywords):
        return any(re.search(r'\b' + kw.lower() + r'\b', item_lower) for kw in keywords)

    if match(PLASTIC_KEYWORDS):
        category = "Plastic"
    elif match(ORGANIC_KEYWORDS):
        category = "Organic"
    elif match(EWASTE_KEYWORDS):
        category = "E-Waste"
    elif match(HAZARDOUS_KEYWORDS):
        category = "Hazardous"
    else:
        category = "Unknown"

    guide = DISPOSAL_GUIDE[category]
    return category, guide["instructions"], guide["color"], guide["points"]
