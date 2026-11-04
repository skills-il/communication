#!/usr/bin/env python3
"""Send WhatsApp Business messages via the Meta Cloud API for Israeli market.

Recipient numbers are sent to the API WITHOUT a leading '+' and WITHOUT the
Israeli leading zero, e.g. 972541234567. This script accepts 0521234567,
+972521234567 and 972521234567 and normalises all three to that form. It
rejects +9720521234567 and names the extra zero as the cause. A customer
abroad is sent with --international and the full international number.

The Shabbat and business-hours check runs for template sends only, because a
template may be marketing. Pass --transactional for a utility or
authentication template (an order update or an OTP) to skip it. Free-form
replies (text, interactive, list) are in-window replies and are not checked.

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

    # Named template parameters ({{first_name}}) and a URL button suffix
    # (a tracking link, or the code for a copy-code / one-tap OTP template)
    python send_whatsapp.py --mode template --to 0521234567 --transactional \
        --template-name shipping_update_he \
        --named-parameters first_name=ישראל order_id=A1234 \
        --button-url-param A1234 --dry-run

    # A customer abroad (order updates to a tourist or an overseas buyer)
    python send_whatsapp.py --mode template --international --to +447700900123 \
        --template-name order_confirmation_en --language en --transactional --dry-run

    # Send to a business-scoped user ID (a customer who has a username and
    # arrived with no phone number). Goes in the "recipient" field.
    python send_whatsapp.py --mode template --recipient "<BSUID from webhook>" \
        --template-name order_update_he --dry-run

    # Send a MARKETING template through the Marketing Messages API
    # (POST /<PHONE_NUMBER_ID>/marketing_messages). Cloud API /messages stops
    # accepting marketing templates on 13 October 2027.
    python send_whatsapp.py --mode template --endpoint marketing \
        --to 0521234567 --template-name holiday_sale_he --dry-run

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

# Israel time zone. Prefer pytz when installed, otherwise the standard
# library's zoneinfo (Python 3.9+). Before this fallback the Shabbat and
# business-hours check was silently skipped whenever pytz was missing.
try:
    import pytz
    ISRAEL_TZ = pytz.timezone('Asia/Jerusalem')
except ImportError:
    try:
        from zoneinfo import ZoneInfo
        ISRAEL_TZ = ZoneInfo('Asia/Jerusalem')
    except Exception:  # no tz database available on this machine
        ISRAEL_TZ = None


API_VERSION = "v26.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Israeli mobile prefixes carried on WhatsApp. Written as an explicit
# alternation rather than a character range: the old pattern was 05[0-58],
# a RANGE meaning {0,1,2,3,4,5,8}, which reads like a list and invites the
# next editor to "add 056" as [0-568] and silently admit 056 AND 057.
# 056 (Ooredoo Palestine) and 059 (Jawwal) are +972 mobile ranges used in the
# Palestinian territories only. They are real WhatsApp numbers, so they are
# accepted. 057 is not a current mobile prefix (HOT moved off it in 2014).
MOBILE_PREFIXES = ('050', '051', '052', '053', '054', '055', '056', '058', '059')
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

# What to do for the Cloud API error codes an Israeli integration hits most.
# Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes
ERROR_HINTS = {
    131047: "More than 24 hours since the user last replied. Send an approved "
            "template instead of a free-form message.",
    131026: "Undeliverable: not a WhatsApp number, terms not accepted, or an old "
            "WhatsApp version. Check the number format (972..., no +, no 0).",
    130429: "Rate limit hit. Back off and retry with an increasing delay.",
    131049: "Not delivered to keep ecosystem engagement healthy (per-user "
            "marketing limit). Wait at least 24 hours before resending. For a "
            "US +1 number this is permanent: marketing is not delivered there.",
    131050: "The user stopped marketing messages from your business. Do not "
            "retry; add them to your suppression list.",
    131048: "Sending restricted after too many blocks or spam reports. Stop "
            "campaigns and check quality in WhatsApp Manager.",
    131056: "Too many messages to the same recipient in a short period. Wait "
            "and retry.",
    131042: "Payment method error. Fix billing on the Messaging account.",
    131063: "Marketing templates are disabled on Cloud API for this account. "
            "Resend with --endpoint marketing (Marketing Messages API).",
    130472: "Not sent as part of a Meta marketing message experiment. "
            "Resending gives the same error, so do not retry.",
    130403: "Your business has blocked this user on WhatsApp. Unblock them "
            "first; do not retry.",
    132015: "The template is paused for low quality. Edit it and wait for "
            "re-approval, or use another template.",
    132016: "The template was paused too many times and is permanently "
            "disabled. Create a new template.",
}


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


def parse_name_values(items: list) -> list:
    """Parse 'name=value' named-parameter pairs, checking Meta's name rule."""
    out = []
    for item in items or []:
        if "=" not in item:
            print(f"Error: named parameter must be name=value, got '{item}'")
            sys.exit(1)
        name, value = item.split("=", 1)
        name = name.strip()
        if not re.fullmatch(r'[a-z_]+', name):
            print(f"Error: parameter name '{name}' must be lowercase letters "
                  "and underscores, matching the template's {{name}}")
            sys.exit(1)
        out.append((name, value))
    return out


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


def validate_international_phone(phone: str) -> tuple[bool, str]:
    """Normalise a non-Israeli number given in full international form.

    Accepts '+44 7700 900123' or '447700900123' and returns digits only, as
    the API expects. Israeli numbers belong in validate_israeli_phone().
    """
    clean = re.sub(r'[\s\-\(\)\.\+]', '', phone)
    if clean.startswith('00'):
        clean = clean[2:]
    if not clean.isdigit():
        return False, "International number may contain digits only"
    if clean.startswith('972'):
        return False, "This is an Israeli number: drop --international"
    if clean.startswith('0'):
        return False, ("Give the full international number with its country "
                       "code, e.g. +447700900123")
    if not 8 <= len(clean) <= 15:
        return False, "International number must be 8 to 15 digits with country code"
    return True, clean


def is_valid_sending_time() -> tuple[bool, str]:
    """Check if current time is appropriate for Israeli business messaging.

    Returns:
        Tuple of (is_ok, message).
    """
    if ISRAEL_TZ is None:
        return False, ("No time zone database available, so the Shabbat and "
                       "business-hours check cannot run. Install pytz or "
                       "tzdata, or pass --skip-time-check deliberately.")

    now = datetime.now(ISRAEL_TZ)
    day = now.weekday()  # 0=Monday, 6=Sunday

    # Friday after 14:00 -- pre-Shabbat. Saturday evening also falls outside
    # the 20:00 business-hours cutoff below, so the next window is Sunday.
    if day == 4 and now.time() > time(14, 0):
        return False, "Pre-Shabbat hours. Next send window: Sunday 08:30."

    # Saturday -- Shabbat, then after 20:00 outside business hours
    if day == 5:
        return False, "Shabbat or Saturday night. Next send window: Sunday 08:30."

    # Business hours check
    if now.time() < time(8, 30) or now.time() > time(20, 0):
        return False, "Outside business hours (08:30-20:00 Israel time)."

    return True, "OK to send."


def recipient_fields(to: str) -> dict:
    """Return the addressing fields for a payload.

    A phone number goes in "to". A business-scoped user ID (BSUID), passed
    with a "bsuid:" prefix by main(), goes in "recipient". The two are never
    sent together: when both are present Meta uses the phone number.
    """
    if to.startswith("bsuid:"):
        return {"recipient_type": "individual", "recipient": to[len("bsuid:"):]}
    return {"to": to}


def send_template_message(phone_number_id: str, access_token: str,
                          to: str, template_name: str, language: str,
                          parameters: list, endpoint: str = "messages",
                          named: bool = False,
                          button_url_param: str = None,
                          button_index: int = 0,
                          header_media: tuple = None) -> dict:
    """Send a WhatsApp template message.

    Args:
        phone_number_id: WhatsApp Business Phone Number ID.
        access_token: Meta System User Access Token.
        to: Recipient number (format: 972XXXXXXXXX), or "bsuid:<BSUID>".
        template_name: Approved template name.
        language: Template language code (e.g., "he" for Hebrew).
        parameters: List of template parameter values, or of (name, value)
            pairs when named is True.
        named: Send parameters with parameter_name, for a template created
            with parameter_format "named".
        button_url_param: Dynamic suffix for the template's URL button
            (a tracking code, or the OTP for a copy-code template).
        button_index: Position of that URL button among the template's
            buttons (0 = first).
        header_media: (type, ref) for a template with a media header, type
            being image, document or video and ref an uploaded media ID or an
            https link to hosted media (Meta does not recommend links).
            Meta's pages show no send shape for a text-header variable, so
            this function does not build one.
        endpoint: "messages" (Cloud API) or "marketing_messages"
            (Marketing Messages API, for templates whose latest category is
            MARKETING).

    Returns:
        API response as dict.
    """
    url = f"{BASE_URL}/{phone_number_id}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        **recipient_fields(to),
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
        }
    }

    components = []
    if header_media:
        mtype, ref = header_media
        media = {"link": ref} if ref.startswith("https://") else {"id": ref}
        components.append({"type": "header",
                           "parameters": [{"type": mtype, mtype: media}]})
    if parameters:
        if named:
            body_params = [{"type": "text", "parameter_name": k, "text": v}
                           for k, v in parameters]
        else:
            body_params = [{"type": "text", "text": p} for p in parameters]
        components.append({"type": "body", "parameters": body_params})
    if button_url_param:
        components.append({
            "type": "button", "sub_type": "url", "index": str(button_index),
            "parameters": [{"type": "text", "text": button_url_param}],
        })
    if components:
        payload["template"]["components"] = components

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
        **recipient_fields(to),
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
        **recipient_fields(to),
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
        **recipient_fields(to),
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
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--to", help="Recipient phone number")
    target.add_argument("--recipient",
                        help="Business-scoped user ID (BSUID) from a webhook, "
                             "for a customer with no phone number on file")
    parser.add_argument("--international", action="store_true",
                        help="--to is a non-Israeli number in full "
                             "international form, e.g. +447700900123")
    parser.add_argument("--transactional", action="store_true",
                        help="The template's LATEST category (it can change "
                             "after approval) is utility or authentication: "
                             "skip the Shabbat and business-hours check")
    parser.add_argument("--endpoint", choices=["messages", "marketing"],
                        default="messages",
                        help="'marketing' sends a template through the "
                             "Marketing Messages API (/marketing_messages)")
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
    params = parser.add_mutually_exclusive_group()
    params.add_argument("--parameters", nargs="*",
                        help="Positional template parameters ({{1}}, {{2}}...)")
    params.add_argument("--named-parameters", nargs="*",
                        help="Named template parameters as name=value, for a "
                             "template created with parameter_format named")
    parser.add_argument("--button-url-param",
                        help="Dynamic suffix for the URL button at index 0 "
                             "(tracking code, or the OTP for a copy-code template)")
    parser.add_argument("--button-index", type=int, default=0,
                        help="Position of the URL button among the template's "
                             "buttons (default 0, the first)")
    parser.add_argument("--header-media",
                        help="Media header as type:ref, type being image, "
                             "document or video and ref an uploaded media ID or "
                             "an https link (e.g. document:1234567890)")

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

    if args.endpoint == "marketing" and args.mode != "template":
        print("Error: --endpoint marketing sends template messages only")
        sys.exit(1)

    # Validate the recipient
    if args.recipient:
        if not args.recipient.strip():
            print("Error: --recipient is empty")
            sys.exit(1)
        normalized = "bsuid:" + args.recipient.strip()
    else:
        validator = (validate_international_phone if args.international
                     else validate_israeli_phone)
        is_valid, normalized = validator(args.to)
        if not is_valid:
            print(f"Error: {normalized}")
            sys.exit(1)

    if args.mode != "template" and (args.named_parameters or args.button_url_param
                                    or args.header_media):
        print("Error: --named-parameters, --button-url-param and --header-media "
              "apply to template mode")
        sys.exit(1)
    header_media = None
    if args.header_media:
        mtype, _, media_id = args.header_media.partition(":")
        if mtype not in ("image", "document", "video") or not media_id.strip():
            print("Error: --header-media must be image:, document: or video: "
                  "followed by a media ID or an https:// link")
            sys.exit(1)
        media_id = media_id.strip()
        if media_id.startswith("http") and not media_id.startswith("https://"):
            print("Error: a --header-media link must be https://")
            sys.exit(1)
        header_media = (mtype, media_id)
    if args.button_index < 0:
        print("Error: --button-index must be 0 or more")
        sys.exit(1)
    if args.endpoint == "marketing" and args.transactional:
        print("Error: --transactional and --endpoint marketing contradict each other")
        sys.exit(1)

    # Check sending time. Only template sends can be marketing; free-form
    # replies (text, interactive, list) are in-window answers to the user.
    needs_time_check = args.mode == "template" and not args.transactional
    if needs_time_check and not args.skip_time_check:
        time_ok, time_msg = is_valid_sending_time()
        if not time_ok:
            print(f"Warning: {time_msg}")
            print("Use --skip-time-check to override.")
            sys.exit(1)

    shown = normalized.replace("bsuid:", "BSUID ", 1)
    print(f"Sending {args.mode} message to: {shown}")

    # Send based on mode
    if args.mode == "template":
        if not args.template_name:
            print("Error: --template-name required for template mode")
            sys.exit(1)
        named = bool(args.named_parameters)
        values = (parse_name_values(args.named_parameters) if named
                  else (args.parameters or []))
        result = send_template_message(
            args.phone_id, args.access_token, normalized,
            args.template_name, args.language, values,
            "marketing_messages" if args.endpoint == "marketing" else "messages",
            named=named, button_url_param=args.button_url_param,
            button_index=args.button_index, header_media=header_media
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
        try:
            hint = ERROR_HINTS.get(int(err.get("code")))
        except (TypeError, ValueError):
            hint = None
        if hint:
            print(f"What to do: {hint}")
        sys.exit(1)
    else:
        msg_id = result.get("messages", [{}])[0].get("id", "N/A")
        print("Message sent successfully!" if not args.dry_run
              else "Dry run complete, nothing was sent.")
        print(f"Message ID: {msg_id}")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
