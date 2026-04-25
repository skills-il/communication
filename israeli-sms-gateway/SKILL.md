---
name: israeli-sms-gateway
description: Integrate with Israeli SMS gateway providers for business messaging, OTP, and notifications. Use when user asks about sending SMS in Israel, Israeli SMS providers, phone number validation (Israeli format), OTP implementation, bulk SMS, or SMS marketing compliance. Covers 019 SMS, InforUMobile, SMS4Free, and international providers with Israeli support. Do NOT use for WhatsApp Business API (see separate skill) or non-Israeli telecom.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires API key from chosen SMS provider. Network access required.
version: 1.1.0
---

# Israeli SMS Gateway

## Instructions

### Step 1: Validate Israeli Phone Number
Before sending, validate the phone number format:

```python
import re

def validate_israeli_phone(phone: str) -> tuple[bool, str]:
    """Validate and normalize Israeli phone number."""
    # Remove spaces, dashes, parentheses
    clean = re.sub(r'[\s\-\(\)]', '', phone)

    # Handle +972 prefix
    if clean.startswith('+972'):
        clean = '0' + clean[4:]
    elif clean.startswith('972'):
        clean = '0' + clean[3:]

    # Validate mobile: 05X-XXXXXXX (10 digits, prefixes 050-059)
    if re.match(r'^05[0-9]\d{7}$', clean):
        return True, '+972' + clean[1:]

    # Validate landline: 0X-XXXXXXX (9-10 digits)
    if re.match(r'^0[2-9]\d{7,8}$', clean):
        return True, '+972' + clean[1:]

    return False, "Invalid Israeli phone number"
```

### Step 2: Choose Provider

| Provider | Best For | API Type | Pricing (2026, ex-VAT) |
|----------|----------|----------|------------------------|
| 019 SMS (019 Telecom) | Israeli enterprise, banks | REST | ~0.06-0.10 NIS/SMS, package-based |
| InforUMobile | Marketing, bulk campaigns | REST + SOAP | ~0.07-0.12 NIS/SMS, package-based |
| SMS4Free | Startups, dev/test | REST | Pay per message, free tier deprecated |
| ActiveTrail | Marketing automation | REST | Bundled with email plans |
| Cellact | Enterprise, OTP | REST | Volume pricing |
| Twilio | Global apps targeting +972 | REST | ~$0.04-0.05 USD/SMS to Israel |
| Vonage | Multi-region apps | REST | Volume pricing |
| MessageBird/Bird | Multi-channel | REST | Volume pricing |

Israeli providers (019, InforU, Cellact, ActiveTrail) generally offer cheaper local rates and easier sender ID registration than international providers, but require an Israeli business entity. International providers (Twilio, Vonage, Bird) bill in USD/EUR and route through international carriers, which can affect deliverability and per-message cost.

### Step 3: Send SMS

**InforUMobile example (REST):**
```python
import os
import requests

def send_sms_inforu(to: str, message: str, sender: str) -> dict:
    """Send SMS via InforUMobile REST API.

    Credentials are read from env vars (INFORU_USER, INFORU_PASS).
    Endpoints and exact field names should be confirmed against current
    InforU documentation, which evolves between API versions.
    """
    user = os.environ["INFORU_USER"]
    password = os.environ["INFORU_PASS"]

    payload = {
        "Data": {
            "Message": message,
            "Recipients": [{"Phone": to}],
            "Settings": {"Sender": sender},
        },
        "User": {"Username": user, "Password": password},
    }
    response = requests.post(
        "https://uapi.inforu.co.il/SendMessageXml.ashx",
        json=payload,
        timeout=15,
    )
    return response.json()
```

**Twilio example (international):**
```python
import os
from twilio.rest import Client

def send_sms_twilio(to: str, message: str) -> str:
    """Send SMS via Twilio. `to` must be in +972 international format."""
    client = Client(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"],
    )
    msg = client.messages.create(
        body=message,
        from_=os.environ["TWILIO_FROM"],  # alphanumeric sender ID or +E.164
        to=to,
    )
    return msg.sid
```

**SMS4Free note:** the SMS4Free public API has shifted endpoints multiple times. If you depend on it, fetch the current endpoint from `api.sms4free.co.il` documentation rather than hard-coding URLs from older tutorials. Treat the legacy `https://api.sms4free.co.il/ApiSMS/v2/SendSMS` documentation as a baseline and re-verify before production use.

### Step 4: Compliance Checklist (Chok HaSpam + Privacy Law Amendment 13)

Israeli commercial SMS is governed by Amendment 40 to the Communications (Bezeq and Broadcasts) Law (Chok HaSpam) and, since 14 August 2025, by Amendment 13 to the Privacy Protection Law, which significantly raised obligations on processors of personal data and aligned Israeli rules more closely with the EU GDPR.

Before sending commercial SMS:
- [ ] Recipient gave explicit prior opt-in (active choice, not pre-ticked box)
- [ ] Opt-in record stored: who, what they consented to, timestamp, channel
- [ ] Sender identity clearly stated in the message body
- [ ] Free, easy unsubscribe in every message (reply `עצור` / `STOP`, link, or short code)
- [ ] Unsubscribes processed and honoured within reasonable time (do not retry the same recipient)
- [ ] Sender ID (alphanumeric or short code) registered with provider where required
- [ ] Message content complies with Israeli Consumer Protection rules (no misleading offers, prices in NIS incl. VAT)
- [ ] Phone numbers obtained lawfully under Privacy Law Amendment 13 (purpose limitation, data minimisation, security)
- [ ] No transfer abroad of recipient lists without ensuring adequate protection (Amendment 13 cross-border rules)
- [ ] Sending during reasonable hours (avoid Shabbat for religious recipients, avoid late night)
- [ ] Penalty awareness: civil cause of action up to 1,000 NIS per unsolicited message without proof of damages, plus regulatory fines (Privacy Protection Authority can issue administrative fines under Amendment 13).

## Examples

### Example 1: Send OTP
User says: "Send a verification code to an Israeli mobile number."
Result: Generate a 6-digit code, send via the provider API, log delivery status, expire the code in your backend after 5-10 minutes. OTP messages are transactional, not marketing, so they are not subject to opt-in (Chok HaSpam exempts service messages tied to a transaction the user initiated).

### Example 2: Format Phone Number
User says: "Convert 054-1234567 to international format."
Result: `+972541234567`.

### Example 3: Bulk Marketing SMS
User says: "Send a promotional SMS to my customer list about a holiday sale."
Actions:
1. Validate every phone number (normalise to `+972` international format, drop the local 0).
2. Filter the list against your unsubscribe table and your opt-in record.
3. Apply Israeli anti-spam rules: include sender identity, include opt-out (`עצור` / `STOP`), reference the original consent context.
4. Schedule for Israeli business hours (avoid Shabbat from Friday afternoon to Saturday evening, avoid Jewish holidays for B2C).
5. Send via the provider's bulk endpoint with delivery tracking; reconcile delivery reports back into your CRM.
Result: a Chok HaSpam + Amendment 13 compliant bulk SMS campaign with delivery reports.

## Bundled Resources

### Scripts
- `scripts/send_sms.py`: Sends SMS messages via Israeli gateway providers (SMS4Free, Twilio, InforUMobile). Supports provider selection, message delivery, and delivery status checking. Accepts credentials via CLI arguments or environment variables (SMS_API_KEY, TWILIO_ACCOUNT_SID, etc.). Run: `python scripts/send_sms.py --help`
- `scripts/validate_phone.py`: Validates and normalizes Israeli phone numbers from any common format (local 05X, international +972, with/without dashes) to the standard +972XXXXXXXXX international format. Distinguishes mobile from landline numbers. Run: `python scripts/validate_phone.py --help`

## Reference Links

- Communications Law Amendment 40 (Chok HaSpam) overview, Ministry of Communications: https://www.gov.il/he/departments/ministry_of_communications
- Privacy Protection Law Amendment 13 (in force 14 August 2025), Privacy Protection Authority: https://www.gov.il/he/departments/the_privacy_protection_authority
- 019 SMS (019 Telecom) business messaging: https://019sms.co.il/
- InforUMobile developer docs: https://www.inforu.co.il/en/api/
- SMS4Free API portal: https://www.sms4free.co.il/
- Cellact business SMS: https://www.cellact.com/
- ActiveTrail SMS: https://www.activetrail.co.il/
- Twilio Programmable Messaging (Israel): https://www.twilio.com/en-us/messaging/channels/sms
- Vonage SMS API: https://developer.vonage.com/en/messaging/sms/overview
- GSM-7 vs UCS-2 encoding reference: https://en.wikipedia.org/wiki/GSM_03.38

## Gotchas

- Israeli mobile numbers start with 05x (10 digits total: 05X-XXXXXXX). Agents may validate against US 10-digit formats or miss the leading zero when converting to `+972` (correct form is `+9725XXXXXXXX`, dropping the 0).
- Israel has strict anti-spam rules under Chok HaSpam (Communications Law Amendment 40) and, since August 2025, Privacy Protection Law Amendment 13. Sending unsolicited commercial SMS requires explicit prior opt-in, not opt-out, and unlawful processing of phone numbers can now trigger administrative fines on top of the 1,000 NIS per-message civil exposure.
- Israeli SMS providers (019, InforU, Cellact, ActiveTrail, SMS4Free) use different request shapes from international providers like Twilio. Code generated against Twilio docs will not work against InforU and vice versa.
- Hebrew SMS messages are limited to 70 characters per segment (vs 160 for GSM-7 Latin). Multi-part Hebrew SMS uses 67 characters per segment due to UDH overhead. Agents that ignore this produce surprise multi-part costs.
- Sending SMS on Shabbat (Friday evening to Saturday evening) is poor B2C practice in Israel and a frequent source of complaints to the Privacy Protection Authority.
- Sender ID registration in Israel: alphanumeric sender IDs must be pre-registered with the provider and, in practice, tied to a verified Israeli business. Unregistered IDs fall back to a generic provider number, which hurts open rates.

## Troubleshooting

### Error: "Message not delivered"
Cause: invalid number, carrier blocking, quota exceeded, or sender ID not yet approved.
Solution: re-validate the number, confirm API credentials, and check the provider dashboard for the delivery status code (each provider exposes its own DLR codes).

### Error: "Sender ID rejected"
Cause: custom sender IDs require pre-registration in Israel.
Solution: register the sender ID with your SMS provider and (where required) provide proof of business ownership. While registration is pending, fall back to the provider's default numeric or shared sender.

### Error: "Hebrew characters garbled in SMS"
Cause: Hebrew requires UCS-2 encoding, which reduces SMS length from 160 (GSM-7) to 70 characters per segment.
Solution: send in UCS-2 explicitly. Note that messages over 70 Hebrew characters split into multi-part SMS at 67 characters per segment. Budget bulk costs accordingly. Most Israeli providers detect Hebrew automatically; double-check by sending a test to a real handset rather than only a simulator.
