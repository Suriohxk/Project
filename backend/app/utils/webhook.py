"""
Webhook trigger utility — fires when all user data is collected.
"""
import httpx
from datetime import datetime, timezone
import os
import logging

logger = logging.getLogger(__name__)

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://relay.app/mock-webhook")


async def trigger_webhook(
    user_name: str,
    user_age: str,
    waste_item: str,
    waste_type: str,
    disposal_method: str,
) -> bool:
    """
    Triggers a webhook with the collected user and waste data.
    Returns True on success, False on failure.
    """
    payload = {
        "user_name": user_name,
        "user_age": user_age,
        "waste_item": waste_item,
        "waste_type": waste_type,
        "disposal_method": disposal_method,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(WEBHOOK_URL, json=payload)
            if response.status_code in (200, 201, 202):
                logger.info(f"Webhook triggered successfully: {response.status_code}")
                return True
            else:
                logger.warning(f"Webhook returned status {response.status_code}")
                return False
    except Exception as e:
        logger.error(f"Webhook trigger failed: {e}")
        # Graceful failure — don't break the app
        return False
