---
name: israeli-sms-gateway
description: Integrate with Israeli SMS gateway providers for business messaging, OTP, and notifications. Use when user asks about sending SMS in Israel, Israeli SMS providers, phone number validation (Israeli format), OTP implementation, bulk SMS, or SMS marketing compliance. Covers SMS4Free, InforUMobile, and international providers with Israeli support. Do NOT use for WhatsApp Business API (see separate skill) or non-Israeli telecom.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires API key from chosen SMS provider. Network access required.
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

    # Validate mobile: 05X-XXXXXXX (10 digits)
    if re.match(r'^05[0-8]\d{7}$', clean):
        return True, '+972' + clean[1:]

    # Validate landline: 0X-XXXXXXX (9-10 digits)
    if re.match(r'^0[2-9]\d{7,8}$', clean):
        return True, '+972' + clean[1:]

    return False, "Invalid Israeli phone number"
```

### Step 2: Choose Provider
| Provider | Best For | API Type | Pricing |
|----------|----------|----------|---------|
| SMS4Free | Startups, developers | REST | Pay per message |
| InforUMobile | Marketing campaigns | REST | Packages |
| Twilio | Global + Israeli | REST | Pay per message |
| Vonage | Enterprise | REST | Volume pricing |

### Step 3: Send SMS

**SMS4Free Example:**
```python
import requests

def send_sms_sms4free(to: str, message: str, api_key: str,
                      username: str, pass_key: str, sender: str):
    url = "https://www.sms4free.co.il/ApiSMS/SendSMS"
    payload = {
        "key": api_key,
        "user": username,
        "pass": pass_key,
        "sender": sender,
        "recipient": to,
        "msg": message
    }
    # NOTE: Store credentials in environment variables, not in code
    response = requests.get(url, params=payload)
    return response.text
```

### Step 4: Compliance Checklist
Before sending commercial SMS:
- [ ] Recipient opted in (explicit consent)
- [ ] Unsubscribe mechanism included (reply STOP / link)
- [ ] Not on Robinson List (Do Not Disturb registry)
- [ ] Sender ID registered with provider
- [ ] Message content complies with Israeli advertising law
- [ ] Sending during permitted hours (not Shabbat for religious recipients)

## Examples

### Example 1: Send OTP
User says: "Send a verification code to an Israeli mobile number"
Result: Generate 6-digit code, send via SMS provider API, handle delivery confirmation.

### Example 2: Format Phone Number
User says: "Convert 054-1234567 to international format"
Result: +972541234567

### Example 3: Bulk Marketing SMS
User says: "Send a promotional SMS to my customer list about a holiday sale"
Actions:
1. Validate all phone numbers in list (normalize to +972 format)
2. Check Robinson List compliance and opt-in status
3. Apply Chok HaSpam rules: include sender identity, opt-out mechanism
4. Schedule for Israeli business hours (not Shabbat/holidays)
5. Send via bulk API with delivery tracking
Result: Compliant bulk SMS campaign with delivery report.

## Bundled Resources

### Scripts
- `scripts/send_sms.py` — Sends SMS messages via Israeli gateway providers (SMS4Free, Twilio, InforUMobile). Supports provider selection, message delivery, and delivery status checking. Accepts credentials via CLI arguments or environment variables (SMS_API_KEY, TWILIO_ACCOUNT_SID, etc.). Run: `python scripts/send_sms.py --help`
- `scripts/validate_phone.py` — Validates and normalizes Israeli phone numbers from any common format (local 05X, international +972, with/without dashes) to the standard +972XXXXXXXXX international format. Distinguishes mobile from landline numbers. Run: `python scripts/validate_phone.py --help`

### References
- `references/israeli-sms-compliance.md` — Israeli anti-spam law (Chok HaSpam) requirements for SMS marketing: explicit opt-in consent rules, Robinson List (Do Not Disturb registry) lookup process, required unsubscribe mechanisms, permitted sending hours, and penalty structure for violations (up to 1,000 NIS per unsolicited message). Consult when setting up commercial SMS campaigns or verifying compliance.
- `references/provider-api-docs.md` — API documentation summaries for Israeli SMS providers (SMS4Free, InforUMobile) and international providers with Israeli support (Twilio, Vonage), covering authentication, endpoint URLs, response codes, delivery reports, and Hebrew character encoding (GSM-7 vs. UCS-2 for Hebrew). Consult when integrating with a specific provider or troubleshooting delivery issues.

## Gotchas

- Israeli mobile numbers start with 05x (10 digits total: 05X-XXXXXXX). Agents may validate against US 10-digit formats or miss the leading zero when using the +972 prefix (should be +9725XXXXXXXX, dropping the 0).
- Israel has strict anti-spam laws (Amendment 40 to the Communications Law). Sending unsolicited SMS requires prior explicit opt-in consent, not just opt-out. Agents may recommend opt-out-based flows that violate Israeli law.
- Israeli SMS providers (SMS4Free, InforUMobile, Cellact) use different API formats than international providers like Twilio. Agents may generate Twilio-compatible code that does not work with Israeli providers.
- Hebrew SMS messages are limited to 70 characters per segment (vs 160 for Latin). Agents may not account for this when composing messages, resulting in unexpected multi-part SMS costs.
- Sending SMS on Shabbat (Friday evening to Saturday evening) is considered poor practice for B2C in Israel and may result in customer complaints or opt-outs.

## Troubleshooting

### Error: "Message not delivered"
Cause: Various -- invalid number, carrier blocking, quota exceeded
Solution: Check number validation, verify API credentials, check provider dashboard for delivery status.

### Error: "Sender ID rejected"
Cause: Custom sender IDs require pre-registration in Israel
Solution: Register sender ID with your SMS provider. Unregistered IDs default to provider's generic number.

### Error: "Hebrew characters garbled in SMS"
Cause: Hebrew requires UCS-2 encoding which reduces SMS length from 160 to 70 characters per segment
Solution: Use UCS-2 encoding for Hebrew messages. Note that messages over 70 Hebrew characters are split into multi-part SMS (67 chars per segment). Budget accordingly for bulk SMS costs. Some providers handle encoding automatically.
