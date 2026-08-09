---
name: israeli-whatsapp-business
description: Integrate WhatsApp Business API for the Israeli market with Hebrew message templates, customer communication, and CRM integration. Use when user asks about WhatsApp Business in Israel, Hebrew WhatsApp templates, WhatsApp marketing to Israeli customers, business messaging via WhatsApp, or integrating WhatsApp with Israeli CRM tools (Monday.com, Priority, etc.). Covers Cloud API setup, template creation, conversation pricing, compliance with Israeli anti-spam law and Privacy Law Amendment 13, and Israeli consumer communication preferences. Do NOT use for personal WhatsApp or non-Israeli WhatsApp markets.
license: MIT
allowed-tools: Bash(python:*), Bash(curl:*), WebFetch
compatibility: Requires Meta Business Account and WhatsApp Business API access. Network access required.
version: 1.3.0
---

# Israeli WhatsApp Business

## Instructions

### Step 0: Decide whether the user needs the Platform at all

Most Israeli small businesses are on the free **WhatsApp Business app**, not the **WhatsApp Business Platform** (Cloud API). Ask first. If the user only needs a catalog, quick replies, labels and manual chats, the app is the right answer and the rest of this skill is overhead. Route to the Platform only for automation, templates at scale, CRM sync or webhooks. Two consequences:

- A number already on the WhatsApp Business app must be **migrated** to the Platform, and it **loses its existing chat history** in the process.
- Platform access needs a business portfolio, a WABA and a system user token. A non-technical owner will usually go through a BSP instead.

**Meta Business Verification** is the gate most Israeli businesses trip on. A new business portfolio is capped at a messaging limit of 250 (see Step 3.5), and verifying the business is one of the paths that raises it to 2,000. It is also a prerequisite for the green Official Business Account badge. For an Israeli entity, expect to upload the company registration (ח.פ. for a company, ע.מ. for an עוסק) plus a utility bill or bank statement whose legal name and address match the registration exactly. Mismatched Hebrew and English spellings of the same company name are a very common rejection cause.

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
    url = f"https://graph.facebook.com/v26.0/{phone_number_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

**Choosing between direct Cloud API and a BSP.** The eight BSPs above are not interchangeable. Ask these five questions before picking one:

| Question | Why it matters in Israel |
|---|---|
| Who is billed by Meta? | Some BSPs pass Meta's rate through at cost plus a platform fee; others resell at a markup. Ask for their Israel country rate, not a global average. |
| Do they invoice as an Israeli vendor? | A local invoice with VAT is far easier for an Israeli accountant than a foreign one needing self-assessment. Some BSPs bill from abroad only. |
| Who owns the phone number and the WABA? | The lock-in question. If the BSP holds the number, leaving later needs their cooperation. Prefer the WABA sitting in **your** portfolio with the BSP added as a partner. |
| How good is template management? | You will submit and resubmit Hebrew templates constantly, and a weak template UI multiplies that work. |
| Is there Hebrew support on Israeli hours? | A foreign support desk is painful when sending is paused on a Sunday, a working day in Israel. |

Direct Cloud API is cheaper and removes the lock-in question, but you own token rotation, webhook hosting and retry logic yourself.

### Step 2: Create Hebrew Message Templates

**Conversation categories (Meta pricing model, per-message billing in force since 1 July 2025, replacing the older 24h conversation-based model):**
WhatsApp bills per **template message** in three paid categories plus free non-template messaging:

| Category | When to use | Billing |
|----------|-------------|---------|
| Utility | Transactional updates the user is expecting (order confirmations, shipping, payment receipts, appointment reminders) | Free when sent inside an open customer service window opened by the user; otherwise billed per template message |
| Authentication | OTP and verification codes | Billed per authentication template message |
| Marketing | Promotions, offers, newsletters, re-engagement | Billed per marketing template message (typically the most expensive tier) |
| Service (non-template) | Free-form replies inside the customer service window | Free, and not capped |

Confirm current Israel-specific rates on the Meta pricing page before quoting numbers to a customer. Do not hardcode an Israeli per-message rate into code or a proposal: read Meta's rate card and look up the row for country calling code **972**, because rates vary by country, by template category and by volume tier.

**Free messaging beyond the paid template categories:**
- **24h Customer Service Window (CSW)**: opens when the user sends an inbound message. All non-template messages are free inside it, and have been free and uncapped since 1 November 2024. Utility templates sent in response to the user inside an open CSW are also free.
- **72h free entry point window**: opens when the user clicks a Click-to-WhatsApp (CTWA) ad on Facebook or Instagram. All messages, including template messages, are free for 72 hours. A very common Israeli acquisition pattern.
- **Authentication templates are billed even inside the CSW**, unlike utility templates. Trap that catches Israeli OTP-heavy products (banks, fintech).

**Pricing cadence in 2026, worth designing around:** Meta may update pricing only on the first day of a quarter, so at most four times a year: 1 January, 1 April, 1 July and 1 October. Two further changes matter for planning. Businesses on the Marketing Messages API can set a **max price per marketing message delivery**, so Meta charges that price or lower, which turns marketing spend into a budgeted number rather than a variable one. Separately, a distinct pricing policy applies to **AI Providers** on the platform, effective 16 February 2026.

**Template categories for Israeli businesses:**

| Category | Use Case | Example (Hebrew, simplified) |
|----------|----------|-------------------|
| Appointment reminder (Utility) | Clinics, salons, services | תזכורת: יש לך תור ב-{{1}} בתאריך {{2}} בשעה {{3}} |
| Order confirmation (Utility) | E-commerce, delivery | הזמנתך ({{1}}) התקבלה. נעדכן כשתישלח. |
| Shipping update (Utility) | Logistics | המשלוח שלך בדרך. מעקב: {{1}} |
| Payment receipt (Utility) | Billing, invoicing | התקבל תשלום של {{1}} ש"ח. תודה. |
| OTP (Authentication) | Login, verification | קוד האימות שלך הוא {{1}}. תוקף 5 דקות. |
| Welcome message (Marketing or Utility) | Onboarding | שלום {{1}}, ברוכים הבאים ל-{{2}}. איך נוכל לעזור? |
| Promotion (Marketing) | Sales, holiday campaigns | (see the compliant MARKETING body in Step 4, which carries the mandatory Israeli disclosure block) |

**Hebrew and RTL template mechanics.** Four rules that cause most Israeli template failures:
- Meta's language code for Hebrew is **`he`**, not `he_IL`. A wrong code either fails submission or creates a language version nobody sends to.
- **Template names must be lowercase ASCII with underscores.** A Hebrew template name is rejected outright. Name the template `appointment_reminder_he` and put the Hebrew in the body.
- One template name holds **one version per language**. Create `he` and `en` versions under the same name rather than two differently named templates, so your sending code picks a language rather than a name.
- **Do not start an RTL body with a variable.** A body beginning `{{1}}` gives the reviewer no Hebrew context and renders unpredictably when the substituted value is a number or a Latin string. Start with a Hebrew word (`שלום {{1}}` rather than `{{1}} שלום`).

**Submit template for approval:**
```python
def create_template(waba_id: str, access_token: str, template: dict):
    """Create a WhatsApp message template."""
    url = f"https://graph.facebook.com/v26.0/{waba_id}/message_templates"
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
| Body starting with `{{1}}` and no language code | Variable-first RTL body, unclear language | Start with a Hebrew word, set `language: "he"`, add the Israeli disclosure footer from Step 4 |

### Step 3: Send Messages

**Send a template message:**
```python
def send_template_message(phone_number_id: str, access_token: str,
                          to: str, template_name: str, language: str,
                          parameters: list):
    """Send a WhatsApp template message."""
    url = f"https://graph.facebook.com/v26.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # Format: 972541234567 (no leading + and no leading 0)
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

**Send an interactive list (within the customer service window):**
```python
def send_interactive_list(phone_number_id: str, access_token: str,
                          to: str, body_text: str, sections: list):
    """Send an interactive list message in Hebrew."""
    url = f"https://graph.facebook.com/v26.0/{phone_number_id}/messages"
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

`scripts/send_whatsapp.py` implements the same three shapes (`--mode template|text|interactive|list`) with Israeli phone validation and a `--dry-run` flag.

### Step 3.5: Quality Rating and Number Warming

WhatsApp assigns every business phone number a quality tier (Green, Yellow, Red). Meta evaluates the tier every 6 hours based on user-reported spam, block rate, and template rejection ratio. A Yellow or Red tier limits how many users you can message per 24h, and a sustained Red tier can pause sending entirely.

**Warming a new Israeli number (the first 30 days are critical):**

1. **Days 1-7**: send only UTILITY templates to opted-in customers who actively expect them (order confirmations, OTP). No marketing.
2. **Days 7-14**: introduce small marketing batches (50-200 recipients), only to users who opted in within the last 30 days.
3. **Days 14-30**: scale gradually. Stop immediately if quality drops to Yellow.
4. **Always**: include a clear opt-out line in marketing templates ("להסרה השיבו 'הסר'"), and remove opted-out numbers from the sending list before the next send.

**If quality drops to Yellow**: pause marketing for 48h, send only UTILITY to engaged users, review recent template content for promotional drift, and audit the opt-in source for the affected segment.

**Messaging limits are set at the business portfolio level and shared by every phone number in that portfolio**, which means moving a campaign to a fresh number does NOT reset your limit if the new number is under the same portfolio. The limit is the number of unique WhatsApp users you can message outside a customer service window in a moving 24-hour period. The full ladder is:

| Limit | How you reach it |
|---|---|
| 250 | Default for a newly created business portfolio |
| 2,000 | Complete a scaling path: verify your business, have your partner verify it, or deliver 2,000 messages outside customer service windows to unique users over a 30-day moving window using high-quality templates |
| 10,000 | Automatic scaling, based on Meta's analysis of message quality |
| 100,000 | Automatic scaling |
| Unlimited | Automatic scaling |

The intermediate 2,000 tier is the one people forget: it is the only rung you actively earn, and business verification is the fastest route to it. Verify your current cap in WhatsApp Manager, or via the `whatsapp_business_manager_messaging_limit` field on the phone number (the older `messaging_limit_tier` field is deprecated).

### Step 4: Israeli Timing and Compliance

**Statutory scope, stated honestly.** Israeli commercial messaging is governed by section 30א of the Communications (Bezeq and Broadcasts) Law, known as חוק הספאם, added by Amendment 40. Section 30א enumerates exactly four channels: פקסימיליה, מערכת חיוג אוטומטי, הודעה אלקטרונית and מסר קצר. **WhatsApp is not named in the statute.** Coverage is generally assumed through a broad reading of "electronic message", which is an interpretive position rather than statutory text, and public guidance still lists only those four channels. The practical instruction is therefore: **assume WhatsApp marketing is covered and comply fully.** Do not tell an Israeli business the statute names WhatsApp, and do not tell them it clearly does not apply.

The definition of דבר פרסומת is broader than "an advert". It covers a commercially distributed message encouraging a purchase or other spending, a message soliciting a donation or propaganda, and a message distributed to the public that merely invites the recipient to call a number. Messages inducing a callback, including the צינתוק pattern where an automated dialler hangs up before answer and the returned call plays an advert, fall inside it.

**Consent, and the existing-customer route that actually exists.** The default rule is prior explicit opt-in. But section 30א(ג) provides a real route for an existing customer list, and telling an Israeli marketer their customer list is simply illegal is wrong. The route applies where **all** of the following hold:

1. The recipient gave their details **in the course of purchasing a product or service, or during negotiations toward such a purchase**.
2. The advertiser **notified them** that the details given would be used to send advertising.
3. The advertiser gave a **simple and reasonable opportunity to refuse**, and the recipient did not refuse.
4. The advertising concerns **goods or services of the same kind** as those purchased or negotiated.

Limb 4 is the one that gets skipped. Sources differ on whether it is counted as a separate condition or folded into the others, so treat it as part of a four-part test and flag it: a gym cannot use this route to advertise an unrelated insurance product to its members.

Two further carve-outs: a **single, one-off approach to a business recipient** offering to send it marketing messages is permitted, and an עמותה or חל"צ may send donation-solicitation or propaganda messages until the recipient refuses.

**Mandatory message content, section 30א(ה).** This is absent from most Israeli WhatsApp implementations and it is not optional. A commercial message must state, conspicuously and clearly (באופן בולט וברור):
- that the message is a **דבר פרסומת**;
- the advertiser's **name, address and contact details**;
- the recipient's **right to refuse** further advertising and **how to exercise it**.

The subject or heading must faithfully reflect the content. A marketing template without this block is non-compliant even if consent was perfect. A compliant Hebrew MARKETING body therefore looks like this, and this is the shape to copy:

```
דבר פרסומת
מבצע חג: {{1}} בהנחה של {{2}}%. בתוקף עד {{3}}.
המפרסם: מרפאת השיניים ד״ר כהן, רחוב הרצל 10 תל אביב, טלפון 03-1234567.
אינך חייב לקבל פרסומות. להסרה השיבו 'הסר' להודעה זו.
```

**Exposure, stated precisely.** Under section 30א(י)(1) a court **may** award compensation of up to **NIS 1,000 per advertisement** sent in breach, without the recipient proving any damage. It is a discretionary ceiling, not an automatic tariff, and awards accumulate across messages. Enforcement in practice is overwhelmingly private, through small-claims suits and class actions, rather than regulator action. Breach is also a criminal offence carrying a fine of up to NIS 226,000, though criminal enforcement has been rare.

**Amendment 13 to the Privacy Protection Law, in force 14 August 2025, made operational.** The point for a marketer is simple: **a marketing phone list is a מאגר מידע.** Amendment 13 expanded the Privacy Protection Authority's investigative and audit powers and introduced a mandatory ממונה על הגנת הפרטיות (privacy protection officer) for public bodies, their processors, data brokers, operators conducting systematic monitoring, and processors of sensitive data at scale. So: know where each number came from, keep the opt-in record, do not buy lists, and do not ship the list to a processor abroad without an adequate protection basis.

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
        "Consent basis recorded: explicit opt-in, or the section 30A(c) existing-customer route",
        "Opt-in record stored: who, what, timestamp, channel",
        "Opt-out mechanism included (e.g., reply 'הסר' / 'STOP')",
        "Phone numbers obtained lawfully; the list is treated as a database",
        "Message sent in appropriate language (Hebrew or English)",
    ]
    if message_type == "marketing":
        checks.extend([
            "Marketing template approved by Meta in MARKETING category",
            "Message labelled as a davar pirsomet",
            "Advertiser name, address and contact details stated in the body",
            "Right to refuse and how to exercise it stated in the body",
            "If relying on the existing-customer route, the goods are of the same kind",
            "Not sent during Shabbat or Jewish holidays for B2C",
            "No cross-border list transfer without adequate protection",
        ])
    return checks
```

### Step 4.5: Beyond Templates (Flows, Calls, Catalog, CTWA)

Common 2026 features Israeli businesses ask about, in priority order:

- **WhatsApp Flows**: native multi-step forms (lead capture, booking, surveys) rendered inside the chat. Cloud API only. Replaces many "external Google Form linked from WhatsApp" patterns. Useful for kupot/clinic intake, real-estate lead capture, restaurant reservations.
- **Click-to-WhatsApp ads (CTWA)**: Facebook/Instagram ads that open a chat with your business. Opens the 72h free entry point window described above. Israel's dominant paid acquisition channel for WhatsApp.
- **WhatsApp Business Calling API**: voice calling from a verified business number. User-initiated calling is available everywhere Cloud API is available. Business-initiated calling is available everywhere Cloud API is available **except** the United States, Canada, Egypt, Vietnam and Nigeria, so **Israel is supported**. Pricing is separate from messaging.
- **Catalog and Commerce**: product catalogs and in-chat product cards. WhatsApp Pay is NOT available in Israel. In-chat payments exist only in India and Brazil (where card payments ended on 15 January 2026, leaving Pix and payment links), plus a business-only capability in Singapore. Israeli checkout must redirect to your own payment page (Cardcom, Tranzila, Pelecard, Bit, Apple/Google Pay, etc.).
- **Phone-number migration between BSPs**: 2-step verification PIN must be removed before migration. Plan a maintenance window because messages in flight can be dropped. Document the source phone-number ID before initiating.
- **On-Premises API has reached end of support (final version expired 23 October 2025).** Migrate any legacy On-Prem deployments to Cloud API or to a BSP-hosted gateway. Do NOT recommend the On-Prem path to new users.

**General-purpose AI assistant restriction (effective 15 January 2026, with new sign-ups blocked from 15 October 2025):** Meta no longer permits general-purpose AI chatbots on WhatsApp Business. Purpose-specific bots (customer support, bookings, product Q&A, order status) remain allowed. This affects the local ChatGPT-style WhatsApp wrapper market.

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
Result: an approved UTILITY template with sending automation and compliance checks. Utility templates sent in response to the user inside an open customer service window are free; outside the window they are billed per template message.

### Example 2: E-commerce Order Updates
User says: "I want to send order confirmations and shipping updates via WhatsApp."
Actions:
1. Create an order confirmation UTILITY template (Hebrew).
2. Create a shipping notification UTILITY template with a tracking link.
3. Set up the inbound webhook to receive delivery status updates.
4. Integrate with Israeli shipping providers (Cheetah, HFD, Israel Post, Yamit, Yango Delivery).
Result: automated order lifecycle messaging in Hebrew, with predictable per-message billing.

### Example 3: Marketing Campaign
User says: "Send a promotion to our customer list for a holiday sale."
Actions:
1. Establish the consent basis: explicit opt-in, or the section 30A(c) existing-customer route including the same-kind-of-goods limb.
2. Create a MARKETING template carrying the mandatory disclosure block (davar pirsomet label, advertiser name and address, refusal route).
3. Confirm the portfolio messaging limit covers the audience size, and schedule for Israeli business hours (avoid Shabbat and chag eve).
4. Track delivery, read rates, and replies; honour opt-outs and remove them before the next send.
Result: a compliant promotional campaign with Israeli timing and per-message marketing billing.

## Bundled Resources

### Scripts
- `scripts/send_whatsapp.py`: Sends WhatsApp Business messages via the Meta Cloud API for the Israeli market. Supports template messages, free-form text, interactive reply buttons (Hebrew labels by default) and interactive lists. Includes Israeli phone number validation, Shabbat-aware sending time checks, HTTP status handling and a `--dry-run` mode. Run: `python scripts/send_whatsapp.py --help`

## Reference Links

- WhatsApp Business Platform overview: https://developers.facebook.com/documentation/business-messaging/whatsapp
- Graph API changelog (find current stable version): https://developers.facebook.com/docs/graph-api/changelog
- WhatsApp pricing (per-message, in force since 1 July 2025): https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- Messaging limits and the scaling ladder: https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits
- Per-user marketing template message limits: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits
- WhatsApp Business Calling API: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling
- Cloud API error codes: https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes
- Israeli anti-spam law, compensation and the exemptions (Kol-Zchut): https://www.kolzchut.org.il/he/index.php?curid=14302
- Information for recipients of spam, Israel Internet Association: https://www.isoc.org.il/freedom-of-internet/spam/information-to-recipients-of-spam
- Privacy Protection Authority (Amendment 13): https://www.gov.il/he/departments/the_privacy_protection_authority
- 360dialog (BSP): https://www.360dialog.com/
- MessageBird/Bird (BSP): https://bird.com/
- Twilio WhatsApp Business: https://www.twilio.com/en-us/messaging/channels/whatsapp
- Infobip WhatsApp: https://www.infobip.com/whatsapp-business
- Vonage WhatsApp: https://developer.vonage.com/en/messages/concepts/whatsapp
- Gupshup WhatsApp: https://www.gupshup.io/whatsapp
- AiSensy (BSP, popular with SMBs): https://www.aisensy.com/
- Sinch WhatsApp: https://www.sinch.com/products/messaging/whatsapp/
- WhatsApp Flows overview: https://developers.facebook.com/docs/whatsapp/flows
- On-Premises API sunset notice (final version expired 23 October 2025): https://developers.facebook.com/docs/whatsapp/on-premises/sunset

## Gotchas

- Israeli phone numbers for the WhatsApp API use the 972 country code **without a leading `+` and without the leading zero**: `972521234567`. Both `+9720521234567` (extra zero) and `0521234567` (local form) are wrong for the API. Agents add the extra zero constantly, which causes "phone number not found on WhatsApp" errors. The bundled script normalises all three forms and names the leading-zero cause explicitly in its error message.
- WhatsApp message templates submitted in Hebrew must pass Meta's review. UTILITY templates with promotional language are commonly rejected (and should be MARKETING). Templates with Hebrew text inside code blocks or with missing variable examples are also commonly rejected.
- **Every Hebrew MARKETING template needs the section 30א(ה) disclosure block** (davar pirsomet label, advertiser name and address, refusal route). Templates copied from generic international examples never have it.
- **The existing-customer route is real but narrow.** Section 30א(ג) permits messaging a customer who gave their details during a purchase or negotiation, was told the details would be used for advertising, was given a simple opportunity to refuse and did not, provided the advertising concerns goods of the same kind. Missing any limb puts you back on the explicit opt-in rule.
- WhatsApp Business has a 24-hour customer service window. After 24 hours since the user's last inbound message, only pre-approved template messages can be sent, and depending on category they are billed per template message under the pricing model in force since 1 July 2025.
- Hebrew text in template variables can break formatting when mixed with numbers or English. Use Unicode isolate characters (U+2066 to U+2069) around mixed-direction content, or design templates so variables don't contain mixed-direction substrings.
- Per-message pricing (since 1 July 2025): utility, authentication and marketing categories are billed per template message, not per 24h conversation. Non-template messages inside the customer service window have been free and uncapped since 1 November 2024, so any advice built around a monthly free-conversation allowance is obsolete. Always re-check the Meta rate card for country code 972 before quoting Israeli rates.
- **The per-user marketing cap DOES apply to Israeli recipients.** WhatsApp limits how many marketing template messages a given user receives when they are less likely to engage, and the limit adapts to that user's recent read rate and inbox activity. It is not active only for messages sent from or to the European Economic Area, the United Kingdom, Japan or South Korea. **Israel is not on that exclusion list, so plan for the cap.** Separately, marketing template messages are **not currently delivered to United States (+1) numbers at all**, so an Israeli business with US customers needs a different channel for them.
- **Messaging limits are per business portfolio**, not per phone number. Adding a second number under the same portfolio will NOT double your daily cap. The ladder is 250, then 2,000 (earned), then 10,000, 100,000 and unlimited by automatic scaling.
- **Authentication templates are billed even inside the 24h Customer Service Window**, unlike utility templates which are free in window. Israeli OTP-heavy products (banks, e-wallets, identity verification) frequently overlook this.
- **Israeli mobile prefixes accepted by WhatsApp**: 050 (Pelephone), 051 (We4G), 052 (Cellcom), 053 (HOT Mobile), 054 (Partner), 055 (MVNOs), 058 (Golan Telecom). Validation regex that excludes 051 will reject real subscribers. A landline fallback pattern that is not anchored against `05` will silently accept invalid mobile prefixes such as 056, 057 and 059.

## Troubleshooting

### Error: "Template rejected"
Cause: the template content does not match its category, or the submission is missing required fields.
Solution: work through the rejection table in Step 2, which lists the four patterns that account for most Hebrew rejections and the corrected text for each. Then confirm the Hebrew and RTL mechanics in Step 2 (language code `he`, lowercase ASCII template name, no variable-first body).

### Error: "Message failed to send"
Cause: depends on the error code returned. Read it rather than guessing.

| Code | Meaning | What to do |
|---|---|---|
| 131047 | More than 24 hours have passed since the recipient last replied to your number | Send an approved template instead of a free-form message |
| 131026 | Message undeliverable: the number is not a WhatsApp number, the recipient has not accepted the current Terms and Privacy Policy, or is on an unsupported WhatsApp version | Verify the number format (`972...`, no `+`, no leading zero) and confirm the recipient is reachable on WhatsApp |
| 130429 | Rate limit hit | Back off and retry with exponential delay; check throughput against your portfolio limit |
| 131049 | Not delivered in order to maintain healthy ecosystem engagement: the per-user marketing template limit, or repeated retries to a user who already hit it | Wait at least 24 hours before resending to that user. Do not retry immediately, which triggers further suppression |

Note that the per-user marketing cap shows up as suppression and non-delivery reported through the messages webhook, not as a synchronous send error, so check webhook statuses and not just the API response.

### Error: "Webhook not receiving messages"
Cause: webhook URL not verified, Meta App not subscribed to `messages` field, WABA not subscribed to the app, or signature validation failing.
Solution: ensure the webhook URL is HTTPS, the verification token matches, the Meta App is subscribed to the `messages` webhook field, **and the WABA itself is subscribed to your app** (a separate step from the app subscribing to the field, and a common miss), and that your handler validates `X-Hub-Signature-256` against the App secret.
