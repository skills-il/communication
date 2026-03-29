---
name: israeli-whatsapp-business
description: Integrate WhatsApp Business API for the Israeli market with Hebrew message templates, customer communication, and CRM integration. Use when user asks about WhatsApp Business in Israel, Hebrew WhatsApp templates, WhatsApp marketing to Israeli customers, business messaging via WhatsApp, or integrating WhatsApp with Israeli CRM tools (Monday.com, Priority, etc.). Covers Cloud API setup, template creation, compliance with Israeli anti-spam law, and Israeli consumer communication preferences. Do NOT use for personal WhatsApp or non-Israeli WhatsApp markets.
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: Requires Meta Business Account and WhatsApp Business API access. Network access required.
version: 1.0.1
---

# וואטסאפ עסקי ישראלי

## הנחיות

### שלב 1: אימות הגדרות WhatsApp Business
ודאו שלמשתמש יש:
1. חשבון Meta Business (business.facebook.com)
2. חשבון WhatsApp Business מקושר ל-Meta Business
3. מספר טלפון רשום עם קידומת ישראלית (972+)
4. Access Token של System User עם הרשאת `whatsapp_business_messaging`

```python
import requests

def verify_whatsapp_setup(access_token: str, phone_number_id: str) -> dict:
    """Verify WhatsApp Business API access."""
    url = f"https://graph.facebook.com/v27.0/{phone_number_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

### שלב 2: יצירת תבניות הודעות בעברית

**קטגוריות תבניות לעסקים ישראליים:**

| קטגוריה | שימוש | דוגמה (עברית) |
|----------|----------|-------------------|
| תזכורת פגישה | מרפאות, מכוני יופי, שירותים | תזכורת: יש לך תור ב-{{1}} בתאריך {{2}} בשעה {{3}} |
| אישור הזמנה | מסחר אלקטרוני, משלוחים | הזמנתך ({{1}}) התקבלה! נעדכן כשתישלח |
| עדכון משלוח | לוגיסטיקה, משלוחים | המשלוח שלך בדרך! מעקב: {{1}} |
| קבלת תשלום | חיוב, חשבוניות | התקבל תשלום של {{1}} ש"ח. תודה! |
| הודעת ברוכים הבאים | קליטה | שלום {{1}}! ברוכים הבאים ל-{{2}}. איך נוכל לעזור? |
| מעקב תמיכה | שירות לקוחות | שלום {{1}}, רצינו לוודא שהפנייה שלך טופלה. הכל בסדר? |

**הגשת תבנית לאישור:**
```python
def create_template(waba_id: str, access_token: str, template: dict):
    """Create a WhatsApp message template."""
    url = f"https://graph.facebook.com/v27.0/{waba_id}/message_templates"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
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
            "text": "Shalom {{1}},\nReminder: appointment at {{2}} on {{3}} at {{4}}.\nConfirm reply 1, Cancel reply 2.",
            "example": {
                "body_text": [["Israel", "Dr. Cohen Dental Clinic", "15.03.2026", "10:00"]]
            }
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {"type": "QUICK_REPLY", "text": "Confirmed"},
                {"type": "QUICK_REPLY", "text": "Need to reschedule"}
            ]
        }
    ]
}
```

### שלב 3: שליחת הודעות

**שליחת הודעת תבנית:**
```python
def send_template_message(phone_number_id: str, access_token: str,
                          to: str, template_name: str, language: str,
                          parameters: list):
    """Send a WhatsApp template message."""
    url = f"https://graph.facebook.com/v27.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # Format: 972541234567
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": p} for p in parameters
                    ]
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Send appointment reminder
send_template_message(
    phone_number_id="YOUR_PHONE_ID",
    access_token="YOUR_TOKEN",
    to="972541234567",
    template_name="appointment_reminder_he",
    language="he",
    parameters=["Israel", "Dental Clinic", "15.03.2026", "10:00"]
)
```

**שליחת הודעה אינטראקטיבית (בחלון 24 השעות):**
```python
def send_interactive_list(phone_number_id: str, access_token: str,
                          to: str, body_text: str, sections: list):
    """Send an interactive list message in Hebrew."""
    url = f"https://graph.facebook.com/v27.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": body_text},
            "action": {
                "button": "Choose option",
                "sections": sections
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### שלב 4: תזמון ועמידה בתקנות בישראל

**לוח זמנים לשליחה בשוק הישראלי:**
```python
from datetime import datetime, time
import pytz

def is_valid_sending_time() -> tuple[bool, str]:
    """Check if current time is appropriate for Israeli business messaging."""
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now = datetime.now(israel_tz)
    day = now.weekday()  # 0=Monday, 6=Sunday

    # Friday after 14:00 -- pre-Shabbat
    if day == 4 and now.time() > time(14, 0):
        return False, "Pre-Shabbat hours. Send after Saturday 20:00."

    # Saturday before 20:00 -- Shabbat
    if day == 5:
        if now.time() < time(20, 0):
            return False, "Shabbat. Send after 20:00."

    # Sunday-Thursday business hours
    if now.time() < time(8, 30) or now.time() > time(20, 0):
        return False, "Outside business hours. Send between 08:30-20:00."

    return True, "OK to send."

def compliance_checklist(message_type: str) -> list:
    """Return compliance checklist for Israeli WhatsApp messaging."""
    checks = [
        "Recipient opted in to receive WhatsApp messages",
        "Opt-out mechanism included (reply 'remove' to unsubscribe)",
        "Business identity clearly stated",
        "Message in appropriate language (Hebrew/English)",
    ]
    if message_type == "marketing":
        checks.extend([
            "Compliant with Chok HaSpam (Israeli Anti-Spam Law)",
            "Not sending during Shabbat/holidays",
            "Frequency cap respected (avoid over-messaging)",
            "Marketing category template approved by Meta",
        ])
    return checks
```

### שלב 5: הנחיות לאינטגרציה עם CRM

**Monday.com + WhatsApp:**
1. השתמשו בשיטות אינטגרציה של Monday.com (אוטומציות או מחברים של צד שלישי)
2. הפעילו שליחת הודעות WhatsApp בשינוי סטטוס בלוח
3. תעדו הודעות נכנסות כעדכונים ב-Monday.com
4. הגדירו זרימות עבודה אוטומטיות: "כשסטטוס משתנה ל-X, שלח תבנית WhatsApp"

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
                        # Extract message data for CRM
                        crm_data = {
                            "phone": msg["from"],
                            "message": msg.get("text", {}).get("body", ""),
                            "timestamp": msg["timestamp"],
                            "type": msg["type"],
                            "wa_message_id": msg["id"]
                        }
                        # Send to CRM system
                        # update_crm(crm_data)
    return {"status": "ok"}
```

## דוגמאות

### דוגמה 1: מערכת תזכורות תורים
המשתמש אומר: "הקם תזכורות תורים בוואטסאפ למרפאת השיניים שלי בעברית"
פעולות:
1. צרו תבנית בעברית עם משתנים לשם המרפאה, תאריך ושעה
2. הוסיפו כפתורי תגובה מהירה לאישור/שינוי תור
3. הגדירו כללי תזמון (ללא שליחה בשבת)
4. ספקו קוד אינטגרציה למערכת ניהול המרפאה
תוצאה: תבנית מאושרת עם אוטומציית שליחה ובדיקות עמידה בתקנות.

### דוגמה 2: עדכוני הזמנות למסחר אלקטרוני
המשתמש אומר: "אני רוצה לשלוח אישורי הזמנה ועדכוני משלוח דרך וואטסאפ"
פעולות:
1. צרו תבנית אישור הזמנה (בעברית)
2. צרו תבנית עדכון משלוח עם קישור מעקב
3. הגדירו webhook לקבלת עדכוני סטטוס מסירה
4. שלבו עם ספקי משלוחים ישראליים (צ'יטה, HFD, דואר ישראל)
תוצאה: מערכת הודעות אוטומטית למחזור חיי הזמנה בעברית.

### דוגמה 3: קמפיין שיווקי
המשתמש אומר: "שלח מבצע לרשימת הלקוחות שלנו לקראת מכירת חג"
פעולות:
1. בדקו עמידה בתקנות (רשימת הסכמה, חוק הספאם)
2. צרו תבנית שיווקית עם פרטי ההצעה
3. תזמנו לשעות עסקיות מתאימות בישראל
4. הגדירו מעקב אחר שיעורי פתיחה ותגובות
תוצאה: קמפיין פרסומי תקני עם תזמון ישראלי.

## משאבים מצורפים

### סקריפטים
- `scripts/send_whatsapp.py` — שולח הודעות WhatsApp Business דרך Meta Cloud API לשוק הישראלי. תומך בהודעות תבנית (עם החלפת שפה ופרמטרים) ובהודעות טקסט חופשי בחלון השיחה של 24 שעות. כולל אימות מספרי טלפון ישראליים ובדיקות זמן שליחה מותאמות לשבת. הרצה: `python scripts/send_whatsapp.py --help`

## מלכודות נפוצות

- מספרי טלפון ישראליים ל-WhatsApp API חייבים להשתמש בקידומת 972 ללא האפס המוביל: +972521234567, לא +9720521234567. סוכנים כוללים את האפס המיותר לעיתים קרובות.
- תבניות הודעות WhatsApp בעברית חייבות לעבור בדיקה של Meta. תבניות עם טקסט עברי בבלוקי קוד עלולות להידחות כי בלוקי קוד לא תומכים ב-RTL כראוי.
- עסקים ישראליים ששולחים הודעות שיווק ב-WhatsApp חייבים לעמוד בתיקון 40 לחוק התקשורת (נגד ספאם). נדרשת הסכמה מפורשת מראש (opt-in), לא רק קשר עסקי קיים.
- ל-WhatsApp Business API יש חלון שירות לקוחות של 24 שעות. אחרי 24 שעות, רק הודעות תבנית מאושרות מראש ניתנות לשליחה. סוכנים עלולים לא להתחשב בכך בעיצוב תהליכי שיחה.
- טקסט עברי במשתני תבנית WhatsApp עלול לשבור את עיצוב ההודעה כשהוא מעורב עם מספרים או אנגלית. יש להשתמש בתווי Unicode isolate (U+2066/U+2069) סביב תוכן מעורב כיוונים.

## פתרון בעיות

### שגיאה: "התבנית נדחתה"
סיבה: התבנית מפרה את מדיניות WhatsApp או בעיות עיצוב
פתרון: ודאו שהטקסט בעברית מעוצב כראוי, ללא תוכן אסור (הימורים, מבוגרים), משתנים כוללים דוגמאות, והקטגוריה תואמת את סוג התוכן.

### שגיאה: "שליחת ההודעה נכשלה"
סיבה: מגוון -- מספר לא תקין, המשתמש לא בוואטסאפ, חריגה ממגבלת קצב
פתרון: ודאו פורמט 972+, בדקו שלמשתמש יש WhatsApp, כבדו מגבלות קצב (80 הודעות/שנייה ב-Cloud API).

### שגיאה: "ה-webhook לא מקבל הודעות"
סיבה: כתובת webhook לא אומתה או אפליקציית Meta לא מוגדרת
פתרון: ודאו שכתובת ה-webhook היא HTTPS, אסימון האימות תואם, ואפליקציית Meta רשומה ל-webhook של הודעות.