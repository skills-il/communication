---
name: israeli-telegram-business-bot
description: "Set up Telegram bots for Israeli small businesses with appointment booking, order management, FAQ auto-replies in Hebrew, business hours awareness (Sunday-Thursday), payment links, and customer notifications. Use when an Israeli business owner asks about creating a Telegram bot, automating customer replies, taking orders via Telegram, or scheduling appointments through a bot. Helps non-technical users deploy a working business bot without writing code, reducing missed customer messages and manual response overhead. Do NOT use for WhatsApp Business (use israeli-whatsapp-business), building bots from code (use telegram-bot-builder), voice bots (use hebrew-voice-bot-builder), or general support ticket routing (use israeli-customer-support-automator)."
license: MIT
---

# Israeli Telegram Business Bot

Set up a Telegram bot for an Israeli small business. Covers bot creation, Hebrew auto-replies, appointment booking, order management, business hours handling (Sunday-Thursday), payment links, and customer notifications. Designed for non-technical business owners.

## Problem

Israeli small business owners lose bookings because messages arrive on Shabbat, at night, or mid-appointment. Telegram bots can be built without code and add inline keyboards, menus and in-chat payments, but existing guides assume developer knowledge. This skill walks the owner through a Hebrew bot with Israeli business hours built in.

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

Two limits decide whether Option A fits. The owner chooses which chats the bot may access, and the bot's `can_reply` right covers only private chats that had an incoming message in the last 24 hours. So a connected bot answers customers who just wrote, but it cannot send a day-before reminder or any message into a quiet chat. Reminders and broadcasts need Option B.

Setup on the bot side: @BotFather, Bot Settings, then the business toggle. Telegram renamed it, so you may see either name: the current developer page (`core.telegram.org/bots/features`) calls it **Secretary Mode**, while the older overview page (`core.telegram.org/bots`) still calls it **Business Mode**. On the owner side it is then connected from the Telegram client under Settings, Telegram Business, Chatbots (a client UI path, not something the API docs describe). Connected bots work for non-Premium users too.

Choose this when customers already message the owner directly and you only want to automate the repetitive replies, not send reminders.

### Option B: Standalone bot (a separate `@business_bot` username)

The architecture the rest of this skill builds. Choose it when you need structured flows the owner's DM thread cannot carry: multi-step booking state, a product catalog, order tracking, or payments.

### Before building anything: use the native features

Telegram Business ships features that replace hand-built automation. They come with a Telegram Business subscription, currently bundled with Telegram Premium, so the OWNER needs Premium (connected bots are the exception).

Opening Hours (with real timezone support) replaces the Phase 4 weekly schedule (it is one weekly schedule, so holidays still need a dated Away Message), Away Messages replace the after-hours auto-reply, Greeting Messages replace the Phase 2 welcome, Quick Replies replace the Phase 3 canned answers, and Business Location, Business Intro and Chat Links replace the Phase 3 location and contact cards.

Start there, and add a bot only for booking state, orders, and payments. Native Opening Hours takes a real timezone, which also solves the Asia/Jerusalem daylight-saving problem.

Sources: `core.telegram.org/api/business`, `telegram.org/blog/telegram-business`.

### The constraint that decides Telegram vs WhatsApp

**A Telegram bot cannot start a conversation.** It can only message users who have already pressed Start on it. There is no way to import a phone list into it. Every broadcast idea in Phase 8 depends on an audience the owner must first build, one Start press at a time. Tell the business owner this before they choose Telegram over WhatsApp, not after.

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
5. **Save the token** BotFather sends you. It looks like: `7123456789:AAHxxx...`. It controls your bot: keep it in a password manager and paste it only into the platform that runs the bot. Never paste it into a chat, including a chat with an AI assistant; if that already happened, rotate it with `/token`. Full handling rules: `references/compliance-and-security.md` section 1.

### Configure Bot Profile

Send @BotFather `/setdescription` (the Hebrew text customers see before starting a chat), `/setabouttext` (a short profile line), `/setuserpic` (the business logo), and `/setcommands` (the command menu: start, hours, book, menu, contact, cancel, status, help). Ready-to-paste Hebrew values for all four are in `references/business-bot-templates.md`.

## Phase 2: Welcome Message and Auto-Greeting

When a customer opens your bot for the first time and presses "Start", they should immediately receive a warm Hebrew greeting with clear navigation options.

### Welcome Message Template

Three lines at most, defaulting to Hebrew: a greeting, "ברוכים הבאים ל[שם העסק]", and "איך אפשר לעזור?". Pair it with an inline keyboard of two buttons per row: 📅 קביעת תור and 📋 תפריט/שירותים, then 🕐 שעות פעילות and 📍 מיקום, then 📞 דברו איתנו. Add an English button only if you serve tourists. Personal beats corporate: "שלום!" beats "שלום וברוכים הבאים לשירות הלקוחות שלנו". Worked flows per business type are in `references/business-bot-templates.md`.

## Phase 3: FAQ Auto-Replies

Set up automatic answers to the questions you get asked 10 times a day.

### What to automate

Cover the questions you answer ten times a day: **business hours** (the Sunday-Thursday / Friday / Shabbat block), **location** (address, city, a Google Maps link, parking), and **contact** (phone as `050-XXX-XXXX`, a WhatsApp link, an email, and an invitation to write in the bot).

For many questions, nest the menu two levels deep at most (שירותים, מחירים, קביעת תור, שעות פעילות), each branch ending with "⬅️ חזרה לתפריט". Worked screens: `references/business-bot-templates.md`.

## Phase 4: Business Hours Logic

Israeli business hours follow a unique weekly pattern. Your bot must handle this correctly.

### Israeli Weekly Schedule

The table is the common pattern. **Ask the owner which day the business closes**: many Arab-Israeli and Christian businesses close Friday or Sunday instead of Saturday, and some are busiest on Saturday. Make the weekly closed day a setting, and make the greetings follow it ("שבת שלום" only where Shabbat is the closed day).

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

Major closing holidays, in **Israel day-counts** (outside Israel most run an extra day, so a generic calendar closes the business on a day it should be open):

- **Rosh Hashana** (ראש השנה) - 2 days
- **Yom Kippur** (יום כיפור) - 1 day (nearly everything closes)
- **Sukkot** (סוכות) - day 1, then Shmini Atzeret (a single day, which in Israel is also Simchat Torah)
- **Pesach** (פסח) - day 1 and day 7
- **Shavuot** (שבועות) - 1 day
- **Yom Ha'atzmaut** (יום העצמאות) - 1 day

Treat **Chol HaMoed** (חול המועד, the intermediate days of Sukkot and Pesach, roughly 10 days a year, when much of the workforce is on leave) and **erev chag** (ערב חג, a short day like Friday) as owner-configurable short days. Yom HaZikaron, the day before Yom Ha'atzmaut, closes places of entertainment and quietens trading.

Hebcal is a Jewish calendar, so a business that closes for Ramadan hours, Eid al-Fitr, Eid al-Adha, Christmas or Easter needs those dates entered by the owner (Islamic dates can shift by a day with the moon sighting). If many customers speak Arabic, add an Arabic button to the welcome screen.

Have the bot check a holiday calendar and switch to holiday auto-reply mode, set to the Israel schedule (Hebcal's `i=on` flag) or you inherit the diaspora day-counts.

---

## Phase 5: Appointment Booking

Let customers book appointments directly through the bot using inline keyboards.

### Booking Flow

Four inline-keyboard steps, each with a "⬅️ חזרה" button:

1. **Service** - "מה תרצו לקבוע?" with one button per service.
2. **Date** - "באיזה יום?" with the next open days only (never the weekly closed day).
3. **Time** - "באיזו שעה?" with the free slots for that day.
4. **Confirmation** - a summary of service, day, and time, plus [✅ אישור] and [❌ ביטול].

Keep ONE source of truth for availability (a calendar or booking tool the platform reads, which also holds walk-ins and phone bookings) and re-check the slot at confirmation so two customers cannot take it. Since Bot API 10.3 a full slot can be a disabled button, where the platform exposes it. For a one-chair business, linking to an existing booking system that already sends SMS reminders and takes deposits is often the right first version.

### Confirmation and reminders

After booking, send a confirmation with the service, date, time, address, price, business details and cancellation terms (see Deposits below), plus /cancel. Send two reminders: a day before ("תזכורת: יש לך תור מחר ב-10:00") and two hours before with a navigation link. They need Option B (Phase 0); schedule them in `Asia/Jerusalem`, cancel them with the booking, never at night. A "book again" nudge after a no-show is a promotion, not a reminder: Phase 8 rules apply.

### Deposits (מקדמה)

Use a payment link per booking and hold the slot once it is paid. A bot booking is likely a distance transaction (s.14ג חוק הגנת הצרכן). For a one-off service, a customer who cancels within 14 days of booking (or of receiving the written booking details, if later) AND at least two non-rest days before the appointment gets the deposit back less at most 5% of the FULL price or ₪100, whichever is lower: a ₪2,500 colour with a ₪500 deposit means keep ₪100, refund ₪400. Never write "deposit forfeited on any cancellation". Cosmetic treatments, leisure bookings and session packages follow other windows, a cancellation the business caused carries no fee, and the confirmation must carry the business details and cancellation terms: all in `references/compliance-and-security.md` section 2.

### Important: Friday Booking Logic

For a Saturday-closed business, on Friday show morning slots only (to 13:00 or 14:00), never offer Saturday, and make Sunday the next available day after Thursday. Apply the same logic to whichever day the owner closes.

---

## Phase 6: Order Management

For businesses that sell products or take food orders.

### Order Flow

Three inline-keyboard screens: **categories**, **items** (name, price, "הוסף לסל", "⬅️ חזרה לקטגוריות"), and the **cart** (lines, "סה"כ", [✅ שלח הזמנה] [🗑 נקה סל]). Confirm with an order number, the total, a preparation time and /status. Worked screens: `references/business-bot-templates.md`.

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
one step: Morning (formerly Green Invoice), iCount, Rivhit, Grow (formerly Meshulam) or Cardcom.
PayBox has no public merchant API that we found, so it is a manual step. **Feature sets
change without notice, so confirm invoicing and API support with the provider before you build.**
Comparison table and Bit acceptance terms: `references/israeli-payment-providers.md`.

### Option 2: Telegram Native Payments (Payment API)

Telegram's built-in Payment API lets the bot send native invoice messages customers pay without leaving Telegram. Connect a provider through @BotFather's `/mybots` -> "Payments" menu.

ILS is supported (currency `ILS`, min ₪3.68, max ₪36,788.20 per invoice). Telegram publishes no public provider list: the payments page says only "more than 20 providers", and the real set is whatever @BotFather offers under Bot Settings > Payments. As of 2026-10-29 no Israeli solek is named anywhere in the payments documentation, and Stripe remains the documented reference provider. For clearing through an Israeli solek, use Option 1 or Option 4.

### Option 3: Telegram Stars (for Digital Goods)

Telegram Stars is for digital goods only (online courses, downloadable files and templates, premium content), so physical products and in-person services need an external payment link or the native Payment API. Two consequences worth knowing before you commit: digital sales must go through Stars (currency tag `XTR`), because, in Telegram's words, it "cannot display your bot or mini-app to mobile users if you attempt to sell digital goods and services via other currencies or through third-party payment providers"; and any bot selling with Stars must answer the `/paysupport` command and handle payment complaints. The `provider_token` parameter is only needed for physical goods, so leave it empty for digital ones. Refunds go through `refundStarPayment`. Stars are an in-app virtual item that Telegram says you "can later convert to a reward", not shekels in your bank account, so check the current withdrawal route and its tax treatment with your accountant before pricing in Stars.

### Option 4: Telegram Mini Apps (TWA)

A Mini App is a web page that opens inline inside Telegram, with native APIs for identity, theme, MainButton and payments. Use one when the bot needs richer UX than inline keyboards (catalog grids, calendar pickers, custom checkout with an Israeli provider iframe). Skip it for simple FAQ/booking bots. Setup is via @BotFather (`/mybots`, Bot Settings, Configure Mini App); Israeli providers (Tranzila, PayMe) embed directly, with no Telegram-specific integration. Since Bot API 10.2 Mini App methods work by default only from the Mini App's own domain (an owner can opt out), so the provider's iframe cannot call them.

See `references/mini-apps-implementation.md` for the full setup guide, payment-embedding patterns, and `initData` validation.

### You still have to issue a real invoice

Collecting money through the bot does not change the business's tax obligations: every payment, a deposit included, needs a חשבונית מס or a קבלה. A provider that issues the document with the payment link keeps the bot from becoming a channel that takes money without paperwork. The חשבוניות ישראל allocation number applies only to tax invoices ABOVE the current threshold issued to a registered dealer who will deduct input VAT, so a cafe or salon selling to private consumers will rarely meet it; read the current threshold off the Tax Authority page. Detail: `references/israeli-payment-providers.md`.

Source: `gov.il/he/departments/israel_tax_authority`.

---

## Phase 8: Customer Notifications and Broadcasting

### Channel posts vs DM broadcasts (important distinction)

- **Channel post**: one message reaching every subscriber. The default for promotions, updates and holiday greetings.
- **DM broadcast**: one `sendMessage` per customer, subject to rate limits and, for marketing, to Section 30a. **It reaches only customers who already pressed Start** (Phase 0). Reserve it for transactional updates and promotions to customers who may lawfully receive them.

### Getting customers into the bot: deep links

A bot cannot start a conversation, so grow the reachable audience with start deep links, `t.me/<your_bot>?start=<payload>`. The payload arrives with `/start`, so you can attribute the source (a counter QR code, the receipt, the Instagram bio). It is capped at **64 characters** of `A-Z a-z 0-9 _ -`. An Option A bot must also handle the `/start bizChat<user_chat_id>` link Telegram sends when the owner taps "Manage Bot" in a managed chat. Placements, Business Chat Links and the manage link in detail: `references/business-bot-templates.md` ("Deep-link placements").

Source: `core.telegram.org/bots/features#deep-linking`.

### Telegram Channel for Updates

Create a channel named `[שם העסק] - עדכונים`, add the bot as an administrator, and share the link.

Three shapes cover almost everything: a **promotion** (headline offer, the days it runs, the bot
username for booking, an explicit expiry, plus the labelling rules below), an **order status
update** (the stages with the current one marked, and an ETA), and a **holiday greeting**
naming the return day and hour. Worked message templates are in
`references/business-bot-templates.md`.

### Israeli Spam Law (חוק הספאם) Compliance

Section 30a of the Communications (Telecommunications and Broadcasting) Law, 5742-1982 governs unsolicited advertising. It names fax, automated dialing, electronic messages (הודעה אלקטרונית) and SMS; Telegram is **not named**, and coverage would run through the broad "electronic message" definition, which Israeli practice has not settled. Assume a promotional Telegram broadcast is covered and comply, but do not tell a client the statute names instant messaging.

Four separate requirements: (1) **prior explicit consent** (pressing Start is NOT consent; transactional messages the customer asked for need none), (2) **the word פרסומת at the head of the message**, the one most often missed, (3) **sender identification**: name, address, ways to make contact and a working email for the opt-out, and (4) **a working opt-out in every message**, which the recipient may use in writing or through the medium the promotion arrived in, so a Telegram promotion needs a Telegram opt-out. Honour opt-outs immediately. Keep provable consent records: Telegram user id, the exact opt-in text shown, and the timestamp. The compliant template and the full rules are in `references/business-bot-templates.md`.

Consent is not the only route. Under s.30a(ג) a customer who gave their details while buying, was told then that they would get offers, and was given a chance to refuse may receive promotions for similar services. For a bot, put that notice and a "לא, תודה" button in the first booking message (`references/compliance-and-security.md` section 3).

Penalties: statutory damages up to ₪1,000 per message without proof of harm, and a criminal fine. When in doubt, treat a message as a promotion.

### Privacy: the bot's customer list is a database

A bot that stores customer names, phone numbers, appointment histories, and order records is a **מאגר מידע** under Israel's Privacy Protection Law as amended by Amendment 13. A typical salon or cafe bot does not need to register it or appoint a privacy officer (those duties target public bodies, data traders and large-scale monitoring or sensitive-data processing); a clinic or therapist bot holding health data needs a review. What every such bot does need:

- **A notice at collection (s.11)**: purpose, the owner's name and contact details, whether giving the data is optional, who receives it, and the right to see and correct it. A ready Hebrew notice is in `references/compliance-and-security.md` section 4.
- **A way to see and correct the data**, for example a /mydata command the owner actually handles.
- **Basic security**: encrypted transfer (HTTPS), few people with access, no customer data in spreadsheets shared by link, and old records deleted on a schedule.
- **Direct mail** (s.17ו) adds its own labelling and deletion right if you promote to a segment of the database.
- **Data held abroad**: messages pass through Telegram, and a US no-code host (BotPress cloud, ManyChat) moves the data out of Israel; read its processing terms first and name both in the notice.

Source: `gov.il/he/departments/the_privacy_protection_authority`. A business holding a substantial customer database should get its obligations reviewed.

---

## Phase 9: No-Code Bot Platforms

No code is needed. Three visual editors are worth looking at for an Israeli SMB: **BotPress** (drag-and-drop flows, best for
multi-step booking), **n8n** (Telegram trigger plus a Schedule Trigger for reminders, best for
wiring the bot to Google Sheets, calendars, CRMs or Green Invoice), and **ManyChat** (best if the
business already uses it for Instagram or WhatsApp). **Tiers, Hebrew support and integration
coverage change without notice, so check the vendor's own pricing page before committing.**
Comparison in `references/no-code-platforms.md`.

### Webhook vs Polling (Deployment Note)

Telegram delivers updates by polling or by webhook (a push to your HTTPS URL). Cloud no-code platforms hide this. If you self-host (for example n8n), set a webhook secret so your server can reject calls that are not from Telegram (`references/compliance-and-security.md` section 1).

---

## Phase 10: Hebrew-Specific Setup

### RTL Considerations

Hebrew displays RTL by default, including button labels; commands such as `/start` stay LTR. For a mixed run in the wrong order, see the bidi fix in Troubleshooting.

### Greetings and tone

Match the greeting to the moment and to the owner's closed day, keep it friendly, direct and brief, and use plural "אתם/אתן" for a general audience. The full list of greeting conventions and the tone guide are in `references/business-bot-templates.md`.

### Hebrew Command Aliases

Bot commands must be Latin characters, but customers should never have to type them. Give every command a Hebrew button label instead: 🏠 תפריט ראשי for `/start`, 📅 קביעת תור for /book, 📋 תפריט for /menu, 🕐 שעות פעילות for /hours, 📞 צרו קשר for /contact, ❌ ביטול for /cancel, 📦 סטטוס הזמנה for /status.

## Bundled Resources

- `references/business-bot-templates.md` - full message flows for restaurant, salon, and freelance service bots
- `references/mini-apps-implementation.md` - Mini App setup, embedding an Israeli payment provider, and `initData` validation
- `references/israeli-payment-providers.md` - provider comparison, which ones issue the invoice, Bit acceptance terms
- `references/no-code-platforms.md` - BotPress, n8n and ManyChat feature comparison
- `references/compliance-and-security.md` - token handling and incident response, deposits and consumer cancellation law, the s.30a existing-customer route, privacy duties
- `references/domain-checklist.md` - what a complete version of this skill must cover

---

## Gotchas

Common mistakes agents make when helping set up Israeli business bots:

1. **Forgetting the weekly closed day** - For most businesses that is Shabbat: a Shabbat auto-reply, no Saturday slots, a short Friday. Ask first, since some businesses close Friday or Sunday instead.

2. **Using Sunday as a day off** - The Israeli work week is Sunday to Thursday. Do not copy Western business-hour templates.

3. **Writing stiff Hebrew** - Use "אפשר" rather than "ניתן", and "בואו" rather than "הנכם מוזמנים". The bot should sound like a friendly shop owner, not a government form.

4. **Over-engineering version one** - Ship welcome, hours, FAQ, and one booking or ordering flow. Add the rest once those work.

5. **Leaking the token** - The token is a password. Never post it in chats (an AI chat included), forums, screenshots or a browser address bar. If it leaks, send @BotFather `/token` to generate a new one; the old token stops working.

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

Complete flows for all three (menu trees, stylist selection, confirmations, the document checklist) are in `references/business-bot-templates.md`; read it instead of re-deriving them.

## Troubleshooting

### Bot Not Responding

- **The same token is connected in two places.** A bot token can feed one consumer. Platforms differ: some poll, some register a webhook (n8n's Telegram Trigger does, and Telegram keeps a single webhook per bot). Two pollers make each other fail (platforms commonly log a 409 Conflict; Telegram's docs do not name the code); a polling platform cannot run while a webhook is set ("This method will not work if an outgoing webhook is set up"); and a second webhook platform silently takes over, so the first goes quiet with no error. Fix: disconnect the token everywhere except one platform, using each platform's own disconnect button, or create a second bot with `/newbot`. If the old platform is gone, reconnecting the one you keep usually clears its webhook. Never ask the owner for the token to test this, and do not call the API from a browser address bar (`core.telegram.org/bots/api#getupdates`).
- **Check the token**: Make sure you copied the full token from BotFather without extra spaces
- **Bot not connected to platform**: Verify the token is entered correctly in your no-code platform (BotPress, n8n, etc.)
- **Platform is down**: Check the platform's status page
- **Webhook URL unreachable**: If using webhooks deliberately, the URL must be HTTPS and publicly accessible

### Messages Not Arriving

- **Privacy mode**: By default, bots in groups only see messages starting with `/`. Use BotFather's `/setprivacy` to change this if needed
- **Bot blocked**: The user may have blocked your bot. You cannot send messages to users who blocked you. Telegram signals it with a `my_chat_member` update, which for private chats arrives only when the bot is blocked or unblocked; mark that customer unreachable
- **Rate limits** (`core.telegram.org/bots/faq`): about 1 message per second to one chat, 20 messages per minute to one group, and about 30 messages per second across users. Exceeding them returns HTTP 429, so space out DM broadcasts or post to a channel. Paid broadcasts (up to 1,000 per second, 0.1 Stars per message above the free 30) need 100,000 Stars and 100,000 monthly active users per the FAQ: not for an SMB.
- **Version note**: this skill is aligned with Bot API 10.3 (August 24, 2026). Check the changelog at the top of `core.telegram.org/bots/api` if a feature behaves differently.

### Hebrew Text Display Issues

- **Ensure your platform sends UTF-8**: All modern platforms do, but verify if text appears garbled
- **Mixed LTR/RTL**: an English word, URL or number in the wrong place inside Hebrew is Unicode bidi resolution, not a Telegram bug. Wrap the LTR run in U+2066 (LRI) and U+2069 (PDI), or U+2068 (FSI) to let it pick its direction; a U+200F (RLM) after the run also restores RTL. Apply the same to button labels that mix Hebrew with a price, a Latin name or a phone number.

### Booking Shows Wrong Times

- **Timezone**: Make sure your platform is set to `Asia/Jerusalem` (UTC+2, or UTC+3 during daylight saving)
- **DST transitions**: Israel changes clocks in March and October. Verify your time logic handles this
- **Friday hours**: Double-check that Friday only shows shortened hours, not full-day availability

### Payment Link Not Working

- **Link expired**: Payment links expire, but the window is set per provider and per link. Check your provider's link-expiry setting rather than assuming a fixed window, and generate a fresh link per order
- **Mobile browser redirect**: Test the payment link on mobile. Some gateways redirect poorly on Telegram's in-app browser
- **Currency**: Make sure the payment page shows ILS (₪), not USD or EUR

### Bot Got Compromised

Open @BotFather and send `/token`, which is the documented way to generate a new authorization token when the existing one is compromised. Pick the bot and update the new token in your platform immediately. Then re-check what the old token could change (name, description, commands, menu button, Mini App URL, webhook) and warn customers not to act on messages you did not send. Telegram keeps no sent-message log for you to review. Full checklist: `references/compliance-and-security.md` section 1.

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
