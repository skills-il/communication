# Israeli SMS Gateway Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for integrating with Israeli SMS gateway providers for business messaging, OTP, and notifications.

**Architecture:** MCP Enhancement skill (Category 3). Guides integration with Israeli SMS providers, handling Israeli phone number formatting and regulatory requirements.

**Tech Stack:** SKILL.md, references for provider APIs and Israeli telecom regulations.

---

## Research

### Israeli SMS Providers
- **SMS4Free:** Popular Israeli gateway, REST API, competitive pricing
- **InforUMobile:** Israeli SMS + WhatsApp gateway, REST API
- **019 SMS:** Bezeq subsidiary, enterprise-focused
- **SMSGlobal/Vonage/Twilio:** International providers with Israeli number support
- **Cellact:** Israeli SMS marketing platform

### Israeli Phone Number Format
- Country code: +972
- Mobile prefixes: 050, 051, 052, 053, 054, 055, 056, 058
- Landline: 02 (Jerusalem), 03 (Tel Aviv), 04 (Haifa), 08 (South), 09 (Sharon)
- Format: +972-5X-XXX-XXXX (mobile), +972-X-XXX-XXXX (landline)
- Local format: 05X-XXXXXXX

### Regulatory Requirements
- **Spam Law (Chok HaSpam):** Anti-spam legislation requires opt-in consent for commercial SMS
- **Opt-out:** Must include unsubscribe mechanism
- **Sender ID:** Custom sender IDs need registration with provider
- **DND Registry:** Israel has a "Do Not Disturb" registry (Robinson List)

### Use Cases
1. **Send SMS** — Single message via Israeli provider API
2. **OTP/Verification** — Send one-time passwords
3. **Bulk messaging** — Campaign sending with compliance
4. **Phone validation** — Validate Israeli phone numbers
5. **Provider comparison** — Choose the right Israeli SMS provider

---

## Build Steps

### Task 1: Create SKILL.md

```markdown
---
name: israeli-sms-gateway
description: >-
  Integrate with Israeli SMS gateway providers for business messaging, OTP,
  and notifications. Use when user asks about sending SMS in Israel, Israeli
  SMS providers, phone number validation (Israeli format), OTP implementation,
  bulk SMS, or SMS marketing compliance. Covers SMS4Free, InforUMobile, and
  international providers with Israeli support. Do NOT use for WhatsApp
  Business API (see separate skill) or non-Israeli telecom.
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: "Requires API key from chosen SMS provider. Network access required."
metadata:
  author: skills-il
  version: 1.0.0
  category: communication
  tags: [sms, messaging, otp, telecom, notifications, israel]
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

def send_sms_sms4free(to: str, message: str, api_key: str, sender: str):
    url = "https://www.sms4free.co.il/ApiSMS/SendSMS"
    payload = {
        "key": api_key,
        "user": "username",
        "pass": "password",
        "sender": sender,
        "recipient": to,
        "msg": message
    }
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

## Troubleshooting

### Error: "Message not delivered"
Cause: Various — invalid number, carrier blocking, quota exceeded
Solution: Check number validation, verify API credentials, check provider dashboard for delivery status.

### Error: "Sender ID rejected"
Cause: Custom sender IDs require pre-registration in Israel
Solution: Register sender ID with your SMS provider. Unregistered IDs default to provider's generic number.
```
