---
name: israeli-whatsapp-business
description: Integrate WhatsApp Business API for the Israeli market with Hebrew message templates, customer communication, and CRM integration. Use when user asks about WhatsApp Business in Israel, Hebrew WhatsApp templates, WhatsApp marketing to Israeli customers, business messaging via WhatsApp, or integrating WhatsApp with Israeli CRM tools (Monday.com, Priority, etc.). Covers Cloud API setup, template creation, conversation pricing, compliance with Israeli anti-spam law and Privacy Law Amendment 13, and Israeli consumer communication preferences. Do NOT use for personal WhatsApp or non-Israeli WhatsApp markets.
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: Requires Meta Business Account and WhatsApp Business API access. Network access required.
version: 1.2.0
---

# Israeli WhatsApp Business

## Instructions

### Step 1: Verify WhatsApp Business Setup
Ensure the user has:
1. Meta Business Account (`business.facebook.com`)
2. WhatsApp Business Account (WABA) linked to that Meta Business
3. A registered phone number with Israeli prefix (`+972`), either the official Cloud API hosted by Meta, or via a Business Solution Provider (BSP). Currently active BSPs serving Israeli accounts: 360dialog, MessageBird/Bird, Twilio, Infobip, Vonage, Gupshup, AiSensy, Sinch
4. System User Access Token with `whatsapp_business_messaging` permission (and `whatsapp_business_management` for template ops)

```python
import requests

def verify_whatsapp_setup(access_token: str, phone_number_id: str) -> dict:
    """Verify WhatsApp Business API access against the Cloud API."""
    # Use the latest stable Graph API version. Check
    # https://developers.facebook.com/docs/graph-api/changelog for current.
    url = f"https://graph.facebook.com/v25.0/{phone_number_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

### Step 2: Create Hebrew Message Templates

**Conversation categories (Meta pricing model, per-template billing in force since 1 July 2025, replacing the older 24h conversation-based model):**
WhatsApp now bills per **template message** in three paid categories plus one free category:

| Category | When to use | Billing |
|----------|-------------|---------|
| Utility | Transactional updates the user is expecting (order confirmations, shipping, payment receipts, appointment reminders) | Free when sent inside an open service (24h) window opened by the user; otherwise billed per template message |
| Authentication | OTP and verification codes | Billed per authentication template message |
| Marketing | Promotions, offers, newsletters, re-engagement | Billed per marketing template message (typically the most expensive tier) |
| Service | Free-form replies inside the 24h customer service window | Free; counts as a service conversation |

The legacy "conversation-based" pricing (24h window per category) was retired on 1 July 2025 and replaced with per-template-message pricing for utility, authentication and marketing templates, plus a free-tier allowance per WABA. Confirm current Israel-specific rates on the Meta pricing page before quoting numbers to a customer; rates vary by country and are revised periodically.

**Free messaging windows beyond the default 24h CSW:**
- **24h Customer Service Window (CSW)**: opens when the user sends an inbound message. Free-form replies, free utility templates, free service messages.
- **72h Click-to-WhatsApp (CTWA) free window**: opens when the user clicks a CTWA ad on Facebook/Instagram. Free messages in any category for 72 hours, very common Israeli acquisition pattern.
- **Authentication templates are billed even inside the CSW** (unlike utility, which is free in window). Trap that catches Israeli OTP-heavy products (banks, fintech).
- **Free-tier allowance**: 1,000 free service conversations per WABA per month at time of writing. Re-check current numbers on the Meta pricing page.

**Template categories for Israeli businesses:**

| Category | Use Case | Example (Hebrew, simplified) |
|----------|----------|-------------------|
| Appointment reminder (Utility) | Clinics, salons, services | תזכורת: יש לך תור ב-{{1}} בתאריך {{2}} בשעה {{3}} |
| Order confirmation (Utility) | E-commerce, delivery | הזמנתך ({{1}}) התקבלה. נעדכן כשתישלח. |
| Shipping update (Utility) | Logistics | המשלוח שלך בדרך. מעקב: {{1}} |
| Payment receipt (Utility) | Billing, invoicing | התקבל תשלום של {{1}} ש"ח. תודה. |
| OTP (Authentication) | Login, verification | קוד האימות שלך הוא {{1}}. תוקף 5 דקות. |
| Welcome message (Marketing or Utility) | Onboarding | שלום {{1}}, ברוכים הבאים ל-{{2}}. איך נוכל לעזור? |
| Promotion (Marketing) | Sales, holiday campaigns | מבצע חג: {{1}} בהנחת {{2}}%. עד {{3}}. |

**Submit template for approval:**
```python
def create_template(waba_id: str, access_token: str, template: dict):
    """Create a WhatsApp message template."""
    url = f"https://graph.facebook.com/v25.0/{waba_id}/message_templates"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
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
            "text": "שלום {{1}}, תזכורת על תור ב-{{2}} בתאריך {{3}} בשעה {{4}}. לאישור השיבו 1, לביטול השיבו 2.",
            "example": {
                "body_text": [["ישראל", "מרפאת השיניים ד״ר כהן", "15.03.2026", "10:00"]],
            },
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {"type": "QUICK_REPLY", "text": "מאשר"},
                {"type": "QUICK_REPLY", "text": "צריך לשנות"},
            ],
        },
    ],
}
```

Template approval typically takes minutes to a few hours when content is clean; rejections are most often caused by promotional language in a UTILITY template, missing variable examples, or formatting issues with mixed-direction text.

**Concrete rejection patterns we've seen on Hebrew templates:**

| Rejected text | Why | Fixed version |
|---|---|---|
| "מבצע!! 20% הנחה רק היום, מהרו!" (in UTILITY) | Promotional copy + urgency markers in UTILITY category | Move to MARKETING, or rewrite as transactional: "ההנחה שלך {{1}}% פעילה עד {{2}}." |
| "תזכורת: יש לך תור ב-{{1}}" with example `["מחר"]` | Vague placeholder, not a realistic value | Use a real example like `["מרפאת השיניים ד\"ר כהן, 15.06.2026 בשעה 10:00"]` |
| Body with 6+ variables and 30 chars of literal text | Spam-like ratio of variables to text | Reduce to ≤3 variables, add more natural sentence connectives |
| "{{1}}{{2}}" with no separator and no language code | Missing footer + unclear language | Add explicit `language: "he"` plus a footer line like "להסרה השיבו 'הסר'" |

### Step 3: Send Messages

**Send a template message:**
```python
def send_template_message(phone_number_id: str, access_token: str,
                          to: str, template_name: str, language: str,
                          parameters: list):
    """Send a WhatsApp template message."""
    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # Format: 972541234567 (no leading + or 0)
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": p} for p in parameters
                    ],
                }
            ],
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

**Send interactive message (within the 24-hour service window):**
```python
def send_interactive_list(phone_number_id: str, access_token: str,
                          to: str, body_text: str, sections: list):
    """Send an interactive list message in Hebrew."""
    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body_text},
            "action": {"button": "בחר אפשרות", "sections": sections},
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### Step 3.5: Quality Rating and Number Warming

WhatsApp assigns every business phone number a quality tier (Green, Yellow, Red). Meta evaluates the tier every 6 hours based on user-reported spam, block rate, and template rejection ratio. A Yellow or Red tier limits how many users you can message per 24h, and a sustained Red tier can pause sending entirely.

**Warming a new Israeli number (the first 30 days are critical):**

1. **Days 1-7**: send only UTILITY templates to opted-in customers who actively expect them (order confirmations, OTP). No marketing.
2. **Days 7-14**: introduce small marketing batches (50-200 recipients), only to users who opted in within the last 30 days.
3. **Days 14-30**: scale gradually. Stop immediately if quality drops to Yellow.
4. **Always**: include a clear opt-out line in marketing templates ("להסרה השיבו 'הסר'"), and act on opt-outs within minutes (block the wa_id from your sending list).

**If quality drops to Yellow**: pause marketing for 48h, send only UTILITY to engaged users, review recent template content for promotional drift, and audit the opt-in source for the affected segment.

**Messaging limits since October 2025 apply per Business Portfolio, not per phone number**, which means moving a campaign to a fresh number does NOT reset your limit if the new number is under the same portfolio. New portfolios start at a low default daily cap (~250 marketing conversations to unique users at time of writing) and advance based on Meta's portfolio-level evaluation of utilization and quality. Treat the historical per-phone-number tier table (1k → 10k → 100k → unlimited) as legacy; verify your current cap in Business Manager → WhatsApp Manager → Insights.

### Step 4: Israeli Timing and Compliance

Israeli commercial WhatsApp messaging is governed by Amendment 40 to the Communications (Bezeq and Broadcasts) Law (Chok HaSpam) and, since 14 August 2025, by Amendment 13 to the Privacy Protection Law, which significantly tightened obligations on processors of personal data and aligned Israeli rules more closely with the EU GDPR. WhatsApp marketing requires explicit prior opt-in just like SMS, and unlawful processing of phone numbers can now also trigger administrative fines from the Privacy Protection Authority.

**Sending schedule for Israeli market** (the Friday-14:00 / Saturday-20:00 cutoffs below are conservative heuristics; real Shabbat times vary by ~30-60 minutes by season and city. For production use, derive entry/exit from a Hebcal-style API for the user's location):
```python
from datetime import datetime, time
import pytz

def is_valid_sending_time() -> tuple[bool, str]:
    """Check if current time is appropriate for Israeli business messaging."""
    israel_tz = pytz.timezone("Asia/Jerusalem")
    now = datetime.now(israel_tz)
    day = now.weekday()  # 0=Monday, 6=Sunday

    # Friday after 14:00, pre-Shabbat
    if day == 4 and now.time() > time(14, 0):
        return False, "Pre-Shabbat hours. Send after Saturday 20:00."

    # Saturday before 20:00, Shabbat
    if day == 5 and now.time() < time(20, 0):
        return False, "Shabbat. Send after 20:00."

    # Sunday-Thursday business hours
    if now.time() < time(8, 30) or now.time() > time(20, 0):
        return False, "Outside business hours. Send between 08:30 and 20:00."

    return True, "OK to send."

def compliance_checklist(message_type: str) -> list:
    """Return compliance checklist for Israeli WhatsApp messaging."""
    checks = [
        "Recipient gave explicit prior opt-in to receive WhatsApp messages",
        "Opt-in record stored: who, what, timestamp, channel",
        "Opt-out mechanism included (e.g., reply 'הסר' / 'STOP')",
        "Business identity clearly stated in the message",
        "Phone numbers obtained lawfully under Privacy Law Amendment 13",
        "Message sent in appropriate language (Hebrew or English)",
    ]
    if message_type == "marketing":
        checks.extend([
            "Marketing template approved by Meta in MARKETING category",
            "Compliant with Chok HaSpam (Communications Law Amendment 40)",
            "Not sent during Shabbat or Jewish holidays for B2C",
            "Frequency cap respected (avoid over-messaging)",
            "No cross-border list transfer without adequate protection (Amendment 13)",
        ])
    return checks
```

### Step 4.5: Beyond Templates (Flows, Calls, Catalog, CTWA)

Common 2025-2026 features Israeli businesses ask about, in priority order:

- **WhatsApp Flows**: native multi-step forms (lead capture, booking, surveys) rendered inside the chat. Cloud API only. Replaces many "external Google Form linked from WhatsApp" patterns. Useful for kupot/clinic intake, real-estate lead capture, restaurant reservations.
- **Click-to-WhatsApp ads (CTWA)**: Facebook/Instagram ads that open a chat with your business. Opens the 72h free messaging window described above. Israel's dominant paid acquisition channel for WhatsApp.
- **WhatsApp Business Calling API**: voice calling from a verified business number. Announced July 2025, with SMB-tier rollout phased through BSPs across 2026. Country and BSP coverage is uneven; check the official calling-API docs and your BSP for current Israeli availability before designing a calling-dependent flow. Pricing is separate from messaging (Meta business calling rates).
- **Catalog and Commerce**: product catalogs and in-chat product cards. Note: WhatsApp Pay is NOT available in Israel (the in-chat payment product launched only in Brazil, India and Singapore); checkout must redirect to your own payment page (Cardcom, Tranzila, Pelecard, Bit, Apple/Google Pay, etc.).
- **Phone-number migration between BSPs**: 2-step verification PIN must be removed before migration. Plan a maintenance window because messages in flight can be dropped. Document the source phone-number ID before initiating.
- **On-Premises API has reached end of support (final version expired 23 October 2025).** Migrate any legacy On-Prem deployments to Cloud API or to a BSP-hosted gateway. Do NOT recommend the On-Prem path to new users.

**General-purpose AI assistant restriction (effective 15 January 2026):** Meta no longer permits general-purpose AI chatbots on WhatsApp Business. Purpose-specific bots (customer support, bookings, product Q&A, order status) remain allowed. This affects the local ChatGPT-style WhatsApp wrapper market.

### Step 5: CRM Integration Guidance

**Monday.com + WhatsApp:**
1. Use Monday.com automations or third-party connectors (Make, Zapier, Pipedream) to bridge WhatsApp Cloud API and your boards.
2. Trigger WhatsApp template messages from board status changes (e.g., "Order shipped" status sends a UTILITY template).
3. Log incoming WhatsApp messages as Monday.com updates via the inbound webhook.
4. Map WhatsApp `wa_id` to a Monday.com item so threads stay linked.

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
                        crm_data = {
                            "phone": msg["from"],
                            "message": msg.get("text", {}).get("body", ""),
                            "timestamp": msg["timestamp"],
                            "type": msg["type"],
                            "wa_message_id": msg["id"],
                        }
                        # update_crm(crm_data)
    return {"status": "ok"}
```

## Examples

### Example 1: Appointment Reminder System
User says: "Set up WhatsApp appointment reminders for my dental clinic in Hebrew."
Actions:
1. Create a Hebrew UTILITY template with clinic name, date, and time variables.
2. Add confirm/reschedule quick reply buttons.
3. Set timing rules (no Shabbat sending).
4. Provide integration code for the clinic management system.
Result: an approved UTILITY template with sending automation and compliance checks. Utility templates sent inside an open 24h service window are free; outside the window they are billed per template message.

### Example 2: E-commerce Order Updates
User says: "I want to send order confirmations and shipping updates via WhatsApp."
Actions:
1. Create an order confirmation UTILITY template (Hebrew).
2. Create a shipping notification UTILITY template with a tracking link.
3. Set up the inbound webhook to receive delivery status updates.
4. Integrate with Israeli shipping providers (Cheetah, HFD, Israel Post, Yamit, Yango Delivery).
Result: automated order lifecycle messaging in Hebrew, with predictable per-template billing.

### Example 3: Marketing Campaign
User says: "Send a promotion to our customer list for a holiday sale."
Actions:
1. Confirm compliance (opt-in evidence, Chok HaSpam, Privacy Law Amendment 13).
2. Create a MARKETING template with offer details and a clear opt-out line.
3. Schedule for Israeli business hours (avoid Shabbat and chag eve).
4. Track delivery, read rates, and replies; honour opt-outs immediately.
Result: a compliant promotional campaign with Israeli timing and per-message marketing billing.

## Bundled Resources

### Scripts
- `scripts/send_whatsapp.py`: Sends WhatsApp Business messages via the Meta Cloud API for the Israeli market. Supports template messages (with language and parameter substitution) and free-form text messages within the 24-hour conversation window. Includes Israeli phone number validation and Shabbat-aware sending time checks. Run: `python scripts/send_whatsapp.py --help`

## Reference Links

- WhatsApp Cloud API overview: https://developers.facebook.com/docs/whatsapp/cloud-api
- Graph API changelog (find current stable version): https://developers.facebook.com/docs/graph-api/changelog
- WhatsApp pricing (template-based, in force since July 2024): https://developers.facebook.com/docs/whatsapp/pricing
- WhatsApp template guidelines: https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates
- Communications Law Amendment 40 (Chok HaSpam), Ministry of Communications: https://www.gov.il/he/departments/ministry_of_communications
- Privacy Protection Law Amendment 13 (in force 14 August 2025), Privacy Protection Authority: https://www.gov.il/he/departments/the_privacy_protection_authority
- 360dialog (BSP): https://www.360dialog.com/
- MessageBird/Bird (BSP): https://bird.com/
- Twilio WhatsApp Business: https://www.twilio.com/en-us/messaging/channels/whatsapp
- Infobip WhatsApp: https://www.infobip.com/whatsapp-business
- Vonage WhatsApp: https://developer.vonage.com/en/messages/concepts/whatsapp
- Gupshup WhatsApp: https://www.gupshup.io/channels/whatsapp
- AiSensy (BSP, popular with SMBs): https://www.aisensy.com/
- Sinch WhatsApp: https://www.sinch.com/products/messaging/whatsapp/
- Monday.com automations: https://support.monday.com/hc/en-us/categories/115000091445
- WhatsApp Flows overview: https://developers.facebook.com/docs/whatsapp/flows
- WhatsApp Business Calling API: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/calling
- On-Premises API sunset notice (final version expired 23 October 2025): https://developers.facebook.com/docs/whatsapp/on-premises/sunset

## Gotchas

- Israeli phone numbers for the WhatsApp API use the 972 country code without the leading zero: `+972521234567`, not `+9720521234567`. Agents frequently include the extra zero, which causes "phone number not found on WhatsApp" errors.
- WhatsApp message templates submitted in Hebrew must pass Meta's review. UTILITY templates with promotional language are commonly rejected (and should be MARKETING). Templates with Hebrew text inside code blocks or with missing variable examples are also commonly rejected.
- Israeli businesses sending WhatsApp marketing must comply with Communications Law Amendment 40 (Chok HaSpam) and, since August 2025, Privacy Protection Law Amendment 13. Prior explicit opt-in is required, not an "existing business relationship".
- WhatsApp Business has a 24-hour customer service window. After 24 hours since the user's last inbound message, only pre-approved template messages can be sent, and (depending on category) they will be billed per template message under the post-July-2024 pricing model.
- Hebrew text in template variables can break formatting when mixed with numbers or English. Use Unicode isolate characters (U+2066 to U+2069) around mixed-direction content, or design templates so variables don't contain mixed-direction substrings.
- Template-based pricing (since 1 July 2025): utility/authentication/marketing categories are billed per template message, not per 24h conversation. Free-tier allowances apply per WABA. Always re-check the Meta pricing page before quoting Israeli rates to a customer; rates change.
- **Per-user marketing frequency cap (rollout in progress)**: Meta is rolling out per-user marketing-template frequency caps to reduce spam in selected markets. At time of writing the cap is enforced for users with India (+91) country codes; Meta has signalled expansion but Israeli (+972) recipients are NOT subject to a documented hard cap as of this update. Check the current scope on the Meta pricing/policy pages before assuming the cap is in force for your Israeli campaign, and design your opt-in flow as if a cap is coming.
- **Messaging limits are per Business Portfolio since October 2025**, not per phone number. Adding a second number under the same portfolio will NOT double your daily cap.
- **Authentication templates are billed even inside the 24h Customer Service Window**, unlike utility templates which are free in window. Israeli OTP-heavy products (banks, e-wallets, identity verification) frequently overlook this.
- **Israeli mobile prefixes accepted by WhatsApp**: 050 (Pelephone), 051 (We4G), 052 (Cellcom), 053 (HOT Mobile), 054 (Partner), 055 (MVNOs), 058 (Golan Telecom). Validation regex that excludes 051 will reject real subscribers.

## Troubleshooting

### Error: "Template rejected"
Cause: template violates WhatsApp policy or has formatting issues.
Solution: ensure Hebrew text is properly formatted, no prohibited content (gambling, adult content, regulated goods), variables have realistic examples, and the category matches the actual content (UTILITY templates must be transactional, MARKETING templates must be promotional).

### Error: "Message failed to send"
Cause: invalid number, recipient not on WhatsApp, rate limit, or out-of-window free-form attempt.
Solution: verify `+972` format without leading zero, confirm recipient has WhatsApp, respect rate limits (Cloud API default ~80 messages/second per business phone number, scaling up to ~1,000 MPS for unlimited-tier accounts; daily-conversation limits apply per Business Portfolio since October 2025). If outside the 24h window, switch to an approved template message. If the failure is on a marketing template and the recipient has been opted-in correctly, suspect the 7-day rolling per-user marketing cap.

### Error: "Webhook not receiving messages"
Cause: webhook URL not verified, Meta App not subscribed to `messages` field, or signature validation failing.
Solution: ensure the webhook URL is HTTPS, the verification token matches, the Meta App is subscribed to the `messages` webhook field on the WABA, and your handler validates `X-Hub-Signature-256` against the App secret.
