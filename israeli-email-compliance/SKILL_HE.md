# תאימות דוא"ל ישראלי

## הנחיות

### שלב 1: הבנת חוק הספאם הישראלי

תיקון 40 לחוק התקשורת (בזק ושידורים), התשמ"ב-1982, הוא חוק הספאם הישראלי. הבדלים עיקריים מחוק CAN-SPAM האמריקאי:

| דרישה | ישראל (חוק הספאם) | ארה"ב (CAN-SPAM) |
|--------|---------------------|-------------------|
| מודל הסכמה | הסכמה מוקדמת מפורשת נדרשת לפני השליחה | מודל הסרה (שלח עד לבקשת הסרה) |
| פורמט הסכמה | בכתב, מוקלט, או דיגיטלי עם חותמת זמן | ללא פורמט מוגדר |
| מועד הסרה | מיידי (עד 2 ימי עסקים) | 10 ימי עסקים |
| קנסות | עד 1,000 ש"ח לכל הודעה ללא הסכמה (אזרחי), קנסות פליליים | עד $46,517 לכל דוא"ל |
| תביעות פרטיות | הנמען יכול לתבוע 1,000 ש"ח לכל הודעה ללא הוכחת נזק | חובה להוכיח נזק |

**חריגים בהם לא נדרשת הסכמה מוקדמת:**
1. לקוח קיים שרכש מוצרים/שירותים דומים בשנה האחרונה
2. ההודעה קשורה בבירור למוצר/שירות שהלקוח רכש בעבר
3. ניתנה ללקוח הזדמנות ברורה לסרב בעת הרכישה

### שלב 2: ניהול הסכמות

```python
from datetime import datetime, timezone
from dataclasses import dataclass, field

@dataclass
class ConsentRecord:
    """Track opt-in consent per Israeli anti-spam law requirements."""
    email: str
    consented_at: str  # ISO 8601 timestamp
    consent_method: str  # "web_form", "written", "verbal_recorded"
    consent_source: str  # URL or description of where consent was given
    ip_address: str = ""
    channels: list = field(default_factory=lambda: ["email"])
    is_active: bool = True
    revoked_at: str = ""

    def to_record(self) -> dict:
        return {
            "email": self.email,
            "consented_at": self.consented_at,
            "method": self.consent_method,
            "source": self.consent_source,
            "ip": self.ip_address,
            "channels": self.channels,
            "active": self.is_active,
            "revoked_at": self.revoked_at
        }

def validate_consent(record: ConsentRecord) -> list:
    """Validate consent record meets Israeli legal requirements."""
    issues = []
    if not record.consented_at:
        issues.append("Missing consent timestamp (required by law)")
    if record.consent_method not in ("web_form", "written", "verbal_recorded"):
        issues.append("Consent method must be verifiable")
    if not record.consent_source:
        issues.append("Must record where consent was obtained")
    return issues
```

**ניהול הסכמות רב-ערוצי (דוא"ל + SMS):**
כאשר משתמש נותן הסכמה לדוא"ל, זה לא מכסה אוטומטית SMS או WhatsApp. כל ערוץ דורש הסכמה מפורשת נפרדת לפי חוק הספאם.

### שלב 3: בניית תבניות דוא"ל בעברית (RTL)

דוא"ל בעברית דורש סימון RTL (ימין לשמאל) תקין. ללא זה, ספקי דוא"ל עלולים לסמן את ההודעה כספאם או להציגה בצורה שגויה.

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      direction: rtl;
      text-align: right;
      font-family: Arial, Helvetica, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
    }
    .container {
      max-width: 600px;
      margin: 0 auto;
      background-color: #ffffff;
      padding: 20px;
    }
    .header { text-align: center; padding: 20px 0; }
    .content { padding: 20px; line-height: 1.8; }
    .unsubscribe {
      text-align: center;
      padding: 20px;
      font-size: 12px;
      color: #666666;
      border-top: 1px solid #eeeeee;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>COMPANY_NAME</h1>
    </div>
    <div class="content">
      <p>MESSAGE_BODY</p>
    </div>
    <div class="unsubscribe">
      <p>
        UNSUBSCRIBE_TEXT_HE
        <a href="UNSUBSCRIBE_URL">UNSUBSCRIBE_LINK_HE</a>
      </p>
      <p>COMPANY_ADDRESS</p>
    </div>
  </div>
</body>
</html>
```

**כללי RTL קריטיים:**
- תמיד הגדירו `dir="rtl"` על אלמנט השורש
- השתמשו ב-`text-align: right` כברירת מחדל
- תוכן מעורב עברית/אנגלית: עטפו קטעי אנגלית ב-`<span dir="ltr">`
- בדקו ב-Outlook (נפוץ בארגונים ישראליים) וב-Gmail

### שלב 4: שליחה לספקי אינטרנט ישראליים

לספקי אינטרנט ישראליים יש דפוסים ספציפיים המשפיעים על יכולת המסירה:

| ספק | דומיין דוא"ל | הערות |
|------|-------------|--------|
| בזק | @bezeq.net, @bezequint.net | מסנני ספאם שמרנים, חממו לאט |
| HOT | @hot.co.il, @hotmail.co.il | עקבו אחרי שיעורי חזרות בקפידה |
| פרטנר (012) | @012.net.il | הגבלת קצב אגרסיבית |
| סלקום | @cellcom.co.il | יכולת מסירה סטנדרטית |
| וואלה! | @walla.co.il | ווב-מייל ישראלי פופולרי, בדקו הצגת תמונות |
| Gmail IL | @gmail.com | מסנני Google סטנדרטיים, כותרות בעברית תקינות |

**שיטות עבודה מומלצות לשליחה בישראל:**
1. חממו כתובות IP חדשות בהדרגה (התחילו ב-50/יום, הכפילו שבועית)
2. אמתו עם SPF, DKIM ו-DMARC
3. כותרות בעברית: שמרו על פחות מ-50 תווים (נחתך בנייד)
4. שלחו בשעות עסקים ישראליות: ראשון-חמישי, 09:00-18:00
5. הימנעו משליחה מצהרי יום שישי עד מוצאי שבת

### שלב 5: מנגנון הסרה חובה

לפי חוק הספאם, כל דוא"ל מסחרי חייב לכלול מנגנון הסרה ברור ופעיל בעברית.

```python
def generate_unsubscribe_section(unsub_url: str, company_name: str) -> dict:
    """Generate bilingual unsubscribe section for Israeli emails."""
    return {
        "he": (
            f"אינך מעוניין/ת לקבל הודעות מ-{company_name}? "
            f'<a href="{unsub_url}">לחצ/י כאן להסרה מרשימת התפוצה</a>. '
            "ההסרה תתבצע תוך 2 ימי עסקים."
        ),
        "en": (
            f"Don't want to receive emails from {company_name}? "
            f'<a href="{unsub_url}">Click here to unsubscribe</a>. '
            "Removal will be processed within 2 business days."
        )
    }
```

**דרישות הסרה לפי חוק הספאם:**
- חייבת להיות בעברית (או דו-לשונית)
- תהליך בלחיצה אחת או שלב בודד (ללא צורך בהתחברות)
- חייבת להתבצע תוך 2 ימי עסקים
- חייבת לכלול כותרת List-Unsubscribe עבור תוכנות דוא"ל

### שלב 6: שילוב חוק הגנת הצרכן

חוק הגנת הצרכן הישראלי מעניק זכות ביטול של 14 יום לעסקאות שנעשו דרך תקשורת מסחרית:

```python
def cancellation_notice_required(transaction_type: str) -> dict:
    """Check 14-day cancellation requirements for email-driven transactions."""
    rules = {
        "cooling_off_period_days": 14,
        "notice_required": True,
        "applies_to": [
            "Purchases made via email promotions",
            "Subscriptions initiated from email campaigns",
            "Services booked through email offers"
        ],
        "must_include_in_email": [
            "Clear pricing in NIS (including VAT)",
            "Cancellation rights notice in Hebrew",
            "Business registration number",
            "Contact details for cancellation requests"
        ]
    }
    return rules
```

### שלב 7: הרצת בדיקת תאימות

השתמשו בסקריפט הבדיקה המצורף כדי לאמת את קמפיין הדוא"ל:

```bash
python scripts/check_email.py --html campaign.html --consent-db consents.json
```

הסקריפט בודק:
- נוכחות קישור הסרה בעברית
- תקינות סימון RTL
- טקסט משפטי נדרש
- שלמות רשומות הסכמה

## דוגמאות

### דוגמה 1: הקמת קמפיין שיווקי
המשתמש אומר: "צרו קמפיין דוא"ל בעברית למבצע פסח"
פעולות:
1. ודאו שקיימות רשומות הסכמה לכל הנמענים עם ערוץ "דוא"ל"
2. בנו תבנית RTL בעברית עם תוכן חגיגי
3. הוסיפו סעיף הסרה חובה בעברית
4. כללו הודעת זכות ביטול 14 יום למוצרים המוצעים
5. תזמנו לימים ראשון-חמישי לפני פסח (הימנעו משבת וחג)
תוצאה: דוא"ל שיווקי תקני בעברית עם אימות הסכמה.

### דוגמה 2: תבנית דוא"ל טרנזקציוני
המשתמש אומר: "הקימו דוא"ל אישור הזמנה בעברית לאתר המסחר שלנו"
פעולות:
1. צרו תבנית HTML ב-RTL עם פרטי ההזמנה
2. כללו מספר עוסק ותמחור בש"ח כולל מע"מ
3. הוסיפו הודעת זכות ביטול (14 ימי צינון)
4. בדקו הצגה ב-Walla!, Gmail ו-Outlook
תוצאה: תבנית דוא"ל טרנזקציונית תקינה משפטית בעברית.

### דוגמה 3: מיגרציית הסכמות
המשתמש אומר: "אנחנו עוברים מ-Mailchimp ל-SendGrid, איך מטפלים ברשומות הסכמה ישראליות?"
פעולות:
1. ייצאו את כל רשומות ההסכמה עם חותמות זמן ומקור הסכמה
2. מפו שדות הסכמה לפלטפורמה החדשה (שמרו תאריך הסכמה מקורי)
3. ודאו שלכל רשומה יש שדות נדרשים (חותמת זמן, שיטה, מקור)
4. אמתו מחדש מול דרישות חוק הספאם
תוצאה: מסד נתוני הסכמות מועבר עם שמירה מלאה על תאימות משפטית.

### דוגמה 4: ביקורת תאימות רב-ערוצית
המשתמש אומר: "אנחנו שולחים גם דוא"ל וגם SMS ללקוחות, האם מערך ההסכמות שלנו נכון?"
פעולות:
1. ודאו שקיימות רשומות הסכמה נפרדות לכל ערוץ
2. בדקו שהסכמת דוא"ל לא מניחה הסכמת SMS
3. אמתו שקיימים מנגנוני הסרה לכל ערוץ
4. אשרו שחותמות זמן ומקורות הסכמה מתועדים
תוצאה: דוח ביקורת עם סטטוס תאימות לכל ערוץ.

## משאבים מצורפים

### סקריפטים
- `scripts/check_email.py` -- מאמת HTML של קמפיין דוא"ל מול דרישות חוק הספאם הישראלי. בודק קישורי הסרה בעברית, סימון RTL, טקסט משפטי נדרש ושלמות רשומות הסכמה. הרצה: `python scripts/check_email.py --help`

### הפניות
- `references/anti-spam-law.md` -- סיכום תיקון 40 לחוק התקשורת (חוק הספאם): דרישות הסכמה, קנסות, חריגים, דפוסי אכיפה והשוואה עם חוקי ספאם בינלאומיים. התייעצו בעת אימות תאימות קמפיין או ייעוץ בנושא ארכיטקטורת הסכמות.

## פתרון בעיות

### שגיאה: "לא נמצאה רשומת הסכמה לנמען"
סיבה: דוא"ל הנמען לא נמצא במסד ההסכמות או שההסכמה בוטלה.
פתרון: ודאו שהנמען הסכים מפורשות. לפי החוק הישראלי, אסור לשלוח דוא"ל מסחרי ללא הסכמה מוקדמת. בדקו שההסכמה נרשמה עם חותמת זמן ומקור.

### שגיאה: "הצגת RTL שבורה ב-Outlook"
סיבה: Outlook משתמש במנוע הצגה של Word שמטפל ב-RTL בצורה לא עקבית.
פתרון: הוסיפו `dir="rtl"` לכל תא טבלה בנפרד, לא רק לעטיפה. השתמשו בסגנונות inline במקום מחלקות CSS עבור מאפייני כיוון.

### שגיאה: "שיעור חזרות גבוה בספקי אינטרנט ישראליים"
סיבה: שליחה מהירה מדי לדומיינים של ספקים ישראליים או היגיינת רשימה ירודה.
פתרון: יישמו הגבלת קצב לפי דומיין (מקסימום 100/שעה לבזק, 200/שעה ל-HOT). הסירו חזרות קשות מיידית. חממו בהדרגה על כתובות IP חדשות.
