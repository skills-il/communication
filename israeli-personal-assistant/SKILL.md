---
name: israeli-personal-assistant
description: "A smart personal assistant that understands the Israeli context: workday planning (Sunday-Thursday), drafting messages in natural Hebrew, reminders for business obligations (VAT, Bituach Leumi, holidays), and help composing emails to official bodies. Use when you need a morning brief, professional WhatsApp drafting, scheduling around Shabbat and holidays, or writing formal Hebrew emails. Saves daily time and prevents communication missteps. Do NOT use for calendar API integration (use shabbat-aware-scheduler), automated email sending (use gws-hebrew-email-automation), or accounting calculations (use accounting skills)."
license: MIT
---

## Overview

Israeli Personal Assistant is a **judgment layer** for Israeli daily life and work. It gives your AI agent the context it needs to behave like a local: the right work week, natural Hebrew phrasing, awareness of Jewish holidays, and knowledge of recurring business obligations.

This skill does **not** integrate with live APIs, calendars, or email services. For live integrations, pair it with:
- **shabbat-aware-scheduler** (calendar API with Shabbat/holiday awareness)
- **gws-hebrew-email-automation** (automated email sending via Google Workspace)

What this skill provides: context, conventions, templates, and judgment. Think of it as the cultural and operational knowledge layer that makes your AI assistant feel Israeli rather than generic.

**Do NOT use this skill for:**
- Connecting to calendar APIs or creating live calendar events (use shabbat-aware-scheduler)
- Sending emails automatically (use gws-hebrew-email-automation)
- Calculating VAT, income tax, or payroll (use accounting category skills)
- Legal document drafting (use legal-tech category skills)

**Primary audience:** Freelancers, small business owners, and knowledge workers. No technical background required.

---

## When to Use

| Situation | What to ask |
|-----------|-------------|
| Start of day | "Give me a morning brief for today, [date]" |
| Writing a follow-up message | "Draft a WhatsApp to a client who hasn't paid invoice #42" |
| Planning a meeting | "What days work this week around Shabbat and [holiday]?" |
| Government correspondence | "Help me write a formal letter to Bituach Leumi about [topic]" |
| Invoice reminder | "Write a polite but firm payment reminder for [client name]" |
| Deadline check | "When is my next VAT reporting window?" |
| Scheduling with context | "Is next Friday afternoon a good time for a meeting?" |

---

## Israeli Work Week and Calendar

### Work Week

The Israeli work week runs **Sunday (יום ראשון) through Thursday (יום חמישי)**.

| Day | Hebrew | Status |
|-----|--------|--------|
| Sunday | יום ראשון | Full workday, start of week |
| Monday | יום שני | Full workday |
| Tuesday | יום שלישי | Full workday |
| Wednesday | יום רביעי | Full workday |
| Thursday | יום חמישי | Full workday, end of week |
| Friday | יום שישי | Short day, most businesses close by 13:00-14:00 |
| Saturday | שבת | Rest day. No business activity whatsoever |

**Friday scheduling rule:** Never schedule meetings, calls, or deliveries on Friday afternoon. The cutoff is generally 13:00 for most businesses. Erev Chag (the eve of a Jewish holiday) follows the same short-day rule.

### Jewish Holiday Impact on Business

| Holiday | Duration | Business Impact |
|---------|----------|-----------------|
| Yom Kippur | 1 day | Complete shutdown. Even secular Israelis don't work |
| Rosh Hashana | 2 days | Full shutdown, most take additional days |
| Sukkot | 7 days | Full shutdown on first/last days; Chol HaMoed is partial |
| Pesach | 7 days | Full shutdown on first/last days; Chol HaMoed is partial |
| Shavuot | 1-2 days | Full shutdown |
| Purim | 1 day | Many take the day off; expect slow responses |

**Chol HaMoed note:** Businesses technically operate during Chol HaMoed (intermediate days of Sukkot and Pesach), but many employees are on vacation. Expect 30-50% slower response times and limited availability.

**August:** Israeli summer vacation season. Many families travel. Expect slower response rates throughout the month, especially during the last two weeks.

### Key Business Obligation Dates

| Obligation | Frequency | Window |
|------------|-----------|--------|
| VAT (מע"מ) reporting | Bi-monthly | 15th of the month following the reporting period |
| VAT payment | Bi-monthly | Same as reporting |
| Bituach Leumi (NII) advance payments | Monthly | 15th of each month |
| Annual tax return (עצמאים) | Annual | Typically April-May (check current year deadline) |
| Income tax advance (מקדמות) | Monthly | 15th of each month |

Always verify current deadlines with the relevant authority (רשות המיסים, המוסד לביטוח לאומי), as dates can shift around holidays.

---

## Daily Brief Template

Use this structure when asking for a morning brief. Ask your AI: "Give me a morning brief for [date]."

### Brief Structure

1. **Hebrew date** (e.g., י״ח בניסן תשפ״ו) alongside the Gregorian date
2. **Day of week** with any scheduling notes (short day? Erev Chag?)
3. **Open tasks** you have provided
4. **Upcoming deadlines** in the next 7 days
5. **Holiday or Chag alerts** this week and next
6. **Business obligation reminders** (VAT window, Bituach Leumi, etc.)

### Example Morning Brief (English)

```
Morning Brief - Sunday, April 5, 2026 / י״ח בניסן תשפ״ו

Day: Start of work week (Sunday). Full workday.
Holiday alert: Pesach Chol HaMoed (through April 7). Many contacts may be on vacation - expect slower responses.

Open tasks:
- Follow up with Rivka on the design proposal (3 days overdue)
- Send invoice #87 to client ABC Ltd.

Upcoming deadlines:
- Pesach last days: April 8-9 (full shutdown, plan ahead)
- Bituach Leumi advance payment due April 15

Reminders:
- Next VAT deadline: May 15 (for Mar-Apr period)
- Post-Pesach week starts April 12 (expect gradual ramp-up)
```

### Example Morning Brief (Hebrew)

```
סיכום בוקר - יום ראשון, 5.4.2026 / י״ח בניסן תשפ״ו

יום: תחילת שבוע עבודה (ראשון). יום עבודה מלא.
התראת חג: חול המועד פסח (עד 7 באפריל). רבים בחופשה - צפויות תגובות איטיות.

משימות פתוחות:
- לעקוב אחרי רבקה בנושא הצעת העיצוב (3 ימי איחור)
- לשלוח חשבונית מספר 87 ללקוח ABC בע"מ

דדליינים קרובים:
- ימי פסח אחרונים: 8-9 באפריל (סגירה מוחלטת, לתכנן מראש)
- תשלום מקדמה לביטוח לאומי עד 15 באפריל

תזכורות:
- דיווח מע"מ הבא: 15 במאי (לתקופת מרץ-אפריל)
- שבוע אחרי פסח מתחיל ב-12 באפריל (צפויה עלייה הדרגתית בפעילות)
```

---

## Hebrew Message Drafting

### Israeli Communication Norms

| Context | Tone | Opening | Example opener |
|---------|------|---------|----------------|
| Client follow-up (WhatsApp) | Direct but warm | First name | "היי [שם], מזכיר בנושא..." |
| Government office (email/letter) | Formal but not archaic | Title | "לכבוד [גוף הרלוונטי], הנדון: ..." |
| Colleague (Slack/WhatsApp) | Casual, first name | Informal | "מה קורה, יש עדכון על...?" |
| Supplier | Professional | First name or position | "שלום [שם], רציתי לבדוק..." |
| Invoice reminder | Polite but firm | First name | "היי [שם], מזכיר שחשבונית מספר X..." |
| New client intro | Friendly, professional | First name | "שלום [שם], שמחתי לדבר אתך..." |

### Anti-Patterns to Avoid

**Over-formal corporate Hebrew (sounds translated from English):**
- Instead of: "הנני מתכבד להודיעך כי..."
- Use: "רציתי לעדכן אותך ש..."

**Passive voice in WhatsApp messages:**
- Instead of: "ההודעה נשלחה על ידי..."
- Use: "שלחתי לך..."

**Overly long openings:**
- Instead of: "תחילה, אני מקווה שאתה בריא ושהכל טוב..."
- Use: "היי [שם]," (and get to the point)

**Archaic phrases:**
- Avoid: "הנני", "כבודו", "לכבוד מר/גב'"
- These are fine for official government letters but jarring in any other context

**American politeness patterns that sound odd in Hebrew:**
- Avoid: "כיצד אוכל לסייע לך היום?" (call-center Hebrew)
- Use: "במה אפשר לעזור?" or just state the matter directly

---

## Israeli Formatting Conventions

Use these formats consistently in all drafted content:

| Field | Israeli Format | NOT This |
|-------|---------------|----------|
| Date | DD/MM/YYYY or DD.MM.YYYY | MM/DD/YYYY |
| Phone (mobile) | 05X-XXX-XXXX | +9725XXXXXXXX in casual context |
| Phone (landline) | 0X-XXX-XXXX | - |
| Currency | ₪1,234.56 (symbol before amount) | 1,234.56 ₪ |
| Address | רחוב [שם] [מספר], [עיר], מיקוד [7 digits] | - |
| Business number | ח.פ. XXXXXXXXX (9 digits) | - |
| ID number | ת.ז. XXXXXXXXX (9 digits) | - |

**Date format is critical.** 03/04/2026 means April 3rd in Israel, not March 4th. Always use DD/MM/YYYY.

---

## Follow-up Sequences

### Invoice Payment Reminder Cadence

**Day 1 (due date passed) - Friendly:**
```
היי [שם],
רציתי להזכיר שחשבונית מספר [X] על סך ₪[סכום] הגיעה לפירעון.
אשמח שתסדיר בנוח.
תודה, [שמך]
```

**Day 14 - Reminder:**
```
שלום [שם],
מזכיר שוב בנוגע לחשבונית מספר [X] על סך ₪[סכום] שלא שולמה עדיין.
נשמח לקבל את התשלום בהקדם.
[שמך]
```

**Day 30 - Firm:**
```
שלום [שם],
חשבונית מספר [X] על סך ₪[סכום] עדיין לא שולמה למרות תזכורות קודמות.
אבקש לסדר את התשלום עד [תאריך] לכל המאוחר.
לפרטים נוספים, [מספר טלפון].
[שמך]
```

See `references/hebrew-communication-templates.md` for the full template library.

---

## Scheduling Intelligence

### Rules for Scheduling

1. **Shabbat cutoff:** Nothing after 13:00 on Friday (earlier for religious businesses or in cities like Bnei Brak, Jerusalem)
2. **Erev Chag:** Same rule as Erev Shabbat
3. **Motzei Shabbat:** Saturday night. Some people work Motzei Shabbat; others don't. Confirm before scheduling
4. **Chol HaMoed:** Business operates but expect partial availability. Good for internal meetings, not client-facing work
5. **August:** Israel's vacation month. Give extra lead time for any request during August
6. **National memorial days** (Yom HaShoah, Yom HaZikaron): Culturally sensitive. Entertainment and leisure events are inappropriate

### Scheduling Checklist

Before confirming any meeting or deadline, ask:
- Is this day a Jewish holiday or Erev Chag?
- Is this on a Friday (half-day)?
- Is this during Chol HaMoed (reduced availability)?
- Is the other party observant (affects Shabbat timing)?

---

## Gotchas

**1. Work week start day**

Agents default to Monday as the first workday. The Israeli work week starts **Sunday**. A "beginning of the week meeting" or "early this week" should be Sunday, not Monday. When drafting scheduling messages, always use יום ראשון for the start of the week.

**2. Date format confusion**

Agents trained on English content default to MM/DD/YYYY. Israel uses **DD/MM/YYYY**. Writing "03/04/2026" means April 3rd in Israel, not March 4th. When in doubt, write dates as "3 באפריל 2026" (spelled out) to avoid any ambiguity.

**3. Hebrew formality levels**

Agents tend to produce overly formal Hebrew that sounds like a translation from English corporate speak. Israeli business communication is direct and less formal than American English. "הנני מתכבד להודיעך" is archaic and sounds strange in any modern context outside official legal documents. Use "רציתי לעדכן אותך" instead. When in doubt, write shorter and more direct.

**4. Friday is a half-day**

Agents don't know that Friday is a shortened workday in Israel. Scheduling a "Friday afternoon meeting at 15:00" is like scheduling a Sunday meeting in the US. Use this skill to apply the Friday 13:00 cutoff rule before suggesting any Friday time slot.

**5. Holiday awareness affects planning across multiple weeks**

Agents lack context about how Jewish holidays affect business for the days around them, not just the holiday itself. Pesach, Sukkot, and the High Holiday season in Tishrei effectively compress the business calendar significantly. A deadline that falls in the week after Pesach may need to be set two weeks earlier than it appears on a calendar, because the week of Chol HaMoed will have minimal productivity.

---

## Pairing with Other Skills

| Skill | What it adds | Use together when |
|-------|-------------|-------------------|
| **shabbat-aware-scheduler** | Live calendar integration with Shabbat/holiday-aware scheduling | You need to actually create calendar events, not just plan |
| **gws-hebrew-email-automation** | Automated Hebrew email sending via Google Workspace | You want to send emails automatically, not just draft them |
| **israeli-email-sequences** | Multi-step email drip sequences for Israeli audience | You need automated follow-up campaigns |
| **accounting skills** | VAT calculation, invoice generation, financial reporting | You need numbers, not just reminders |
| **legal-tech skills** | Contract templates, legal correspondence | Formal legal documents beyond standard business letters |

---

## Bundled Resources

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/morning-brief.py` | Generates a structured morning brief with Hebrew date from HebCal API | `python3 morning-brief.py [--date YYYY-MM-DD] [--lang he\|en\|both] [--tasks "task1, task2"]` |

**Requirements:** `pip install requests python-dateutil`

### References

| File | Contents |
|------|----------|
| `references/hebrew-communication-templates.md` | Ready-to-use Hebrew message templates: invoice reminders, client communication, government correspondence, supplier messages, and team updates |
| `references/israeli-business-calendar.md` | Jewish holiday dates (5786 cycle), recurring business deadlines, VAT reporting periods, and seasonal business patterns |

---

## Troubleshooting

**The Hebrew sounds stiff or translated**
Ask your agent: "Rewrite this in more natural Israeli Hebrew, like you'd send a WhatsApp to a colleague." The agent should use shorter sentences, direct phrasing, and avoid passive constructions.

**The agent scheduled something on Shabbat or Friday afternoon**
Remind the agent of the Israeli work week rules: Sunday-Thursday full days, Friday until 13:00, Saturday no business. If using a calendar integration, pair with shabbat-aware-scheduler.

**The morning brief doesn't include Hebrew dates**
Ask explicitly: "Include the Hebrew date (e.g., י״ח בניסן תשפ״ו) alongside the Gregorian date." You can also use the `scripts/morning-brief.py` script which fetches Hebrew dates from HebCal automatically.

**Holiday dates are wrong or missing**
Jewish holiday dates shift every year based on the Hebrew calendar. Ask your agent to fetch the current year's dates from HebCal (https://www.hebcal.com) or use the `scripts/morning-brief.py` script which calls the HebCal API.

---

## References

- HebCal Hebrew calendar API: https://www.hebcal.com/home/195/jewish-calendar-rest-api
- Israel Tax Authority (רשות המיסים): https://www.gov.il/he/departments/israel_tax_authority
- National Insurance Institute (ביטוח לאומי): https://www.btl.gov.il
- `references/hebrew-communication-templates.md` - Full Hebrew message template library
- `references/israeli-business-calendar.md` - Key dates and seasonal patterns