---
name: israeli-whatsapp-business
description: Integrate WhatsApp Business API for the Israeli market with Hebrew message templates, customer communication, and CRM integration. Use when user asks about WhatsApp Business in Israel, Hebrew WhatsApp templates, WhatsApp marketing to Israeli customers, business messaging via WhatsApp, or integrating WhatsApp with Israeli CRM tools (Monday.com, Priority, etc.). Covers Cloud API setup, template creation, per-message pricing, compliance with Israeli anti-spam law and Privacy Law Amendment 13, and Israeli consumer communication preferences. Do NOT use for personal WhatsApp or non-Israeli WhatsApp markets.
license: MIT
allowed-tools: Bash(python:*), Bash(curl:*), WebFetch
compatibility: Requires Meta Business Account and WhatsApp Business API access. Network access required.
---

# Israeli WhatsApp Business

## Instructions

### Step 0: Decide whether the user needs the Platform at all

Most Israeli small businesses are on the free **WhatsApp Business app**, not the **WhatsApp Business Platform** (Cloud API). Ask first. If the user only needs a catalog, quick replies, labels and manual chats, the app is the right answer and the rest of this skill is overhead. Route to the Platform only for automation, templates at scale, CRM sync or webhooks. Two consequences:

- A number already on the WhatsApp Business app does **not** necessarily lose its chats. Embedded Signup can onboard it while the business keeps using the app, and WhatsApp keeps message history in sync between the app and the Platform (`references/platform-2026.md` section 7). Confirm the BSP's signup flow supports this before promising it.
- Platform access needs a business portfolio, a WABA and a system user token. A non-technical owner will usually go through a BSP instead.

**Meta Business Verification** is the gate most Israeli businesses trip on. A new business portfolio is capped at a messaging limit of 250 (see Step 3.5), and verifying the business is one of the paths that raises it to 2,000.

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

**Direct Cloud API or a BSP?** Direct is cheaper and avoids lock-in, but you own token rotation, webhook hosting and retries. Before recommending one of the BSPs above, walk the five selection questions in `references/bsp-selection.md` (billing pass-through, Israeli invoicing, WABA ownership, template tooling, Hebrew support on Israeli hours).

### Step 2: Create Hebrew Message Templates

**Message categories (Meta pricing model, per-message billing in force since 1 July 2025, replacing the older 24h conversation-based model):**
WhatsApp bills per **template message** in three paid categories, plus non-template (service) messages, which become billable on 1 October 2026:

| Category | When to use | Billing |
|----------|-------------|---------|
| Utility | Transactional updates the user is expecting (order confirmations, shipping, payment receipts, appointment reminders) | Free in response to the user inside an open customer service window until 30 September 2026, billed from 1 October 2026; outside the window, billed per template message |
| Authentication | OTP and verification codes | Billed per authentication template message |
| Marketing | Promotions, offers, newsletters, re-engagement | Billed per marketing template message (typically the most expensive tier) |
| Service (non-template) | Free-form replies inside the customer service window | Free until 30 September 2026. From 1 October 2026 billed per message, with 1,000 free service messages a month per business phone number |

Confirm current Israel-specific rates on the Meta pricing page before quoting numbers to a customer. Do not hardcode an Israeli per-message rate into code or a proposal: read Meta's rate card and look up the row for country calling code **972**, because rates vary by country, by template category and by volume tier.

**Free messaging windows (changing on 1 October 2026):**
- **24h Customer Service Window (CSW)**: opens when the user sends an inbound message. Non-template messages inside it have been free since 1 November 2024, and utility templates sent in response to the user inside it since 1 July 2025. **Both become billable on 1 October 2026.** Each business phone number then gets 1,000 free service messages a month, and Meta charges from the 1,001st. Add a payment method to the WhatsApp Business account by 30 September 2026: Meta's pages differ on whether an account without one gets its first 1,000 service messages a month delivered or has service-message delivery stopped from 1 October. A support-heavy Israeli store should budget for this now (`references/platform-2026.md` section 1).
- **72h free entry point window**: opens when the user clicks a Click-to-WhatsApp (CTWA) ad on Facebook or Instagram. All messages, including template messages, are free for 72 hours. A very common Israeli acquisition pattern.
- **Authentication templates are always billed per message.** Meta's category table has no in-window exception for them, so an open CSW does not make an OTP free. Trap that catches Israeli OTP-heavy products (banks, fintech).

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

**Concrete Hebrew rejection patterns**, with the corrected text for each, are in `references/template-rejections.md`.

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

`scripts/send_whatsapp.py` implements four modes (`--mode template|text|interactive|list`) with Israeli phone validation and a `--dry-run` flag. An interactive-list example is in `references/interactive-list.md`.

### Step 3.5: Quality Rating and Number Warming

WhatsApp tracks how users receive each business number's messages (blocks, spam reports and similar signals). Poor quality stops the messaging limit from scaling, can pause the templates involved (`references/platform-2026.md` section 5), and can restrict sending from the number altogether (error 131048). Meta raises a portfolio's limit by one level within 6 hours once it is sending high-quality messages and has used at least half its current limit in the last 7 days.

**Warming a new Israeli number (the first 30 days are critical):**

1. **Days 1-7**: send only UTILITY templates to opted-in customers who actively expect them (order confirmations, OTP). No marketing.
2. **Days 7-14**: introduce small marketing batches (50-200 recipients), only to users who opted in within the last 30 days.
3. **Days 14-30**: scale gradually. Stop immediately if the quality rating drops.
4. **Always**: include a clear opt-out line in marketing templates ("להסרה השיבו 'הסר'"), and remove opted-out numbers from the sending list before the next send.

**If the quality rating drops**: pause marketing for 48h, send only UTILITY to engaged users, review recent template content for promotional drift, and audit the opt-in source for the affected segment.

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

**Statutory scope, stated honestly.** Israeli commercial messaging is governed by section 30א of the Communications (Bezeq and Broadcasts) Law, known as חוק הספאם. Section 30א enumerates exactly four channels: פקסימיליה, מערכת חיוג אוטומטי, הודעה אלקטרונית and מסר קצר. **WhatsApp is not named in the statute.** Coverage is generally assumed through a broad reading of "electronic message", which is an interpretive position rather than statutory text, and public guidance still lists only those four channels. The practical instruction is therefore: **assume WhatsApp marketing is covered and comply fully.** Do not tell an Israeli business the statute names WhatsApp, and do not tell them it clearly does not apply.

The definition of דבר פרסומת is broader than "an advert". It covers a commercially distributed message encouraging a purchase or other spending, a message soliciting a donation or propaganda, and a message distributed to the public that merely invites the recipient to call a number. Messages inducing a callback, including the צינתוק pattern where an automated dialler hangs up before answer and the returned call plays an advert, fall inside it.

**Consent, and the existing-customer route that actually exists.** The default rule is prior explicit opt-in. But section 30א(ג) provides a real route for an existing customer list, and telling an Israeli marketer their customer list is simply illegal is wrong. The route applies where **all** of the following hold:

1. The recipient gave their details **in the course of purchasing a product or service, or during negotiations toward such a purchase**.
2. The advertiser **notified them** that the details given would be used to send advertising.
3. The advertiser gave a **simple and reasonable opportunity to refuse**, and the recipient did not refuse.
4. The advertising concerns **goods or services of the same kind** as those purchased or negotiated.

Limb 4 is the one that gets skipped. Sources differ on whether it is counted as a separate condition or folded into the others, so treat it as part of a four-part test and flag it: a gym cannot use this route to advertise an unrelated insurance product to its members.

Two further carve-outs: a **single, one-off approach to a business recipient** offering to send it marketing messages is permitted, Donation-solicitation and propaganda messages from an עמותה or חל"צ are also exempt from prior consent until the recipient refuses, but **only when sent by email**, so this carve-out does not cover WhatsApp.

**Mandatory message content, section 30א(ה).** This is absent from most Israeli WhatsApp implementations and it is not optional. A commercial message must state, conspicuously and clearly (באופן בולט וברור):
- the advertiser's **name, address and contact details**;
- the recipient's **right to refuse** further advertising and **how to exercise it**.

Opening the message with the words דבר פרסומת is common, prudent practice; confirm the exact statutory wording with counsel. A marketing template without the advertiser details and the refusal route is non-compliant even if consent was perfect. A compliant Hebrew MARKETING body therefore looks like this, and this is the shape to copy:

```
דבר פרסומת
מבצע חג: {{1}} בהנחה של {{2}}%. בתוקף עד {{3}}.
המפרסם: מרפאת השיניים ד״ר כהן, רחוב הרצל 10 תל אביב, טלפון 03-1234567.
אינך חייב לקבל פרסומות. להסרה השיבו 'הסר' להודעה זו.
```

**Exposure, stated precisely.** Under section 30א(י)(1) a court **may** award compensation of up to **NIS 1,000 per advertisement** sent in breach, without the recipient proving any damage. It is a discretionary ceiling, not an automatic tariff, and awards accumulate across messages. Enforcement in practice is overwhelmingly private, through small-claims suits and class actions, rather than regulator action. Breach is also a criminal offence carrying a fine of up to NIS 226,000, though criminal enforcement has been rare.

**Amendment 13 to the Privacy Protection Law, made operational.** The point for a marketer is simple: **treat a marketing phone list as a מאגר מידע** and check the Privacy Protection Authority's current guidance before building one. So: know where each number came from, keep the opt-in record, do not buy lists, and do not ship the list to a processor abroad without an adequate protection basis.

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

```

A pre-send compliance checklist (consent basis, opt-in record, the section 30A(e) disclosure block, same-kind goods, no Shabbat or chag sends, no cross-border list transfer) is in `references/compliance-checklist.md`.

### Step 4.5: Beyond Templates (Flows, Calls, Catalog, CTWA)

Common 2026 features Israeli businesses ask about, in priority order:

- **WhatsApp Flows**: native multi-step forms (lead capture, booking, surveys) rendered inside the chat. Cloud API only. Replaces many "external Google Form linked from WhatsApp" patterns. Useful for kupot/clinic intake, real-estate lead capture, restaurant reservations.
- **Click-to-WhatsApp ads (CTWA)**: Facebook/Instagram ads that open a chat with your business. Opens the 72h free entry point window described above. Israel's dominant paid acquisition channel for WhatsApp.
- **WhatsApp Business Calling API**: voice calling from a verified business number. User-initiated calling is available everywhere Cloud API is available. Business-initiated calling is available everywhere Cloud API is available **except** the United States, Canada, Egypt, Vietnam and Nigeria, so **Israel is supported**. Pricing is separate from messaging.
- **Catalog and Commerce**: product catalogs and in-chat product cards. WhatsApp Pay is NOT available in Israel. Meta's in-chat Payments API documentation covers India and Brazil, not Israel. Israeli checkout must redirect to your own payment page (Cardcom, Tranzila, Pelecard, Bit, Apple/Google Pay, etc.).
- **Phone-number migration between BSPs**: check with both BSPs that the WABA's account setup allows migration before planning a switch, then follow the destination BSP's migration checklist and record the source phone-number ID before starting.
- **On-Premises API has reached end of support (final version expired 23 October 2025).** Migrate any legacy On-Prem deployments to Cloud API or to a BSP-hosted gateway. Do NOT recommend the On-Prem path to new users.

**General-purpose AI assistant restriction (effective 15 January 2026):** under WhatsApp's updated Terms of Service, "AI Providers" may offer general-purpose AI assistants on the WhatsApp Business Platform only where Meta is legally required to permit it. A bot scoped to your own business (support, bookings, order status) is a different use case. This affects the local ChatGPT-style WhatsApp wrapper market.

### Step 5: CRM Integration Guidance

**Monday.com + WhatsApp:**
1. Use Monday.com automations or third-party connectors (Make, Zapier, Pipedream) to bridge WhatsApp Cloud API and your boards.
2. Trigger WhatsApp template messages from board status changes (e.g., "Order shipped" status sends a UTILITY template).
3. Log incoming WhatsApp messages as Monday.com updates via the inbound webhook.
4. Link each Monday.com item to both the phone number (`wa_id`) and the business-scoped user ID (`user_id`). A customer who adopts a WhatsApp username can arrive with no phone number at all (`references/platform-2026.md` section 2).

**Custom CRM Integration:**
```python
SEEN_IDS: set = set()  # use a persistent store in production

def webhook_handler(event: dict) -> dict:
    """Handle a WhatsApp webhook: messages, delivery statuses and opt-outs."""
    for entry in event.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            if change.get("field") == "user_preferences":
                # User stopped or resumed marketing inside WhatsApp:
                # write it to the same suppression list as 'הסר' replies.
                # record_marketing_preference(value)
                continue
            if change.get("field") != "messages":
                continue
            for status in value.get("statuses", []):
                # sent / delivered / read / failed for an order update
                # status.get("errors") carries codes such as 131049 / 131050 on failures
                # update_delivery_status(status["id"], status["status"])
                pass
            contact = (value.get("contacts") or [{}])[0]
            for msg in value.get("messages", []):
                if msg["id"] in SEEN_IDS:  # Meta retries for up to 7 days
                    continue
                SEEN_IDS.add(msg["id"])
                crm_data = {
                    # Phone can be missing for users with a username
                    "phone": msg.get("from") or contact.get("wa_id"),
                    "bsuid": contact.get("user_id"),
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
Result: an approved UTILITY template with sending automation and compliance checks. Utility templates are billed per template message outside the customer service window, and from 1 October 2026 inside it as well.

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

### References
- `references/platform-2026.md`: the 2026 platform changes an Israeli integration must handle (service-message charging from 1 October 2026, business-scoped user IDs, in-WhatsApp marketing opt-out, webhook retries, template pausing, extra error codes, onboarding an existing app number).
- `references/bsp-selection.md`: the five questions for choosing between direct Cloud API and a BSP.
- `references/interactive-list.md`: a Hebrew interactive-list send example.
- `references/compliance-checklist.md`: the pre-send compliance checklist function.
- `references/domain-checklist.md`: the coverage checklist this skill is reviewed against.

## Reference Links

- WhatsApp Business Platform overview: https://developers.facebook.com/documentation/business-messaging/whatsapp
- Graph API changelog (find current stable version): https://developers.facebook.com/docs/graph-api/changelog
- WhatsApp pricing (per-message, in force since 1 July 2025): https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- Messaging limits and the scaling ladder: https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits
- Per-user marketing template message limits: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits
- WhatsApp Business Calling API: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling
- Cloud API error codes: https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes
- Israeli anti-spam law, compensation and the exemptions (Kol-Zchut): https://www.kolzchut.org.il/he/%D7%A4%D7%99%D7%A6%D7%95%D7%99_%D7%91%D7%92%D7%99%D7%9F_%D7%9E%D7%A9%D7%9C%D7%95%D7%97_%D7%93%D7%91%D7%A8%D7%99_%D7%A4%D7%A8%D7%A1%D7%95%D7%9E%D7%AA_%D7%9C%D7%9C%D7%90_%D7%94%D7%A1%D7%9B%D7%9E%D7%94_%D7%A9%D7%9C_%D7%94%D7%A0%D7%9E%D7%A2%D7%9F_(%D7%97%D7%95%D7%A7_%D7%94%D7%A1%D7%A4%D7%90%D7%9D)
- Information for recipients of spam, Israel Internet Association: https://www.isoc.org.il/freedom-of-internet/spam/information-to-recipients-of-spam
- Privacy Protection Authority (Amendment 13): https://www.gov.il/he/departments/the_privacy_protection_authority
- 360dialog (BSP): https://www.360dialog.com/whatsapp-business-api
- MessageBird/Bird (BSP): https://bird.com/
- Twilio WhatsApp Business: https://www.twilio.com/en-us/messaging/channels/whatsapp
- Infobip WhatsApp: https://www.infobip.com/whatsapp-business
- Vonage WhatsApp: https://developer.vonage.com/en/messages/concepts/whatsapp
- Gupshup WhatsApp: https://www.gupshup.io/whatsapp
- AiSensy (BSP, popular with SMBs): https://www.aisensy.com/
- Sinch WhatsApp: https://www.sinch.com/products/messaging/whatsapp/
- WhatsApp Flows overview: https://developers.facebook.com/documentation/business-messaging/whatsapp/flows
- On-Premises API sunset notice (final version expired 23 October 2025): https://developers.facebook.com/docs/whatsapp/on-premises/sunset

## Gotchas

- Israeli phone numbers for the WhatsApp API use the 972 country code **without a leading `+` and without the leading zero**: `972521234567`. Both `+9720521234567` (extra zero) and `0521234567` (local form) are wrong for the API. Agents add the extra zero constantly, which causes "phone number not found on WhatsApp" errors. The bundled script normalises all three forms and names the leading-zero cause explicitly in its error message.
- WhatsApp message templates submitted in Hebrew must pass Meta's review. UTILITY templates with promotional language are commonly rejected (and should be MARKETING). Templates with Hebrew text inside code blocks or with missing variable examples are also commonly rejected.
- **Every Hebrew MARKETING template needs the section 30א(ה) disclosure block** (davar pirsomet label, advertiser name and address, refusal route). Templates copied from generic international examples never have it.
- **The existing-customer route is real but narrow.** Section 30א(ג) permits messaging a customer who gave their details during a purchase or negotiation, was told the details would be used for advertising, was given a simple opportunity to refuse and did not, provided the advertising concerns goods of the same kind. Missing any limb puts you back on the explicit opt-in rule.
- WhatsApp Business has a 24-hour customer service window. After 24 hours since the user's last inbound message, only pre-approved template messages can be sent, and depending on category they are billed per template message under the pricing model in force since 1 July 2025.
- Hebrew text in template variables can break formatting when mixed with numbers or English. Use Unicode isolate characters (U+2066 to U+2069) around mixed-direction content, or design templates so variables don't contain mixed-direction substrings.
- Per-message pricing (since 1 July 2025): utility, authentication and marketing categories are billed per template message, not per 24h conversation. **From 1 October 2026 service messages and in-window utility replies are billed as well**, with 1,000 free service messages a month per business phone number, so any advice calling in-window replies free expires on that date. Always re-check the Meta rate card for country code 972 before quoting Israeli rates.
- **The per-user marketing cap DOES apply to Israeli recipients.** WhatsApp limits how many marketing template messages a given user receives when they are less likely to engage, and the limit adapts to that user's recent read rate and inbox activity. It is not active only for messages sent from or to the European Economic Area, the United Kingdom, Japan or South Korea. **Israel is not on that exclusion list, so plan for the cap.** Separately, marketing template messages are **not currently delivered to United States (+1) numbers at all**, so an Israeli business with US customers needs a different channel for them.
- **A customer may arrive without a phone number.** Since April 2026 webhooks carry a business-scoped user ID in `user_id`, and a user who adopts a WhatsApp username can arrive with no `wa_id`. Key CRM records on both identifiers (`references/platform-2026.md` section 2).
- **Messaging limits are per business portfolio**, not per phone number. Adding a second number under the same portfolio will NOT double your daily cap. The ladder is 250, then 2,000 (earned), then 10,000, 100,000 and unlimited by automatic scaling.
- **Authentication templates are billed per message even inside the 24h Customer Service Window.** The in-window exception for utility templates ends on 1 October 2026 and never applied to authentication. Israeli OTP-heavy products (banks, e-wallets, identity verification) frequently overlook this.
- **Israeli mobile prefixes accepted by WhatsApp**: 050 (Pelephone), 051 (We4G), 052 (Cellcom), 053 (HOT Mobile), 054 (Partner), 055 (MVNOs), 058 (Golan Telecom). Validation regex that excludes 051 will reject real subscribers. A landline fallback pattern that is not anchored against `05` will silently accept invalid mobile prefixes such as 056, 057 and 059.

## Troubleshooting

### Error: "Template rejected"
Cause: the template content does not match its category, or the submission is missing required fields.
Solution: work through `references/template-rejections.md`, which lists the four patterns that account for most Hebrew rejections and the corrected text for each. Then confirm the Hebrew and RTL mechanics in Step 2 (language code `he`, lowercase ASCII template name, no variable-first body).

### Error: "Message failed to send"
Cause: depends on the error code returned. Read it rather than guessing.

| Code | Meaning | What to do |
|---|---|---|
| 131047 | More than 24 hours have passed since the recipient last replied to your number | Send an approved template instead of a free-form message |
| 131026 | Message undeliverable: the number is not a WhatsApp number, the recipient has not accepted the current Terms and Privacy Policy, or is on an unsupported WhatsApp version | Verify the number format (`972...`, no `+`, no leading zero) and confirm the recipient is reachable on WhatsApp |
| 130429 | Rate limit hit | Back off and retry with exponential delay; check throughput against your portfolio limit |
| 131049 | Not delivered in order to maintain healthy ecosystem engagement: the per-user marketing template limit, or repeated retries to a user who already hit it | Wait at least 24 hours before resending to that user. Do not retry immediately, which triggers further suppression |
| 131050 | The user stopped marketing messages from your business inside WhatsApp | Do not retry. Add them to the same suppression list as 'הסר' replies, and subscribe to the `user_preferences` webhook |

Note that the per-user marketing cap shows up as suppression and non-delivery reported through the messages webhook, not as a synchronous send error, so check webhook statuses and not just the API response. Codes 131048, 131056 and 131042 are in `references/platform-2026.md` section 6.

### Error: "Webhook not receiving messages"
Cause: webhook URL not verified, Meta App not subscribed to `messages` field, WABA not subscribed to the app, or signature validation failing.
Solution: ensure the webhook URL is HTTPS, the verification token matches, the Meta App is subscribed to the `messages` webhook field, **and the WABA itself is subscribed to your app** (a separate step from the app subscribing to the field, and a common miss), and that your handler validates `X-Hub-Signature-256` against the App secret.
