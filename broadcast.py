import logging
import os
import requests
from typing import Optional


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def send_telegram_message(
    chat_id: str, message: str, bot_token: str, parse_mode: Optional[str] = "HTML", disable_preview: bool = False
) -> None:
    """
    Send a message to a Telegram chat using the Telegram Bot API.

    Args:
        chat_id: Unique identifier for the target chat
        message: Text message to send
        bot_token: Authentication token for the Telegram bot
        parse_mode: Mode for parsing entities in the message text
        disable_preview: If True, disables link previews in the message
    """
    # Construct the API endpoint URL
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Prepare the request payload
    payload = {"chat_id": chat_id, "text": message}

    # Add optional parameters if provided
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if disable_preview:
        payload["disable_web_page_preview"] = True

    try:
        # Send POST request to Telegram API
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses

    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending Telegram message: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def extract_tgid(username: str) -> int | None:
    try:
        # Split by 'tgid-' and take the last part
        tgid_str = username.split("tgid-")[-1]
        return int(tgid_str)
    except (IndexError, ValueError):
        return None


def get_message():
    with open("message", "r") as file:
        content = file.read()
        return content


BOT_TOKEN = os.environ["TG_BOT_TOKEN"]


def get_users():
    # Prepare headers with authorization token
    headers = {"Authorization": f"Bearer {os.environ['ADMIN_TOKEN']}"}

    # Make GET request to API
    response = requests.get(f"{os.environ['API_BASE_URL']}/api/user", headers=headers)

    # Check if request was successful
    if not response.ok:
        raise Exception(f"Failed to fetch users: {response.text}")

    # Parse JSON response
    body = response.json()
    users = body["users"]

    return users


def main():
    users = get_users()
    message = get_message()

    for i, user in enumerate(users):
        tgid = extract_tgid(user["username"])

        if tgid is None:
            logger.info(f"Skipped {user} ({i + 1}/{len(users)})")
            continue

        send_telegram_message(tgid, message, BOT_TOKEN)
        logger.info(f"Sent message to {user} ({i + 1}/{len(users)})")
