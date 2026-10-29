# Compliance and security for an Israeli business bot

Detail behind SKILL.md Phase 1 (token), Phase 5 (deposits), and Phase 8 (spam and privacy). Each
section names the statute it rests on. These are working summaries for a business owner, not a
substitute for advice on a specific policy: where a section says "check", it means the point is
not settled by the text alone.

## 1. The bot token

The token is the bot's password. Whoever holds it can send as the bot, read what customers send it,
and change its webhook.

**Where it may go:** a password manager, and the token field of the one no-code platform that runs
the bot. **Where it must not go:**

- a chat with an AI assistant. If the owner pastes it "so you can set it up", tell them to rotate
  it with `/token` afterwards, and do not repeat it back in your reply;
- a notes app, a WhatsApp-to-self message, an email, or a shared spreadsheet;
- a screenshot or screen share of the @BotFather chat or the platform's credentials screen (the
  most common real leak is a setup screenshot sent to a support desk);
- a browser address bar. A call typed as `https://api.telegram.org/bot<token>/<method>` stays in
  browser history and in any synced history. Prefer the platform's own "disconnect" or
  "reconnect" button. If you did use the address bar, rotate the token afterwards.

**Self-hosted webhooks (for example self-hosted n8n):** set a secret when registering the
webhook. Telegram then sends it back on every call in the `X-Telegram-Bot-Api-Secret-Token`
header, and the server should reject any request without it. Cloud no-code platforms handle this
themselves.

**If the token leaked:**

1. In @BotFather send `/token` and pick the bot. This generates a new token; the old one stops
   working.
2. Put the new token into the platform and confirm the bot answers.
3. Re-check everything someone holding the old token could have changed: the bot's name,
   description, about text, command list, the menu button and any Mini App URL. Repoint the
   webhook from the platform (do not assume it is still yours).
4. If customers may have received messages you did not send, tell them in the bot not to act on
   them.
5. The bot's customer list is a database (section 4). Check with the Privacy Protection
   Authority's guidance whether the leak is a security incident you must document or report.

Telegram gives the owner no log of messages the bot sent, so "check what was sent" is usually not
possible; the steps above are what can actually be done.

## 2. Deposits (מקדמה) and cancellation

### Collecting the deposit

- Send a payment link per booking, carrying the booking reference, and hold the slot only once the
  payment is confirmed. Release it automatically if the link is not paid within the window you
  chose.
- A deposit is a payment received, so it needs a receipt like any other payment (see SKILL.md
  Phase 7, "You still have to issue a real invoice"). A provider that issues the document with the
  payment does this in one step.
- Refunds go through the provider's dashboard. Telegram's own `refundStarPayment` refunds only
  Stars, which do not apply to an in-person service.
- For a card hold charged only on a no-show, ask the provider whether its payment links support it.
  Do not promise customers a hold model the provider has not confirmed.

### The consumer-law constraint

A booking made through the bot, with no face-to-face meeting, is likely a distance transaction
(עסקת מכר מרחוק) under s.14ג of חוק הגנת הצרכן, התשמ"א-1981. The statute defines it as a sale of
goods or a service "ללא נוכחות משותפת של הצדדים לעסקה", following distance marketing that
expressly includes electronic communication of any kind. Whether a booking the CUSTOMER started is
"distance marketing" is a reading of the text; treat it as covered.

**The basic rule for a one-off service (a haircut, a consultation).** The customer may cancel when
BOTH hold (s.14ג(ג)(2)):

1. the cancellation is within 14 days of the booking, or of receiving the written details in
   s.14ג(ב), whichever is LATER (`בתוך ארבעה עשר ימים מיום עשיית העסקה או מיום קבלת המסמך`); and
2. it is made at least two days that are not rest days before the appointment (`בתנאי שביטול כאמור
   ייעשה לפחות שני ימים, שאינם ימי מנוחה, קודם למועד שבו אמור השירות להינתן`).

Then the business refunds within 14 days of the notice and may keep at most **5% of the FULL price
of the service, or ₪100, whichever is lower** (s.14ה(ב)(1)). The base is the price, not the
deposit:

| Booking | Cancelled | Business may keep | Refund |
|---|---|---|---|
| Haircut ₪120, deposit ₪50 | 3 non-rest days ahead, inside 14 days | ₪6 (5% of 120) | ₪44 |
| Colour ₪2,500, deposit ₪500 | 3 non-rest days ahead, inside 14 days | ₪100 (the cap) | ₪400 |
| Haircut ₪120, deposit ₪50 | the evening before | no statutory right; the disclosed terms decide | per the terms |

Outside either condition (the evening before, or more than 14 days after a booking whose written
details were sent), the statutory right does not apply and the business's own disclosed terms
govern. A late-cancellation or no-show charge must be disclosed before booking and be
proportionate; disclosure is necessary but not sufficient, so get the wording reviewed. Sending the
written details in the booking confirmation is what starts the 14-day clock; a bot that never sends
them leaves the window open until two non-rest days before the appointment.

**Rest days.** The statute counts days that are not rest days (Shabbat and Jewish holidays at
least), not the business's working days. Do not reuse the business's "closed day" setting for this
count; when unsure, count conservatively in the customer's favour.

**Cases that follow different rules:**

- **The business caused the cancellation** (moved or missed the appointment, gave wrong details):
  full refund and no fee at all (s.14ה(א)).
- **Leisure and hospitality** (`שירותי הארחה, נסיעה, חופש או בילוי`, for example a zimmer, a tour,
  an event night): the distance-cancellation right does not apply to a cancellation inside seven
  non-rest days before the service (s.14ג(ד)(2)). A restaurant event booking is arguably here; a
  haircut is not.
- **Packages and memberships** (10 sessions, a monthly plan): a continuing transaction may be
  cancelled within 14 days whether or not it has begun; the customer pays for the sessions already
  used, plus at most the 5% / ₪100 fee (s.14ג(ג)(2), s.14ה(ב1)).
- **Cosmetic and aesthetic treatments** (`שירותי קוסמטיקה ואסתטיקה`, including hair removal) are
  also listed in תקנות הגנת הצרכן (ביטול עסקה), התשע"א-2010, which give a cancellation right within
  14 days of the booking or the written contract, "בין אם הוחל במתן השירות ובין אם לא", whatever
  the channel, with the same 5% / ₪100 fee cap (plus a proven card-clearing fee) and a refund within
  7 business days (regs 4-5). There is NO two-day condition, so for these treatments the
  customer-facing terms must not say "at least two days before" (use the cosmetic variant in
  Template 2). It matters most for treatment series and hair-removal packages; for a one-off
  treatment already given, get the policy reviewed rather than assume a refund. Whether a plain
  haircut counts as aesthetics is unsettled; assume the customer may rely on the more favourable
  rule. The same Regulations also give leisure services, classes and gym or spa memberships their
  own windows.
- **Seniors (65+), people with disabilities and new immigrants** get four months instead of 14 days
  where the transaction included a conversation, "ובכלל זה שיחה באמצעות תקשורת אלקטרונית"
  (s.14ג1(ג)). A fully automated bot flow is probably not a conversation; a booking where staff
  typed replies in the chat may be.

**Disclose before the booking is made** (s.14ג(א)): the business name, ID number (ח.פ. / ע.מ.) and
address, the service, the price and payment terms, the date and place, how long the offer (a held
slot) stands, and the customer's STATUTORY cancellation right, alongside your own late-cancellation
terms. **Then send in writing**, no later than the service (s.14ג(ב)): the business and service
details, the price and payment terms, how to cancel, and any other terms. The booking confirmation
is the natural place. A policy more generous than the statute ("free cancellation up to 4 hours
before") is fine; say it there.

**Paperwork on a refund.** If a receipt or invoice was issued for the deposit, issue the matching
credit document from the same invoicing system when you refund it.

## 3. Spam law (s.30a): the existing-customer route

The four requirements and the compliant promotion template are in
`references/business-bot-templates.md` ("Broadcast message shapes" and "Section 30a requirements
in full"). Two points that sit next to them:

**Prior consent is not the only lawful route.** s.30a(ג) allows a promotion without consent when
ALL of these hold:

1. the customer gave their details during a purchase of a product or service (or negotiating one),
   and the business told them then that the details would be used to send it advertising;
2. the business gave them a chance to refuse, and they did not;
3. the promotion is for a product or service of a similar kind.

For a bot this means: at the first booking, say in the same message that you may send offers on
similar services and give a "לא, תודה" button. Record that this was shown and what the customer
pressed, the same way you record consent. If you take this route, the privacy notice in section 4
must name marketing as a purpose too (use its optional line). The פרסומת label, the sender details
and the opt-out in every message still apply, and the customer may refuse at any time
(s.30a(ד)(1), "בכל עת").

**What counts as a promotion.** A reminder about an appointment the customer booked is
transactional. A "book again" nudge after a no-show, a win-back message, or a review request is
not: it encourages a new purchase, so treat it as a promotion.

**Penalties, stated accurately.** Statutory damages are up to ₪1,000 per advertisement received,
without proof of damage. The damages clause speaks of sending "ביודעין" (knowingly), with a
presumption that a sender who breached the section did so knowingly. The criminal offence is a
fine under the Penal Law and its text has no "knowingly" element.

## 4. Privacy (Privacy Protection Law, as amended by Amendment 13)

### Is the bot's customer list a database?

Yes, in practice. The statute's "מאגר מידע" excludes only a collection holding nothing but
names, addresses and contact details for up to 100,000 people that reveals nothing more about
them. A booking or order history does reveal more, so a bot table of that shape is a database.

### What a typical salon or cafe bot does NOT need

- **Registration.** After Amendment 13 the registration duty applies to public bodies and to
  databases whose main purpose is passing personal data to others as a business, including direct
  mail services, with more than 10,000 people (s.8א). A business keeping its own customers is
  normally neither.
- **A privacy officer (ממונה על הגנת הפרטיות).** Required of public bodies, the same
  data-trading databases, and bodies whose main activity is large-scale systematic monitoring or
  large-scale processing of especially sensitive data (s.17ב1). Again, not a typical SMB.

A clinic, therapist or dietitian bot that stores health information is different: health data is
especially sensitive, which can raise the security level (see Security below) and brings the
professional-secrecy rules of that profession. Get that case reviewed.

### What it DOES need

**A notice when collecting (s.11).** The first message that asks for a name or phone number is a
request for personal data, so it must say: the purpose; the owner's name and contact details;
whether the customer must give the data or it is their choice, and what happens if they decline;
who the data is passed to and why; and that the customer may ask to see and correct it (ss.13-14).
A short form for the bot:

```
כדי לקבוע תור נשמור את השם ופרטי התור שלך, לצורך ניהול התורים והתזכורות כאן בצ'אט.
[אופציונלי, רק אם תשלחו הצעות, יחד עם הכפתור "בלי הצעות": נשתמש בפרטים גם כדי לשלוח לך הצעות על שירותים דומים, אפשר לסרב עכשיו או בכל עת.]
מסירת הפרטים בבחירתך, בלי שם לא נוכל לקבוע את התור.
הפרטים נשמרים אצל [שם העסק], [טלפון / מייל], עוברים דרך טלגרם ונשמרים בפלטפורמת [שם הפלטפורמה] שמפעילה את הבוט.
אפשר לבקש לראות את הפרטים או לתקן אותם בכל עת: /mydata
[✅ מאשר/ת] [🚫 בלי הצעות (רק עם השורה האופציונלית)] [❌ ביטול]
```

Collect only what the bot uses. The reminders run inside the Telegram chat, so a phone number is
not needed for them; ask for one only if you really call or text customers, and say so.

Note that /mydata is a command you define on your own bot and must actually handle (send the
customer what is stored, and a way to correct it). Add it to the `/setcommands` list. Since
Amendment 13 a court may award exemplary damages of up to ₪10,000 without proof of harm for, among
other things, collecting data without this notice (after a demand and 30 days) or refusing access
(s.15א).

**Security (Privacy Protection (Data Security) Regulations, 2017).** Amendment 13 attached
administrative fines to breaches of these Regulations, scaled by security level (Privacy Protection
Law, Third Schedule: `עיצום כספי על הפרת תקנות אבטחת מידע`). As defined there:

- the lightest regime, a database run by an individual (or a company owned by one or two
  individuals) used by at most two other authorised people, excludes a database with 10,000 people
  or more and one holding information under professional secrecy (so an accountant's, lawyer's or
  therapist's client list never qualifies);
- the basic level covers an ordinary business database that is not a data-trading database or a
  public body; if it holds especially sensitive data (health, for example), it stays basic only if
  at most ten people have access, and otherwise moves to the medium level.

Whatever the level, data sent over the internet must be encrypted (`העברת מידע
ממאגר המידע, ברשת ציבורית או באינטרנט, תיעשה תוך שימוש בשיטות הצפנה מקובלות`), which in practice
means HTTPS everywhere and no customer data in plain spreadsheets shared by link. Keep the list of
who has access short, and remove staff who leave.

**Keep only what you use.** Decide how long booking history and no-show flags stay, and delete
old records on that schedule. No fixed period is set for this here; pick one you can justify.

### Direct mail (דיוור ישיר, s.17ו)

Separate from the spam law. Direct mail is a personal approach to someone based on their belonging
to a group defined by one or more characteristics of the people in a database. Every direct-mail
approach must state clearly that it is direct mail (with the registration number of the database
used for direct-mail services, where there is one), tell the recipient of their right to be deleted
and the address to ask at, and name the database owner and where the data came from. A written
deletion demand must be acted on and confirmed in writing; if the owner does not confirm within
30 days, the person may go to the Magistrates' Court.

Whether a promotion to a SEGMENT of the bot's own customers ("everyone who had a colour treatment
last spring") is direct mail is not settled by the text. A promotion sent to all subscribers is the
safer pattern; if you segment, add the 17ו elements as well as the s.30a ones. Note that s.17ג was
repealed, so the operative provisions are ss.17ד-17ו.

### Customer data held abroad

Hosting the bot on a non-Israeli platform moves the data out of Israel, and every message also
passes through Telegram. Under the Privacy Protection (Transfer of Data to Databases Abroad)
Regulations, 2001, a transfer is allowed where, among other grounds, the customer consented
(`האדם שעליו המידע הסכים להעברה`), or the recipient undertook by contract to keep the conditions
that apply to a database in Israel. Separately, the owner must secure a WRITTEN undertaking from
the recipient that it protects the data and will not pass it on (reg 3). In practice: read the
platform's data-processing terms (they usually contain such an undertaking) before putting real
customer records into it, and name Telegram and the platform in the collection notice above.

## Sources

- Consumer Protection Law, ss.14ג, 14ג1 and 14ה: `he.wikisource.org`, חוק הגנת הצרכן
- Consumer Protection (Cancellation of Transaction) Regulations 2010: `he.wikisource.org`, תקנות הגנת הצרכן (ביטול עסקה)
- Communications Law s.30a: `nevo.co.il/law_html/law01/032_002.htm`
- Privacy Protection Law (ss.7, 8א, 11, 17ב1, 17ו): `he.wikisource.org`, חוק הגנת הפרטיות
- Data Security Regulations 2017 and Transfer Abroad Regulations 2001: `he.wikisource.org`
- Webhook secret token: `core.telegram.org/bots/api#setwebhook`
- Token regeneration: `core.telegram.org/bots/features`
