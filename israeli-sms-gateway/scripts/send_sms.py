#!/usr/bin/env python3
"""Send SMS via Israeli SMS gateway providers, and estimate Hebrew segment cost.

Usage:
    python send_sms.py --provider sms4free --to 054-1234567 --message "Hello" \
        --api-key YOUR_KEY --user YOUR_USER --pass-key YOUR_PASS --sender MySender

    python send_sms.py --provider twilio --to 054-1234567 --message "Hello" \
        --account-sid YOUR_SID --auth-token YOUR_TOKEN --from-number +972XXXXXXX

    python send_sms.py --provider inforu --to 054-1234567 --message "שלום" \
        --user YOUR_USER --api-key YOUR_API_TOKEN --sender MyBrand

    # Cost/segment estimate only, no network call and no credentials needed:
    python send_sms.py --estimate --message "שלום, ההזמנה שלך יצאה למשלוח" \
        --price-per-segment 0.09

Environment variables (alternative to CLI args):
    SMS_PROVIDER        Provider name (sms4free, twilio, inforu)
    SMS_API_KEY         API key (sms4free) or API token (inforu)
    SMS_USER            Username (sms4free, inforu)
    SMS_PASS_KEY        Pass key (sms4free)
    SMS_SENDER          Sender ID
    TWILIO_ACCOUNT_SID  Twilio Account SID
    TWILIO_AUTH_TOKEN   Twilio Auth Token
    TWILIO_FROM_NUMBER  Twilio sender number
"""

import argparse
import base64
import os
import re
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


# --------------------------------------------------------------------------
# Phone validation
# --------------------------------------------------------------------------

# Explicit alternation, not a character range. See validate_phone.py for the
# full rationale: 056 and 059 are Palestinian networks and 057 is retired, so a
# range like 05[0-8] quietly admits numbers this skill is supposed to reject.
MOBILE_RE = re.compile(r'^(?:050|051|052|053|054|055|058)\d{7}$')
LANDLINE_GEO_RE = re.compile(r'^0(?:2|3|4|8|9)\d{7}$')
LANDLINE_NONGEO_RE = re.compile(r'^07\d{8}$')
PALESTINIAN_MOBILE_PREFIXES = ('056', '059')


def validate_israeli_phone(phone: str) -> tuple[bool, str]:
    """Validate and normalize an Israeli phone number to international format."""
    raw = re.sub(r'[\s\-\(\)\.]', '', phone)
    clean = raw
    if clean.startswith('+972'):
        clean = '0' + clean[4:]
    elif clean.startswith('972'):
        clean = '0' + clean[3:]

    if (raw.startswith('+972') or raw.startswith('972')) and clean.startswith('00'):
        return False, ('Invalid: an extra leading zero. In +972 form the national '
                       'trunk 0 is dropped (050-1234567 becomes +972501234567).')

    if MOBILE_RE.match(clean):
        return True, '+972' + clean[1:]

    if clean[:3] in PALESTINIAN_MOBILE_PREFIXES:
        return False, (f'Rejected: {clean[:3]} is a Palestinian mobile network '
                       '(056 Ooredoo Palestine, 059 Jawwal), not an Israeli one.')

    if LANDLINE_GEO_RE.match(clean) or LANDLINE_NONGEO_RE.match(clean):
        return True, '+972' + clean[1:]

    return False, 'Invalid Israeli phone number'


# --------------------------------------------------------------------------
# Encoding + segmentation
# --------------------------------------------------------------------------

# GSM 03.38 basic character set. Anything outside it (every Hebrew letter, and
# the emoji people paste into marketing copy) forces the whole message to UCS-2.
GSM7_BASIC = (
    '@£$¥èéùìòÇ\nØø\rÅå'
    'Δ_ΦΓΛΩΠΨΣΘΞÆæßÉ'
    ' !"#¤%&\'()*+,-./0123456789:;<=>?'
    '¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§'
    '¿abcdefghijklmnopqrstuvwxyzäöñüà'
)
# Characters reachable only through the escape sequence; each costs 2 septets.
GSM7_EXTENDED = '^{}\\[~]|€'

GSM7_SINGLE, GSM7_MULTI = 160, 153
UCS2_SINGLE, UCS2_MULTI = 70, 67


def segment_count(message: str) -> dict:
    """Report the encoding, unit count, and number of SMS segments.

    A carrier bills per segment, not per send. A Hebrew message is UCS-2, so it
    fits 70 characters in one segment and only 67 per segment once it splits,
    because the concatenation header (UDH) eats into the payload. A Latin GSM-7
    message gets 160 and 153. Mixing one Hebrew character into a Latin message
    downgrades the entire message to UCS-2 and cuts its capacity by more than
    half, which is the usual cause of a campaign costing twice its estimate.

    Args:
        message: The message text as it will be sent.

    Returns:
        Dict with encoding, units, per-segment capacity, and segment count.
    """
    if all(c in GSM7_BASIC or c in GSM7_EXTENDED for c in message):
        encoding = 'GSM-7'
        units = sum(2 if c in GSM7_EXTENDED else 1 for c in message)
        single, multi = GSM7_SINGLE, GSM7_MULTI
    else:
        encoding = 'UCS-2'
        # UCS-2 bills per 16-bit code unit, so an astral character (an emoji,
        # for instance) is a surrogate pair and costs two units, not one.
        units = sum(2 if ord(c) > 0xFFFF else 1 for c in message)
        single, multi = UCS2_SINGLE, UCS2_MULTI

    if units == 0:
        segments = 0
    elif units <= single:
        segments = 1
    else:
        segments = -(-units // multi)  # ceiling division

    return {
        'encoding': encoding,
        'units': units,
        'per_segment': single if segments <= 1 else multi,
        'segments': segments,
    }


def _safe_json(response):
    """Parse a JSON body without letting a non-JSON error page crash the caller.

    Gateways return HTML maintenance pages, WAF blocks, and plain-text codes.
    `response.json()` raises JSONDecodeError, which is NOT a RequestException,
    so it escapes the usual `except requests.RequestException` block.
    """
    try:
        return response.json(), None
    except ValueError:
        body = (response.text or '').strip()
        return None, f'Non-JSON response (HTTP {response.status_code}): {body[:200]}'


# --------------------------------------------------------------------------
# Providers
# --------------------------------------------------------------------------

def send_sms4free(to: str, message: str, api_key: str, user: str,
                  pass_key: str, sender: str) -> dict:
    """Send SMS via SMS4Free (api.sms4free.co.il), v2 JSON endpoint.

    v1 (/ApiSMS/SendSMS) answers with a bare integer body and v2
    (/ApiSMS/v2/SendSMS) answers with a JSON envelope, so the two cannot share
    a parser. This function targets v2 and reads the envelope. Only -1
    (authentication failure) is a documented, observed code; every other
    outcome is reported using the API's own `message` field verbatim rather
    than a guessed lookup table.

    Args:
        to: Recipient phone number (international format).
        message: Message text (Hebrew supported).
        api_key: SMS4Free API key.
        user: SMS4Free username (the mobile number used at signup).
        pass_key: SMS4Free account password.
        sender: Sender ID (numeric sender IDs need one-time ownership proof).

    Returns:
        Dict with status and response details.
    """
    url = 'https://api.sms4free.co.il/ApiSMS/v2/SendSMS'
    payload = {
        'key': api_key,
        'user': user,
        'pass': pass_key,
        'sender': sender,
        'recipient': to.replace('+', ''),
        'msg': message,
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
    except requests.RequestException as e:
        return {'success': False, 'status': f'Request failed: {e}', 'provider': 'sms4free'}

    result, err = _safe_json(response)
    if err:
        return {'success': False, 'status': err, 'provider': 'sms4free'}

    status = result.get('status')
    # A positive status is the count of messages accepted. It is NOT the
    # literal string "1": comparing against "1" reports failure on every
    # successful multi-recipient send.
    success = isinstance(status, int) and status > 0

    if status == -1:
        detail = 'Authentication failed (key, user, or pass rejected)'
    else:
        # Surface the API's own wording instead of inventing a code table.
        detail = result.get('message') or f'status={status}'

    return {
        'success': success,
        'status': detail,
        'raw_response': result,
        'provider': 'sms4free',
    }


def send_twilio(to: str, message: str, account_sid: str,
                auth_token: str, from_number: str) -> dict:
    """Send SMS via Twilio.

    Args:
        to: Recipient phone number (international format).
        message: Message text.
        account_sid: Twilio Account SID.
        auth_token: Twilio Auth Token.
        from_number: Sender phone number (Twilio number) or registered sender ID.

    Returns:
        Dict with status and response details.
    """
    api_base = 'https://api.twilio.com/2010-04-01'
    url = f'{api_base}/Accounts/{account_sid}/Messages.json'
    data = {'To': to, 'From': from_number, 'Body': message}

    try:
        response = requests.post(url, data=data, auth=(account_sid, auth_token), timeout=30)
    except requests.RequestException as e:
        return {'success': False, 'status': f'Request failed: {e}', 'provider': 'twilio'}

    result, err = _safe_json(response)
    if err:
        return {'success': False, 'status': err, 'provider': 'twilio'}

    if response.status_code != 201:
        # Twilio puts the actionable part of a failure in code + message, which
        # a bare result.get("status") silently discards.
        code = result.get('code', 'unknown')
        detail = result.get('message', 'no message returned')
        more_info = result.get('more_info', '')
        return {
            'success': False,
            'status': f'Twilio error {code}: {detail} {more_info}'.strip(),
            'raw_response': result,
            'provider': 'twilio',
        }

    return {
        'success': True,
        'status': result.get('status', 'unknown'),
        'message_sid': result.get('sid', ''),
        'raw_response': result,
        'provider': 'twilio',
    }


def send_inforu(to: str, message: str, user: str, api_token: str, sender: str) -> dict:
    """Send SMS via InforUMobile.

    Contract per InforU's published API collection:
        POST https://capi.inforu.co.il/api/v2/SMS/SendSms
        Authorization: Basic base64("<username>:<api token>")
        Body is envelope-wrapped under a top-level "Data" key.

    The credential pair is username plus API TOKEN, not the account password,
    and the header value must be genuinely base64-encoded. Responses carry
    StatusId and StatusDescription; StatusId 1 is success.

    Args:
        to: Recipient phone number (international format).
        message: Message text (Hebrew supported).
        user: InforUMobile username.
        api_token: InforUMobile API token.
        sender: Sender name or number.

    Returns:
        Dict with status and response details.
    """
    url = 'https://capi.inforu.co.il/api/v2/SMS/SendSms'
    credentials = base64.b64encode(f'{user}:{api_token}'.encode('utf-8')).decode('ascii')
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json; charset=utf-8',
    }
    payload = {
        'Data': {
            'Message': message,
            'Recipients': [{'Phone': to.replace('+', '')}],
            'Settings': {'Sender': sender},
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
    except requests.RequestException as e:
        return {'success': False, 'status': f'Request failed: {e}', 'provider': 'inforu'}

    result, err = _safe_json(response)
    if err:
        return {'success': False, 'status': err, 'provider': 'inforu'}

    status_id = result.get('StatusId')
    detail = result.get('StatusDescription', 'unknown')
    detailed = result.get('DetailedDescription')
    if detailed:
        detail = f'{detail} ({detailed})'

    return {
        'success': status_id == 1,
        'status': detail,
        'raw_response': result,
        'provider': 'inforu',
    }


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def print_estimate(message: str, price_per_segment: float | None, recipients: int) -> None:
    info = segment_count(message)
    print(f'Encoding:     {info["encoding"]}')
    print(f'Units:        {info["units"]}')
    print(f'Per segment:  {info["per_segment"]}')
    print(f'Segments:     {info["segments"]}')
    if info['encoding'] == 'UCS-2':
        print('Note: UCS-2 (Hebrew or any non-GSM-7 character) fits 70 units in a '
              'single segment and 67 per segment once split.')
    if price_per_segment is not None:
        total = info['segments'] * price_per_segment * recipients
        print(f'Recipients:   {recipients}')
        print(f'Estimated cost: {total:.4f} per the unit you passed to '
              f'--price-per-segment ({price_per_segment} x {info["segments"]} '
              f'segments x {recipients} recipients)')


def main():
    parser = argparse.ArgumentParser(
        description='Send SMS via Israeli SMS gateway providers, or estimate segments and cost.'
    )
    parser.add_argument('--provider', choices=['sms4free', 'twilio', 'inforu'],
                        default=os.environ.get('SMS_PROVIDER', 'sms4free'),
                        help='SMS provider to use')
    parser.add_argument('--to', help='Recipient phone number (not needed with --estimate)')
    parser.add_argument('--message', required=True, help='Message text')

    parser.add_argument('--estimate', action='store_true',
                        help='Only report encoding, segment count, and estimated cost. No network call.')
    parser.add_argument('--price-per-segment', type=float, default=None,
                        help='Your negotiated price per SEGMENT, used with --estimate')
    parser.add_argument('--recipients', type=int, default=1,
                        help='Recipient count for the --estimate cost total')

    # SMS4Free / InforU options
    parser.add_argument('--api-key', default=os.environ.get('SMS_API_KEY'),
                        help='API key (sms4free) or API token (inforu)')
    parser.add_argument('--user', default=os.environ.get('SMS_USER'),
                        help='Username (sms4free, inforu)')
    parser.add_argument('--pass-key', default=os.environ.get('SMS_PASS_KEY'),
                        help='Account password (sms4free)')
    parser.add_argument('--sender', default=os.environ.get('SMS_SENDER'),
                        help='Sender ID')

    # Twilio options
    parser.add_argument('--account-sid', default=os.environ.get('TWILIO_ACCOUNT_SID'),
                        help='Twilio Account SID')
    parser.add_argument('--auth-token', default=os.environ.get('TWILIO_AUTH_TOKEN'),
                        help='Twilio Auth Token')
    parser.add_argument('--from-number', default=os.environ.get('TWILIO_FROM_NUMBER'),
                        help='Twilio sender number')

    args = parser.parse_args()

    if args.estimate:
        print_estimate(args.message, args.price_per_segment, args.recipients)
        return

    if not args.to:
        print('Error: --to is required unless you pass --estimate')
        sys.exit(1)

    is_valid, normalized = validate_israeli_phone(args.to)
    if not is_valid:
        print(f'Error: {normalized}')
        sys.exit(1)

    info = segment_count(args.message)
    print(f'Sending to: {normalized} via {args.provider}')
    print(f'Encoding: {info["encoding"]}, segments billed: {info["segments"]}')

    if args.provider == 'sms4free':
        if not all([args.api_key, args.user, args.pass_key, args.sender]):
            print('Error: sms4free requires --api-key, --user, --pass-key, --sender')
            sys.exit(1)
        result = send_sms4free(normalized, args.message, args.api_key,
                               args.user, args.pass_key, args.sender)

    elif args.provider == 'twilio':
        if not all([args.account_sid, args.auth_token, args.from_number]):
            print('Error: twilio requires --account-sid, --auth-token, --from-number')
            sys.exit(1)
        result = send_twilio(normalized, args.message, args.account_sid,
                             args.auth_token, args.from_number)

    elif args.provider == 'inforu':
        if not all([args.api_key, args.user, args.sender]):
            print('Error: inforu requires --user, --api-key (the API token), --sender')
            sys.exit(1)
        result = send_inforu(normalized, args.message, args.user, args.api_key, args.sender)

    if result['success']:
        print(f'SMS sent successfully via {result["provider"]}')
        print(f'Status: {result["status"]}')
    else:
        print(f'SMS failed via {result["provider"]}')
        print(f'Status: {result["status"]}')
        sys.exit(1)


if __name__ == '__main__':
    main()
