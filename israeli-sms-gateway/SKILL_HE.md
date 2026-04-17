---
name: israeli-sms-gateway
description: Integrate with Israeli SMS gateway providers for business messaging, OTP, and notifications. Use when user asks about sending SMS in Israel, Israeli SMS providers, phone number validation (Israeli format), OTP implementation, bulk SMS, or SMS marketing compliance. Covers SMS4Free, InforUMobile, and international providers with Israeli support. Do NOT use for WhatsApp Business API (see separate skill) or non-Israeli telecom.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires API key from chosen SMS provider. Network access required.
version: 1.0.1
---

# שער SMS ישראלי

## הנחיות

### שלב 1: אימות מספר טלפון ישראלי
לפני שליחה, תאמתו את פורמט מספר הטלפון:

```python
import re

def validate_israeli_phone(phone: str) -> tuple[bool, str]:
    """Validate and normalize Israeli phone number."""
    # Remove spaces, dashes, parentheses
    clean = re.sub(r'[\s\-\(\)]', '', phone)

    # Handle +972 prefix
    if clean.startswith('+972'):
        clean = '0' + clean[4:]
    elif clean.startswith('972'):
        clean = '0' + clean[3:]

    # Validate mobile: 05X-XXXXXXX (10 digits)
    if re.match(r'^05[0-8]\d{7}$', clean):
        return True, '+972' + clean[1:]

    # Validate landline: 0X-XXXXXXX (9-10 digits)
    if re.match(r'^0[2-9]\d{7,8}$', clean):
        return True, '+972' + clean[1:]

    return False, "Invalid Israeli phone number"
```

### שלב 2: בחירת ספק
| ספק | מתאים במיוחד ל | סוג API | תמחור |
|----------|----------|----------|---------|
| SMS4Free | סטארטאפים, מפתחים | REST | תשלום לפי הודעה |
| InforUMobile | קמפיינים שיווקיים | REST | חבילות |
| Twilio | גלובלי + ישראלי | REST | תשלום לפי הודעה |
| Vonage | ארגוני | REST | תמחור לפי נפח |

### שלב 3: שליחת SMS

**דוגמה עם SMS4Free:**
```python
import requests

def send_sms_sms4free(to: str, message: str, api_key: str,
                      username: str, pass_key: str, sender: str):
    # הערה: נקודת הקצה המקורית של SMS4Free כבר לא זמינה
    # תפנו ל-SMS4Free כדי לקבל תיעוד API ונקודות קצה עדכניות
    payload = {
        "key": api_key,
        "user": username,
        "pass": pass_key,
        "sender": sender,
        "recipient": to,
        "msg": message
    }
    # הערה: תשמרו פרטי התחברות במשתני סביבה, לא בקוד
    # תבדקו עם SMS4Free מה נקודת הקצה הנוכחית
    print("תפנו ל-SMS4Free לקבלת נקודת קצה ותיעוד עדכניים")
```

### שלב 4: רשימת בדיקה לעמידה בתקנות
לפני שליחת SMS מסחרי:
- [ ] הנמען הסכים (הסכמה מפורשת)
- [ ] יש מנגנון הסרה מרשימת תפוצה (השב STOP / קישור)
- [ ] לא רשום במאגר "אל תפריע" הישראלי (דרישות רגולטוריות נוכחיות)
- [ ] זיהוי השולח רשום אצל הספק
- [ ] תוכן ההודעה עומד בחוק הפרסומת הישראלי
- [ ] שליחה בשעות מותרות (לא בשבת לנמענים דתיים)

## דוגמאות

### דוגמה 1: שליחת OTP
המשתמש אומר: "שלח קוד אימות למספר נייד ישראלי"
תוצאה: יצירת קוד בן 6 ספרות, שליחה דרך API של ספק SMS, טיפול באישור מסירה.

### דוגמה 2: פורמט מספר טלפון
המשתמש אומר: "המר את 054-1234567 לפורמט בינלאומי"
תוצאה: +972541234567

### דוגמה 3: SMS שיווקי המוני
המשתמש אומר: "שלח SMS קידום מכירות לרשימת הלקוחות שלי על מבצע חג"
פעולות:
1. תאמתו את כל מספרי הטלפון ברשימה (תנרמלו לפורמט +972)
2. תבדקו התאמה למאגר "אל תפריע" ונתוני הסכמה
3. תיישמו תקנות ספאם ישראליות: תכללו זיהוי שולח ומנגנון ביטול
4. תתזמנו לשעות עסקים ישראליות (לא בשבת/חגים)
5. תשלחו דרך API המוני עם מעקב מסירה
תוצאה: קמפיין SMS המוני תואם חוק עם דוח מסירה.

## משאבים מצורפים

### סקריפטים
- `scripts/send_sms.py` — שולח הודעות SMS דרך ספקי שערים ישראליים (SMS4Free, Twilio, InforUMobile). תומך בבחירת ספק, שליחת הודעות ובדיקת סטטוס מסירה. מקבל פרטי התחברות דרך ארגומנטים בשורת הפקודה או משתני סביבה (SMS_API_KEY, TWILIO_ACCOUNT_SID וכו'). הרצה: `python scripts/send_sms.py --help`
- `scripts/validate_phone.py` — מאמת ומנרמל מספרי טלפון ישראליים מכל פורמט נפוץ (מקומי 05X, בינלאומי +972, עם/בלי מקפים) לפורמט בינלאומי סטנדרטי +972XXXXXXXXX. מבחין בין מספרי נייד לקווים נייחים. הרצה: `python scripts/validate_phone.py --help`

### הפניות
- `references/israeli-sms-compliance.md` — דרישות חוק ספאם ישראלי לשיווק SMS: כללי הסכמה מפורשת, תהליך בדיקה במאגר "אל תפריע", מנגנוני ביטול נדרשים, שעות שליחה מותרות ומבנה עונשים על הפרות (עד 1,000 ש"ח לכל הודעה לא רצויה). תסתכלו על זה כשאתם מקימים קמפיינים מסחריים או בודקים התאמה לחוק.
- `references/provider-api-docs.md` — סיכומי תיעוד API לספקי SMS ישראליים (SMS4Free, InforUMobile) ולספקים בינלאומיים עם תמיכה ישראלית (Twilio, Vonage), כולל אימות, כתובות נקודות קצה, קודי תגובה, דוחות מסירה וקידוד תווים עבריים (GSM-7 לעומת UCS-2 לעברית). תסתכלו על זה כשאתם משלבים עם ספק מסוים או פותרים בעיות מסירה.

## מלכודות נפוצות

- מספרי סלולר ישראליים מתחילים ב-05x (סה"כ 10 ספרות: 05X-XXXXXXX). סוכנים עלולים לבדוק מול פורמטים אמריקאיים או להחמיץ את האפס המוביל כשמשתמשים בקידומת +972 (צריך להיות +9725XXXXXXXX, בלי ה-0).
- בישראל תקנות ספאם מחמירות תחת חוק התקשורת. שליחת SMS ללא הסכמה דורשת opt-in מפורש מראש, לא רק opt-out. סוכנים עלולים להמליץ על תהליכי opt-out שמפרים את החוק הישראלי.
- ספקי SMS ישראליים (SMS4Free, InforUMobile, Cellact) משתמשים בפורמטים שונים מספקים בינלאומיים כמו Twilio. סוכנים עלולים ליצור קוד תואם Twilio שלא עובד עם ספקים ישראליים.
- הודעות SMS בעברית מוגבלות ל-70 תווים לסגמנט (לעומת 160 ללטינית). סוכנים עלולים לא להתחשב בכך בניסוח הודעות, מה שמוביל לעלויות SMS רב-חלקי בלתי צפויות.
- שליחת SMS בשבת (שישי בערב עד מוצאי שבת) נחשבת לפרקטיקה גרועה ל-B2C בישראל ועלולה להוביל לתלונות לקוחות או ביטול הסכמה.

## פתרון בעיות

### שגיאה: "ההודעה לא נמסרה"
סיבה: מגוון -- מספר לא תקין, חסימת מפעיל, חריגה ממכסה
פתרון: תבדקו אימות מספר, תוודאו פרטי התחברות ל-API, ותבדקו בלוח הבקרה של הספק את סטטוס המסירה.

### שגיאה: "זיהוי השולח נדחה"
סיבה: זיהוי שולח מותאם אישית דורש רישום מראש בישראל
פתרון: תרשמו את זיהוי השולח אצל ספק ה-SMS. זיהוי לא רשום יופיע כמספר גנרי של הספק.

### שגיאה: "תווים עבריים מעוותים ב-SMS"
סיבה: עברית דורשת קידוד UCS-2 שמקטין את אורך ה-SMS מ-160 ל-70 תווים לסגמנט
פתרון: תשתמשו בקידוד UCS-2 להודעות בעברית. שימו לב שהודעות מעל 70 תווים עבריים מתחלקות ל-SMS רב-חלקי (67 תווים לסגמנט). תתקצבו בהתאם לעלויות SMS המוני. חלק מהספקים מטפלים בקידוד אוטומטית.