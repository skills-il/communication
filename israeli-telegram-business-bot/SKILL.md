---
name: israeli-telegram-business-bot
description: "Set up Telegram bots for Israeli small businesses with appointment booking, order management, FAQ auto-replies in Hebrew, business hours awareness (Sunday-Thursday), payment links, and customer notifications. Use when an Israeli business owner asks about creating a Telegram bot, automating customer replies, taking orders via Telegram, or scheduling appointments through a bot. Helps non-technical users deploy a working business bot without writing code, reducing missed customer messages and manual response overhead. Do NOT use for WhatsApp Business (use israeli-whatsapp-business), building bots from code (use telegram-bot-builder), voice bots (use hebrew-voice-bot-builder), or general support ticket routing (use israeli-customer-support-automator)."
license: MIT
---

# Israeli Telegram Business Bot

Set up a Telegram bot for an Israeli small business. Covers bot creation, Hebrew auto-replies, appointment booking, order management, business hours handling (Sunday-Thursday), payment links, and customer notifications. Designed for non-technical business owners.

## Problem

Israeli small business owners lose customers because they cannot respond fast enough. Messages arrive during Shabbat, late at night, or while the owner is with another client, and the result is missed bookings.

Most Israeli businesses live on WhatsApp, but Telegram offers bot automation WhatsApp does not: inline keyboards, automatic replies, structured menus, and payments, with no code. Existing guides assume developer knowledge.

This skill walks a business owner through a Telegram bot that handles the repetitive parts of customer communication in Hebrew, with Israeli business hours built in.

## When to Use This Skill

- A business owner wants to automate customer replies on Telegram
- Someone asks how to create a Telegram bot for their Israeli business
- A freelancer wants appointment booking via Telegram
- A restaurant or cafe wants to take orders through a bot
- A service provider needs after-hours auto-replies in Hebrew
- Someone wants to send updates to customers via a Telegram channel

## When NOT to Use This Skill

- **WhatsApp automation** - use `israeli-whatsapp-business` instead
- **Building a bot from code** (Node.js, Python) - use `telegram-bot-builder`
- **Voice bots or IVR** - use `hebrew-voice-bot-builder`
- **Support ticket routing/helpdesk** - use `israeli-customer-support-automator`
- **Marketing chatbots for lead generation** - use `hebrew-chatbot-builder`

---

## Phase 0: Pick the Right Architecture First

"Business bot" has two different meanings on Telegram, and picking the wrong one wastes weeks.

### Option A: Telegram Business connected bot (customers keep messaging the owner)

Since Bot API 7.2 a bot can be connected to the owner's own personal Telegram account. It replies inside the owner's real DMs, so customers never learn a separate `@..._bot` username. Technically the bot receives `business_message` and `edited_business_message` updates and passes `business_connection_id` on its send methods.

Setup on the bot side: @BotFather, Bot Settings, then the business toggle. Telegram renamed it, so you may see either name: the current developer page (`core.telegram.org/bots/features`) calls it **Secretary Mode**, while the older overview page (`core.telegram.org/bots`) still calls it **Business Mode**. On the owner side it is then connected from the Telegram client under Settings, Telegram Business, Chatbots (a client UI path, not something the API docs describe). Connected bots work for non-Premium users too.

Choose this when customers already message the owner directly and you only want to automate the repetitive replies.

### Option B: Standalone bot (a separate `@business_bot` username)

The architecture the rest of this skill builds. Choose it when you need structured flows the owner's DM thread cannot carry: multi-step booking state, a product catalog, order tracking, or payments.

### Before building anything: use the native features

Telegram Business ships several features that replace hand-built automation. Be precise about who gets them: the native features are included in a Telegram Business subscription, currently bundled with Telegram Premium, so the OWNER needs Premium. Connected bots are the exception and work for non-Premium users too.

Opening Hours (with real timezone support) replaces the Phase 4 business-hours logic, Away Messages replace the after-hours auto-reply, Greeting Messages replace the Phase 2 welcome, Quick Replies replace the Phase 3 canned answers, and Business Location, Business Intro and Chat Links replace the Phase 3 location and contact cards.

Start there. Add a bot only for what the native features cannot do: booking state, orders, and payments. Native Opening Hours takes a real timezone identifier, which resolves the Asia/Jerusalem daylight-saving problem in Troubleshooting with no custom logic.

Sources: `core.telegram.org/api/business`, `telegram.org/blog/telegram-business`.

### The constraint that decides Telegram vs WhatsApp

**A Telegram bot cannot start a conversation.** It can only message users who have already pressed Start on it. There is no way to import a phone list the way WhatsApp Business allows. Every broadcast idea in Phase 8 depends on an audience the owner must first build, one Start press at a time. Tell the business owner this before they choose Telegram over WhatsApp, not after.

Source: `core.telegram.org/bots` ("Bots can't start conversations with users").

---

## Phase 1: Create Your Bot with BotFather

BotFather is Telegram's official tool for creating bots. No coding required.

### Step-by-Step Bot Creation

1. **Open Telegram** and search for `@BotFather`
2. Start a chat and send `/newbot`
3. **Choose a display name** - this is what customers see. Use your business name in Hebrew or English:
   - Good: `מסעדת שמש` or `Shemesh Restaurant`
   - Good: `ספרא - תורים` (Sapra - Appointments)
4. **Choose a username** - must end in `bot` and be unique:
   - Good: `shemesh_restaurant_bot`, `sapra_booking_bot`
   - Bad: `mybot` (too generic, probably taken)
5. **Save the token** BotFather sends you. It looks like: `7123456789:AAHxxx...`. Keep this private, it controls your bot.

### Configure Bot Profile

Send @BotFather `/setdescription` (the Hebrew text customers see before starting a chat), `/setabouttext` (a short profile line), `/setuserpic` (the business logo), and `/setcommands` (the command menu: start, hours, book, menu, contact, help). Ready-to-paste Hebrew values for all four are in `references/business-bot-templates.md`.

## Phase 2: Welcome Message and Auto-Greeting

When a customer opens your bot for the first time and presses "Start", they should immediately receive a warm Hebrew greeting with clear navigation options.

### Welcome Message Template

Three lines at most, defaulting to Hebrew: a greeting, "ברוכים הבאים ל[שם העסק]", and "איך אפשר לעזור?". Pair it with an inline keyboard of two buttons per row: 📅 קביעת תור and 📋 תפריט/שירותים, then 🕐 שעות פעילות and 📍 מיקום, then 📞 דברו איתנו. Add an English button only if you serve tourists. Personal beats corporate: "שלום!" beats "שלום וברוכים הבאים לשירות הלקוחות שלנו". Worked flows per business type are in `references/business-bot-templates.md`.

## Phase 3: FAQ Auto-Replies

Set up automatic answers to the questions you get asked 10 times a day.

### What to automate

Cover the questions you answer ten times a day: **business hours** (the Sunday-Thursday / Friday / Shabbat block), **location** (address, city, a Google Maps link, parking), and **contact** (phone as `050-XXX-XXXX`, a WhatsApp link, an email, and an invitation to write in the bot).

For a business with many questions, nest the menu: a main screen with שירותים, מחירים, קביעת תור and שעות פעילות, where each branch lists its items and ends with "⬅️ חזרה לתפריט". Keep it to two levels; deeper trees lose people. Worked screens are in `references/business-bot-templates.md`.

## Phase 4: Business Hours Logic

Israeli business hours follow a unique weekly pattern. Your bot must handle this correctly.

### Israeli Weekly Schedule

| Days | Typical Hours | Status |
|------|---------------|--------|
| Sunday to Thursday (ראשון-חמישי) | 08:00/09:00 - 17:00/18:00 | Open |
| Friday (שישי) | 08:00/09:00 - 13:00/14:00 | Short day |
| Saturday (שבת) | Closed | Shabbat |

### After-Hours Auto-Reply

When someone messages outside business hours, reply automatically:

**Regular evening or night (Sunday-Thursday):**
```
היי! 🌙
קיבלנו את ההודעה שלך.
אנחנו פעילים ראשון-חמישי בין 09:00-18:00, ונחזור אליך מחר בבוקר.
בינתיים אפשר לקבוע תור או לראות מידע דרך התפריט.
```

**Friday afternoon and Shabbat:** the same message opening with "שבת שלום! 🕯" and promising a reply on Sunday.

**Erev Chag (holiday eve):** same shape, opening with "חג שמח!" and naming the return date.

### Holiday Awareness

Major Israeli holidays when businesses typically close. **These are Israel day-counts, not diaspora day-counts.** Outside Israel most of these festivals run an extra day, so a generic holiday calendar will close the business for a day it should be open:

- **Rosh Hashana** (ראש השנה) - 2 days
- **Yom Kippur** (יום כיפור) - 1 day (nearly everything closes)
- **Sukkot** (סוכות) - day 1, then Shmini Atzeret (a single day, which in Israel is also Simchat Torah)
- **Pesach** (פסח) - day 1 and day 7
- **Shavuot** (שבועות) - 1 day
- **Yom Ha'atzmaut** (יום העצמאות) - 1 day

Two day-types sit between "open" and "closed", and ignoring them sells slots nobody shows up for:

- **Chol HaMoed** (חול המועד), the intermediate days of Sukkot and Pesach, roughly 10 days a year. Schools are closed and much of the workforce is on leave, so most SMBs run reduced hours.
- **Erev chag** (ערב חג), which is a short day like Friday for every festival above. Yom HaZikaron, the day before Yom Ha'atzmaut, closes places of entertainment and quietens trading generally.

Treat both as owner-configurable short days, not as full working days.

Configure your bot to check a holiday calendar and switch to holiday auto-reply mode. Most no-code platforms support date-based logic or scheduled message changes. Whatever calendar source you use, set it to the Israel schedule (Hebcal exposes this as the `i=on` flag) or you will inherit the diaspora day-counts.

---

## Phase 5: Appointment Booking

Let customers book appointments directly through the bot using inline keyboards.

### Booking Flow

Four inline-keyboard steps, each with a "⬅️ חזרה" button:

1. **Service** - "מה תרצו לקבוע?" with one button per service.
2. **Date** - "באיזה יום?" with the next open days only (never Saturday).
3. **Time** - "באיזו שעה?" with the free slots for that day.
4. **Confirmation** - a summary of service, day, and time, plus [✅ אישור] and [❌ ביטול].

### Confirmation and reminders

After booking, echo back service, date, time and address, promise a reminder the day before, and give /cancel for changes. Send three reminders: a day before ("תזכורת: יש לך תור מחר ב-10:00"), two hours before with a navigation link, and after a no-show a short "לא הספקת להגיע?" with a /book link.

### Important: Friday Booking Logic

On Friday show morning slots only (to 13:00 or 14:00), never offer Saturday, and make Sunday the next available day after Thursday.

---

## Phase 6: Order Management

For businesses that sell products or take food orders.

### Order Flow

Three inline-keyboard screens: **categories** (a button per category), **items in a category** (name and price per line, an "הוסף לסל" button per item, and "⬅️ חזרה לקטגוריות"), and the **cart** (quantity, item and line price, a "סה"כ" line, then [✅ שלח הזמנה] [🗑 נקה סל]). Confirm with an order number, the total, an estimated preparation time, and a /status command for tracking. Full worked screens are in `references/business-bot-templates.md`.

## Phase 7: Payment Integration

### Option 1: External Payment Links

The simplest approach. Generate a payment link from your existing provider and send it in the bot:

```
💳 לתשלום:

סה"כ לתשלום: ₪103

בחרו אמצעי תשלום:
[💳 כרטיס אשראי] -> link to payment page
[📱 ביט] -> Bit payment link
[🏦 העברה בנקאית] -> bank details
```

**Israeli payment gateways.** Prefer one that issues the payment link AND the compliant invoice in
one step, currently Green Invoice, iCount or Rivhit. PayMe, Meshulam and Tranzila clear without
invoicing; Bit is ILS-only and single-payment; PayBox has no public merchant API. **Feature sets
change without notice, so confirm invoicing and API support with the provider before you build.**
Comparison table and Bit acceptance terms: `references/israeli-payment-providers.md`.

### Option 2: Telegram Native Payments (Payment API)

Telegram's built-in Payment API lets the bot send native invoice messages customers pay without leaving Telegram. Connect a provider through @BotFather's `/mybots` -> "Payments" menu.

ILS is supported (currency `ILS`, min ₪3.68, max ₪36,788.20 per invoice). However, Telegram publishes no public provider list: the payments page states only "more than 20 providers", and the actual set is whatever @BotFather offers your bot under Bot Settings > Payments. As of 2026-09-01 no Israeli solek is named anywhere in the payments documentation, and Stripe remains the documented reference provider. Practical implications:

- Foreign cards cleared in ILS via Stripe: works today through the global Stripe integration.
- Clearing through an Israeli solek (for tax/reporting): use Option 1 (external link) or Option 4 (Mini App with an Israeli provider iframe). The native Payment API is not the right tool for "pure Israeli" merchant setups.

### Option 3: Telegram Stars (for Digital Goods)

Telegram Stars covers in-app purchases of digital goods: consultations, online courses, downloadable files and templates, premium content. Stars is for digital goods only, so physical products and in-person services need an external payment link or the native Payment API. Two consequences worth knowing before you commit: digital sales must go through Stars (currency tag `XTR`) and not a third-party provider, or Telegram will not show the bot to mobile users at all; and any bot selling with Stars must answer the `/paysupport` command and handle payment complaints. The `provider_token` parameter is only needed for physical goods, so leave it empty for digital ones.

### Option 4: Telegram Mini Apps (TWA)

A Mini App is a web page that opens inline inside Telegram, with native APIs for identity, theme, MainButton and payments. Use one when the bot needs richer UX than inline keyboards (catalog grids, calendar pickers, custom checkout with an Israeli provider iframe). Skip it for simple FAQ/booking bots. Setup is via @BotFather (`/mybots`, Bot Settings, Configure Mini App); Israeli providers embed directly, with no Telegram-specific integration.

See `references/mini-apps-implementation.md` for the full setup guide, payment-embedding patterns, and `initData` validation.

### You still have to issue a real invoice

Collecting money through the bot does not change the business's tax obligations. An Israeli business must issue a חשבונית מס or a קבלה for the payment, and under the חשבוניות ישראל reform a tax invoice ABOVE the current threshold needs an allocation number from the Tax Authority before the customer can deduct the input VAT. Note the scope before you alarm a business owner: what triggers it is the RECIPIENT being a registered dealer who will deduct input VAT, not the document type or the business type. A cafe or salon selling to private consumers will rarely meet it; the same cafe invoicing a company for a catering order above the threshold does. The threshold falls year on year, so read the current figure off the Tax Authority page rather than quoting one from memory.

This is the reason the Phase 7 shortlist leads with Green Invoice, iCount, and Rivhit: they generate the payment link and the compliant invoice in one step, so the bot never becomes a channel that takes money without paperwork. If the owner uses a bare payment link from a provider that does not invoice, they must still issue the document separately.

Source: `gov.il/he/departments/israel_tax_authority`.

---

## Phase 8: Customer Notifications and Broadcasting

### Channel posts vs DM broadcasts (important distinction)

Two very different things get called "broadcasting":

- **Channel post**: one message to opted-in subscribers. Counts as a single API call regardless of subscriber count, so no bot rate limit. Right tool for promotions, weekly updates, holiday greetings.
- **DM broadcast**: bot calls `sendMessage` once per customer. Subject to Telegram bot rate limits AND to Israel's anti-spam law (Section 30a) for marketing content. **Reaches only customers who already pressed Start on the bot** (see Phase 0). There is no customer-list import.

Default to channels for promotional content. Reserve DM broadcasts for transactional updates the customer asked for, or promotions to customers who explicitly opted in.

### Getting customers into the bot: deep links

A bot cannot start a conversation, so growing the reachable audience is its own task. Use start deep links:

`t.me/<your_bot>?start=<payload>`

The payload arrives with the `/start` command, so you can attribute the source. It is capped at **64 characters** and only `A-Z a-z 0-9 _ -` are allowed, so encode anything longer or richer with base64url rather than packing it in raw. Practical placements:

Attribute the source by placement: a QR code on the counter (`qr_counter`), the receipt (`receipt`), an SMS or email footer (`sms_may`), the Instagram or Facebook bio (`ig_bio`). The full placement table is in `references/business-bot-templates.md`.

Telegram Business Chat Links are the Option A equivalent: each carries a preset opening message and a view counter. They are part of the Business subscription and are capped per account.

If you built Option A, handle one more entry point: an owner whose bot is connected sees a "Manage Bot" action at the top of each managed chat, and tapping it sends your bot a deep link in the form `/start bizChat<user_chat_id>`. A bot that only parses its own marketing payloads will silently ignore that.

Source: `core.telegram.org/bots/features#deep-linking`.

### Telegram Channel for Updates

Create a channel named `[שם העסק] - עדכונים`, add the bot as an administrator, and share the link.

Three shapes cover almost everything: a **promotion** (headline offer, the days it runs, the bot
username for booking, an explicit expiry, plus the labelling rules below), an **order status
update** (the stages with the current one marked, and an ETA), and a **holiday greeting**
naming the return day and hour. Worked message templates are in
`references/business-bot-templates.md`.

### Israeli Spam Law (חוק הספאם) Compliance

Section 30a of the Communications (Telecommunications and Broadcasting) Law, 5742-1982 governs unsolicited advertising. **Read the scope question carefully before relying on it either way:** the section as drafted enumerates four channels, fax, automated dialing systems, electronic messages (הודעה אלקטרונית), and SMS (מסרון). Telegram and other instant-messaging apps are **not named in the statute**. Coverage, where asserted, runs through the broad "electronic message" definition rather than explicit statutory text, and Israeli practice is not settled on it.

The practical conclusion for a business owner is unchanged: assume a promotional Telegram broadcast is covered and comply. The downside of complying unnecessarily is a consent button; the downside of guessing wrong is class-action exposure. Do not, however, tell a client the statute names instant messaging, because it does not.

Four requirements, and each is separate. (1) **Prior explicit consent**: the customer must actively opt in, and pressing Start on the bot is NOT consent. Transactional messages the customer asked for do not need it. (2) **The word פרסומת at the head of the message**, which is distinct from identifying the sender and is the one most often missed. (3) **Sender identification**: the advertiser's name, address and ways to make contact, including a working email address for the opt-out. (4) **A working opt-out in every message**. The recipient may give the opt-out notice in writing or through the medium the advertisement arrived in, at their choice, so a Telegram promotion needs a Telegram opt-out route and not only an email link. Honour opt-outs immediately.

**Keep provable consent records.** If consent is disputed the business has to show it was given. Store, per customer, the Telegram user id, the exact opt-in text shown, and the timestamp. A compliant promotion template is in `references/business-bot-templates.md`.

Penalties: statutory damages up to ₪1,000 per message (no need to prove harm), class-action exposure, and criminal liability for knowingly sending without consent. When in doubt, treat a message as a promotion and get consent first. Consult `kolzchut.org.il` or a lawyer for current obligations.

### Privacy: the bot's customer list is a database

A bot that stores customer names, phone numbers, appointment histories, and order records is a **מאגר מידע** under Israel's Privacy Protection Law. Amendment 13 reshaped the regime and sharpened the Privacy Protection Authority's enforcement powers. Check the Authority's own guidance for the current registration thresholds, the information-security duty and when a privacy officer (ממונה על הגנת הפרטיות) is required, rather than relying on a figure quoted here.

Two practical consequences for a bot built with this skill:

- Tell customers at collection time what you store and why, and keep it to what the bot actually needs.
- Hosting the bot on a US no-code platform (BotPress cloud, ManyChat) transfers Israeli customer data abroad. Check the platform's data-residency and processing terms before putting real customer records into it.

Source: `gov.il/he/departments/the_privacy_protection_authority`. This is a summary, not legal advice; a business holding a substantial customer database should get its obligations reviewed.

---

## Phase 9: No-Code Bot Platforms

You do NOT need to write code to build a Telegram business bot. These platforms offer visual editors.

Three are worth looking at for an Israeli SMB: **BotPress** (drag-and-drop flows, best for
multi-step booking), **n8n** (Telegram trigger plus a Schedule Trigger for reminders, best for
wiring the bot to Google Sheets, calendars, CRMs or Green Invoice), and **ManyChat** (best if the
business already uses it for Instagram or WhatsApp). **Tiers, Hebrew support and integration
coverage change without notice, so check the vendor's own pricing page before committing.**
Comparison in `references/no-code-platforms.md`.

### Webhook vs Polling (Deployment Note)

Telegram delivers updates by polling (the bot asks repeatedly) or by webhook (Telegram pushes to your HTTPS URL). The no-code platforms above hide this, so it only matters if you self-host later or debug a silent bot.

---

## Phase 10: Hebrew-Specific Setup

### RTL Considerations

Hebrew displays RTL by default, inline keyboard labels take Hebrew, and mixed Hebrew and Latin text usually renders fine. Commands such as `/start` stay LTR, which is expected. For a mixed run in the wrong order, see the bidi fix in Troubleshooting.

### Hebrew Greeting Conventions

Match the greeting to the moment: "שלום!" or "היי!" generally, "בוקר טוב!" / "ערב טוב!" by time of day, "שבת שלום!" from Friday afternoon, "שבוע טוב!" after Shabbat, "חג שמח!" on a holiday, "תודה רבה!" to close.

### Hebrew Command Aliases

Bot commands must be Latin characters, but customers should never have to type them. Give every command a Hebrew button label instead: 🏠 תפריט ראשי for `/start`, 📅 קביעת תור for /book, 🕐 שעות פעילות for /hours, 📞 צרו קשר for /contact.

### Tone of Voice

Friendly and direct, never corporate. Plural "אתם/אתן" for a general audience, "את/ה" for an intimate business. Emojis welcome, slang not. Keep it brief: Israelis expect answers, not paragraphs.

## Bundled Resources

- `references/business-bot-templates.md` - full message flows for restaurant, salon, and freelance service bots
- `references/mini-apps-implementation.md` - Mini App setup, embedding an Israeli payment provider, and `initData` validation
- `references/israeli-payment-providers.md` - provider comparison, which ones issue the invoice, Bit acceptance terms
- `references/no-code-platforms.md` - BotPress, n8n and ManyChat feature comparison
- `references/domain-checklist.md` - what a complete version of this skill must cover

---

## Gotchas

Common mistakes agents make when helping set up Israeli business bots:

1. **Forgetting Shabbat handling** - The bot MUST have a Shabbat auto-reply, must never offer Saturday slots, and must shorten Friday. Skipping this is the single most common mistake.

2. **Using Sunday as a day off** - The Israeli work week is Sunday to Thursday. Do not copy Western business-hour templates.

3. **Writing stiff Hebrew** - Use "אפשר" rather than "ניתן", and "בואו" rather than "הנכם מוזמנים". The bot should sound like a friendly shop owner, not a government form.

4. **Over-engineering version one** - Ship welcome, hours, FAQ, and one booking or ordering flow. Add the rest once those work.

5. **Leaking the token** - The token is a password. Never post it in group chats, forums, or screenshots. If it leaks, send @BotFather `/token` to generate a new one; the old token stops working.

6. **No human handoff** - Include a "דברו עם נציג" option that forwards to the owner's personal Telegram.

7. **Wrong phone format** - Use `050-XXX-XXXX`, or `+972-50-XXX-XXXX` internationally.

8. **Missing a "back" button** - Every sub-menu needs "⬅️ חזרה", or customers get stuck.

9. **Not testing on mobile** - Most Israeli Telegram users are on a phone. Buttons that fit on desktop often do not.

10. **Hardcoding holiday dates** - Israeli holidays move every year with the Hebrew calendar. Resolve them from a calendar source instead.

---

## Examples

### Example 1: Restaurant Bot

"Cafe Shemesh", Tel Aviv: menu viewing, takeout orders, table booking.

```
שלום! ☀️
ברוכים הבאים לקפה שמש.

מה בא לכם?
[📋 תפריט] [🛒 הזמנה לטייקאווי]
[📅 הזמנת שולחן] [🕐 שעות פעילות]
```

### Example 2: Hair Salon Bot

"Salon Dana", Haifa: appointment booking and a price list, so the first screen is a service picker where each button carries the service name and its starting price.

### Example 3: Freelance Accountant Bot

"Moshe Levi, CPA": consultation scheduling, a required-documents checklist, and a tax FAQ.

Complete message-flow templates for all three, including menu trees, stylist selection, confirmation messages and the full document checklist, are in `references/business-bot-templates.md`. Read that file instead of re-deriving the flows.

## Troubleshooting

### Bot Not Responding

- **`getUpdates` comes back 409 Conflict.** 409 is the symptom, and it has TWO causes. Telegram does not document the status code at all; the docs state only the behavioural rule ("This method will not work if an outgoing webhook is set up"), so diagnose by cause, not by the number.
  - **A webhook is set.** Long polling cannot run alongside one. Fix: call `deleteWebhook`, then reconnect.
  - **Two pollers on one token.** BotPress, n8n and ManyChat all long-poll by default, so pasting the same token into a second platform produces 409 with no webhook anywhere. Fix: disconnect the token from the other platform, or create a second bot with `/newbot`. The tell is that `deleteWebhook` returns `true` and nothing changes: that means there was no webhook and you are in this case.
  See `core.telegram.org/bots/api#getupdates`.
- **Check the token**: Make sure you copied the full token from BotFather without extra spaces
- **Bot not connected to platform**: Verify the token is entered correctly in your no-code platform (BotPress, n8n, etc.)
- **Platform is down**: Check the platform's status page
- **Webhook URL unreachable**: If using webhooks deliberately, the URL must be HTTPS and publicly accessible

### Messages Not Arriving

- **Privacy mode**: By default, bots in groups only see messages starting with `/`. Use BotFather's `/setprivacy` to change this if needed
- **Bot blocked**: The user may have blocked your bot. You cannot send messages to users who blocked you
- **Rate limits**: Telegram enforces three separate limits for bot sends, all per official FAQ at `core.telegram.org/bots/faq`:
  - **Per chat**: no more than ~1 message per second to the same chat.
  - **Per group**: no more than 20 messages per minute to the same group.
  - **Global broadcasts**: a bot can broadcast to roughly 30 different users per second (free tier). Exceed any of these and the API returns HTTP 429.
  - **Paid broadcasts**: a bot can opt in to pay Telegram for higher throughput (up to 1,000 messages/sec). Costs 0.1 Stars per message above the free 30/sec, and requires the bot to hold ≥100,000 Stars balance and have ≥100,000 monthly active users , practical only for large businesses, not typical Israeli SMBs.
  - For DM broadcasts to a customer list, add deliberate delays between sends to stay under the limits. For mass announcements, post to a Telegram channel instead , channel posts are a single API call and do not consume the per-second budget.
  - This rate-limit information and the BotFather command set described in this skill are aligned with Bot API 10.3 (released August 24, 2026); the Bot API is versioned and updated regularly at `core.telegram.org/bots/api`, so check the changelog at the top of that page if a feature behaves differently than documented here.

### Hebrew Text Display Issues

- **Ensure your platform sends UTF-8**: All modern platforms do, but verify if text appears garbled
- **Mixed LTR/RTL**: If an English word, a URL, or a number sequence appears in the wrong position inside a Hebrew sentence, this is Unicode bidi resolution, not a Telegram bug. Wrap the LTR run in isolate characters: U+2066 (LRI) before and U+2069 (PDI) after, or use U+2068 (FSI) to let the run pick its own direction. A U+200F (RLM) after the run also forces the surrounding text back to RTL.
- **Inline keyboard alignment**: Apply the same isolate characters to button labels that mix Hebrew with a price, a Latin name, or a phone number. Do not assume the alignment is unfixable before trying bidi controls.

### Booking Shows Wrong Times

- **Timezone**: Make sure your platform is set to `Asia/Jerusalem` (UTC+2, or UTC+3 during daylight saving)
- **DST transitions**: Israel changes clocks in March and October. Verify your time logic handles this
- **Friday hours**: Double-check that Friday only shows shortened hours, not full-day availability

### Payment Link Not Working

- **Link expired**: Payment links expire, but the window is set per provider and per link. Check your provider's link-expiry setting rather than assuming a fixed window, and generate a fresh link per order
- **Mobile browser redirect**: Test the payment link on mobile. Some gateways redirect poorly on Telegram's in-app browser
- **Currency**: Make sure the payment page shows ILS (₪), not USD or EUR

### Bot Got Compromised

Open @BotFather and send `/token`, which is the documented way to generate a new authorization token when the existing one is compromised. Pick the bot, update the new token in your platform immediately, then review recent bot activity for messages you did not send.

---

## Reference Links

| Resource | URL | What it covers |
|----------|-----|----------------|
| Telegram Bot API | https://core.telegram.org/bots/api | Methods, types, and the changelog at the top |
| Telegram Bot Features | https://core.telegram.org/bots/features | BotFather setup, commands, inline keyboards, privacy mode, deep linking |
| Introduction to Bots | https://core.telegram.org/bots | The rule that a bot cannot start a conversation |
| Telegram Bot Payments docs | https://core.telegram.org/bots/payments | ILS currency limits and the native invoice flow |
| Telegram Mini Apps | https://core.telegram.org/bots/webapps | Setup via @BotFather, JS bridge, MainButton, `initData` |
| Telegram Bot FAQ - rate limits | https://core.telegram.org/bots/faq | Send rate limits, including paid broadcasts |
| Communications Law, statutory text | `nevo.co.il/law_html/law01/032_002.htm` | The wording of Section 30a and its mandatory-content list |
| Israeli Anti-Spam Law (Kol-Zchut) | `kolzchut.org.il`, page פיצוי בגין משלוח דברי פרסומת ללא הסכמה של הנמען | Section 30a obligations and ₪1,000 statutory damages |

---

## Recommended MCP Servers

- **`hebcal`** - Hebrew calendar MCP server. Phase 4 and Gotcha 10 both tell the owner to resolve Israeli holiday dates rather than hardcode them. Use this MCP to find when holidays fall in a given year, drive holiday auto-reply mode, and keep booking off closed days.
