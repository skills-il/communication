#!/usr/bin/env python3
"""Send SMS via Israeli SMS gateway providers.

Usage:
    python send_sms.py --provider sms4free --to 054-1234567 --message "Hello" \
        --api-key YOUR_KEY --user YOUR_USER --pass-key YOUR_PASS --sender MySender

    python send_sms.py --provider twilio --to 054-1234567 --message "Hello" \
        --account-sid YOUR_SID --auth-token YOUR_TOKEN --from-number +972XXXXXXX

Environment variables (alternative to CLI args):
    SMS_PROVIDER        Provider name (sms4free, twilio, inforu)
    SMS_API_KEY         API key for the provider
    SMS_USER            Username (sms4free)
    SMS_PASS_KEY        Pass key (sms4free)
    SMS_SENDER          Sender ID
    TWILIO_ACCOUNT_SID  Twilio Account SID
    TWILIO_AUTH_TOKEN   Twilio Auth Token
    TWILIO_FROM_NUMBER  Twilio sender number
"""

import argparse
import os
import re
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


def validate_israeli_phone(phone: str) -> tuple[bool, str]:
    """Validate and normalize Israeli phone number to international format."""
    clean = re.sub(r'[\s\-\(\)\.]', '', phone)

    if clean.startswith('+972'):
        clean = '0' + clean[4:]
    elif clean.startswith('972'):
        clean = '0' + clean[3:]

    if re.match(r'^05[0-8]\d{7}$', clean):
        return True, '+972' + clean[1:]

    if re.match(r'^0[2-9]\d{7,8}$', clean):
        return True, '+972' + clean[1:]

    return False, "Invalid Israeli phone number"


def send_sms4free(to: str, message: str, api_key: str, user: str,
                  pass_key: str, sender: str) -> dict:
    """Send SMS via SMS4Free (sms4free.co.il).

    Args:
        to: Recipient phone number (international format).
        message: Message text (Hebrew supported).
        api_key: SMS4Free API key.
        user: SMS4Free username.
        pass_key: SMS4Free pass key.
        sender: Sender ID (must be registered).

    Returns:
        Dict with status and response details.
    """
    url = "https://www.sms4free.co.il/ApiSMS/SendSMS"
    params = {
        "key": api_key,
        "user": user,
        "pass": pass_key,
        "sender": sender,
        "recipient": to.replace('+', ''),
        "msg": message
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response_text = response.text.strip()

        # SMS4Free returns numeric codes
        status_codes = {
            "1": "Success",
            "-1": "Authentication failed",
            "-2": "Invalid XML",
            "-3": "Insufficient credits",
            "-4": "Invalid recipient",
            "-5": "Sender not approved",
        }

        status = status_codes.get(response_text, f"Unknown ({response_text})")
        return {
            "success": response_text == "1",
            "status": status,
            "raw_response": response_text,
            "provider": "sms4free"
        }
    except requests.RequestException as e:
        return {"success": False, "status": f"Request failed: {e}", "provider": "sms4free"}


def send_twilio(to: str, message: str, account_sid: str,
                auth_token: str, from_number: str) -> dict:
    """Send SMS via Twilio.

    Args:
        to: Recipient phone number (international format).
        message: Message text.
        account_sid: Twilio Account SID.
        auth_token: Twilio Auth Token.
        from_number: Sender phone number (Twilio number).

    Returns:
        Dict with status and response details.
    """
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    data = {
        "To": to,
        "From": from_number,
        "Body": message
    }

    try:
        response = requests.post(url, data=data, auth=(account_sid, auth_token), timeout=30)
        result = response.json()

        return {
            "success": response.status_code == 201,
            "status": result.get("status", "unknown"),
            "message_sid": result.get("sid", ""),
            "raw_response": result,
            "provider": "twilio"
        }
    except requests.RequestException as e:
        return {"success": False, "status": f"Request failed: {e}", "provider": "twilio"}


def send_inforu(to: str, message: str, api_token: str, sender: str) -> dict:
    """Send SMS via InforUMobile.

    Args:
        to: Recipient phone number (international format).
        message: Message text (Hebrew supported).
        api_token: InforUMobile API token.
        sender: Sender name/number.

    Returns:
        Dict with status and response details.
    """
    url = "https://api.inforu.co.il/SendSMS/SendSMS"
    headers = {
        "Authorization": f"Basic {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "Message": message,
        "Recipients": [{"Phone": to.replace('+', '')}],
        "Settings": {
            "Sender": sender
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        result = response.json()
        return {
            "success": response.status_code == 200,
            "status": result.get("StatusDescription", "unknown"),
            "raw_response": result,
            "provider": "inforu"
        }
    except requests.RequestException as e:
        return {"success": False, "status": f"Request failed: {e}", "provider": "inforu"}


def main():
    parser = argparse.ArgumentParser(
        description="Send SMS via Israeli SMS gateway providers"
    )
    parser.add_argument("--provider", choices=["sms4free", "twilio", "inforu"],
                        default=os.environ.get("SMS_PROVIDER", "sms4free"),
                        help="SMS provider to use")
    parser.add_argument("--to", required=True, help="Recipient phone number")
    parser.add_argument("--message", required=True, help="Message text")

    # SMS4Free / InforU options
    parser.add_argument("--api-key", default=os.environ.get("SMS_API_KEY"),
                        help="API key for the provider")
    parser.add_argument("--user", default=os.environ.get("SMS_USER"),
                        help="Username (sms4free)")
    parser.add_argument("--pass-key", default=os.environ.get("SMS_PASS_KEY"),
                        help="Pass key (sms4free)")
    parser.add_argument("--sender", default=os.environ.get("SMS_SENDER"),
                        help="Sender ID")

    # Twilio options
    parser.add_argument("--account-sid", default=os.environ.get("TWILIO_ACCOUNT_SID"),
                        help="Twilio Account SID")
    parser.add_argument("--auth-token", default=os.environ.get("TWILIO_AUTH_TOKEN"),
                        help="Twilio Auth Token")
    parser.add_argument("--from-number", default=os.environ.get("TWILIO_FROM_NUMBER"),
                        help="Twilio sender number")

    args = parser.parse_args()

    # Validate phone number
    is_valid, normalized = validate_israeli_phone(args.to)
    if not is_valid:
        print(f"Error: {normalized}")
        sys.exit(1)

    print(f"Sending to: {normalized} via {args.provider}")

    # Send based on provider
    if args.provider == "sms4free":
        if not all([args.api_key, args.user, args.pass_key, args.sender]):
            print("Error: sms4free requires --api-key, --user, --password, --sender")
            sys.exit(1)
        result = send_sms4free(normalized, args.message, args.api_key,
                               args.user, args.pass_key, args.sender)

    elif args.provider == "twilio":
        if not all([args.account_sid, args.auth_token, args.from_number]):
            print("Error: twilio requires --account-sid, --auth-token, --from-number")
            sys.exit(1)
        result = send_twilio(normalized, args.message, args.account_sid,
                             args.auth_token, args.from_number)

    elif args.provider == "inforu":
        if not all([args.api_key, args.sender]):
            print("Error: inforu requires --api-key, --sender")
            sys.exit(1)
        result = send_inforu(normalized, args.message, args.api_key, args.sender)

    # Output result
    if result["success"]:
        print(f"SMS sent successfully via {result['provider']}")
        print(f"Status: {result['status']}")
    else:
        print(f"SMS failed via {result['provider']}")
        print(f"Status: {result['status']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
