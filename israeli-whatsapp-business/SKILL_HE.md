---
name: israeli-whatsapp-business
description: Integrate WhatsApp Business API for the Israeli market with Hebrew message templates, customer communication, and CRM integration. Use when user asks about WhatsApp Business in Israel, Hebrew WhatsApp templates, WhatsApp marketing to Israeli customers, business messaging via WhatsApp, or integrating WhatsApp with Israeli CRM tools (Monday.com, Priority, etc.). Covers Cloud API setup, template creation, conversation pricing, compliance with Israeli anti-spam law and Privacy Law Amendment 13, and Israeli consumer communication preferences. Do NOT use for personal WhatsApp or non-Israeli WhatsApp markets.
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: Requires Meta Business Account and WhatsApp Business API access. Network access required.
version: 1.1.0
---

# וואטסאפ עסקי ישראלי

## הנחיות

### שלב 1: אימות הגדרות WhatsApp Business
תוודאו שלמשתמש יש:
1. חשבון Meta Business (`business.facebook.com`)
2. חשבון WhatsApp Business (WABA) מקושר ל-Meta Business
3. מספר טלפון רשום עם קידומת ישראלית (972+), או דרך ה-Cloud API הרשמי של Meta או דרך BSP (Business Solution Provider) כמו 360dialog, MessageBird/Bird, Twilio, Infobip, Vonage, או BSP ישראלי (Cellact, GetWApp, Coral.cx)
4. Access Token של System User עם הרשאת `whatsapp_business_messaging` (וגם `whatsapp_business_management` לפעולות תבניות)

```python
import requests

def verify_whatsapp_setup(access_token: str, phone_number_id: str) -> dict:
    """Verify WhatsApp Business API access against the Cloud API."""
    # Use the latest stable Graph API version. Check
    # https://developers.facebook.com/docs/graph-api/changelog for current.
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

### שלב 2: יצירת תבניות הודעות בעברית

**קטגוריות שיחה (מודל התמחור של Meta, בתוקף מ-1 ביולי 2024 ועדכונים ב-2025-26):**
WhatsApp מחייב היום לפי **הודעת תבנית** בשלוש קטגוריות בתשלום ועוד קטגוריה חינמית:

| קטגוריה | מתי משתמשים | חיוב |
|----------|-------------|---------|
| Utility (שירות) | עדכונים טרנזקציוניים שהמשתמש מצפה להם (אישור הזמנה, משלוח, קבלת תשלום, תזכורת תור) | חינם בתוך חלון שירות פתוח של 24 שעות שהמשתמש פתח; מחוץ לחלון, מחויב לפי הודעת תבנית |
| Authentication (אימות) | OTP וקודי אימות | מחויב לפי הודעת תבנית authentication |
| Marketing (שיווק) | מבצעים, הצעות, ניוזלטרים, החזרת לקוחות | מחויב לפי הודעת תבנית marketing (לרוב הקטגוריה היקרה ביותר) |
| Service (שירות חופשי) | תגובות חופשיות בתוך חלון שירות 24 שעות | חינם, נספר כשיחת שירות |

מודל התמחור הישן ("conversation-based" של 24 שעות לפי קטגוריה) הוצא משימוש ב-1 ביולי 2024 והוחלף בחיוב לפי הודעת תבנית עבור utility, authentication ו-marketing, בתוספת קצבה חינמית לכל WABA. תוודאו את התעריפים הספציפיים לישראל בדף התמחור של Meta לפני שאתם מצטטים מספרים ללקוח, מאחר והם משתנים לפי מדינה ומתעדכנים תקופתית.

**קטגוריות תבניות לעסקים ישראליים:**

| קטגוריה | שימוש | דוגמה (עברית, מפושטת) |
|----------|----------|-------------------|
| תזכורת פגישה (Utility) | מרפאות, מכוני יופי, שירותים | תזכורת: יש לך תור ב-{{1}} בתאריך {{2}} בשעה {{3}} |
| אישור הזמנה (Utility) | מסחר אלקטרוני, משלוחים | הזמנתך ({{1}}) התקבלה. נעדכן כשתישלח. |
| עדכון משלוח (Utility) | לוגיסטיקה | המשלוח שלך בדרך. מעקב: {{1}} |
| קבלת תשלום (Utility) | חיוב, חשבוניות | התקבל תשלום של {{1}} ש"ח. תודה. |
| OTP (Authentication) | התחברות, אימות | קוד האימות שלך הוא {{1}}. תוקף 5 דקות. |
| הודעת ברוכים הבאים (Marketing או Utility) | קליטה | שלום {{1}}, ברוכים הבאים ל-{{2}}. איך נוכל לעזור? |
| מבצע (Marketing) | מכירות, חגים | מבצע חג: {{1}} בהנחת {{2}}%. עד {{3}}. |

**הגשת תבנית לאישור:**
```python
def create_template(waba_id: str, access_token: str, template: dict):
    """Create a WhatsApp message template."""
    url = f"https://graph.facebook.com/v23.0/{waba_id}/message_templates"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=template)
    return response.json()

# Example: Hebrew appointment reminder template
appointment_template = {
    "name": "appointment_reminder_he",
    "language": "he",
    "category": "UTILITY",
    "components": [
        {
            "type": "BODY",
            "text": "שלום {{1}}, תזכורת על תור ב-{{2}} בתאריך {{3}} בשעה {{4}}. לאישור השיבו 1, לביטול השיבו 2.",
            "example": {
                "body_text": [["ישראל", "מרפאת השיניים ד״ר כהן", "15.03.2026", "10:00"]],
            },
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {"type": "QUICK_REPLY", "text": "מאשר"},
                {"type": "QUICK_REPLY", "text": "צריך לשנות"},
            ],
        },
    ],
}
```

אישור תבנית בדרך כלל לוקח דקות עד מספר שעות כשהתוכן נקי. דחיות נובעות לרוב משפה שיווקית בתבנית UTILITY (היה צריך MARKETING), חוסר בדוגמאות למשתנים, או בעיות בעיצוב טקסט מעורב כיוונים.

### שלב 3: שליחת הודעות

**שליחת הודעת תבנית:**
```python
def send_template_message(phone_number_id: str, access_token: str,
                          to: str, template_name: str, language: str,
                          parameters: list):
    """Send a WhatsApp template message."""
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # Format: 972541234567 (no leading + or 0)
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": p} for p in parameters
                    ],
                }
            ],
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

**שליחת הודעה אינטראקטיבית (בתוך חלון שירות 24 שעות):**
```python
def send_interactive_list(phone_number_id: str, access_token: str,
                          to: str, body_text: str, sections: list):
    """Send an interactive list message in Hebrew."""
    url = f"https://graph.facebook.com/v23.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body_text},
            "action": {"button": "בחר אפשרות", "sections": sections},
        },
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### שלב 4: תזמון ועמידה בתקנות בישראל

שליחת WhatsApp מסחרי בישראל כפופה לתיקון 40 לחוק התקשורת (בזק ושידורים), הידוע כחוק הספאם, ומאז 14 באוגוסט 2025 גם לתיקון 13 לחוק הגנת הפרטיות, שהחמיר את החובות על מי שמעבד מידע אישי וקירב את הדין הישראלי לרגולציית ה-GDPR. שיווק ב-WhatsApp דורש opt-in מפורש מראש בדיוק כמו SMS, ועיבוד לא חוקי של מספרי טלפון יכול להוביל לקנסות מנהליים מצד הרשות להגנת הפרטיות.

**לוח זמנים לשליחה בשוק הישראלי:**
```python
from datetime import datetime, time
import pytz

def is_valid_sending_time() -> tuple[bool, str]:
    """Check if current time is appropriate for Israeli business messaging."""
    israel_tz = pytz.timezone("Asia/Jerusalem")
    now = datetime.now(israel_tz)
    day = now.weekday()  # 0=Monday, 6=Sunday

    # Friday after 14:00, pre-Shabbat
    if day == 4 and now.time() > time(14, 0):
        return False, "Pre-Shabbat hours. Send after Saturday 20:00."

    # Saturday before 20:00, Shabbat
    if day == 5 and now.time() < time(20, 0):
        return False, "Shabbat. Send after 20:00."

    # Sunday-Thursday business hours
    if now.time() < time(8, 30) or now.time() > time(20, 0):
        return False, "Outside business hours. Send between 08:30 and 20:00."

    return True, "OK to send."

def compliance_checklist(message_type: str) -> list:
    """Return compliance checklist for Israeli WhatsApp messaging."""
    checks = [
        "Recipient gave explicit prior opt-in to receive WhatsApp messages",
        "Opt-in record stored: who, what, timestamp, channel",
        "Opt-out mechanism included (e.g., reply 'הסר' / 'STOP')",
        "Business identity clearly stated in the message",
        "Phone numbers obtained lawfully under Privacy Law Amendment 13",
        "Message sent in appropriate language (Hebrew or English)",
    ]
    if message_type == "marketing":
        checks.extend([
            "Marketing template approved by Meta in MARKETING category",
            "Compliant with Chok HaSpam (Communications Law Amendment 40)",
            "Not sent during Shabbat or Jewish holidays for B2C",
            "Frequency cap respected (avoid over-messaging)",
            "No cross-border list transfer without adequate protection (Amendment 13)",
        ])
    return checks
```

### שלב 5: הנחיות לאינטגרציה עם CRM

**Monday.com + WhatsApp:**
1. תשתמשו באוטומציות של Monday.com או במחברי צד שלישי (Make, Zapier, Pipedream) כדי לחבר את WhatsApp Cloud API ללוחות שלכם.
2. תפעילו שליחת תבניות WhatsApp בשינוי סטטוס (למשל, סטטוס "נשלח" שולח תבנית UTILITY).
3. תתעדו הודעות נכנסות מ-WhatsApp כעדכונים ב-Monday.com דרך webhook נכנס.
4. תמפו `wa_id` של WhatsApp לפריט ב-Monday.com כדי שהשרשורים יישארו מחוברים.

**אינטגרציית CRM מותאמת אישית:**
```python
def webhook_handler(event: dict) -> dict:
    """Handle incoming WhatsApp webhook for CRM integration."""
    if event.get("entry"):
        for entry in event["entry"]:
            for change in entry.get("changes", []):
                if change["field"] == "messages":
                    messages = change["value"].get("messages", [])
                    for msg in messages:
                        crm_data = {
                            "phone": msg["from"],
                            "message": msg.get("text", {}).get("body", ""),
                            "timestamp": msg["timestamp"],
                            "type": msg["type"],
                            "wa_message_id": msg["id"],
                        }
                        # update_crm(crm_data)
    return {"status": "ok"}
```

## דוגמאות

### דוגמה 1: מערכת תזכורות תורים
המשתמש אומר: "הקם תזכורות תורים בוואטסאפ למרפאת השיניים שלי בעברית."
פעולות:
1. תיצרו תבנית UTILITY בעברית עם משתנים לשם המרפאה, תאריך ושעה.
2. תוסיפו כפתורי תגובה מהירה לאישור/שינוי.
3. תגדירו כללי תזמון (בלי שליחה בשבת).
4. תספקו קוד אינטגרציה למערכת ניהול המרפאה.
תוצאה: תבנית UTILITY מאושרת עם אוטומציית שליחה ובדיקות עמידה בתקנות. תבניות UTILITY שנשלחות בתוך חלון שירות פתוח של 24 שעות הן חינם; מחוץ לחלון מחויבים לפי הודעת תבנית.

### דוגמה 2: עדכוני הזמנות למסחר אלקטרוני
המשתמש אומר: "אני רוצה לשלוח אישורי הזמנה ועדכוני משלוח דרך וואטסאפ."
פעולות:
1. תיצרו תבנית UTILITY לאישור הזמנה (עברית).
2. תיצרו תבנית UTILITY לעדכון משלוח עם קישור מעקב.
3. תגדירו webhook נכנס לקבלת עדכוני סטטוס מסירה.
4. תשלבו עם ספקי משלוחים ישראליים (צ'יטה, HFD, דואר ישראל, ימית, Yango Delivery).
תוצאה: מערכת הודעות אוטומטית למחזור חיי הזמנה בעברית, עם חיוב חזוי לפי הודעת תבנית.

### דוגמה 3: קמפיין שיווקי
המשתמש אומר: "שלח מבצע לרשימת הלקוחות שלנו לקראת מכירת חג."
פעולות:
1. תוודאו עמידה (תיעוד opt-in, חוק הספאם, תיקון 13 לחוק הגנת הפרטיות).
2. תיצרו תבנית MARKETING עם פרטי ההצעה ושורת opt-out ברורה.
3. תתזמנו לשעות עסקים בישראל (להימנע משבת ומערבי חג).
4. תעקבו אחר מסירה, קריאה ותגובות; תכבדו opt-out מיד.
תוצאה: קמפיין פרסומי תקני עם תזמון ישראלי וחיוב לפי הודעת marketing.

## משאבים מצורפים

### סקריפטים
- `scripts/send_whatsapp.py`: שולח הודעות WhatsApp Business דרך Meta Cloud API לשוק הישראלי. תומך בהודעות תבנית (עם החלפת שפה ופרמטרים) ובהודעות טקסט חופשי בחלון השיחה של 24 שעות. כולל אימות מספרי טלפון ישראליים ובדיקות זמן שליחה מותאמות לשבת. הרצה: `python scripts/send_whatsapp.py --help`

## קישורים חיצוניים

- WhatsApp Cloud API, סקירה: https://developers.facebook.com/docs/whatsapp/cloud-api
- Graph API changelog (לאיתור הגרסה היציבה הנוכחית): https://developers.facebook.com/docs/graph-api/changelog
- תמחור WhatsApp (לפי תבנית, בתוקף מיולי 2024): https://developers.facebook.com/docs/whatsapp/pricing
- הנחיות תבניות WhatsApp: https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates
- חוק התקשורת תיקון 40 (חוק הספאם), משרד התקשורת: https://www.gov.il/he/departments/ministry_of_communications
- חוק הגנת הפרטיות תיקון 13 (בתוקף 14 באוגוסט 2025), הרשות להגנת הפרטיות: https://www.gov.il/he/departments/the_privacy_protection_authority
- 360dialog (BSP): https://www.360dialog.com/
- MessageBird/Bird (BSP): https://bird.com/
- Twilio WhatsApp Business: https://www.twilio.com/en-us/messaging/channels/whatsapp
- Infobip WhatsApp: https://www.infobip.com/whatsapp-business
- Vonage WhatsApp: https://developer.vonage.com/en/messaging/sms/overview
- אוטומציות Monday.com: https://support.monday.com/hc/en-us/categories/115000091445

## מלכודות נפוצות

- מספרי טלפון ישראליים ל-WhatsApp API חייבים להשתמש בקידומת 972 ללא האפס המוביל: `+972521234567`, לא `+9720521234567`. סוכנים כוללים את האפס המיותר לעיתים קרובות, מה שגורם לשגיאת "המספר לא נמצא ב-WhatsApp".
- תבניות הודעות בעברית חייבות לעבור בדיקה של Meta. תבניות UTILITY עם שפה שיווקית נדחות לעיתים קרובות (היה צריך MARKETING). תבניות עם טקסט עברי בבלוקי קוד או בלי דוגמאות למשתנים גם נדחות.
- עסקים ישראליים ששולחים שיווק ב-WhatsApp חייבים לעמוד בתיקון 40 לחוק התקשורת (חוק הספאם), ומאז אוגוסט 2025 גם בתיקון 13 לחוק הגנת הפרטיות. נדרשת הסכמה מפורשת מראש (opt-in), לא רק "קשר עסקי קיים".
- ל-WhatsApp Business יש חלון שירות לקוחות של 24 שעות. אחרי 24 שעות מאז ההודעה האחרונה של המשתמש, אפשר לשלוח רק תבניות מאושרות מראש, ובהתאם לקטגוריה הן יחויבו לפי הודעת תבנית במודל התמחור החדש (מיולי 2024).
- טקסט עברי במשתני תבנית עלול לשבור את עיצוב ההודעה כשהוא מעורב עם מספרים או אנגלית. תשתמשו בתווי Unicode isolate (U+2066 עד U+2069) סביב תוכן מעורב כיוונים, או תעצבו תבניות כך שהמשתנים לא יכילו טקסט מעורב.
- תמחור לפי תבנית (מ-1 ביולי 2024): קטגוריות utility/authentication/marketing מחויבות לפי הודעת תבנית, לא לפי שיחת 24 שעות. יש קצבה חינמית לכל WABA. תבדקו תמיד את דף התמחור של Meta לפני שאתם מצטטים תעריפים ישראליים ללקוח. התעריפים משתנים.

## פתרון בעיות

### שגיאה: "התבנית נדחתה"
סיבה: התבנית מפרה את מדיניות WhatsApp או שיש בה בעיות עיצוב.
פתרון: תוודאו שהטקסט בעברית מעוצב כראוי, אין תוכן אסור (הימורים, תוכן למבוגרים, מוצרים מפוקחים), שיש דוגמאות ריאליות למשתנים, ושהקטגוריה תואמת את התוכן (UTILITY חייבת להיות טרנזקציונית, MARKETING חייבת להיות שיווקית).

### שגיאה: "שליחת ההודעה נכשלה"
סיבה: מספר לא תקין, הנמען לא ב-WhatsApp, חריגה ממגבלת קצב, או ניסיון שליחת טקסט חופשי מחוץ לחלון.
פתרון: תוודאו פורמט `+972` בלי אפס מוביל, תבדקו שלנמען יש WhatsApp, תכבדו את מגבלות הקצב (Cloud API תומך בכ-80 הודעות/שנייה למספר, עם הרחבה לפי quality tier). אם אתם מחוץ לחלון 24 שעות, עברו לתבנית מאושרת.

### שגיאה: "ה-webhook לא מקבל הודעות"
סיבה: כתובת webhook לא אומתה, אפליקציית Meta לא רשומה לשדה `messages`, או אימות חתימה נכשל.
פתרון: תוודאו שכתובת ה-webhook היא HTTPS, שטוקן האימות תואם, שאפליקציית Meta רשומה לשדה `messages` ב-WABA, ושההנדלר שלכם מאמת את `X-Hub-Signature-256` מול ה-App secret.
