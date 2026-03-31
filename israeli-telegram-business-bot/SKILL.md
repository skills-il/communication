---
name: israeli-telegram-business-bot
description: "Set up Telegram bots for Israeli small businesses with appointment booking, order management, FAQ auto-replies in Hebrew, business hours awareness (Sunday-Thursday), payment links, and customer notifications. Use when an Israeli business owner asks about creating a Telegram bot, automating customer replies, taking orders via Telegram, or scheduling appointments through a bot. Helps non-technical users deploy a working business bot without writing code, reducing missed customer messages and manual response overhead. Do NOT use for WhatsApp Business (use israeli-whatsapp-business), building bots from code (use telegram-bot-builder), voice bots (use hebrew-voice-bot-builder), or general support ticket routing (use israeli-customer-support-automator)."
license: MIT
---

# Israeli Telegram Business Bot

Set up a Telegram bot for an Israeli small business. Covers bot creation, Hebrew auto-replies, appointment booking, order management, business hours handling (Sunday-Thursday), payment links, and customer notifications. Designed for non-technical business owners.

## Problem

Israeli small business owners lose customers every day because they can't respond fast enough. Messages come in during Shabbat, late at night, or when the owner is with another client. The result: unanswered questions, missed bookings, and lost revenue.

Most Israeli businesses rely on WhatsApp, but Telegram offers powerful bot automation that WhatsApp doesn't: inline keyboards, automatic replies, structured menus, and payment integration, all without writing a single line of code. The problem is that most business owners don't know how to set up a Telegram bot, and existing guides assume developer knowledge.

This skill bridges that gap. It walks business owners through creating a professional Telegram bot that handles the repetitive parts of customer communication: answering FAQs, booking appointments, taking orders, and sending notifications, in Hebrew, with Israeli business hours and culture built in.

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

Send these commands to @BotFather:

```
/setdescription
```
Write a Hebrew description customers see before starting a chat:
> ברוכים הבאים! אני הבוט של [שם העסק]. אפשר לקבוע תור, לראות תפריט, ולקבל מידע על שעות פעילות. זמין 24/7!

```
/setabouttext
```
Short "about" text for the bot profile:
> בוט שירות לקוחות של [שם העסק] - תורים, הזמנות, ומידע

```
/setuserpic
```
Upload your business logo or a professional photo.

```
/setcommands
```
Set the command menu:
```
start - התחל שיחה
hours - שעות פעילות
book - קבע תור
menu - תפריט / שירותים
contact - צור קשר
help - עזרה
```

---

## Phase 2: Welcome Message and Auto-Greeting

When a customer opens your bot for the first time and presses "Start", they should immediately receive a warm Hebrew greeting with clear navigation options.

### Welcome Message Template

```
שלום! 👋
ברוכים הבאים ל[שם העסק].

איך אפשר לעזור?
```

Pair this with an **inline keyboard** showing the main options:

| Button Row | Button Text | Action |
|-----------|-------------|--------|
| Row 1 | 📅 קביעת תור | -> Booking flow |
| Row 1 | 📋 תפריט/שירותים | -> Menu/services list |
| Row 2 | 🕐 שעות פעילות | -> Business hours |
| Row 2 | 📍 מיקום | -> Location/map link |
| Row 3 | 📞 דברו איתנו | -> Contact info |

### Important Notes for the Welcome Flow

- Keep the greeting short, no more than 3 lines before the buttons
- Use Hebrew as the default language
- Include an English option button if you serve tourists or English speakers
- The greeting should feel personal, not corporate. "שלום!" is better than "שלום וברוכים הבאים לשירות הלקוחות שלנו"

---

## Phase 3: FAQ Auto-Replies

Set up automatic answers to the questions you get asked 10 times a day.

### Common FAQ Categories for Israeli Businesses

**Business Hours:**
```
🕐 שעות פעילות:

ראשון - חמישי: 09:00 - 18:00
שישי: 09:00 - 14:00
שבת: סגור

חגים: לפי עדכונים בערוץ שלנו
```

**Location:**
```
📍 המיקום שלנו:

[כתובת מלאה]
[עיר]

🗺 לניווט: [Google Maps link]
🅿️ חניה: [פרטי חניה]
```

**Prices / Menu:**
```
📋 התפריט שלנו:

[Display as inline keyboard categories or send a PDF/image]
```

**Contact:**
```
📞 צרו קשר:

טלפון: 050-XXX-XXXX
ווטסאפ: [WhatsApp link]
אימייל: info@business.co.il

או כתבו לנו כאן ונחזור אליכם בשעות הפעילות!
```

### Multi-Level FAQ with Inline Keyboards

For businesses with many questions, use a tree structure:

```
Main Menu
├── 📋 שירותים
│   ├── תספורת גברים - ₪80
│   ├── תספורת נשים - ₪120-200
│   ├── צבע - ₪250+
│   └── ⬅️ חזרה לתפריט
├── 💰 מחירים
│   ├── מחירון מלא (PDF)
│   └── ⬅️ חזרה לתפריט
├── 📅 קביעת תור
└── 🕐 שעות פעילות
```

---

## Phase 4: Business Hours Logic

Israeli business hours follow a unique weekly pattern. Your bot must handle this correctly.

### Israeli Weekly Schedule

| Day | Hebrew | Typical Hours | Status |
|-----|--------|---------------|--------|
| Sunday (יום ראשון) | א׳ | 08:00/09:00 - 17:00/18:00 | Open |
| Monday (יום שני) | ב׳ | 08:00/09:00 - 17:00/18:00 | Open |
| Tuesday (יום שלישי) | ג׳ | 08:00/09:00 - 17:00/18:00 | Open |
| Wednesday (יום רביעי) | ד׳ | 08:00/09:00 - 17:00/18:00 | Open |
| Thursday (יום חמישי) | ה׳ | 08:00/09:00 - 17:00/18:00 | Open |
| Friday (יום שישי) | ו׳ | 08:00/09:00 - 13:00/14:00 | Short day |
| Saturday (שבת) | ש׳ | Closed | Shabbat |

### After-Hours Auto-Reply

When someone messages outside business hours, reply automatically:

**Regular evening/night (Sunday-Thursday):**
```
היי! 🌙
קיבלנו את ההודעה שלך.
אנחנו פעילים ראשון-חמישי בין 09:00-18:00.
נחזור אליך מחר בבוקר!

בינתיים, אפשר:
📅 לקבוע תור
📋 לראות תפריט
🕐 לבדוק שעות פעילות
```

**Friday afternoon / Shabbat:**
```
שבת שלום! 🕯
קיבלנו את ההודעה. נחזור אליך ביום ראשון.

בינתיים, אפשר לקבוע תור או לראות מידע דרך התפריט.
```

**Erev Chag (holiday eve):**
```
חג שמח! 🎉
אנחנו בחופשת חג ונחזור ב[תאריך חזרה].

לתורים ומידע, השתמשו בתפריט למטה.
```

### Holiday Awareness

Major Israeli holidays when businesses typically close:
- **Rosh Hashana** (ראש השנה) - 2 days
- **Yom Kippur** (יום כיפור) - 1 day (nearly everything closes)
- **Sukkot** (סוכות) - 1st and last days
- **Pesach** (פסח) - 1st and last days
- **Shavuot** (שבועות) - 1 day
- **Yom Ha'atzmaut** (יום העצמאות) - 1 day

Configure your bot to check a holiday calendar and switch to holiday auto-reply mode. Most no-code platforms support date-based logic or scheduled message changes.

---

## Phase 5: Appointment Booking

Let customers book appointments directly through the bot using inline keyboards.

### Booking Flow

```
Step 1: Service Selection
┌─────────────────────────┐
│ מה תרצו לקבוע?          │
│                         │
│ [💇 תספורת]  [💅 מניקור] │
│ [💆 טיפול פנים] [✂️ צבע] │
└─────────────────────────┘

Step 2: Date Selection
┌─────────────────────────┐
│ באיזה יום?              │
│                         │
│ [ראשון 2/4] [שני 3/4]   │
│ [שלישי 4/4] [רביעי 5/4] │
│ [חמישי 6/4] [שישי 7/4]  │
└─────────────────────────┘

Step 3: Time Selection
┌─────────────────────────┐
│ באיזו שעה?              │
│                         │
│ [09:00] [10:00] [11:00] │
│ [14:00] [15:00] [16:00] │
└─────────────────────────┘

Step 4: Confirmation
┌─────────────────────────┐
│ ✅ סיכום התור:           │
│                         │
│ שירות: תספורת           │
│ יום: שני 3/4            │
│ שעה: 10:00              │
│                         │
│ [✅ אישור] [❌ ביטול]    │
└─────────────────────────┘
```

### Confirmation Message

After booking:
```
✅ התור נקבע!

שירות: תספורת
תאריך: יום שני, 3 באפריל
שעה: 10:00
כתובת: [כתובת העסק]

נשלח תזכורת יום לפני.
לביטול או שינוי, שלחו /cancel
```

### Reminder Notifications

- **24 hours before**: "תזכורת: יש לך תור מחר ב-10:00 ב[שם העסק]. לאישור לחצו ✅"
- **2 hours before**: "התור שלך ב[שם העסק] בעוד שעתיים. נתראה! 📍 [קישור לניווט]"
- **After no-show**: Wait 30 minutes, then "לא הספקת להגיע? אפשר לקבוע תור חדש כאן: /book"

### Important: Friday Booking Logic

When a customer tries to book for Friday:
- Only show morning time slots (until 13:00 or 14:00 depending on the business)
- Never show Saturday (Shabbat) as an option
- After Thursday, the next available day should be Sunday

---

## Phase 6: Order Management

For businesses that sell products or take food orders.

### Product Catalog via Inline Keyboard

```
🛒 ההזמנה שלך

קטגוריות:
[🍕 פיצות] [🥗 סלטים]
[🍝 פסטות] [🥤 שתייה]
[🍰 קינוחים]
```

When a customer selects a category:
```
🍕 פיצות:

מרגריטה - ₪45
פפרוני - ₪52
ארבע גבינות - ₪55
ירקות - ₪48

[הוסף לסל: מרגריטה]
[הוסף לסל: פפרוני]
[הוסף לסל: ארבע גבינות]
[הוסף לסל: ירקות]
[⬅️ חזרה לקטגוריות]
```

### Order Summary

```
🛒 סיכום ההזמנה:

1x פיצה מרגריטה - ₪45
2x קולה - ₪20
1x סלט יווני - ₪38

סה"כ: ₪103

[✅ שלח הזמנה] [🗑 נקה סל] [📋 חזרה לתפריט]
```

### Order Confirmation

```
✅ ההזמנה התקבלה!

מספר הזמנה: #1247
סה"כ: ₪103

זמן הכנה משוער: 30-40 דקות
נעדכן כשההזמנה מוכנה!

לסטטוס: /status
```

---

## Phase 7: Payment Integration

### Option 1: External Payment Links

The simplest approach for Israeli businesses. Generate a payment link from your existing payment provider and send it in the bot:

```
💳 לתשלום:

סה"כ לתשלום: ₪103

בחרו אמצעי תשלום:
[💳 כרטיס אשראי] -> link to payment page
[📱 ביט] -> Bit payment link
[🏦 העברה בנקאית] -> bank details
```

**Popular Israeli payment gateways:**
- **Green Invoice** (חשבונית ירוקה) - generates payment links with automatic invoice
- **Rivhit** (רווחית) - payment collection with accounting integration
- **PayMe** - simple payment page creation
- **iCount** - invoicing with payment links
- **Meshulam** - payment clearing for small businesses

### Option 2: Telegram Stars (for Digital Goods)

Telegram supports Telegram Stars for in-app purchases of digital goods and services. This works well for:
- Digital consultations
- Online courses
- Digital files/templates
- Premium content access

Note: Telegram Stars is for digital goods only. Physical products and services should use external payment links.

### Payment Confirmation Message

```
✅ התשלום התקבל!

סכום: ₪103
אמצעי תשלום: כרטיס אשראי
מספר הזמנה: #1247

חשבונית תשלח לאימייל שלך.
תודה על הקנייה! 🙏
```

---

## Phase 8: Customer Notifications and Broadcasting

### Telegram Channel for Updates

Create a Telegram channel linked to your bot for broadcasting updates:

1. Create a new channel in Telegram
2. Name it: `[שם העסק] - עדכונים`
3. Add your bot as an administrator
4. Share the channel link with customers

### Types of Broadcasts

**Promotions:**
```
🔥 מבצע סוף שבוע!

20% הנחה על כל הטיפולים ביום חמישי וביום שישי.
לקביעת תור: @your_bot

בתוקף עד שישי 7/4 בצהריים.
```

**Status Updates (for orders):**
```
📦 עדכון הזמנה #1247:

✅ ההזמנה התקבלה
✅ בהכנה
🔄 בדרך אליך
⬜ נמסרה

זמן הגעה משוער: 15 דקות
```

**Holiday Greetings:**
```
🕯 שבת שלום מ[שם העסק]!

נחזור ביום ראשון ב-09:00.
לקביעת תורים, כתבו לבוט שלנו.

שבת מנוחה! 🌸
```

---

## Phase 9: No-Code Bot Platforms

You do NOT need to write code to build a Telegram business bot. These platforms offer visual editors.

### Recommended Platforms

**BotPress**
- Visual flow builder with Hebrew support
- Free tier available
- Good Telegram integration
- Drag-and-drop conversation design
- Best for: complex conversation flows, multi-step booking

**n8n (Self-Hosted or Cloud)**
- Visual workflow automation
- Telegram trigger node built-in
- Code node for custom logic (optional)
- Schedule Trigger node for timed messages (reminders, promotions)
- Best for: connecting Telegram to other business tools (Google Sheets, calendars, CRMs)
- Can integrate with Israeli platforms like Monday.com and Green Invoice

**ManyChat**
- Full native Telegram support with visual flow builder
- Drag-and-drop automation sequences
- Subscriber management and broadcasts
- Also supports Instagram, WhatsApp, Facebook Messenger
- Best for: businesses already using ManyChat for other channels, visual flow design

### Platform Comparison

| Feature | BotPress | n8n | ManyChat |
|---------|----------|-----|----------|
| Hebrew support | Yes | Yes | Partial |
| Visual builder | Yes | Yes | Yes |
| Free tier | Yes | Yes (self-host) | Limited |
| Telegram integration | Native | Native node | Native |
| Appointment booking | With flows | With calendar integration | Basic |
| Payment links | Via messages | Via HTTP nodes | Via messages |
| Learning curve | Medium | Medium | Low |
| Israeli platform integrations | Via API | Native nodes for many | Limited |

---

## Phase 10: Hebrew-Specific Setup

### RTL Considerations

- Hebrew text in Telegram displays correctly RTL by default
- Mixed Hebrew/English text (like prices "₪45") renders properly
- Inline keyboard buttons support Hebrew text
- Bot commands (like /start) remain LTR - this is normal and expected

### Hebrew Greeting Conventions

Use greetings appropriate to Israeli culture:

| Time/Context | Greeting |
|-------------|----------|
| General | שלום! / היי! |
| Morning | בוקר טוב! ☀️ |
| Evening | ערב טוב! 🌙 |
| Friday | שבת שלום! 🕯 |
| After Shabbat | שבוע טוב! |
| Holiday | חג שמח! 🎉 |
| Thank you | תודה רבה! 🙏 |

### Hebrew Command Aliases

While bot commands must be in Latin characters, you can map Hebrew text to commands:

| Command | Hebrew Alias (button text) |
|---------|---------------------------|
| /start | 🏠 תפריט ראשי |
| /book | 📅 קביעת תור |
| /menu | 📋 תפריט / שירותים |
| /hours | 🕐 שעות פעילות |
| /contact | 📞 צרו קשר |
| /help | ❓ עזרה |
| /cancel | ❌ ביטול |
| /status | 📦 סטטוס הזמנה |

### Tone of Voice

Israeli business communication on Telegram should be:
- **Friendly and direct** - no corporate stiffness
- **Use "אתם/אתן"** (plural you) for general audiences, or **"את/ה"** if the business is personal/intimate
- **Casual but professional** - emojis are welcome, slang is not
- **Brief** - Israelis expect quick answers, not paragraphs

---

## Bundled Resources

- `references/business-bot-templates.md` - Complete message flow templates for restaurant, salon, and freelance service bots

---

## Gotchas

Common mistakes agents make when helping set up Israeli business bots:

1. **Forgetting Shabbat handling** - The most common mistake. The bot MUST have a Shabbat auto-reply. Never show Saturday availability for booking. Friday must have shortened hours. If you skip this, the business owner will get complaints from religious customers and confusion from everyone else.

2. **Using Sunday as a day off** - Israel's work week is Sunday-Thursday, not Monday-Friday. Sunday is a regular working day. Do not copy Western business hour templates.

3. **Writing stiff/formal Hebrew** - Do not use "ניתן" (formal "it is possible"), use "אפשר" (casual "you can"). Do not use "הנכם מוזמנים" (you are cordially invited), use "בואו" or "אפשר". The bot should sound like a friendly shop owner, not a government form.

4. **Over-engineering the first version** - Start with: welcome message, business hours, FAQ, and one booking or ordering flow. Do not try to build a full CRM bot on day one. Add features once the basics are working.

5. **Ignoring the token security** - The bot token is a password. Do not share it in group chats, paste it in public forums, or include it in screenshots. If leaked, anyone can control the bot. Use BotFather's `/revoke` command if compromised.

6. **Not setting up a human handoff** - Bots can't handle everything. Include a "דברו עם נציג" (talk to a human) option that either forwards the message to the business owner's personal Telegram or sends a notification.

7. **Wrong phone number format** - Israeli numbers should be formatted as `050-XXX-XXXX` or `+972-50-XXX-XXXX` for international. Do not use `(050) XXX-XXXX` or other non-Israeli formats.

8. **Missing a "back" button** - Every sub-menu must have a "⬅️ חזרה" (back) button. Customers get frustrated when they're stuck in a menu with no way to return to the main screen.

9. **Not testing on mobile** - Most Israeli Telegram users are on mobile. Test every flow on a phone, not just desktop. Buttons that look fine on desktop may be too small or too wide on mobile.

10. **Hardcoding holiday dates** - Israeli holidays fall on different dates each year (Hebrew calendar). Use a holiday API or update manually before each holiday season rather than hardcoding dates.

---

## Examples

### Example 1: Restaurant Bot

**Scenario:** "Cafe Shemesh" in Tel Aviv wants a Telegram bot for viewing the menu, ordering takeout, and booking tables.

**Agent should generate:**

Welcome message with inline keyboard:
```
שלום! ☀️
ברוכים הבאים לקפה שמש.

מה בא לכם?
[📋 תפריט] [🛒 הזמנה לטייקאווי]
[📅 הזמנת שולחן] [🕐 שעות פעילות]
[📍 איך מגיעים] [📞 צרו קשר]
```

Menu flow with categories:
```
📋 התפריט שלנו:

[☕ קפה ושתייה]
[🥐 ארוחות בוקר]
[🥗 ארוחות צהריים]
[🍰 קינוחים]
[⬅️ חזרה לתפריט הראשי]
```

Business hours with Friday/Shabbat:
```
🕐 שעות פעילות:

ראשון - חמישי: 07:30 - 23:00
שישי: 07:30 - 15:00
שבת: סגור

📍 רחוב דיזנגוף 99, תל אביב
```

### Example 2: Hair Salon Bot

**Scenario:** "Salon Dana" in Haifa wants appointment booking, price list, and before/after photos.

**Agent should generate:**

Booking flow with service selection:
```
💇 קביעת תור בסלון דנה

בחרו שירות:
[💇‍♀️ תספורת נשים - מ-₪120]
[💇‍♂️ תספורת גברים - ₪80]
[🎨 צבע - מ-₪250]
[💅 מניקור - ₪90]
[💆‍♀️ טיפול פנים - ₪180]
[⬅️ חזרה]
```

Stylist selection (if relevant):
```
עם מי תרצו להזמין?

[דנה - בעלים ומעצבת ראשית]
[שירה - צבע ותספורות]
[יובל - תספורות גברים]
[⬅️ חזרה]
```

After booking confirmation:
```
✅ התור נקבע!

שירות: תספורת נשים
מעצבת: דנה
תאריך: יום שלישי, 5 באפריל
שעה: 14:00

📍 סלון דנה, רחוב הרצל 15, חיפה
🅿️ חניה חינם ברחוב

נשלח תזכורת מחר.
לביטול: /cancel
```

### Example 3: Freelance Accountant Bot

**Scenario:** "Moshe Levi, CPA" wants a bot for scheduling consultations, sharing document checklists, and answering common tax questions.

**Agent should generate:**

Welcome with professional tone:
```
שלום! 👋
משרד רו"ח משה לוי

איך אפשר לעזור?
[📅 קביעת פגישת ייעוץ]
[📄 מסמכים נדרשים]
[❓ שאלות נפוצות]
[💰 מחירון שירותים]
[📞 צרו קשר]
```

FAQ with tax-related questions:
```
❓ שאלות נפוצות:

[📊 מתי מגישים דוח שנתי?]
[🧾 איזה קבלות לשמור?]
[💼 פתיחת תיק עוסק מורשה]
[🏠 ניכוי הוצאות עבודה מהבית]
[📱 דיווח הכנסות מאפליקציות]
[⬅️ חזרה]
```

Document checklist (when selected):
```
📄 מסמכים נדרשים לדוח שנתי:

✅ תלושי שכר (כל 12 החודשים)
✅ טפסי 106 מכל מעסיק
✅ אישורי ריבית מהבנק
✅ קבלות על תרומות
✅ אישור ביטוח לאומי
✅ אישורי קופות גמל/פנסיה

💡 טיפ: צלמו הכל ושלחו לנו כאן, ונבדוק שיש את הכל.

[📅 קבע פגישה] [⬅️ חזרה]
```

---

## Troubleshooting

### Bot Not Responding

- **Check the token**: Make sure you copied the full token from BotFather without extra spaces
- **Bot not connected to platform**: Verify the token is entered correctly in your no-code platform (BotPress, n8n, etc.)
- **Platform is down**: Check the platform's status page
- **Webhook issues**: If using webhooks, make sure the URL is HTTPS and publicly accessible

### Messages Not Arriving

- **Privacy mode**: By default, bots in groups only see messages starting with `/`. Use BotFather's `/setprivacy` to change this if needed
- **Bot blocked**: The user may have blocked your bot. You cannot send messages to users who blocked you
- **Rate limits**: Telegram limits bots to 30 messages/second. For broadcasts to many users, add delays between messages

### Hebrew Text Display Issues

- **Ensure your platform sends UTF-8**: All modern platforms do, but verify if text appears garbled
- **Mixed LTR/RTL**: If numbers or English text appear in wrong order, try wrapping Hebrew text segments separately
- **Inline keyboard alignment**: Hebrew buttons may appear left-aligned in some Telegram clients. This is a client-side rendering behavior and not something you can control

### Booking Shows Wrong Times

- **Timezone**: Make sure your platform is set to `Asia/Jerusalem` (UTC+2, or UTC+3 during daylight saving)
- **DST transitions**: Israel changes clocks in March and October. Verify your time logic handles this
- **Friday hours**: Double-check that Friday only shows shortened hours, not full-day availability

### Payment Link Not Working

- **Link expired**: Some payment gateways expire links after 24-72 hours. Generate fresh links per order
- **Mobile browser redirect**: Test the payment link on mobile. Some gateways redirect poorly on Telegram's in-app browser
- **Currency**: Make sure the payment page shows ILS (₪), not USD or EUR

### Bot Got Compromised

If you suspect someone has your bot token:
1. Open @BotFather
2. Send `/revoke`
3. Select your bot
4. You'll get a new token. Update it in your platform immediately
5. Check recent bot activity for suspicious messages
