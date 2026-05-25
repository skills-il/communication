---
name: israeli-sms-gateway
description: Integrate with Israeli SMS gateway providers for business messaging, OTP, and notifications. Use when user asks about sending SMS in Israel, Israeli SMS providers, phone number validation (Israeli format), OTP implementation, bulk SMS, or SMS marketing compliance. Covers 019 SMS, InforUMobile, SMS4Free, and international providers with Israeli support. Do NOT use for WhatsApp Business API (see separate skill) or non-Israeli telecom.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires API key from chosen SMS provider. Network access required.
version: 1.2.0
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

    # Validate mobile: 05X-XXXXXXX (10 digits, prefixes 050-059)
    if re.match(r'^05[0-9]\d{7}$', clean):
        return True, '+972' + clean[1:]

    # Validate landline: 0X-XXXXXXX (9-10 digits)
    if re.match(r'^0[2-9]\d{7,8}$', clean):
        return True, '+972' + clean[1:]

    return False, "Invalid Israeli phone number"
```

### שלב 2: בחירת ספק

| ספק | מתאים במיוחד ל | סוג API | תמחור (2026, ללא מע"מ) |
|----------|----------|----------|---------|
| 019 SMS (019 טלקום) | ארגונים, בנקים | REST | כ-0.06-0.10 ש"ח להודעה, חבילות |
| InforUMobile | קמפיינים שיווקיים, המוני | REST + SOAP | כ-0.07-0.12 ש"ח להודעה, חבילות |
| SMS4Free | סטארטאפים, פיתוח | REST | תשלום לפי הודעה, מסלול חינמי הוצא משימוש |
| ActiveTrail | אוטומציות שיווק | REST | בחבילה עם מסלולי דוא"ל |
| Cellact | ארגונים, OTP | REST | תמחור לפי נפח |
| Twilio | אפליקציות גלובליות שמכוונות ל-+972 | REST | כ-$0.26 דולר להודעה לסלולר בישראל (תעריף Twilio מאי 2026, יש לאמת ב-twilio.com/en-us/sms/pricing/il) |
| Vonage | אפליקציות מולטי-אזוריות | REST | תמחור לפי נפח |
| MessageBird/Bird | רב-ערוצי | REST | תמחור לפי נפח |

ספקים ישראליים (019, InforU, Cellact, ActiveTrail) בדרך כלל זולים יותר על תעבורה מקומית ומקלים על רישום זיהוי שולח, אבל דורשים ישות עסקית ישראלית. ספקים בינלאומיים (Twilio, Vonage, Bird) מחייבים בדולר/אירו ומנתבים דרך ספקים בינלאומיים, מה שמשפיע על אחוז המסירה ועל המחיר להודעה.

### שלב 3: שליחת SMS

**דוגמה עם InforUMobile (XML-over-HTTP, ההסכם הקנוני של InforU):**

נקודת הקצה הקנונית של InforU מקבלת XML (לא JSON). POST של JSON ל-`SendMessageXml.ashx` נדחה בשקט. תבנו XML, או תשתמשו במוצר ה-JSON REST הנפרד של InforU אם החשבון שלכם הוקצה לו (כתובת ה-JSON ושמות השדות משתנים לפי תיקוף החשבון, יש לאמת מול הדאשבורד ב-https://apidoc.inforu.co.il/ לפני קוד פרודקשן).

```python
import os
import requests
from xml.etree.ElementTree import Element, SubElement, tostring

def send_sms_inforu_xml(to: str, message: str, sender: str) -> str:
    """Send SMS via InforU XML-over-HTTP endpoint.

    Credentials are read from env vars (INFORU_USER, INFORU_PASS).
    Returns the raw response body for the caller to parse. Verify the
    exact field set against https://apidoc.inforu.co.il/ . InforU adds
    optional fields (DLR callbacks, campaign tagging) without bumping
    the wire version.
    """
    user = os.environ["INFORU_USER"]
    password = os.environ["INFORU_PASS"]

    root = Element("Inforu")
    user_el = SubElement(root, "User")
    SubElement(user_el, "Username").text = user
    SubElement(user_el, "Password").text = password
    content = SubElement(root, "Content", {"Type": "sms"})
    SubElement(content, "Message").text = message
    recipients = SubElement(root, "Recipients")
    SubElement(recipients, "PhoneNumber").text = to
    settings = SubElement(root, "Settings")
    SubElement(settings, "Sender").text = sender

    xml_body = tostring(root, encoding="utf-8")
    response = requests.post(
        "https://api.inforu.co.il/SendMessageXml.ashx",
        params={"InforuXML": xml_body.decode("utf-8")},
        timeout=15,
    )
    return response.text
```

**דוגמה עם Twilio (בינלאומי):**
```python
import os
from twilio.rest import Client

def send_sms_twilio(to: str, message: str) -> str:
    """Send SMS via Twilio. `to` must be in +972 international format."""
    client = Client(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"],
    )
    msg = client.messages.create(
        body=message,
        from_=os.environ["TWILIO_FROM"],  # alphanumeric sender ID or +E.164
        to=to,
    )
    return msg.sid
```

**הערה על SMS4Free:** ה-API הציבורי של SMS4Free שינה נקודות קצה כמה פעמים. אם אתם תלויים בו, תמשכו את נקודת הקצה הנוכחית מהתיעוד באתר `api.sms4free.co.il` ולא מתוך הדרכות ישנות. תתייחסו לתיעוד הישן (`https://api.sms4free.co.il/ApiSMS/v2/SendSMS`) כבסיס בלבד ותאמתו מחדש לפני production.

### שלב 4: רשימת בדיקה לעמידה בתקנות (חוק הספאם + תיקון 13 לחוק הגנת הפרטיות)

שליחת SMS מסחרי בישראל כפופה לתיקון 40 לחוק התקשורת (בזק ושידורים) הידוע כחוק הספאם, ומאז 14 באוגוסט 2025 גם לתיקון 13 לחוק הגנת הפרטיות, שהחמיר משמעותית את החובות על מי שמעבד מידע אישי וקירב את הדין הישראלי לרגולציית ה-GDPR האירופית.

לפני שליחת SMS מסחרי:
- [ ] הנמען נתן הסכמה מפורשת מראש (פעולה אקטיבית, לא תיבה מסומנת מראש)
- [ ] תיעוד הסכמה: מי, למה הסכים, מתי, באיזה ערוץ
- [ ] זיהוי השולח מופיע בגוף ההודעה
- [ ] מנגנון הסרה חינם וקל בכל הודעה (`עצור` / `STOP`, קישור, או מספר קצר)
- [ ] הסרות מטופלות ומכובדות מהר (לא שולחים שוב לאותו נמען)
- [ ] זיהוי השולח (אלפא-נומרי או short code) רשום אצל הספק היכן שנדרש
- [ ] תוכן ההודעה תואם חוק הגנת הצרכן (אין הצעות מטעות, מחירים בש"ח כולל מע"מ)
- [ ] מספרי הטלפון נאספו כדין לפי תיקון 13 (תכלית, מינימום מידע, אבטחה)
- [ ] אין העברה לחו"ל של רשימות נמענים בלי הגנה הולמת (כללי העברה לחו"ל בתיקון 13)
- [ ] שליחה בשעות סבירות (להימנע משבת לנמענים דתיים, להימנע משעות לילה מאוחרות)
- [ ] מודעות לסנקציות: עילת תביעה אזרחית עד 1,000 ש"ח להודעה לא רצויה ללא צורך בהוכחת נזק, בנוסף לקנסות מנהליים שהרשות להגנת הפרטיות יכולה להטיל לפי תיקון 13.

## דוגמאות

### דוגמה 1: שליחת OTP
המשתמש אומר: "שלח קוד אימות למספר נייד ישראלי."
תוצאה: יצירת קוד בן 6 ספרות, שליחה דרך API של ספק SMS, תיעוד סטטוס המסירה, פגות הקוד ב-backend אחרי 5-10 דקות. הודעות OTP הן הודעות שירות טרנזקציוניות, לא שיווקיות, ולכן חוק הספאם פוטר אותן מהדרישה ל-opt-in (הן קשורות לפעולה שהמשתמש עצמו יזם).

### דוגמה 2: פורמט מספר טלפון
המשתמש אומר: "המר את 054-1234567 לפורמט בינלאומי."
תוצאה: `+972541234567`.

### דוגמה 3: SMS שיווקי המוני
המשתמש אומר: "שלח SMS קידום מכירות לרשימת הלקוחות שלי על מבצע חג."
פעולות:
1. תאמתו את כל מספרי הטלפון (תנרמלו לפורמט `+972` בינלאומי, תורידו את ה-0 המוביל).
2. תסננו את הרשימה מול טבלת ההסרות שלכם ותיעוד ההסכמות.
3. תיישמו תקנות ספאם ישראליות: זיהוי שולח, מנגנון הסרה (`עצור` / `STOP`), והפניה להקשר ההסכמה המקורית.
4. תתזמנו לשעות עסקים בישראל (להימנע משבת מאחר הצהרים ועד מוצאי שבת, להימנע מחגי ישראל ב-B2C).
5. תשלחו דרך נקודת הקצה ההמונית של הספק עם מעקב מסירה; תזרימו את דוחות המסירה חזרה ל-CRM.
תוצאה: קמפיין SMS המוני שעומד בחוק הספאם ובתיקון 13, עם דוחות מסירה.

## משאבים מצורפים

### סקריפטים
- `scripts/send_sms.py`: שולח הודעות SMS דרך ספקי שערים ישראליים (SMS4Free, Twilio, InforUMobile). תומך בבחירת ספק, שליחת הודעות ובדיקת סטטוס מסירה. מקבל פרטי התחברות דרך ארגומנטים בשורת הפקודה או משתני סביבה (SMS_API_KEY, TWILIO_ACCOUNT_SID וכו'). הרצה: `python scripts/send_sms.py --help`
- `scripts/validate_phone.py`: מאמת ומנרמל מספרי טלפון ישראליים מכל פורמט נפוץ (מקומי 05X, בינלאומי +972, עם/בלי מקפים) לפורמט בינלאומי סטנדרטי +972XXXXXXXXX. מבחין בין מספרי נייד לקווים נייחים. הרצה: `python scripts/validate_phone.py --help`

## קישורים חיצוניים

- חוק התקשורת תיקון 40 (חוק הספאם), משרד התקשורת: https://www.gov.il/he/departments/ministry_of_communications
- חוק הגנת הפרטיות תיקון 13 (בתוקף 14 באוגוסט 2025), הרשות להגנת הפרטיות: https://www.gov.il/he/departments/the_privacy_protection_authority
- 019 SMS (019 טלקום), הודעות עסקיות: https://019sms.co.il/
- InforUMobile, תיעוד מפתחים: https://apidoc.inforu.co.il/
- SMS4Free, פורטל API: https://www.sms4free.co.il/
- Cellact, SMS עסקי: https://www.cellact.com/
- ActiveTrail SMS: https://www.activetrail.co.il/
- Twilio Programmable Messaging (ישראל): https://www.twilio.com/en-us/messaging/channels/sms
- Vonage SMS API: https://developer.vonage.com/en/messaging/sms/overview
- קידוד GSM-7 לעומת UCS-2: https://en.wikipedia.org/wiki/GSM_03.38

## מלכודות נפוצות

- מספרי סלולר ישראליים מתחילים ב-05x (סה"כ 10 ספרות: 05X-XXXXXXX). סוכנים עלולים לבדוק מול פורמטים אמריקאיים או להחמיץ את האפס המוביל בהמרה ל-`+972` (הצורה הנכונה היא `+9725XXXXXXXX`, בלי ה-0).
- בישראל יש כללי ספאם מחמירים תחת חוק הספאם (תיקון 40 לחוק התקשורת), ומאז אוגוסט 2025 גם תחת תיקון 13 לחוק הגנת הפרטיות. שליחת SMS מסחרי לא רצוי דורשת opt-in מפורש מראש, לא opt-out, ועיבוד לא חוקי של מספרי טלפון יכול היום להוביל גם לקנסות מנהליים, מעבר לחשיפה האזרחית של עד 1,000 ש"ח להודעה.
- ספקי SMS ישראליים (019, InforU, Cellact, ActiveTrail, SMS4Free) משתמשים במבני בקשה שונים מספקים בינלאומיים כמו Twilio. קוד שנוצר לפי תיעוד של Twilio לא יעבוד מול InforU ולהפך.
- הודעות SMS בעברית מוגבלות ל-70 תווים לסגמנט (לעומת 160 ב-GSM-7 לטיני). SMS עברי רב-חלקי משתמש ב-67 תווים לסגמנט בגלל overhead של UDH. סוכנים שמתעלמים מזה יוצרים עלויות הפתעה.
- שליחת SMS בשבת (משישי בערב עד מוצאי שבת) היא פרקטיקה גרועה ל-B2C בישראל ומקור תכוף לתלונות לרשות להגנת הפרטיות.
- רישום זיהוי שולח בישראל: זיהוי שולח אלפא-נומרי חייב להירשם מראש אצל הספק וקשור בפועל לישות עסקית ישראלית מאומתת. רישום דומסטי לוקח כשבוע (לוח הזמנים של Twilio נכון למאי 2026). מספרים מקומיים שלא ממופים למפעיל אמיתי לא מאושרים כזיהוי שולח. זיהוי לא רשום ייפול חזרה למספר גנרי של הספק, מה שפוגע באחוזי הפתיחה.
- ניתוב לפי קידומת: ספקים בינלאומיים כמו Twilio מחלקים את התעבורה ב-+972 כך ש-+97256 ו-+97259 (Jawwal ו-Wataniya) מנותבות דרך הרשאת ה-geo של פלסטין ולא דרך ישראל. הטווחים 050-058 של מפעילים ישראליים לא מושפעים, אבל אם ה-regex של האימות מתרחב ל"+972 כל קידומת שמתחילה ב-5", אתם עלולים להגיע לרשתות פלסטיניות תחת תעריף ומדיניות שונים.
- נקודות הקצה JSON ו-XML של InforU הן מוצרים שונים על hosts שונים. POST של JSON ל-`SendMessageXml.ashx` נכשל בשקט. תשתמשו ב-XML endpoint עם XML body, או תעברו למוצר REST-JSON של InforU (`https://apidoc.inforu.co.il/`) ותוודאו שהחשבון שלכם הוקצה לו.

## פתרון בעיות

### שגיאה: "ההודעה לא נמסרה"
סיבה: מספר לא תקין, חסימת מפעיל, חריגה ממכסה, או זיהוי שולח שטרם אושר.
פתרון: תאמתו שוב את המספר, תוודאו פרטי התחברות ל-API, ותבדקו בלוח הבקרה של הספק את קוד סטטוס המסירה (לכל ספק יש קודי DLR משלו).

### שגיאה: "זיהוי השולח נדחה"
סיבה: זיהוי שולח מותאם אישית דורש רישום מראש בישראל.
פתרון: תרשמו את זיהוי השולח אצל ספק ה-SMS ו(במקום שצריך) תספקו אישור על בעלות עסקית. עד שהרישום מאושר, תיפלו חזרה למספר ברירת המחדל הנומרי של הספק או לזיהוי משותף.

### שגיאה: "תווים עבריים מעוותים ב-SMS"
סיבה: עברית דורשת קידוד UCS-2, שמקטין את אורך ה-SMS מ-160 (GSM-7) ל-70 תווים לסגמנט.
פתרון: שלחו ב-UCS-2 במפורש. שימו לב שהודעות מעל 70 תווים עבריים מתחלקות ל-SMS רב-חלקי של 67 תווים לסגמנט. תתקצבו עלויות המוני בהתאם. רוב הספקים הישראליים מזהים עברית אוטומטית; תוודאו על-ידי בדיקה במכשיר אמיתי, לא רק בסימולטור.
