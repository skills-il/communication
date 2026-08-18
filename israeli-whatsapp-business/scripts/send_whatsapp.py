#!/usr/bin/env python3
"""Send WhatsApp Business messages via the Meta Cloud API for Israeli market.

Recipient numbers are sent to the API WITHOUT a leading '+' and WITHOUT the
Israeli leading zero, e.g. 972541234567. This script accepts 0521234567,
+972521234567 and 972521234567 and normalises all three to that form.

Usage:
    # Send template message
    python send_whatsapp.py --mode template \
        --to 972541234567 \
        --template-name appointment_reminder_he \
        --language he \
        --parameters "Israel" "Dental Clinic" "15.03.2026" "10:00"

    # Send text message (within the 24-hour customer service window)
    python send_whatsapp.py --mode text \
        --to 972541234567 \
        --message "Thank you for your message!"

    # Send interactive reply buttons (Hebrew labels by default)
    python send_whatsapp.py --mode interactive \
        --to 972541234567 \
        --message "לאשר את התור?" \
        --buttons "confirm=מאשר" "reschedule=צריך לשנות"

    # Send an interactive list
    python send_whatsapp.py --mode list \
        --to 972541234567 \
        --message "בחרו שירות" \
        --list-button "בחר אפשרות" \
        --list-rows "cleaning=ניקוי אבנית" "checkup=בדיקה תקופתית"

    # Validate everything without sending
    python send_whatsapp.py --mode template --to 0521234567 \
        --template-name appointment_reminder_he --dry-run

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


API_VERSION = "v26.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Israeli mobile prefixes carried on WhatsApp. Written as an explicit
# alternation rather than a character range: the old pattern was 05[0-58],
# a RANGE meaning {0,1,2,3,4,5,8}, which reads like a list and invites the
# next editor to "add 056" as [0-568] and silently admit 056 AND 057.
MOBILE_PREFIXES = ('050', '051', '052', '053', '054', '055', '058')
MOBILE_RE = re.compile(r'^(?:' + '|'.join(MOBILE_PREFIXES) + r')\d{7}$')
# Landline: area codes 2,3,4,8,9 plus the 07x non-geographic ranges, but
# NEVER 05x. Without excluding 05 this branch matched any 10-digit 05x
# number and silently re-admitted the mobile prefixes the check above just
# rejected (0561234567, 0571234567, 0591234567 all came back valid).
LANDLINE_RE = re.compile(r'^0(?:[2-4]|[689]|7\d)\d{7}$')

# Default Hebrew quick-reply labels. This is a Hebrew-market skill, so English
# button text is the wrong default; override with --buttons.
DEFAULT_BUTTONS = [
    {"id": "confirm", "title": "מאשר"},
    {"id": "reschedule", "title": "צריך לשנות"},
]

DRY_RUN = False


def _post(url: str, headers: dict, payload: dict) -> dict:
    """POST to the Cloud API and return a dict, never raising on a bad body.

    Checks the HTTP status explicitly. A 5xx from Meta often returns an HTML
    error page, and calling .json() on that raises JSONDecodeError with no
    useful context, so decode defensively and surface the status.
    """
    if DRY_RUN:
        print("[dry-run] POST " + url)
        print("[dry-run] " + json.dumps(payload, indent=2, ensure_ascii=False))
        return {"dry_run": True, "messages": [{"id": "DRY-RUN"}]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
    except requests.RequestException as exc:
        return {"error": {"message": f"Network error: {exc}", "code": "network"}}

    try:
        body = response.json()
    except ValueError:
        return {"error": {
            "message": (f"HTTP {response.status_code}: non-JSON response from "
                        f"the API: {response.text[:300]}"),
            "code": response.status_code,
        }}

    if response.status_code == 429:
        body.setdefault("error", {})
        body["error"].setdefault(
            "message", "Rate limit hit (HTTP 429). Back off and retry later.")
        body["error"]["http_status"] = 429
        return body

    if not response.ok and "error" not in body:
        body["error"] = {"message": f"HTTP {response.status_code}",
                         "code": response.status_code}

    if "error" in body:
        body["error"]["http_status"] = response.status_code

    return body


def parse_kv_pairs(items: list, what: str) -> list:
    """Parse 'id=title' CLI pairs into [{'id':..., 'title':...}]."""
    parsed = []
    for item in items or []:
        if "=" not in item:
            print(f"Error: {what} must be given as id=title, got '{item}'")
            sys.exit(1)
        key, title = item.split("=", 1)
        if not key.strip() or not title.strip():
            print(f"Error: {what} '{item}' has an empty id or title")
            sys.exit(1)
        parsed.append({"id": key.strip(), "title": title.strip()})
    return parsed


def validate_israeli_phone(phone: str) -> tuple[bool, str]:
    """Validate and normalize an Israeli phone number for WhatsApp.

    WhatsApp requires numbers WITHOUT the '+' prefix and WITHOUT the Israeli
    leading zero, e.g. 972541234567.

    Args:
        phone: Phone number in any format.

    Returns:
        Tuple of (is_valid, normalized_number_or_error_message).
    """
    clean = re.sub(r'[\s\-\(\)\.\+]', '', phone)

    # Normalize to a local 0XXXXXXXXX form first, then strip the zero.
    if clean.startswith('972'):
        rest = clean[3:]
        # The #1 gotcha: +9720521234567 keeps the local leading zero after
        # the country code. Name the cause instead of a generic rejection.
        if rest.startswith('0'):
            return False, (
                "Invalid Israeli number: drop the leading zero after the 972 "
                f"country code. Got '{phone}'; use '972{rest.lstrip('0')}' "
                "(e.g. 972521234567, not +9720521234567)."
            )
        local = '0' + rest
    elif clean.startswith('0'):
        local = clean
    else:
        return False, "Number must start with 0, +972, or 972"

    if MOBILE_RE.match(local):
        return True, '972' + local[1:]

    if LANDLINE_RE.match(local):
        return True, '972' + local[1:]

    if local.startswith('05'):
        return False, (
            f"Invalid Israeli mobile prefix '{local[:3]}'. Supported prefixes: "
            + ', '.join(MOBILE_PREFIXES) + "."
        )

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

    return _post(url, headers, payload)


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

    return _post(url, headers, payload)


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

    return _post(url, headers, payload)


def send_interactive_list(phone_number_id: str, access_token: str,
                          to: str, body_text: str,
                          rows: list, button_text: str = "בחר אפשרות",
                          section_title: str = "אפשרויות") -> dict:
    """Send an interactive list message.

    Args:
        phone_number_id: WhatsApp Business Phone Number ID.
        access_token: Meta System User Access Token.
        to: Recipient number (format: 972XXXXXXXXX).
        body_text: Message body text.
        rows: List of dicts with 'id' and 'title' keys (max 10).
        button_text: Label on the button that opens the list.
        section_title: Heading for the single section.

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
            "type": "list",
            "body": {"text": body_text},
            "action": {
                "button": button_text,
                "sections": [
                    {
                        "title": section_title,
                        # WhatsApp allows max 10 rows across all sections
                        "rows": [
                            {"id": row["id"], "title": row["title"]}
                            for row in rows[:10]
                        ],
                    }
                ],
            },
        }
    }

    return _post(url, headers, payload)


def main():
    global DRY_RUN
    parser = argparse.ArgumentParser(
        description="Send WhatsApp Business messages for Israeli market"
    )
    parser.add_argument("--mode",
                        choices=["template", "text", "interactive", "list"],
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
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate the number and print the payload "
                             "without calling the API")

    # Template options
    parser.add_argument("--template-name", help="Template name")
    parser.add_argument("--language", default="he", help="Template language code")
    parser.add_argument("--parameters", nargs="*", help="Template parameters")

    # Text / interactive body
    parser.add_argument("--message", help="Message text (body text for "
                                          "interactive and list modes)")

    # Interactive button options
    parser.add_argument("--buttons", nargs="*",
                        help="Reply buttons as id=title (max 3). Defaults to "
                             "Hebrew: confirm=maasher, reschedule=tzarich "
                             "leshanot")

    # List options
    parser.add_argument("--list-rows", nargs="*",
                        help="List rows as id=title (max 10), for --mode list")
    parser.add_argument("--list-button", default="בחר אפשרות",
                        help="Label on the button that opens the list")
    parser.add_argument("--list-section", default="אפשרויות",
                        help="Section heading for the list")

    args = parser.parse_args()
    DRY_RUN = args.dry_run

    # Validate required credentials
    if args.dry_run:
        args.phone_id = args.phone_id or "DRY-RUN-PHONE-ID"
        args.access_token = args.access_token or "DRY-RUN-TOKEN"
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
        buttons = parse_kv_pairs(args.buttons, "--buttons") or DEFAULT_BUTTONS
        result = send_interactive_buttons(
            args.phone_id, args.access_token, normalized,
            args.message, buttons
        )

    elif args.mode == "list":
        if not args.message:
            print("Error: --message required for list mode")
            sys.exit(1)
        rows = parse_kv_pairs(args.list_rows, "--list-rows")
        if not rows:
            print("Error: --list-rows required for list mode (id=title pairs)")
            sys.exit(1)
        result = send_interactive_list(
            args.phone_id, args.access_token, normalized,
            args.message, rows, args.list_button, args.list_section
        )

    # Output result
    if "error" in result:
        err = result["error"]
        print(f"Error: {err.get('message', 'Unknown error')}")
        print(f"Code: {err.get('code', 'N/A')}")
        if err.get("http_status"):
            print(f"HTTP status: {err['http_status']}")
        sys.exit(1)
    else:
        msg_id = result.get("messages", [{}])[0].get("id", "N/A")
        print("Message sent successfully!" if not args.dry_run
              else "Dry run complete, nothing was sent.")
        print(f"Message ID: {msg_id}")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
