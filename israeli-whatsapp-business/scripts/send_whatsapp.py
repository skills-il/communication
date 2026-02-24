#!/usr/bin/env python3
"""Send WhatsApp Business messages via the Meta Cloud API for Israeli market.

Usage:
    # Send template message
    python send_whatsapp.py --mode template \
        --to 972541234567 \
        --template-name appointment_reminder_he \
        --language he \
        --parameters "Israel" "Dental Clinic" "15.03.2025" "10:00"

    # Send text message (within 24-hour window)
    python send_whatsapp.py --mode text \
        --to 972541234567 \
        --message "Thank you for your message!"

Environment variables:
    WHATSAPP_ACCESS_TOKEN   Meta System User Access Token
    WHATSAPP_PHONE_ID       WhatsApp Business Phone Number ID
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, time

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)

try:
    import pytz
    HAS_PYTZ = True
except ImportError:
    HAS_PYTZ = False


API_VERSION = "v18.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"


def validate_israeli_phone(phone: str) -> tuple[bool, str]:
    """Validate and normalize Israeli phone number for WhatsApp.

    WhatsApp requires numbers WITHOUT the + prefix, e.g., 972541234567.

    Args:
        phone: Phone number in any format.

    Returns:
        Tuple of (is_valid, normalized_number_for_whatsapp).
    """
    clean = re.sub(r'[\s\-\(\)\.\+]', '', phone)

    # Normalize to 972XXXXXXXXX format (no + prefix for WhatsApp API)
    if clean.startswith('972'):
        local = '0' + clean[3:]
    elif clean.startswith('0'):
        local = clean
    else:
        return False, "Number must start with 0, +972, or 972"

    # Validate mobile
    if re.match(r'^05[0-8]\d{7}$', local):
        return True, '972' + local[1:]

    # Validate landline
    if re.match(r'^0[2-9]\d{7,8}$', local):
        return True, '972' + local[1:]

    return False, "Invalid Israeli phone number"


def is_valid_sending_time() -> tuple[bool, str]:
    """Check if current time is appropriate for Israeli business messaging.

    Returns:
        Tuple of (is_ok, message).
    """
    if not HAS_PYTZ:
        return True, "pytz not installed, skipping time check"

    israel_tz = pytz.timezone('Asia/Jerusalem')
    now = datetime.now(israel_tz)
    day = now.weekday()  # 0=Monday, 6=Sunday

    # Friday after 14:00 -- pre-Shabbat
    if day == 4 and now.time() > time(14, 0):
        return False, "Pre-Shabbat hours. Send after Saturday 20:00."

    # Saturday before 20:00 -- Shabbat
    if day == 5 and now.time() < time(20, 0):
        return False, "Shabbat. Send after 20:00."

    # Business hours check
    if now.time() < time(8, 30) or now.time() > time(20, 0):
        return False, "Outside business hours (08:30-20:00 Israel time)."

    return True, "OK to send."


def send_template_message(phone_number_id: str, access_token: str,
                          to: str, template_name: str, language: str,
                          parameters: list) -> dict:
    """Send a WhatsApp template message.

    Args:
        phone_number_id: WhatsApp Business Phone Number ID.
        access_token: Meta System User Access Token.
        to: Recipient number (format: 972XXXXXXXXX).
        template_name: Approved template name.
        language: Template language code (e.g., "he" for Hebrew).
        parameters: List of template parameter values.

    Returns:
        API response as dict.
    """
    url = f"{BASE_URL}/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
        }
    }

    # Add parameters if provided
    if parameters:
        payload["template"]["components"] = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": p} for p in parameters
                ]
            }
        ]

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    return response.json()


def send_text_message(phone_number_id: str, access_token: str,
                      to: str, message: str) -> dict:
    """Send a free-form text message (within 24-hour customer window).

    Args:
        phone_number_id: WhatsApp Business Phone Number ID.
        access_token: Meta System User Access Token.
        to: Recipient number (format: 972XXXXXXXXX).
        message: Message text (Hebrew supported).

    Returns:
        API response as dict.
    """
    url = f"{BASE_URL}/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    return response.json()


def send_interactive_buttons(phone_number_id: str, access_token: str,
                             to: str, body_text: str,
                             buttons: list) -> dict:
    """Send an interactive button message.

    Args:
        phone_number_id: WhatsApp Business Phone Number ID.
        access_token: Meta System User Access Token.
        to: Recipient number (format: 972XXXXXXXXX).
        body_text: Message body text.
        buttons: List of dicts with 'id' and 'title' keys.

    Returns:
        API response as dict.
    """
    url = f"{BASE_URL}/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body_text},
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {"id": btn["id"], "title": btn["title"]}
                    }
                    for btn in buttons[:3]  # WhatsApp allows max 3 buttons
                ]
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Send WhatsApp Business messages for Israeli market"
    )
    parser.add_argument("--mode", choices=["template", "text", "interactive"],
                        required=True, help="Message type to send")
    parser.add_argument("--to", required=True, help="Recipient phone number")
    parser.add_argument("--phone-id",
                        default=os.environ.get("WHATSAPP_PHONE_ID"),
                        help="WhatsApp Phone Number ID")
    parser.add_argument("--access-token",
                        default=os.environ.get("WHATSAPP_ACCESS_TOKEN"),
                        help="Meta access token")
    parser.add_argument("--skip-time-check", action="store_true",
                        help="Skip Israeli business hours check")

    # Template options
    parser.add_argument("--template-name", help="Template name")
    parser.add_argument("--language", default="he", help="Template language code")
    parser.add_argument("--parameters", nargs="*", help="Template parameters")

    # Text options
    parser.add_argument("--message", help="Message text")

    args = parser.parse_args()

    # Validate required credentials
    if not args.phone_id or not args.access_token:
        print("Error: --phone-id and --access-token required (or set env vars)")
        sys.exit(1)

    # Validate phone number
    is_valid, normalized = validate_israeli_phone(args.to)
    if not is_valid:
        print(f"Error: {normalized}")
        sys.exit(1)

    # Check sending time
    if not args.skip_time_check:
        time_ok, time_msg = is_valid_sending_time()
        if not time_ok:
            print(f"Warning: {time_msg}")
            print("Use --skip-time-check to override.")
            sys.exit(1)

    print(f"Sending {args.mode} message to: {normalized}")

    # Send based on mode
    if args.mode == "template":
        if not args.template_name:
            print("Error: --template-name required for template mode")
            sys.exit(1)
        result = send_template_message(
            args.phone_id, args.access_token, normalized,
            args.template_name, args.language, args.parameters or []
        )

    elif args.mode == "text":
        if not args.message:
            print("Error: --message required for text mode")
            sys.exit(1)
        result = send_text_message(
            args.phone_id, args.access_token, normalized, args.message
        )

    elif args.mode == "interactive":
        if not args.message:
            print("Error: --message required for interactive mode")
            sys.exit(1)
        # Default Hebrew buttons
        buttons = [
            {"id": "confirm", "title": "Confirm"},
            {"id": "cancel", "title": "Cancel"},
        ]
        result = send_interactive_buttons(
            args.phone_id, args.access_token, normalized,
            args.message, buttons
        )

    # Output result
    if "error" in result:
        print(f"Error: {result['error'].get('message', 'Unknown error')}")
        print(f"Code: {result['error'].get('code', 'N/A')}")
        sys.exit(1)
    else:
        msg_id = result.get("messages", [{}])[0].get("id", "N/A")
        print(f"Message sent successfully!")
        print(f"Message ID: {msg_id}")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
