# Israeli WhatsApp Business Skill — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a skill for integrating WhatsApp Business API tailored to the Israeli market — Hebrew message templates, customer communication patterns, and integration with Israeli CRM and business tools.

**Architecture:** MCP Enhancement skill (Category 3). Guides WhatsApp Business API integration with Israeli-specific templates, consumer preferences, and compliance with Israeli communication regulations.

**Tech Stack:** SKILL.md, references for WhatsApp Business Cloud API, Hebrew template best practices, and Israeli CRM integrations.

---

## Research

### WhatsApp in Israel
- **Market penetration:** 95%+ of Israeli smartphone users (highest globally per capita)
- **Primary messaging app:** Dominant over SMS, Telegram, and others
- **Business usage:** Israelis expect business communication via WhatsApp
- **Common use cases:** Appointment reminders, delivery updates, customer support, marketing
- **Cultural note:** Informal tone accepted, voice messages widely used, Hebrew+emoji standard

### WhatsApp Business API (Cloud API)
- **Base URL:** `https://graph.facebook.com/v18.0/{phone_number_id}/messages`
- **Auth:** Bearer token (System User Access Token)
- **Setup:** Meta Business Suite > WhatsApp > Business Account
- **Pricing:** Conversation-based pricing (per 24-hour session)
  - Marketing: ~0.15 NIS per conversation
  - Utility: ~0.08 NIS per conversation
  - Service: Free (user-initiated)
- **Requirements:** Verified Meta Business Account, approved phone number
- **Message types:**
  - Template messages (pre-approved, can initiate conversations)
  - Free-form messages (within 24-hour customer-initiated window)
  - Interactive messages (buttons, lists, products)

### Hebrew Template Requirements
- **Direction:** RTL (right-to-left) — WhatsApp handles RTL natively
- **Character set:** Hebrew Unicode (U+0590 to U+05FF)
- **Template approval:** Meta reviews templates (24-72 hours)
- **Variables:** `{{1}}`, `{{2}}`, etc. for dynamic content
- **Best practices for Hebrew:**
  - Keep messages concise (Israelis prefer short, direct messages)
  - Use informal register ("את/ה" over formal constructs)
  - Include business name in Hebrew
  - Emojis are standard in Israeli business WhatsApp communication

### Israeli Consumer Preferences
- **Response time expectation:** Within 1-2 hours during business hours
- **Preferred hours:** Sunday-Thursday 9:00-18:00, Friday 9:00-13:00 (pre-Shabbat)
- **Avoid:** Friday evening through Saturday evening (Shabbat), Jewish holidays
- **Language mix:** Hebrew primary, some English technical terms accepted
- **Voice messages:** Very common in Israel — consider audio response capabilities
- **Group behavior:** Israeli businesses frequently use WhatsApp groups for teams

### Israeli CRM Integration
- **Monday.com:** Israeli-built, native WhatsApp integration available
- **Priority Software:** Israeli ERP/CRM, WhatsApp connector exists
- **Salesforce Israel:** Used by enterprise, WhatsApp integration via API
- **HubSpot:** Popular with Israeli startups, WhatsApp integration available
- **Kommo (formerly amoCRM):** Popular in Israeli SMB market, built-in WhatsApp
- **Profit.co.il / Rivhit:** Israeli accounting platforms, some WhatsApp integration

### Regulatory Compliance
- **Chok HaSpam (Anti-Spam Law):** Opt-in required for marketing messages
- **Israeli Privacy Protection Law:** Consent for data collection
- **WhatsApp Commerce Policy:** No prohibited content categories
- **Opt-out:** Must provide easy unsubscribe mechanism
- **Data retention:** Israeli privacy law governs customer data storage

### Use Cases
1. **Message templates** — Create and manage Hebrew WhatsApp templates
2. **Customer communication** — Send notifications, reminders, and support
3. **Marketing campaigns** — Promotional messages with Israeli compliance
4. **CRM integration** — Connect WhatsApp with Israeli business tools
5. **Automated responses** — Chatbot flows for common Israeli business scenarios

---

## Build Steps

### Task 1: Create SKILL.md

**Files:**
- Create: `repos/communication/israeli-whatsapp-business/SKILL.md`

```markdown
---
name: israeli-whatsapp-business
description: >-
  Integrate WhatsApp Business API for the Israeli market with Hebrew message
  templates, customer communication, and CRM integration. Use when user asks
  about WhatsApp Business in Israel, Hebrew WhatsApp templates, WhatsApp
  marketing to Israeli customers, business messaging via WhatsApp, or
  integrating WhatsApp with Israeli CRM tools (Monday.com, Priority, etc.).
  Covers Cloud API setup, template creation, compliance with Israeli anti-spam
  law, and Israeli consumer communication preferences. Do NOT use for personal
  WhatsApp or non-Israeli WhatsApp markets.
license: MIT
allowed-tools: "Bash(python:*) Bash(curl:*) WebFetch"
compatibility: "Requires Meta Business Account and WhatsApp Business API access. Network access required."
metadata:
  author: skills-il
  version: 1.0.0
  category: communication
  tags: [whatsapp, messaging, business, crm, hebrew, marketing, israel]
---

# Israeli WhatsApp Business

## Instructions

### Step 1: Verify WhatsApp Business Setup
Ensure the user has:
1. Meta Business Account (business.facebook.com)
2. WhatsApp Business Account linked to Meta Business
3. Registered phone number with Israeli prefix (+972)
4. System User Access Token with `whatsapp_business_messaging` permission

```python
import requests

def verify_whatsapp_setup(access_token: str, phone_number_id: str) -> dict:
    """Verify WhatsApp Business API access."""
    url = f"https://graph.facebook.com/v18.0/{phone_number_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

### Step 2: Create Hebrew Message Templates

**Template categories for Israeli businesses:**

| Category | Use Case | Example (Hebrew) |
|----------|----------|-------------------|
| Appointment reminder | Clinics, salons, services | תזכורת: יש לך תור ב-{{1}} בתאריך {{2}} בשעה {{3}} |
| Order confirmation | E-commerce, delivery | ההזמנה שלך ({{1}}) התקבלה! נעדכן כשהמשלוח יצא |
| Shipping update | Logistics, delivery | המשלוח שלך בדרך! מספר מעקב: {{1}} |
| Payment receipt | Billing, invoicing | התקבל תשלום בסך {{1}} ש"ח. תודה! |
| Welcome message | Onboarding | היי {{1}}! ברוכים הבאים ל-{{2}}. איך נוכל לעזור? |
| Support follow-up | Customer service | היי {{1}}, רצינו לוודא שהפנייה שלך טופלה. הכל בסדר? |

**Submit template for approval:**
```python
def create_template(waba_id: str, access_token: str, template: dict):
    """Create a WhatsApp message template."""
    url = f"https://graph.facebook.com/v18.0/{waba_id}/message_templates"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=template)
    return response.json()

# Example: Hebrew appointment reminder template
appointment_template = {
    "name": "appointment_reminder_he",
    "language": "he",
    "category": "UTILITY",
    "components": [
        {
            "type": "BODY",
            "text": "שלום {{1}},\nתזכורת: יש לך תור ב-{{2}} בתאריך {{3}} בשעה {{4}}.\nלאישור השב 1, לביטול השב 2.",
            "example": {
                "body_text": [["ישראל", "מרפאת שיניים דר כהן", "15.03.2025", "10:00"]]
            }
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {"type": "QUICK_REPLY", "text": "מאשר/ת ✅"},
                {"type": "QUICK_REPLY", "text": "צריך לשנות 📅"}
            ]
        }
    ]
}
```

### Step 3: Send Messages

**Send a template message:**
```python
def send_template_message(phone_number_id: str, access_token: str,
                          to: str, template_name: str, language: str,
                          parameters: list):
    """Send a WhatsApp template message."""
    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # Format: 972541234567
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": p} for p in parameters
                    ]
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Send appointment reminder
send_template_message(
    phone_number_id="YOUR_PHONE_ID",
    access_token="YOUR_TOKEN",
    to="972541234567",
    template_name="appointment_reminder_he",
    language="he",
    parameters=["ישראל", "מרפאת שיניים", "15.03.2025", "10:00"]
)
```

**Send interactive message (within 24-hour window):**
```python
def send_interactive_list(phone_number_id: str, access_token: str,
                          to: str, body_text: str, sections: list):
    """Send an interactive list message in Hebrew."""
    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
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
                "button": "בחר אפשרות",
                "sections": sections
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### Step 4: Israeli Timing and Compliance

**Sending schedule for Israeli market:**
```python
from datetime import datetime, time
import pytz

def is_valid_sending_time() -> tuple[bool, str]:
    """Check if current time is appropriate for Israeli business messaging."""
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now = datetime.now(israel_tz)
    day = now.weekday()  # 0=Monday, 6=Sunday

    # Friday after 14:00 — pre-Shabbat
    if day == 4 and now.time() > time(14, 0):
        return False, "Pre-Shabbat hours. Send after Saturday 20:00."

    # Saturday before 20:00 — Shabbat
    if day == 5:
        if now.time() < time(20, 0):
            return False, "Shabbat. Send after 20:00."

    # Sunday-Thursday business hours
    if now.time() < time(8, 30) or now.time() > time(20, 0):
        return False, "Outside business hours. Send between 08:30-20:00."

    return True, "OK to send."

def compliance_checklist(message_type: str) -> list:
    """Return compliance checklist for Israeli WhatsApp messaging."""
    checks = [
        "Recipient opted in to receive WhatsApp messages",
        "Opt-out mechanism included (reply 'הסר' to unsubscribe)",
        "Business identity clearly stated",
        "Message in appropriate language (Hebrew/English)",
    ]
    if message_type == "marketing":
        checks.extend([
            "Compliant with Chok HaSpam (Israeli Anti-Spam Law)",
            "Not sending during Shabbat/holidays",
            "Frequency cap respected (avoid over-messaging)",
            "Marketing category template approved by Meta",
        ])
    return checks
```

### Step 5: CRM Integration Guidance

**Monday.com + WhatsApp:**
1. Use Monday.com WhatsApp integration (native)
2. Trigger WhatsApp messages from board status changes
3. Log incoming messages as Monday.com updates
4. Use Monday.com automations: "When status changes to X, send WhatsApp template"

**Custom CRM Integration:**
```python
def webhook_handler(event: dict) -> dict:
    """Handle incoming WhatsApp webhook for CRM integration."""
    if event.get("entry"):
        for entry in event["entry"]:
            for change in entry.get("changes", []):
                if change["field"] == "messages":
                    messages = change["value"].get("messages", [])
                    for msg in messages:
                        # Extract message data for CRM
                        crm_data = {
                            "phone": msg["from"],
                            "message": msg.get("text", {}).get("body", ""),
                            "timestamp": msg["timestamp"],
                            "type": msg["type"],
                            "wa_message_id": msg["id"]
                        }
                        # Send to CRM system
                        # update_crm(crm_data)
    return {"status": "ok"}
```

## Examples

### Example 1: Appointment Reminder System
User says: "Set up WhatsApp appointment reminders for my dental clinic in Hebrew"
Actions:
1. Create Hebrew template with clinic name, date, time variables
2. Add confirmation/reschedule quick reply buttons
3. Set up timing rules (no Shabbat sending)
4. Provide integration code for clinic management system
Result: Approved template with sending automation and compliance checks.

### Example 2: E-commerce Order Updates
User says: "I want to send order confirmations and shipping updates via WhatsApp"
Actions:
1. Create order confirmation template (Hebrew)
2. Create shipping notification template with tracking link
3. Set up webhook to receive delivery status updates
4. Integrate with Israeli shipping providers (Cheetah, HFD, Israel Post)
Result: Automated order lifecycle messaging in Hebrew.

### Example 3: Marketing Campaign
User says: "Send a promotion to our customer list for a holiday sale"
Actions:
1. Check compliance (opt-in list, Chok HaSpam)
2. Create marketing template with offer details
3. Schedule for appropriate Israeli business hours
4. Set up tracking for open rates and responses
Result: Compliant promotional campaign with Israeli timing.

## Troubleshooting

### Error: "Template rejected"
Cause: Template violates WhatsApp policy or formatting issues
Solution: Ensure Hebrew text is properly formatted, no prohibited content (gambling, adult), variables have examples, and category matches content type.

### Error: "Message failed to send"
Cause: Various — invalid number, user not on WhatsApp, rate limit
Solution: Verify +972 format, check user has WhatsApp, respect rate limits (80 messages/second for Cloud API).

### Error: "Webhook not receiving messages"
Cause: Webhook URL not verified or Meta app not configured
Solution: Ensure webhook URL is HTTPS, verification token matches, and Meta App is subscribed to messages webhook field.
```

**Step 2: Create references**
- `references/hebrew-templates.md` — Library of pre-built Hebrew WhatsApp templates by industry
- `references/israeli-crm-connectors.md` — Integration guides for Monday.com, Priority, and other Israeli CRMs

**Step 3: Validate and commit**
