---
name: israeli-whatsapp-business
description: Integrate WhatsApp Business API for the Israeli market with Hebrew message templates, customer communication, and CRM integration. Use when user asks about WhatsApp Business in Israel, Hebrew WhatsApp templates, WhatsApp marketing to Israeli customers, business messaging via WhatsApp, or integrating WhatsApp with Israeli CRM tools (Monday.com, Priority, etc.). Covers Cloud API setup, template creation, compliance with Israeli anti-spam law, and Israeli consumer communication preferences. Do NOT use for personal WhatsApp or non-Israeli WhatsApp markets.
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: Requires Meta Business Account and WhatsApp Business API access. Network access required.
version: 1.0.1
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
    url = f"https://graph.facebook.com/v27.0/{phone_number_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

### Step 2: Create Hebrew Message Templates

**Template categories for Israeli businesses:**

| Category | Use Case | Example (Hebrew) |
|----------|----------|-------------------|
| Appointment reminder | Clinics, salons, services | Reminder: You have an appointment at {{1}} on {{2}} at {{3}} |
| Order confirmation | E-commerce, delivery | Your order ({{1}}) was received! We will update when shipped |
| Shipping update | Logistics, delivery | Your shipment is on the way! Tracking: {{1}} |
| Payment receipt | Billing, invoicing | Payment of {{1}} NIS received. Thank you! |
| Welcome message | Onboarding | Hi {{1}}! Welcome to {{2}}. How can we help? |
| Support follow-up | Customer service | Hi {{1}}, we wanted to make sure your inquiry was handled. All good? |

**Submit template for approval:**
```python
def create_template(waba_id: str, access_token: str, template: dict):
    """Create a WhatsApp message template."""
    url = f"https://graph.facebook.com/v27.0/{waba_id}/message_templates"
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
            "text": "Shalom {{1}},\nReminder: appointment at {{2}} on {{3}} at {{4}}.\nConfirm reply 1, Cancel reply 2.",
            "example": {
                "body_text": [["Israel", "Dr. Cohen Dental Clinic", "15.03.2026", "10:00"]]
            }
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {"type": "QUICK_REPLY", "text": "Confirmed"},
                {"type": "QUICK_REPLY", "text": "Need to reschedule"}
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
    url = f"https://graph.facebook.com/v27.0/{phone_number_id}/messages"
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
    parameters=["Israel", "Dental Clinic", "15.03.2026", "10:00"]
)
```

**Send interactive message (within 24-hour window):**
```python
def send_interactive_list(phone_number_id: str, access_token: str,
                          to: str, body_text: str, sections: list):
    """Send an interactive list message in Hebrew."""
    url = f"https://graph.facebook.com/v27.0/{phone_number_id}/messages"
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
                "button": "Choose option",
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

    # Friday after 14:00 -- pre-Shabbat
    if day == 4 and now.time() > time(14, 0):
        return False, "Pre-Shabbat hours. Send after Saturday 20:00."

    # Saturday before 20:00 -- Shabbat
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
        "Opt-out mechanism included (reply 'remove' to unsubscribe)",
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
1. Use Monday.com integration methods (automation or third-party connectors)
2. Trigger WhatsApp messages from board status changes
3. Log incoming messages as Monday.com updates
4. Set up automated workflows: "When status changes to X, send WhatsApp template"

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

## Bundled Resources

### Scripts
- `scripts/send_whatsapp.py` — Sends WhatsApp Business messages via the Meta Cloud API for the Israeli market. Supports template messages (with language and parameter substitution) and free-form text messages within the 24-hour conversation window. Includes Israeli phone number validation and Shabbat-aware sending time checks. Run: `python scripts/send_whatsapp.py --help`

### References
- `references/whatsapp-api-guide.md` — Meta WhatsApp Business Cloud API reference covering authentication, API versioning, rate limits, template submission guidelines, and message types (text, media, interactive, location). Consult when constructing API requests, troubleshooting template rejections, or handling webhook events.
- `references/israeli-messaging-compliance.md` — Israeli anti-spam law (Chok HaSpam, Amendment 40 to the Communications Law) requirements for commercial messaging: opt-in consent rules, unsubscribe mechanisms, Robinson List (Do Not Disturb registry) checking, permitted sending hours, and penalties for violations. Consult when setting up marketing campaigns or verifying compliance.

## Gotchas

- Israeli phone numbers for WhatsApp API must use the 972 country code without the leading zero: +972521234567, not +9720521234567. Agents frequently include the extra zero.
- WhatsApp message templates submitted in Hebrew must pass Meta's review. Templates with Hebrew text in code blocks may be rejected because code blocks don't support RTL rendering properly.
- Israeli businesses sending WhatsApp marketing messages must comply with Amendment 40 of the Communications Law (anti-spam). Prior explicit opt-in is required, not just an existing business relationship.
- WhatsApp Business API has a 24-hour customer service window. After 24 hours, only pre-approved template messages can be sent. Agents may not account for this when designing conversation flows.
- Hebrew text in WhatsApp template variables can break message formatting when mixed with numbers or English. Use Unicode isolate characters (U+2066/U+2069) around mixed-direction content.

## Troubleshooting

### Error: "Template rejected"
Cause: Template violates WhatsApp policy or formatting issues
Solution: Ensure Hebrew text is properly formatted, no prohibited content (gambling, adult), variables have examples, and category matches content type.

### Error: "Message failed to send"
Cause: Various -- invalid number, user not on WhatsApp, rate limit
Solution: Verify +972 format, check user has WhatsApp, respect rate limits (80 messages/second for Cloud API).

### Error: "Webhook not receiving messages"
Cause: Webhook URL not verified or Meta app not configured
Solution: Ensure webhook URL is HTTPS, verification token matches, and Meta App is subscribed to messages webhook field.