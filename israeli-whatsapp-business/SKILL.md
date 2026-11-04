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

- A number already on the WhatsApp Business app does **not** necessarily lose its chats. Embedded Signup can onboard it while the business keeps using the app, and WhatsApp keeps message history in sync between the app and the Platform (`references/platform-2026.md` section 7). Confirm the BSP supports it before promising it.
- Platform access needs a business portfolio, a WhatsApp account and Messaging account (the two halves of what used to be the WABA, Step 1) and a system user token. A non-technical owner will usually go through a BSP instead.

**Meta Business Verification** is one of the scaling paths that lift a new portfolio's messaging limit from 250 to 2,000 (Step 3.5).

### Step 1: Verify WhatsApp Business Setup

Ensure the user has:
1. Meta Business Account (`business.facebook.com`)
2. A WhatsApp Business account linked to it. Since the account-model rollout (from 23 September 2026, reaching all businesses by mid-October 2026) Meta splits it into a **WhatsApp account** (the phone number, profile and catalog, always owned by the business) and a **Messaging account** (templates, billing, webhook subscriptions; one per partner). Existing WABA IDs now denote Messaging account IDs, and existing IDs, endpoints and tokens keep working (`references/platform-2026.md` section 8).
3. A registered phone number with Israeli prefix (`+972`), either the official Cloud API hosted by Meta, or via a Business Solution Provider (BSP). Examples of BSPs offering WhatsApp Business Platform access: 360dialog, MessageBird/Bird, Twilio, Infobip, Vonage, Gupshup, AiSensy, Sinch. Check that the one you pick serves Israeli accounts and can invoice locally
4. System User Access Token with the `business_management`, `whatsapp_business_messaging` and `whatsapp_business_management` permissions

Smoke test: `GET https://graph.facebook.com/v26.0/{phone_number_id}` with `Authorization: Bearer <token>` should return the number. v26.0 is the latest Graph API version; check the Graph API changelog before pinning another.

**Direct Cloud API or a BSP?** Direct is cheaper and avoids lock-in, but you own token rotation, webhook hosting and retries. Under the new account model a business adds or switches a BSP by sharing its WhatsApp account rather than migrating the number, but templates stay in the old partner's Messaging account. Before recommending one of the BSPs above, walk the five selection questions in `references/bsp-selection.md` (billing pass-through, Israeli invoicing, Messaging account ownership, template tooling, Hebrew support on Israeli hours).

### Step 2: Create Hebrew Message Templates

**Message categories (per-message billing since 1 July 2025, which replaced the older 24h conversation-based model).** Meta has five categories. Three are template categories; the other two are non-template replies, which can only be sent inside an open customer service window:

| Category | When to use | Billing |
|----------|-------------|---------|
| Utility | Transactional updates the user is expecting (order confirmations, shipping, payment receipts, appointment reminders) | Billed per message, inside the customer service window as well as outside it (free in-window only from 1 July 2025 to 30 September 2026) |
| Authentication | OTP and verification codes | Billed per message, inside the customer service window too (free only in a free entry point window) |
| Marketing | Promotions, offers, newsletters, re-engagement | Billed per message (typically the most expensive tier). Moving to the Marketing Messages API, see Step 3 |
| Service (non-template) | Free-form replies inside the window, by people or a third-party AI | Billed per message since 1 October 2026, after 1,000 free service messages a month per business phone number |
| Meta Business Agent (non-template) | Replies generated by Meta's own Business Agent platform (since July 2026) | One per-token charge since 1 August 2026, charged even in the free entry point window |

Israel is a named market on Meta's rate card (country calling code 972). Confirm current Israel-specific rates on the Meta pricing page before quoting numbers to a customer. Do not hardcode an Israeli per-message rate into code or a proposal: read Meta's rate card and look up the row for country calling code **972**, because rates vary by country, by template category and by volume tier.

**Free messaging, as it stands since 1 October 2026:**
- **24h Customer Service Window (CSW)**: opens with each inbound user message, and is the only time non-template messages can be sent. **It is no longer a free window.** Service messages (free since 1 November 2024) and utility templates sent in response inside it (free since 1 July 2025) have both been billed since 1 October 2026. Each business phone number gets 1,000 free service messages a month, which reset monthly and do not roll over. A Messaging account with no payment method gets its free-tier service messages delivered and nothing beyond them, so a support-heavy Israeli store can have replies silently failing from the 1,001st of the month (`references/platform-2026.md` section 1).
- **Free entry point window**: when a user messages you from a Click-to-WhatsApp (CTWA) ad on the Android or iOS app (desktop and web do not qualify) and you reply inside the customer service window, that reply is free and opens a window that may stay open for up to 7 days from your reply. While it is open, marketing, utility, authentication and service messages are free; Meta Business Agent messages are not. Miss the 24h window and there is no free window.
- **Authentication templates are billed even inside the customer service window.** Only a free entry point window makes them free, so an open CSW does not make an OTP free. Trap that catches Israeli OTP-heavy products (banks, fintech).
- **Government bodies and community non-profits** that Meta has identified as eligible keep service messages free beyond the tier through 31 December 2027; do not assume an עמותה qualifies (`references/platform-2026.md` section 1).

**Pricing cadence:** Meta may change prices only on the first day of a quarter (1 January, 1 April, 1 July, 1 October). The Marketing Messages API max price (open beta since 1 October 2026) and the separate AI Providers policy (since 16 February 2026) are in `references/platform-2026.md` sections 9 and 1.

**Template categories for Israeli businesses:**

| Category | Use Case | Example (Hebrew, simplified) |
|----------|----------|-------------------|
| Appointment reminder (Utility) | Clinics, salons, services | תזכורת: יש לך תור ב-{{1}} בתאריך {{2}} בשעה {{3}} |
| Order confirmation (Utility) | E-commerce, delivery | הזמנתך ({{1}}) התקבלה. נעדכן כשתישלח. |
| Shipping update (Utility) | Logistics | המשלוח שלך בדרך. מעקב: {{1}} |
| Payment receipt (Utility) | Billing, invoicing | התקבל תשלום של {{1}} ש"ח. תודה. |
| OTP (Authentication) | Login, verification | No custom text: Meta supplies the preset text, an optional security disclaimer and expiry warning, plus a copy-code, one-tap or zero-tap button. You pass only the code |
| Welcome message (Marketing or Utility) | Onboarding | שלום {{1}}, ברוכים הבאים ל-{{2}}. איך נוכל לעזור? |
| Promotion (Marketing) | Sales, holiday campaigns | (see the compliant MARKETING body in Step 4, which carries the mandatory Israeli disclosure block) |

**Hebrew and RTL template mechanics.** Four rules that cause most Israeli template failures:
- Meta's language code for Hebrew is **`he`**, not `he_IL`. A wrong code either fails submission or creates a language version nobody sends to.
- **Template names must be lowercase ASCII with underscores.** A Hebrew template name is rejected outright. Name the template `appointment_reminder_he` and put the Hebrew in the body.
- One template name can hold **a version per language**. Create `he` and `en` versions under the same name rather than two differently named templates, so your sending code picks a language rather than a name.
- **Positional or named parameters.** Parameters are positional (`{{1}}`) unless you create the template with `parameter_format: "named"`. Named parameters are lowercase letters and underscores (`{{order_id}}`) and are sent with `parameter_name`; the script's `--named-parameters order_id=A1234` does that.
- **Do not start an RTL body with a variable.** A body beginning `{{1}}` gives the reviewer no Hebrew context and renders unpredictably when the substituted value is a number or a Latin string. Start with a Hebrew word (`שלום {{1}}` rather than `{{1}} שלום`).

**Submit for approval** with `POST /{waba_id}/message_templates` (the Messaging account ID). A complete Hebrew UTILITY submission (body with `example.body_text` values and quick-reply buttons) is in `references/template-rejections.md`.

Concrete Hebrew rejection patterns, with the corrected text for each, are in the same file.

### Step 3: Send Messages

**Send a template message.** `scripts/send_whatsapp.py` builds the exact `POST /{phone_number_id}/messages` payload in four modes (`--mode template|text|interactive|list`), validates Israeli numbers and has `--dry-run`, so use it, or read its `send_template_message` function, rather than hand-writing the JSON. The recipient goes in `to` as `972541234567` (no `+`, no leading zero). A customer who arrived with no phone number is addressed by business-scoped user ID in `recipient` instead (`--recipient`), and a customer abroad by the full international number (`--international`). A tracking link or an OTP goes in the URL button parameter (`--button-url-param`, `--button-index` if it is not the first button); an OTP template also carries the code as its body parameter. A media header (an image, or a PDF invoice) is sent with `--header-media document:<media_id>` or an https link; Meta's pages show no send shape for a text-header variable, so the script does not build one. Pass `--transactional` when the template's latest category is utility or authentication, so the Shabbat check does not hold back an order update or a login code. It is your declaration only: it does not change the category Meta bills or routes by. An interactive-list example is in `references/interactive-list.md`.

**Marketing templates are moving off the Cloud API.** Meta is sunsetting marketing messages on `/messages`: a Messaging account created on or after 13 April 2027 cannot send them through the Cloud API at all, and from 13 October 2027 any marketing send to `/messages` errors. Marketing goes to `POST /{phone_number_id}/marketing_messages` (the Marketing Messages API: same template payload, its own terms to accept in the App Dashboard). Route each send by the template's **latest** category, not the one you submitted, because Meta can recategorize a UTILITY template to MARKETING after approval; keep the mapping current from the `template_category_update` webhook. The script's `--endpoint marketing` sends there (`references/platform-2026.md` section 9).

### Step 3.5: Quality Rating and Number Warming

WhatsApp tracks how users receive each business number's messages (blocks, spam reports and similar signals). Poor quality stops the messaging limit from scaling, can pause the templates involved (`references/platform-2026.md` section 5), and can restrict sending from the number altogether (error 131048). Meta raises a portfolio's limit by one level within 6 hours once it is sending high-quality messages and has used at least half its current limit in the last 7 days.

**Warming a new Israeli number.** This schedule is a conservative practice heuristic, not a Meta rule; Meta's documented mechanics are the limits below.

1. **Days 1-7**: send only transactional templates to customers who expect them (UTILITY order confirmations, AUTHENTICATION codes). No marketing.
2. **Days 7-14**: introduce small marketing batches (50-200 recipients), only to users who opted in within the last 30 days.
3. **Days 14-30**: scale gradually. Stop immediately if the quality rating drops.
4. **Always**: include a clear opt-out line in marketing templates ("להסרה השיבו 'הסר'"), and remove opted-out numbers from the sending list before the next send.

**If the quality rating drops**, pause marketing, send only transactional templates, and review recent templates and the opt-in source of the affected segment (a heuristic, like the schedule above).

**Messaging limits are set at the business portfolio level and shared by every phone number in that portfolio**, which means moving a campaign to a fresh number does NOT reset your limit if the new number is under the same portfolio. The limit is the number of unique WhatsApp users you can message outside a customer service window in a moving 24-hour period. The full ladder is:

| Limit | How you reach it |
|---|---|
| 250 | Default for a newly created business portfolio |
| 2,000 | Complete a scaling path: verify your business, have your partner verify it, or deliver 2,000 messages outside customer service windows to unique users over a 30-day moving window using high-quality templates |
| 10,000 | Automatic scaling, based on Meta's analysis of message quality |
| 100,000 | Automatic scaling |
| Unlimited | Automatic scaling |

2,000 is the only rung you earn rather than reach by automatic scaling. Read the current cap in WhatsApp Manager or from the `whatsapp_business_manager_messaging_limit` field (`messaging_limit_tier` is deprecated).

### Step 4: Israeli Timing and Compliance

The statute text, with every subsection cited, is in `references/israeli-law.md`. The points an agent must not get wrong:

**Scope.** Section 30א of the Communications Law (חוק הספאם) bars sending a דבר פרסומת by fax, automatic dialling system, הודעה אלקטרונית or SMS without the recipient's prior express consent in writing. **WhatsApp is not named.** It fits the statutory definition of הודעה אלקטרונית (an encoded message carried over the internet that can be stored and retrieved), but that is a reading, not text. So **assume WhatsApp marketing is covered and comply fully**; never say the statute names WhatsApp, nor that it clearly does not apply. דבר פרסומת is broad: a commercial message encouraging a purchase or spending, a message to the public soliciting a donation or propaganda, and a message to the public inviting a call to a number (the צינתוק pattern).

**Consent, and the existing-customer route.** The default is prior express consent. Section 30א(ג) permits marketing without it when all three paragraphs hold: (1) the recipient gave their details while buying, or negotiating to buy, a product or service, and was told then, by one of the 30א(ב) channels (fax, automatic dialling, electronic message or SMS), that they would be used for advertising; (2) they were given a chance to refuse and did not; (3) the advertising concerns a product or service **of a similar kind**. A gym cannot use it to advertise unrelated insurance. Two traps: when an ongoing customer relationship ends, the customer is treated as having refused (30א(ד)(2)), so stop marketing to churned subscribers; and a refusal sent on the channel the advert came on counts, so a 'הסר' reply on WhatsApp is binding. A one-off approach to a **business** recipient offering to send it marketing is permitted. The עמותה and חל"צ donation carve-out is **email-only** (30א(ב1)) and does not cover WhatsApp.

**Mandatory content, section 30א(ה).** Clearly, conspicuously and not misleadingly:
- the word **פרסומת** at the **start** of the message. This is statutory, not a style choice;
- the advertiser's **name, address and contact details**;
- the right to refuse at any time and a simple, reasonable way to do it. For a הודעה אלקטרונית the statute also requires **a valid internet address of the advertiser for refusals**, so add a web or email opt-out address next to the 'הסר' reply. Do not rely on the shorter SMS list in 30א(ה)(2).

A compliant Hebrew MARKETING body, the shape to copy:

```
פרסומת
מבצע חג: {{1}} בהנחה של {{2}}%. בתוקף עד {{3}}.
המפרסם: מרפאת השיניים ד״ר כהן, רחוב הרצל 10 תל אביב, טלפון 03-1234567.
אינך חייב לקבל פרסומות. להסרה השיבו 'הסר' להודעה זו או היכנסו ל-{{4}}.
```

**Exposure.** A court may award up to **NIS 1,000 per advertisement** received in breach (30א(י)(1)), without proof of damage. It is a discretionary ceiling that accumulates across messages, and the advertiser is presumed to have sent knowingly unless it proves otherwise (30א(י)(5)). Criminal fines: up to NIS 226,000 for sending without a consent basis and up to NIS 75,300 for missing or misleading mandatory content (30א(ו), via Penal Law s.61), and a company's managers and marketing officers carry their own supervision duty (30א(ח)).

**Privacy Protection Law** (detail in `references/israeli-law.md` section 7). Amendment 13 took effect on 14 August 2025. Treat a marketing phone list as a מאגר מידע: keep each number's source and opt-in record, give the section 11 notice on the opt-in form (voluntary or not, purpose, controller and contact details, who receives it, access and correction rights), do not buy lists, and transfer a list abroad only under the transfer regulations. A campaign to a **segment** picked by database characteristics is also **דיוור ישיר**: section 17ו(א) requires each message to state that it is direct mail with the registration number of the database used for direct-mail services, the right to be deleted and where to ask, and the controller's identity, address and data sources.

Give the rules and the checklist; do not tell the user that a specific campaign or list is compliant. That judgement is for an Israeli lawyer.

**Sending schedule.** For template sends without `--transactional`, `scripts/send_whatsapp.py` refuses Friday after 14:00, all of Saturday, and outside 08:30 to 20:00 Israel time; free-form replies are never held. These are conservative heuristics: real Shabbat times vary by 30 to 60 minutes by season and city, and the check does not know Jewish holidays, so derive times from a Hebcal-style source for production B2C sends.

A pre-send compliance checklist (consent basis, opt-in record, the section 30א(ה) block, similar-kind goods, churned customers, direct-mail fields, no Shabbat or chag sends, no cross-border list transfer) is in `references/compliance-checklist.md`.

### Step 4.5: Beyond Templates (Flows, Calls, Catalog, CTWA)

Common 2026 features Israeli businesses ask about, in priority order:

- **WhatsApp Flows**: native multi-step forms (lead capture, booking, surveys) rendered inside the chat. Cloud API only. Replaces many "external Google Form linked from WhatsApp" patterns. Useful for kupot/clinic intake, real-estate lead capture, restaurant reservations.
- **Click-to-WhatsApp ads (CTWA)**: ads that open a chat with your business. Replying inside the window opens the free entry point window described above (up to 7 days).
- **WhatsApp Business Calling API**: voice calling from a verified business number. User-initiated calling is available everywhere Cloud API is available. Business-initiated calling is available everywhere Cloud API is available **except** the United States, Canada, Egypt, Vietnam and Nigeria, so **Israel is supported**. User-initiated calls are free; business-initiated calls are charged in six-second pulses by destination country and monthly volume tier.
- **Catalog and Commerce**: product catalogs and in-chat product cards. Meta's in-chat Payments API documentation covers India and Brazil, not Israel. Israeli checkout must redirect to your own payment page (Cardcom, Tranzila, Pelecard, Bit, Apple/Google Pay, etc.).
- **Changing or adding a BSP**: moving a business phone number from one Solution Partner to another is not supported in the new account model. The business shares its WhatsApp account with the new partner instead: the number does not move and conversations continue. Templates do not follow, because they belong to each partner's Messaging account; migrated templates' quality rating and messaging tier reset, with a ramp-up of roughly 2 to 4 weeks, so do not switch right before a holiday campaign.
- **On-Premises API**: end of support (final version expired 23 October 2025). Migrate legacy deployments to Cloud API or a BSP; never recommend it to new users.

**General-purpose AI assistants** are restricted on the Platform since 15 January 2026; a bot scoped to your own business is a different use case (`references/platform-2026.md` section 1).

### Step 5: CRM Integration Guidance

**Monday.com + WhatsApp:**
1. Use Monday.com automations or third-party connectors (Make, Zapier, Pipedream) to bridge WhatsApp Cloud API and your boards.
2. Trigger WhatsApp template messages from board status changes (e.g., "Order shipped" status sends a UTILITY template).
3. Log incoming WhatsApp messages as Monday.com updates via the inbound webhook.
4. Link each Monday.com item to both the phone number (`wa_id`) and the business-scoped user ID (`user_id`). A customer who adopts a WhatsApp username can arrive with no phone number at all (`references/platform-2026.md` section 2).

**Custom CRM integration.** A webhook handler that deduplicates Meta's retries, handles delivery statuses and in-WhatsApp opt-outs, stores both the phone number and the business-scoped user ID, and merges the record when a user's ID changes (`system` messages `user_changed_number` and `user_changed_user_id` carry `previous_user_id`) is in `references/platform-2026.md` section 11. Verify `X-Hub-Signature-256` (`sha256=` HMAC of the raw body with your app secret) before trusting any payload.

## Examples

### Example 1: Appointment Reminder System
User says: "Set up WhatsApp appointment reminders for my dental clinic in Hebrew."
Actions:
1. Create a Hebrew UTILITY template with clinic name, date, and time variables.
2. Add confirm/reschedule quick reply buttons.
3. Set timing rules (no Shabbat sending).
4. Provide integration code for the clinic management system.
Result: an approved UTILITY template with sending automation, billed per message.

### Example 2: E-commerce Order Updates
User says: "I want to send order confirmations and shipping updates via WhatsApp."
Actions:
1. Create an order confirmation UTILITY template (Hebrew).
2. Create a shipping notification UTILITY template with a URL button whose dynamic suffix is the tracking code (`--button-url-param`).
3. Set up the inbound webhook to receive delivery status updates.
4. Integrate with Israeli shipping providers (Cheetah, HFD, Israel Post, Yamit, Yango Delivery).
Result: automated Hebrew order-lifecycle messaging.

### Example 3: Marketing Campaign
User says: "Send a promotion to our customer list for a holiday sale."
Actions:
1. Establish the consent basis: explicit opt-in, or the section 30A(c) existing-customer route including the same-kind-of-goods limb.
2. Create a MARKETING template carrying the mandatory block (the word פרסומת at the start, advertiser name and address, refusal route with a web or email address), plus the direct-mail fields if the list is a segment.
3. Send through the Marketing Messages API endpoint, confirm the portfolio messaging limit covers the audience, and schedule for Israeli business hours (avoid Shabbat and chag eve).
4. Track delivery and replies; remove opt-outs before the next send.
Result: a compliant campaign with Israeli timing.

## Bundled Resources

### Scripts
- `scripts/send_whatsapp.py`: Sends WhatsApp Business messages via the Meta Cloud API for the Israeli market. Supports template messages (positional or named parameters, a URL button parameter), free-form text, interactive reply buttons (Hebrew labels by default) and interactive lists. Includes Israeli and international number validation, sending to a business-scoped user ID (`--recipient`), the Marketing Messages API endpoint (`--endpoint marketing`), a Shabbat-aware check for template sends, an action hint per common error code and a `--dry-run` mode. Run: `python scripts/send_whatsapp.py --help`

### References
- `references/platform-2026.md`: the 2026 platform changes an Israeli integration must handle (service-message charging since 1 October 2026, business-scoped user IDs, in-WhatsApp marketing opt-out, webhook retries, template pausing, extra error codes, onboarding an existing app number, the WhatsApp account and Messaging account split, the Marketing Messages API sunset, Embedded Signup versions).
- `references/israeli-law.md`: section 30א and the Privacy Protection Law (consent routes, mandatory content, exposure, direct mail, Amendment 13), cited by subsection.
- `references/bsp-selection.md`: the five questions for choosing between direct Cloud API and a BSP.
- `references/interactive-list.md`: a Hebrew interactive-list send example.
- `references/compliance-checklist.md`: the pre-send compliance checklist function.
- `references/domain-checklist.md`: the coverage checklist this skill is reviewed against.

## Reference Links

- WhatsApp Business Platform overview: https://developers.facebook.com/documentation/business-messaging/whatsapp/about-the-platform
- Graph API changelog (find current stable version): https://developers.facebook.com/docs/graph-api/changelog
- WhatsApp pricing (per-message, in force since 1 July 2025): https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- Messaging limits and the scaling ladder: https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits
- Per-user marketing template message limits: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits
- WhatsApp Business Calling API: https://developers.facebook.com/documentation/business-messaging/whatsapp/calling
- Cloud API error codes: https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes
- Israeli anti-spam law, compensation and the exemptions (Kol-Zchut): https://www.kolzchut.org.il/he/%D7%A4%D7%99%D7%A6%D7%95%D7%99_%D7%91%D7%92%D7%99%D7%9F_%D7%9E%D7%A9%D7%9C%D7%95%D7%97_%D7%93%D7%91%D7%A8%D7%99_%D7%A4%D7%A8%D7%A1%D7%95%D7%9E%D7%AA_%D7%9C%D7%9C%D7%90_%D7%94%D7%A1%D7%9B%D7%9E%D7%94_%D7%A9%D7%9C_%D7%94%D7%A0%D7%9E%D7%A2%D7%9F_(%D7%97%D7%95%D7%A7_%D7%94%D7%A1%D7%A4%D7%90%D7%9D)
- Information for recipients of spam, Israel Internet Association: https://www.isoc.org.il/freedom-of-internet/spam/information-to-recipients-of-spam
- BSP vendor pages: `references/bsp-selection.md`
- Privacy Protection Law Amendment 13, as published (Sefer HaChukim 3287): https://fs.knesset.gov.il/25/law/25_lsr_4810658.pdf
- Communications (Bezeq and Broadcasts) Law, full text: https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%AA%D7%A7%D7%A9%D7%95%D7%A8%D7%AA_(%D7%91%D7%96%D7%A7_%D7%95%D7%A9%D7%99%D7%93%D7%95%D7%A8%D7%99%D7%9D)
- Privacy Protection Law, full text (direct mail, sections 17ד to 17ט): https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%92%D7%A0%D7%AA_%D7%94%D7%A4%D7%A8%D7%98%D7%99%D7%95%D7%AA
- Marketing Messages API, including the Cloud API marketing sunset: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview
- WhatsApp account and Messaging account model: https://developers.facebook.com/documentation/business-messaging/whatsapp/account-model-evolution/

## Gotchas

- Israeli phone numbers for the WhatsApp API use the 972 country code **without a leading `+` and without the leading zero**: `972521234567`. Both `+9720521234567` (extra zero) and `0521234567` (local form) are wrong for the API. Agents add the extra zero constantly, which causes "phone number not found on WhatsApp" errors. The bundled script normalises `0521234567`, `+972521234567` and `972521234567`, and rejects `+9720521234567` naming the extra zero.
- **Templates copied from generic international examples never carry the section 30א(ה) block** (the word פרסומת at the start, advertiser name and address, refusal route). Add it to every Hebrew MARKETING template.
- WhatsApp message templates submitted in Hebrew must pass Meta's review. UTILITY templates with promotional language are commonly rejected (and should be MARKETING). Templates with Hebrew text inside code blocks or with missing variable examples are also commonly rejected.
- WhatsApp Business has a 24-hour customer service window. After 24 hours since the user's last inbound message, only pre-approved template messages can be sent, and depending on category they are billed per template message under the pricing model in force since 1 July 2025.
- Hebrew text in template variables can break formatting when mixed with numbers or English. Use Unicode isolate characters (U+2066 to U+2069) around mixed-direction content, or design templates so variables don't contain mixed-direction substrings.
- Per-message pricing (since 1 July 2025): utility, authentication and marketing categories are billed per template message, not per 24h conversation. **Since 1 October 2026 service messages and in-window utility replies are billed as well**, with 1,000 free service messages a month per business phone number, so advice or training data calling in-window replies free is out of date. Always re-check the Meta rate card for country code 972 before quoting Israeli rates.
- **The per-user marketing cap DOES apply to Israeli recipients.** WhatsApp limits how many marketing template messages a given user receives when they are less likely to engage, and the limit adapts to that user's recent read rate and inbox activity. Meta lists where it is not active: the European Economic Area, the United Kingdom, Japan, South Korea, Nigeria, South Africa and Thailand. **Israel is not on that list, so plan for the cap.** Marketing messages sent inside an open 24h window do not count towards it. Separately, marketing template messages are **not currently delivered to United States (+1) numbers at all**, so an Israeli business with US customers needs a different channel for them.
- **A customer may arrive without a phone number.** Since April 2026 webhooks carry a business-scoped user ID in `user_id`, and a user who adopts a WhatsApp username can arrive with no `wa_id`. Key CRM records on both identifiers (`references/platform-2026.md` section 2).
- **+972 mobile prefixes**: 050 (Pelephone), 051 (wecom), 052 (Cellcom), 053 (HOT Mobile), 054 (Partner), 055 (Cellcom ranges and virtual operators), 058 (Golan Telecom), plus 056 (Ooredoo Palestine) and 059 (Jawwal), which serve the Palestinian territories only but are real WhatsApp numbers. A regex that excludes 051, 056 or 059 rejects real subscribers. A landline fallback pattern that is not anchored against `05` silently accepts 057, which is no longer a mobile prefix.

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
| 131049 | Not delivered in order to maintain healthy ecosystem engagement: the per-user marketing template limit, or repeated retries to a user who already hit it | Wait at least 24 hours before resending to that user. Do not retry immediately, which triggers further suppression. For a US +1 number it is permanent: suppress marketing to it |
| 131050 | The user stopped marketing messages from your business inside WhatsApp | Do not retry. Add them to the same suppression list as 'הסר' replies, and subscribe to the `user_preferences` webhook |
| 131063 | The template is categorized MARKETING but marketing templates are disabled on Cloud API for this account | Refresh the template's category and resend through `/marketing_messages` (`--endpoint marketing`) |
| 130472 | Not sent as part of a Meta marketing message experiment | Do not retry: a resend gets the same error (Meta's experiments page) |
| 130403 | Your business has blocked this user | Unblock the user before sending; do not retry |

Note that the per-user marketing cap shows up as suppression and non-delivery reported through the messages webhook, not as a synchronous send error, so check webhook statuses and not just the API response. Codes 131048, 131056 and 131042 are in `references/platform-2026.md` section 6.

### Error: "Webhook not receiving messages"
Cause: webhook URL not verified, Meta App not subscribed to `messages` field, the WABA (now the Messaging account, same ID) not subscribed to the app, or signature validation failing.
Solution: ensure the webhook URL is HTTPS, the verification token matches, the Meta App is subscribed to the `messages` webhook field, **and the WABA itself is subscribed to your app** (a separate step from the app subscribing to the field, and a common miss), and that your handler validates `X-Hub-Signature-256` (`sha256=` plus the HMAC of the raw body) against the App secret.
