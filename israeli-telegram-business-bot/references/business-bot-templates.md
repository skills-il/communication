# Israeli Business Bot Templates

Complete message flow templates for common Israeli business types. Copy and adapt these for your Telegram bot.

**Three screens in every booking flow are mandatory, not decorative:** the privacy notice before
the first name is taken (`references/compliance-and-security.md` section 4), the price and
cancellation terms shown BEFORE the customer confirms, and a confirmation that carries the business
details and cancellation terms in writing (section 2). Template 2 shows all three; add the same to
the other templates.

## Template 1: Restaurant / Cafe Bot

### Welcome Flow

```
שלום! ☀️
ברוכים הבאים ל[שם המסעדה].

מה בא לכם?
```

**Inline keyboard:**
```
[📋 תפריט] [🛒 הזמנה לטייקאווי]
[📅 הזמנת שולחן] [🕐 שעות פעילות]
[📍 איך מגיעים] [📞 צרו קשר]
```

### Menu Categories

```
📋 התפריט שלנו:

[☕ קפה ושתייה חמה]
[🥤 שתייה קרה ומיצים]
[🥐 ארוחות בוקר]
[🥗 סלטים וצהריים]
[🍝 מנות עיקריות]
[🍰 קינוחים]
[⬅️ חזרה לתפריט הראשי]
```

### Sample Category: Breakfast

```
🥐 ארוחות בוקר (מוגש עד 12:00):

🥚 ישראלית קלאסית - ₪52
שקשוקה / ביצים, סלט ישראלי, לחם, ממרחים, קפה

🧀 בוקר גבינות - ₪58
מבחר גבינות, סלט, לחם, ריבה, חמאה, קפה

🥑 בוקר בריאות - ₪55
גרנולה, יוגורט, פירות, אבוקדו, לחם כוסמין, מיץ

🍳 אומלט שף - ₪48
אומלט במילוי לבחירה, לחם, סלט, קפה

[הוסף לסל: ישראלית] [הוסף לסל: גבינות]
[הוסף לסל: בריאות] [הוסף לסל: אומלט]
[⬅️ חזרה לקטגוריות]
```

### Table Reservation Flow

Insert before the name is asked: [מסך הודעת פרטיות, `references/compliance-and-security.md` section 4]. Insert before the customer confirms: [סיכום מחיר, פרטי העסק ותנאי ביטול, כמו ב-Template 2]. The confirmation must repeat the business details and the cancellation terms.

```
📅 הזמנת שולחן

לכמה סועדים?
[1-2] [3-4] [5-6] [7+]
```

Date selection:
```
באיזה תאריך?

[היום - ראשון 2/4]
[מחר - שני 3/4]
[שלישי 4/4]
[רביעי 5/4]
[חמישי 6/4]
[שישי 7/4 (עד 15:00)]
[⬅️ חזרה]
```

Time selection:
```
באיזו שעה?

ארוחות בוקר:
[08:00] [09:00] [10:00] [11:00]

ארוחות צהריים:
[12:00] [13:00] [14:00]

ארוחות ערב:
[18:00] [19:00] [20:00] [21:00]

[⬅️ חזרה]
```

Confirmation:
```
✅ השולחן שמור!

מסעדה: [שם המסעדה]
תאריך: יום שני, 3 באפריל
שעה: 19:00
סועדים: 4
שם: [שם הלקוח]

📍 [כתובת], [עיר]
📞 במקרה של שינוי: 03-XXX-XXXX

נשלח תזכורת ביום ההזמנה.
לביטול: /cancel
```

### Takeout Order Flow

```
🛒 הזמנה לטייקאווי

בחרו מהתפריט:
[🥐 ארוחות בוקר] [🥗 סלטים]
[🍝 מנות עיקריות] [🍰 קינוחים]
[☕ שתייה]
```

Cart summary:
```
🛒 סיכום ההזמנה:

1x ארוחת בוקר ישראלית - ₪52
1x קפה הפוך גדול - ₪16
1x עוגת שוקולד - ₪28

סה"כ: ₪96

מתי תרצו לאסוף?
[עוד 20 דק'] [עוד 30 דק'] [עוד 45 דק'] [עוד שעה]
```

Order confirmed:
```
✅ ההזמנה התקבלה!

מספר הזמנה: #2847
סה"כ: ₪96
איסוף: 10:30

📍 [כתובת]

💳 לתשלום:
[💳 כרטיס אשראי] [📱 ביט]
[💵 מזומן באיסוף]

לסטטוס: /status
```

### Business Hours Message

```
🕐 שעות פעילות:

ראשון - חמישי: 07:30 - 23:00
שישי: 07:30 - 15:00
שבת: סגור

🍳 ארוחות בוקר: עד 12:00
🥗 ארוחות צהריים: 12:00 - 16:00
🍽 ארוחות ערב: 18:00 - 22:30
(מטבח סוגר חצי שעה לפני)

📍 [כתובת], [עיר]
🗺 לניווט: [Google Maps link]
🅿️ חניה: חניון [שם] ברחוב [שם], 2 דקות הליכה

[📅 הזמנת שולחן] [⬅️ חזרה]
```

### After-Hours Auto-Replies

Weekday evening:
```
היי! 🌙
המטבח סגור כרגע.
אנחנו פתוחים מחר מ-07:30.

בינתיים:
[📋 תפריט] [📅 הזמנת שולחן למחר]
```

Friday afternoon:
```
שבת שלום! 🕯
סגרנו להיום.
נפתח ביום ראשון ב-07:30.

[📋 תפריט] [📅 הזמנת שולחן לראשון]
```

---

## Template 2: Hair Salon / Beauty Bot

### Welcome Flow

```
היי! 💇‍♀️
ברוכים הבאים ל[שם הסלון].

[📅 קביעת תור]
[💰 מחירון]
[📸 עבודות אחרונות]
[🕐 שעות פעילות]
[📍 מיקום וחניה]
[📞 צרו קשר]
```

### Service Menu with Prices

```
💇 השירותים שלנו:

תספורות:
[💇‍♀️ תספורת נשים - מ-₪120]
[💇‍♂️ תספורת גברים - ₪80]
[👦 תספורת ילדים - ₪60]

צבע ועיצוב:
[🎨 צבע מלא - מ-₪250]
[✨ גוונים/הבלטות - מ-₪300]
[💫 החלקה - מ-₪400]

טיפולים:
[💆‍♀️ טיפול פנים - ₪180]
[💅 מניקור - ₪90]
[💅 פדיקור - ₪110]
[💅 מניקור + פדיקור - ₪170]

[⬅️ חזרה לתפריט הראשי]
```

### Booking Flow: Service Selection

```
📅 קביעת תור

מה תרצו לעשות?
[💇‍♀️ תספורת] [🎨 צבע]
[💆‍♀️ טיפול פנים] [💅 ציפורניים]
[✨ חבילה משולבת]
[⬅️ חזרה]
```

### Booking Flow: Stylist Selection

```
עם מי תרצו?

[דנה 👩‍🎨 - בעלים, מומחית צבע, 15 שנות ניסיון]
[שירה 💇‍♀️ - תספורות וצבע, 8 שנות ניסיון]
[יובל ✂️ - ברבר, תספורות גברים וילדים]
[🤷 לא משנה לי]
[⬅️ חזרה]
```

### Booking Flow: Date

```
באיזה יום? (השבוע)

[ראשון 2/4 ✅] [שני 3/4 ✅]
[שלישי 4/4 ✅] [רביעי 5/4 ❌ מלא]
[חמישי 6/4 ✅] [שישי 7/4 ✅ (עד 13:00)]

[▶️ שבוע הבא]
[⬅️ חזרה]
```

### Booking Flow: Time

```
שעות פנויות ליום שני 3/4 עם דנה:

בוקר:
[09:00] [09:30] [10:00] [10:30]

צהריים:
[13:00] [13:30] [14:00]

אחה"צ:
[16:00] [16:30] [17:00]

[⬅️ חזרה לבחירת יום]
```

### Before Confirming: Price, Deposit and Cancellation Terms

Shown after the time is picked and before the slot is held. The privacy notice from
`references/compliance-and-security.md` section 4 comes before the name is asked.

```
סיכום לפני אישור:
[שם העסק], ח.פ./ע.מ. [מספר], [כתובת]
תספורת נשים עם דנה, יום שני 3/4 ב-10:00
מחיר: ₪[מחיר], מקדמה: ₪[סכום] (מקוזזת מהמחיר)
השמירה בתוקף ל-[X] דקות עד לתשלום המקדמה.

תנאי ביטול:
- ביטול תוך 14 יום מקביעת התור ולפחות יומיים שאינם ימי מנוחה לפני התור: החזר המקדמה בניכוי דמי ביטול של עד 5% מהמחיר או ₪100, הנמוך מביניהם.
  [לטיפולי קוסמטיקה ואסתטיקה (פנים, הסרת שיער, ציפורניים) במקום השורה הזאת: ביטול תוך 14 יום מקביעת התור, גם סמוך לתור: החזר המקדמה בניכוי דמי ביטול של עד 5% מהמחיר או ₪100, הנמוך מביניהם.]
- [מדיניות הביטול המאוחר שלכם, לדוגמה: ביטול עד 4 שעות לפני בלי חיוב. לטיפולי קוסמטיקה: בתוך 14 יום מקביעת התור, לא יותר מהתקרה שלמעלה.]
- אם אנחנו מבטלים או מזיזים: החזר מלא.

[💳 לתשלום המקדמה] [⬅️ חזרה]
```

The slot is held only once the deposit is paid. For cosmetic and aesthetic treatments use the
bracketed variant: the 2010 Cancellation Regulations give no two-day condition for them. Count rest
days conservatively in the bot logic, not only Shabbat and holidays. Do not word the
late-cancellation line until you have read section 2: a forfeit that ignores the statutory right is
unlawful.

### Booking Confirmation

```
✅ התור נקבע!

שירות: תספורת נשים
מעצבת: דנה
תאריך: יום שני, 3 באפריל
שעה: 10:00
משך משוער: 45 דקות
מחיר: ₪[מחיר] | מקדמה ששולמה: ₪[סכום]

תנאי ביטול: [כמו במסך הקודם]. לביטול: /cancel או הכפתור למטה.

[שם העסק], ח.פ./ע.מ. [מספר]
📍 [כתובת], [עיר]
🅿️ חניה חינם ברחוב / חניון [שם]

💡 טיפים:
- הגיעו עם שיער נקי ויבש
- אם יש לכם תמונות השראה, שלחו אותן כאן

נשלח תזכורת יום לפני.
[❌ ביטול תור] [🔄 שינוי תור]
```

### Reminder Messages

These need a standalone bot (SKILL.md Phase 0, Option B). A connected Business bot can only write
into chats that had an incoming message in the last 24 hours, so it cannot send them.

24 hours before:
```
💇‍♀️ תזכורת מ[שם הסלון]!

יש לך תור מחר (שני 3/4) ב-10:00 עם דנה.
תספורת נשים.

📍 [כתובת]

[✅ מאשר/ת] [🔄 שינוי] [❌ ביטול]
```

2 hours before:
```
היי! התור שלך ב[שם הסלון] בעוד שעתיים (10:00).

📍 לניווט: [Google Maps link]

נתראה! 💇‍♀️
```

### No-Show Follow-Up

This is a promotion, not a reminder (it invites a new booking). Send it only to customers who
may lawfully receive promotions, with the פרסומת label, sender details and an opt-out, as in
"Broadcast message shapes" below.

```
פרסומת
היי, לא הספקת להגיע היום?

אין בעיה, אפשר לקבוע תור חדש:
[📅 קביעת תור חדש]

(ביטולים עד 4 שעות לפני בלי חיוב)

[שם הסלון], [כתובת] | [טלפון] | [מייל]
אפשר להסיר את עצמך מרשימת התפוצה בכל עת, בכפתור כאן או במייל.
[🚫 הסירו אותי מרשימת התפוצה]
```

A late-cancellation charge must be disclosed before the booking, and that alone does not make it
lawful: a customer who cancels within 14 days of booking and at least two non-rest days ahead keeps
the statutory refund right. See `references/compliance-and-security.md` section 2 before wording any
charge.

### After-Hours

```
היי! 💇‍♀️
הסלון סגור כרגע.

שעות פעילות:
ראשון-חמישי: 09:00 - 19:00
שישי: 09:00 - 13:00
שבת: סגור

אפשר לקבוע תור גם עכשיו:
[📅 קביעת תור]
```

---

## Template 3: Freelance Service Provider Bot

Suitable for accountants, lawyers, consultants, tutors, therapists, personal trainers, photographers, and other solo service providers.

### Welcome Flow

```
שלום! 👋
[שם מלא], [תואר מקצועי]

איך אפשר לעזור?

[📅 קביעת פגישה]
[📋 שירותים ומחירון]
[❓ שאלות נפוצות]
[📄 מסמכים ורשימות]
[📞 צרו קשר]
```

### Services & Pricing

**Accountant example:**
```
📋 השירותים שלנו:

[📊 דוח שנתי ליחיד - מ-₪1,200]
[💼 פתיחת עוסק מורשה - ₪800]
[🏢 הנהלת חשבונות חודשית - מ-₪500/חודש]
[📑 דוח מע"מ דו-חודשי - ₪300]
[💰 ייעוץ מס חד-פעמי - ₪350/שעה]
[🏠 החזר מס - מ-₪600]

💡 פגישת היכרות ראשונה ללא עלות.
[📅 קבע פגישת ייעוץ] [⬅️ חזרה]
```

**Lawyer example:**
```
📋 תחומי התמחות:

[🏠 נדל"ן - קנייה, מכירה, שכירות]
[💼 דיני עבודה - חוזים, פיטורין, זכויות]
[👨‍👩‍👧 דיני משפחה - גירושין, מזונות, משמורת]
[📜 צוואות וירושה]
[🏢 הקמת חברות ושותפויות]

💡 פגישת ייעוץ ראשונית: ₪400 (30 דקות)
[📅 קבע פגישה] [⬅️ חזרה]
```

### Consultation Booking Flow

Insert before the name is asked: [מסך הודעת פרטיות, `references/compliance-and-security.md` section 4]. Insert before the customer confirms: [סיכום מחיר, פרטי העסק ותנאי ביטול, כמו ב-Template 2]. The confirmation must repeat the business details and the cancellation terms.

```
📅 קביעת פגישה

סוג הפגישה:
[🏢 במשרד - [כתובת]]
[📱 שיחת וידאו (Zoom)]
[📞 שיחת טלפון]
[⬅️ חזרה]
```

Day selection:
```
באיזה יום? (שבוע הבא)

[ראשון 9/4 - ✅ פנוי]
[שני 10/4 - ✅ פנוי]
[שלישי 11/4 - ❌ מלא]
[רביעי 12/4 - ✅ פנוי]
[חמישי 13/4 - ✅ אחה"צ בלבד]

[▶️ שבוע אחרי]
[⬅️ חזרה]
```

Time selection:
```
שעות פנויות ליום ראשון 9/4:

[09:00] [10:00] [11:00]
[14:00] [15:00] [16:00]

[⬅️ חזרה לבחירת יום]
```

Pre-meeting questionnaire:
```
כדי להתכונן לפגישה, ענו בבקשה:

1. מה הנושא העיקרי? (תארו בקצרה)
2. האם יש דד-ליין? (כן/לא, ואם כן מתי)

כתבו כהודעה רגילה ונקרא לפני הפגישה.
```

Confirmation:
```
✅ הפגישה נקבעה!

[שם מלא], [תואר מקצועי]
סוג: פגישה במשרד
תאריך: יום ראשון, 9 באפריל
שעה: 10:00
משך: 45 דקות

📍 [כתובת מלאה], קומה [X], [עיר]
🅿️ חניון [שם] צמוד לבניין

📄 מסמכים להביא:
[📄 ראו רשימת מסמכים]

💡 אם יש שאלות לפני הפגישה, כתבו כאן.
[❌ ביטול] [🔄 שינוי]
```

### FAQ Section

**Accountant FAQ:**
```
❓ שאלות נפוצות:

[📊 מתי מגישים דוח שנתי?]
[🧾 איזה קבלות צריך לשמור?]
[💼 עוסק פטור או מורשה - מה ההבדל?]
[💰 כמה מס אני צריך לשלם?]
[🏠 איך מנכים הוצאות עבודה מהבית?]
[📱 האם צריך לדווח על הכנסות מאפליקציות?]
[🧮 מה זה מקדמות מס?]
[⬅️ חזרה]
```

Sample answer:
```
📊 מתי מגישים דוח שנתי?

המועד תלוי בסוג המדווח, בשאלה אם הדוח מוגש דרך מייצג, ובהסדר האורכות למייצגים,
שדוחה בפועל את המועד למיוצגים רבים הרבה מעבר למועד הבסיסי.

אל תשלחו ללקוח תאריך מהזיכרון. בדקו את המועד שחל עליו באתר רשות המסים או מול המייצג שלו.
💡 הגשה מוקדמת = החזר מוקדם יותר.
רוצים שנכין את הדוח? פגישת ייעוץ ראשונה חינם.

[📅 קבע פגישה] [❓ שאלה נוספת] [⬅️ חזרה]
```

### Document Checklist

```
📄 מסמכים נדרשים:

לדוח שנתי (שכיר):
✅ תלושי שכר - כל 12 החודשים
✅ טופס 106 מכל מעסיק
✅ אישורי ריבית מהבנק (פיקדונות, משכנתא)
✅ קבלות על תרומות מוכרות (הסכום המזערי מתעדכן משנה לשנה, בדקו ברשות המסים)
✅ אישור ביטוח לאומי
✅ אישורי קופות גמל ופנסיה
✅ אישור ביטוח חיים (אם רלוונטי)
✅ אישור על ילדים עד גיל 18

לעצמאים - גם:
✅ דוח רווח והפסד
✅ ספר הכנסות והוצאות
✅ דוחות מע"מ
✅ חשבוניות הוצאה מהותיות

💡 אפשר לצלם את הכל ולשלוח כאן, ונבדוק שהכל בסדר.

[📅 קבע פגישה] [⬅️ חזרה]
```

### Contact Information

```
📞 פרטי קשר:

[שם מלא], [תואר]
📱 טלפון: 050-XXX-XXXX
📧 אימייל: name@domain.co.il
📍 משרד: [כתובת], [קומה], [עיר]

🕐 שעות מענה:
ראשון-חמישי: 09:00 - 17:00
שישי: 09:00 - 12:00

💬 כתבו כאן ונחזור אליכם בהקדם!
[📅 קבע פגישה] [⬅️ חזרה]
```

### After-Hours (Professional Tone)

```
שלום,
המשרד סגור כרגע.

שעות קבלה:
ראשון-חמישי: 09:00 - 17:00
שישי: 09:00 - 12:00

ההודעה שלך התקבלה ונחזור אליך ביום העבודה הקרוב.

בינתיים, אפשר:
[📅 לקבוע פגישה]
[❓ שאלות נפוצות]
[📄 רשימת מסמכים נדרשים]
```

---

## Universal Templates

### Human Handoff

Every bot should include a way to reach a real person:

```
💬 דברו עם [שם / נציג]:

אני הבוט, ויש דברים שעדיף לדבר עליהם עם בן אדם.

אפשרויות:
[📱 התקשרו: 050-XXX-XXXX]
[💬 שלחו הודעה כאן - נחזור בשעות הפעילות]
[📧 שלחו אימייל: info@business.co.il]

שעות מענה אנושי:
ראשון-חמישי: 09:00 - 18:00
שישי: 09:00 - 13:00
```

### Feedback Request

After service completion:
```
היי! 👋
איך היה? נשמח לשמוע מכם.

[⭐ מצוין!] [👍 טוב] [👎 יש מה לשפר]
```

If positive (keep the review request free of any offer or discount, which would turn it into a promotion):
```
שמחים לשמוע! 🎉
אם תרצו, תשאירו לנו ביקורת ב-Google:
[⭐ השאירו ביקורת]

תודה רבה! 🙏
```

If needs improvement:
```
תודה על הכנות 🙏
ספרו לנו מה אפשר לשפר (כתבו כהודעה):
```

### Cancellation Flow

```
❌ ביטול

מה תרצו לבטל?
[📅 תור/פגישה]
[🛒 הזמנה]
[⬅️ חזרה]
```

```
מצאנו את התור שלך:

שירות: תספורת נשים
תאריך: שני 3/4 ב-10:00

בטוח רוצים לבטל?
[✅ כן, בטלו] [❌ לא, השאירו]
```

```
✅ התור בוטל.

רוצים לקבוע תור אחר?
[📅 קביעת תור חדש] [🏠 תפריט ראשי]
```

### Holiday Mode Toggle

Before a holiday, switch the bot to holiday mode:

```
חג שמח! 🎉
[שם העסק] בחופשת [שם החג].

נחזור ביום [יום], [תאריך].

בינתיים, הבוט זמין:
[📅 קביעת תור (אחרי החג)]
[📋 תפריט / שירותים]
[❓ שאלות נפוצות]

חג שמח ושמח! 🌸
```


## Broadcast message shapes

Every PROMOTIONAL broadcast must carry the four Section 30a elements. They are baked into the
template below; do not strip them. Transactional messages (an order status the customer asked
for, an appointment reminder they booked) are not advertising and do not need them.

### Promotion (requires prior explicit consent)

```
פרסומת

🎉 [שם המבצע] ב[שם העסק]

[ההצעה בשורה אחת].
בתוקף [תאריך] עד [תאריך].

לקביעת תור: @[שם_הבוט]

[שם העסק המלא], [כתובת מלאה]
[טלפון] | [כתובת מייל]

אפשר להסיר את עצמך מרשימת התפוצה בכל עת, בכפתור כאן או במייל [כתובת].
[🚫 הסירו אותי מרשימת התפוצה]
```

Four things make this compliant, and each is a separate requirement:

1. **פרסומת** is the first word of the message. This is distinct from identifying the sender and
   is the element most often missed.
2. The advertiser's **name, address and ways to make contact**, including a working email address
   the opt-out can be sent to.
3. A **working opt-out**, as an inline-keyboard button, or a bot command you define yourself for the purpose (a "stop" command is the usual convention; it is not a Telegram platform command). The recipient may
   give the opt-out notice in writing or through the medium the advertisement arrived in, at their
   choice, so a Telegram promotion needs a Telegram opt-out and not only an email link.
4. It goes only to customers who **actively opted in**. Pressing Start on the bot is not consent.

Store, per customer, the Telegram user id, the exact opt-in text shown, and the timestamp. If
consent is disputed, the business is the party that has to prove it was given.

### Order status update (transactional, no label needed)

```
📦 הזמנה #[מספר]

✅ התקבלה
✅ בהכנה
🔄 בדרך אליך
⬜ נמסרה

זמן הגעה משוער: [שעה]
```

### Holiday greeting

```
[חג שמח / שבת שלום]! 🕯

[שם העסק] סגור [היום / עד יום X].
נחזור ביום [יום] בשעה [שעה].
```

Treat a holiday greeting that also carries an offer as a promotion, and use the promotion
template instead.


## Section 30a requirements in full

Requirements every promotional broadcast must meet:

1. **Prior explicit consent (הסכמה מפורשת מראש)** - The customer must actively opt in. Starting a chat with the bot is NOT consent. Add an inline-keyboard opt-in ("כן, שלחו לי מבצעים ועדכונים"). Transactional messages (order status, appointment reminders the customer requested) do not need this consent. The one alternative is the existing-customer route in s.30a(ג): details given during a purchase, a notice at that time that offers will follow, a chance to refuse that was not taken, and offers for a similar service only. See `references/compliance-and-security.md` section 3.
2. **Label the message as advertising** - The word **פרסומת** must appear at the head of the message. This is a distinct requirement from identifying the sender, and it is the one most often missed.
3. **Sender identification (זיהוי השולח)** - The statute requires the advertiser's **name, address, and ways to make contact**. For a promotion sent as an electronic message it also requires a valid internet address of the advertiser for sending the opt-out, so publish a working email address too. No anonymous promotions.
4. **Opt-out in every message (אפשרות הסרה)** - Include a clear way to stop, e.g. a "הסר אותי מרשימת התפוצה" button, or a stop command you define in your own bot. The recipient must be able to opt out **through the same medium the promotion arrived in**, so a Telegram promotion needs a Telegram opt-out, not only an email link. Honor opt-outs immediately.

**Keep provable consent records.** If consent is ever disputed, the business is the party that has to show it was given. A stored "yes" with no timestamp and no record of what the customer actually agreed to is worth very little. Store, per customer: the Telegram user id, the exact opt-in text that was shown, and the timestamp.

## Deep-link placements

| Placement | Example payload | What it tells you |
|---|---|---|
| QR code on the counter or the menu | `qr_counter` | Walk-in signups |
| Printed on the receipt | `receipt` | Post-purchase signups |
| Link in an SMS or email footer | `sms_may` | Campaign response |
| Instagram or Facebook bio | `ig_bio` | Social conversion |

Rules for the payload: up to 64 characters, only `A-Z a-z 0-9 _ -`. Encode anything longer or
richer with base64url rather than packing it in raw.

**Option A (connected bot) entry points.** Telegram Business Chat Links are the Option A
equivalent of a deep link: each carries a preset opening message and a view counter, and they are
part of the Business subscription and capped per account. An owner whose bot is connected also sees
a "Manage Bot" action at the top of each managed chat; tapping it sends your bot a deep link in the
form `/start bizChat<user_chat_id>`. A bot that only parses its own marketing payloads will
silently ignore that.


## BotFather profile configuration

Send these commands to @BotFather:

- `/setdescription` - the Hebrew text customers see before starting a chat, e.g. "ברוכים הבאים! אני הבוט של [שם העסק]. אפשר לקבוע תור, לראות תפריט, ולקבל מידע על שעות פעילות."
- `/setabouttext` - a short profile line, e.g. "בוט שירות לקוחות של [שם העסק] - תורים, הזמנות, ומידע"
- `/setuserpic` - upload the business logo.
- `/setcommands` - the command menu:
```
start - התחל שיחה
hours - שעות פעילות
book - קבע תור
menu - תפריט / שירותים
contact - צור קשר
cancel - ביטול תור
status - סטטוס הזמנה
mydata - הפרטים שלי
help - עזרה
```

Only list commands the bot actually handles. /cancel and /status are used by the booking and
order flows; /mydata is the access-and-correction route from
`references/compliance-and-security.md` section 4.

---


## Hebrew greeting conventions

Match the greeting to the moment: "שלום!" or "היי!" generally, "בוקר טוב!" in the morning, "ערב טוב!" in the evening, "שבת שלום!" from Friday afternoon, "שבוע טוב!" after Shabbat, "חג שמח!" on a holiday, and "תודה רבה!" to close.


## Tone of voice

Friendly and direct, never corporate. Use plural "אתם/אתן" for a general audience, or "את/ה" for an intimate business. Emojis are welcome, slang is not. Keep it brief: Israelis expect answers, not paragraphs.

---
