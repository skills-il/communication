# שער SMS ישראלי

## הנחיות

### שלב 1: אימות מספר טלפון ישראלי
לפני שליחה, יש לאמת את פורמט מספר הטלפון:

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

def send_sms_sms4free(to: str, message: str, api_key: str, sender: str):
    url = "https://www.sms4free.co.il/ApiSMS/SendSMS"
    payload = {
        "key": api_key,
        "user": "username",
        "pass": "password",
        "sender": sender,
        "recipient": to,
        "msg": message
    }
    response = requests.get(url, params=payload)
    return response.text
```

### שלב 4: רשימת בדיקה לעמידה בתקנות
לפני שליחת SMS מסחרי:
- [ ] הנמען הסכים (הסכמה מפורשת)
- [ ] כלול מנגנון הסרה מרשימת תפוצה (השב STOP / קישור)
- [ ] לא רשום ברשימת רובינסון (מאגר "אל תפריע")
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

## משאבים מצורפים

### סקריפטים
- `scripts/send_sms.py` — שולח הודעות SMS דרך ספקי שערים ישראליים (SMS4Free, Twilio, InforUMobile). תומך בבחירת ספק, שליחת הודעות ובדיקת סטטוס מסירה. מקבל פרטי התחברות דרך ארגומנטים בשורת הפקודה או משתני סביבה (SMS_API_KEY, TWILIO_ACCOUNT_SID וכו'). הרצה: `python scripts/send_sms.py --help`
- `scripts/validate_phone.py` — מאמת ומנרמל מספרי טלפון ישראליים מכל פורמט נפוץ (מקומי 05X, בינלאומי 972+, עם/בלי מקפים) לפורמט בינלאומי סטנדרטי +972XXXXXXXXX. מבחין בין מספרי נייד לקווים נייחים. הרצה: `python scripts/validate_phone.py --help`

## פתרון בעיות

### שגיאה: "ההודעה לא נמסרה"
סיבה: מגוון -- מספר לא תקין, חסימת מפעיל, חריגה ממכסה
פתרון: בדקו אימות מספר, ודאו פרטי התחברות ל-API, בדקו בלוח הבקרה של הספק את סטטוס המסירה.

### שגיאה: "זיהוי השולח נדחה"
סיבה: זיהוי שולח מותאם אישית דורש רישום מראש בישראל
פתרון: רשמו את זיהוי השולח אצל ספק ה-SMS. זיהוי לא רשום יופיע כמספר גנרי של הספק.
