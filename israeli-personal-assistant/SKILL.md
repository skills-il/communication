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

Israel observes a single day of yom tov per holiday side, not the diaspora two-day pattern. This matters: the skill schedules around the Israeli calendar, not the global Jewish calendar.

| Holiday | Duration in Israel | Business Impact |
|---------|--------------------|-----------------|
| Yom Kippur | 1 day | Complete shutdown. Even secular Israelis don't work |
| Rosh Hashana | 2 days | Full shutdown, most take additional days |
| Sukkot | 1 day yom tov + 6 days Chol HaMoed + 1 day Shmini Atzeret/Simchat Torah (combined) | Full shutdown on first day and on Shmini Atzeret; Chol HaMoed is partial. The last Chol HaMoed day, Hoshana Raba, is a short day (eve of Shmini Atzeret) |
| Pesach | 1 day yom tov + 5 days Chol HaMoed + 1 day yom tov (7 days total in Israel) | Full shutdown on first and last days; Chol HaMoed is partial |
| Shavuot | 1 day | Full shutdown |
| Purim | 1 day (Shushan Purim is the day after, and is the one observed in Jerusalem) | Many take the day off; expect slow responses |
| Iron Swords Memorial Day (יום הזיכרון לחללי מלחמת חרבות ברזל) | 1 day (fixed at 24 Tishrei, moved to Sunday 25 Tishrei if it falls on Shabbat) | National observance. Two state ceremonies, 11:00 (fallen soldiers) and 13:00 (murdered civilians). Avoid entertainment events. Established by a government decision of 17 March 2024 (a cabinet decision, not a Knesset law) |

**Chol HaMoed note:** Businesses technically operate during Chol HaMoed (intermediate days of Sukkot and Pesach), but many employees are on vacation. Expect 30-50% slower response times and limited availability.

**August:** Israeli summer vacation season. Many families travel. Expect slower response rates throughout the month, especially during the last two weeks.

### National Observances (Working Days with Cultural Weight)

These are working days, but communication tone and event scheduling should respect them.

**Take the Gregorian dates from `references/israeli-business-calendar.md`, which carries the current cycle. Do not state a Gregorian date from memory.**

| Observance | Hebrew date | What to Avoid |
|------------|-------------|---------------|
| Yom HaShoah (יום השואה) | 27 Nisan | Entertainment, sales pitches, jokes. A national siren sounds in the morning |
| Yom HaZikaron (יום הזיכרון) | 4 Iyar | Entertainment, parties, ad campaigns. Two national sirens, one the preceding evening and one the following morning |
| Yom HaAtzmaut (יום העצמאות) | 5 Iyar | NOT a working day: a full national holiday, most businesses closed. Yom HaZikaron flips to celebration at sunset the evening before. Do not schedule client work or deadlines on it |
| Yom Yerushalayim (יום ירושלים) | 28 Iyar | Mostly Jerusalem-focused; expect road closures and a parade in the city |

**These four do NOT convert straight from the Hebrew date.** Yom HaShoah, Yom HaZikaron and Yom HaAtzmaut are advanced or postponed by law in years where the nominal date would fall next to Shabbat, so deriving the Gregorian date from the Hebrew one gives the wrong answer in those years. Always read them off the reference table or a dated source, never by conversion.

### Key Business Obligation Dates

| Obligation | Frequency | Window |
|------------|-----------|--------|
| VAT (מע"מ) reporting and payment | Bi-monthly (annual turnover up to ₪1,775,000 in 2026, rising to ₪1,805,000 on 1 Jan 2027) or monthly (above) | 15th of the month following the reporting period, or the **19th at 18:30** when filing online through the Tax Authority site |
| Bituach Leumi (NII) contributions, self-employed | Monthly | Per the payment-voucher schedule Bituach Leumi sends. A standing-order bank debit is taken on the **22nd, for the previous month** (the date shifts around Shabbat and holidays). Not the 15th |
| Income tax advance (מקדמות) | Monthly (bi-monthly only with an approval recorded in פנקס המקדמות) | 15th, or the **19th at 18:30** when paying online |
| Annual tax return (עצמאים) | Annual | Typically April-May (check current year deadline) |
| Annual turnover declaration, עוסק פטור | Annual | **31 January**, for the previous calendar year. This date is deferred in emergencies too: the 2025 declaration could be filed until 30.04.2026 |

**Two qualifiers that move the 15th, and that agents routinely miss:**

- **Filing online buys four days, for most but not all filers.** The extension applies to a business that files the periodic report online AND is not obliged to submit a דיווח מפורט (detailed report); for it, the operative deadline for VAT and מקדמות is the 19th at 18:30. A business under the detailed-report obligation does not get the 19th, and neither does anyone filing on paper or at a bank counter. Check which of the two the user is before quoting the later date.
- **The 15th shifts off a rest day.** When the 15th falls on the business owner's weekly rest day, reporting and payment move to the next business day.

**Deadlines move in emergencies, and a reminder that cannot represent that is wrong.** The Tax Authority repeatedly defers filing and payment dates during wars, security operations and around holidays. In 2026 the February monthly report and the Jan-Feb bi-monthly report were both pushed to 26.03.2026, and March reports filed by 29.04.2026 drew no penalty or interest. Never present a monthly date as certain during an active emergency: check the Tax Authority's announcements page for the current period before telling the user a date. Reserve-duty (מילואים) service can also earn an individual extension.

**Not every self-employed person is on the monthly cycle, and the two statuses are independent axes, not one ladder.** עוסק פטור is a VAT status; עסק זעיר is an income-tax status. A business can be either, both or neither, and an עוסק מורשה can also be an עסק זעיר.

| Status | Axis | 2026 turnover ceiling | What it changes |
|--------|------|----------------------|-----------------|
| עוסק פטור | VAT | ₪122,833 | Charges no VAT and cannot reclaim input VAT. Issues a חשבונית עסקה plus a receipt, never a חשבונית מס. No periodic VAT report; one annual turnover declaration by 31 January |
| עסק זעיר | Income tax | ₪122,833 | Automatic flat 30% expense deduction, short-form annual return, and in most cases no income-tax advances |

Two traps before you accept a user's self-reported status:

- **Some professions may never be an עוסק פטור, whatever their turnover.** Under regulation 13 of תקנות מס ערך מוסף (רישום) the list includes עורך דין, רואה חשבון, יועץ מס, מנהל חשבונות, כלכלן, מהנדס, אדריכל, הנדסאי, טכנאי, יועץ לניהול, יועץ לארגון, מודד, שמאי, רופא, רופא שיניים, פסיכולוג, פיזיותרפיסט, וטרינר, מתורגמן, חוקר פרטי and טוען רבני. Several of those are exactly this skill's audience.
- **עסק זעיר has disqualifiers that bite below the ceiling.** It does not apply if the business employs workers, does not keep acceptable books, had income in the tax year that was not from personal exertion (הכנסה שלא מיגיעה אישית), or drew part of its income from its own employer or from a תאגיד שקוף. "Employs workers" rules out a large share of small business owners.

Ask which status the user holds, then check it against both traps, before you generate any reminder schedule.

**Standard VAT rate (2026): 18%** (raised from 17% on Jan 1, 2025; the 2026 budget kept it at 18%).

**חשבוניות ישראל / Allocation Number regime:** As of **Jan 1, 2026**, business invoices above ₪10,000 (ex-VAT) require an Allocation Number (מספר הקצאה) generated in real time by the Tax Authority, or the buyer cannot reclaim VAT. The threshold drops to **₪5,000 from Jun 1, 2026**. Most accounting software (Green Invoice, iCount, Hashavshevet) handles allocation requests automatically. This is the single biggest 2024-2026 change for Israeli freelancers issuing invoices to businesses.

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

### Example Morning Brief

**English:**

```
Morning Brief - Sunday, April 5, 2026 / י״ח בניסן תשפ״ו

Day: Start of work week (Sunday). Full workday.
Holiday alert: Pesach Chol HaMoed (through April 7). Many contacts may be on vacation - expect slower responses.

Open tasks:
- Follow up with Rivka on the design proposal (3 days overdue)
- Send invoice #87 to client ABC Ltd.

Upcoming deadlines:
- Pesach last day (Shvi'i, yom tov): April 8 (full shutdown); April 7 is erev (short day). April 9 is Isru Chag, a normal workday in Israel
- Bituach Leumi standing-order debit on April 22, for March

Reminders:
- Next VAT deadline: May 15 (for Mar-Apr period)
- Post-Pesach week starts April 12 (expect gradual ramp-up)
```

**Hebrew:**

```
סיכום בוקר - יום ראשון, 5.4.2026 / י״ח בניסן תשפ״ו

יום: תחילת שבוע עבודה (ראשון). יום עבודה מלא.
התראת חג: חול המועד פסח (עד 7 באפריל). רבים בחופשה - צפויות תגובות איטיות.

משימות פתוחות:
- לעקוב אחרי רבקה בנושא הצעת העיצוב (3 ימי איחור)
- לשלוח חשבונית מספר 87 ללקוח ABC בע"מ

דדליינים קרובים:
- יום פסח אחרון (שביעי של פסח, יום טוב): 8 באפריל (סגירה מוחלטת); 7 באפריל ערב החג (יום קצר). 9 באפריל הוא איסרו חג, יום עבודה רגיל בישראל
- חיוב הוראת הקבע לביטוח לאומי ב-22 באפריל, עבור מרץ

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

**Before drafting a firm reminder, note that Israeli law already sets the deadline.** חוק מוסר תשלומים לספקים, התשע"ז-2017 fixes maximum payment terms for supply of goods and services, and those terms cannot be pushed out by agreement, even if the supplier consented. Late payment carries linkage differences and interest by operation of law. This changes the tone available to the user: they are asking for something the law already gives them, not requesting a favour. Do not draft a demand letter or advise on enforcement, and point the user to a lawyer or to the legal-tech skills for anything beyond a business reminder.

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

**6. Diaspora holiday feeds silently break Israeli scheduling**

Every general Jewish-calendar source defaults to the DIASPORA scheme, which adds a second yom tov to Rosh Hashana's neighbours, Sukkot, Shmini Atzeret/Simchat Torah, Pesach and Shavuot. Loaded into an Israeli plan, that marks working Chol HaMoed days as full shutdowns and gets the last day of Pesach wrong. When fetching from HebCal, always pass `i=on` (the site equivalent is `https://www.hebcal.com/?i=on`); the bundled script sets it. If a date came from anywhere else, check that Sukkot day 2 shows as Chol HaMoed and that Pesach closes after seven days, not eight.

**7. The "15th of the month" shortcut is wrong for most of this skill's audience**

Agents compress Israeli business obligations into "everything is due on the 15th". Three separate things break that: online filers get until the 19th at 18:30, Bituach Leumi standing orders debit on the 22nd, and an עוסק פטור has no monthly cycle at all. Ask which filing status and filing method the user has before generating any reminder.

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

**Which hosts can run the script, and what the others do instead.** The script is a convenience, never the only route: every capability in this skill is reachable without it. Check the row for the host you are running on before telling a user to run anything.

| Host | Can run `python3 scripts/morning-brief.py`? | Route to use |
|------|--------------------------------------------|--------------|
| claude-code, cursor, windsurf, gemini-cli, openclaw | Yes | Run the script, or use the no-script route if dependencies are unavailable |
| claude-desktop | No (no shell) | No-script route. A locally-installed MCP calendar server can supply dates if the user has one |
| claude-ai, chatgpt | No (no shell, no local process) | No-script route only |

**No-script route (works on every host):** build the brief from the sections above by hand. Take the coming holidays and their Gregorian dates from `references/israeli-business-calendar.md`, then apply the Brief Structure below, the short-day rules and the obligation windows. Never tell a user on a host in the "No" rows to run the script or install a package.

**The Hebrew date is the one part the no-script route cannot always supply.** The bundled reference lists holidays, not a day-by-day Hebrew-date table, and Hebrew dates cannot be derived reliably without a converter. So:

1. If the host can browse, convert it at `https://www.hebcal.com/converter?cfg=json&gy=2026&gm=4&gd=5&g2h=1 (substituting the target year, month and day)` and read the `hebrew` field.
2. If it cannot, **omit the Hebrew date and say so** ("Hebrew date unavailable without a converter"). Give the Gregorian date, the day of the week and everything else in the brief.

Never estimate or reconstruct a Hebrew date from memory. Hebrew months do not map to Gregorian months at a fixed offset and the year boundary moves, so a guessed Hebrew date is wrong far more often than it is right, and a wrong one is worse than an absent one.

### References

| File | Contents |
|------|----------|
| `references/hebrew-communication-templates.md` | Ready-to-use Hebrew message templates: invoice reminders, client communication, government correspondence, supplier messages, and team updates |
| `references/israeli-business-calendar.md` | Jewish holiday dates (5787 cycle, Israel scheme), recurring business deadlines, VAT reporting periods, and seasonal business patterns |

---

## Troubleshooting

**The Hebrew sounds stiff or translated**
Ask your agent: "Rewrite this in more natural Israeli Hebrew, like you'd send a WhatsApp to a colleague." The agent should use shorter sentences, direct phrasing, and avoid passive constructions.

**The agent scheduled something on Shabbat or Friday afternoon**
Remind the agent of the Israeli work week rules: Sunday-Thursday full days, Friday until 13:00, Saturday no business. If using a calendar integration, pair with shabbat-aware-scheduler.

**The morning brief doesn't include Hebrew dates**
Ask explicitly: "Include the Hebrew date (e.g., י״ח בניסן תשפ״ו) alongside the Gregorian date." On a host that can run scripts, `scripts/morning-brief.py` fetches the Hebrew date from HebCal automatically. On claude.ai, ChatGPT or Claude Desktop, use the no-script route in Bundled Resources: convert it through HebCal if the host can browse, and otherwise omit the Hebrew date explicitly rather than guessing it.

**Holiday dates are wrong or missing**
Jewish holiday dates shift every year based on the Hebrew calendar. Read them off `references/israeli-business-calendar.md`, which is the route that works on every host. On a shell-capable host, `scripts/morning-brief.py` fetches them live. If pulling from HebCal directly, pass the Israel scheme (`i=on`) or you will get diaspora dates. Note that HebCal does not return Iron Swords Memorial Day in any category, so that observance always has to come from the reference file or the script's built-in table.

---

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| HebCal Hebrew Calendar API | https://www.hebcal.com/home/195/jewish-calendar-rest-api | Hebrew date conversion, holiday dates, API parameters |
| Israel Tax Authority (רשות המיסים) | https://www.gov.il/he/departments/israel_tax_authority | VAT reporting deadlines, tax return filing dates |
| National Insurance Institute (ביטוח לאומי) | https://www.btl.gov.il/pages/benefitspaymentdates.aspx | Bituach Leumi advance payment dates, self-employed obligations |
| Kol Zchut: income-tax advances (מקדמות) | https://www.kolzchut.org.il/he/תשלום_מקדמות_של_עסק_עצמאי_למס_הכנסה | The 15th vs the online 19th 18:30 deadline, rest-day shift, current emergency deferrals |
| Kol Zchut: Bituach Leumi for the self-employed | https://www.kolzchut.org.il/he/דמי_ביטוח_לאומי_לעצמאי | Payment methods and the 22nd standing-order debit date |
| Kol Zchut: VAT periodic reporting | https://www.kolzchut.org.il/he/הגשת_דו%22חות_תקופתיים_ותשלום_מס_ערך_מוסף | VAT rate, the bi-monthly turnover threshold and its annual update |
| Prime Minister's Office: Iron Swords Memorial Day decision | https://www.gov.il/he/pages/spoke-memorial170324 | The 17 March 2024 cabinet decision, the 24 Tishrei date and the ceremony times |
| `references/hebrew-communication-templates.md` | Bundled | Full Hebrew message template library |
| `references/israeli-business-calendar.md` | Bundled | Holiday dates (5787 cycle, Israel scheme), seasonal business patterns |