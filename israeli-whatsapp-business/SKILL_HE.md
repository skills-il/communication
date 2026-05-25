---
name: israeli-whatsapp-business
description: Integrate WhatsApp Business API for the Israeli market with Hebrew message templates, customer communication, and CRM integration. Use when user asks about WhatsApp Business in Israel, Hebrew WhatsApp templates, WhatsApp marketing to Israeli customers, business messaging via WhatsApp, or integrating WhatsApp with Israeli CRM tools (Monday.com, Priority, etc.). Covers Cloud API setup, template creation, conversation pricing, compliance with Israeli anti-spam law and Privacy Law Amendment 13, and Israeli consumer communication preferences. Do NOT use for personal WhatsApp or non-Israeli WhatsApp markets.
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: Requires Meta Business Account and WhatsApp Business API access. Network access required.
version: 1.2.0
---

# וואטסאפ עסקי ישראלי

## הנחיות

### שלב 1: אימות הגדרות WhatsApp Business
תוודאו שלמשתמש יש:
1. חשבון Meta Business (`business.facebook.com`)
2. חשבון WhatsApp Business (WABA) מקושר ל-Meta Business
3. מספר טלפון רשום עם קידומת ישראלית (972+), או דרך ה-Cloud API הרשמי של Meta או דרך BSP (Business Solution Provider). BSPs פעילים שמשרתים חשבונות ישראליים: 360dialog, MessageBird/Bird, Twilio, Infobip, Vonage, Gupshup, AiSensy, Sinch
4. Access Token של System User עם הרשאת `whatsapp_business_messaging` (וגם `whatsapp_business_management` לפעולות תבניות)

```python
import requests

def verify_whatsapp_setup(access_token: str, phone_number_id: str) -> dict:
    """Verify WhatsApp Business API access against the Cloud API."""
    # Use the latest stable Graph API version. Check
    # https://developers.facebook.com/docs/graph-api/changelog for current.
    url = f"https://graph.facebook.com/v25.0/{phone_number_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

### שלב 2: יצירת תבניות הודעות בעברית

**קטגוריות שיחה (מודל התמחור של Meta, חיוב לפי תבנית בתוקף מ-1 ביולי 2025, מחליף את המודל הישן של 24 שעות):**
WhatsApp מחייב היום לפי **הודעת תבנית** בשלוש קטגוריות בתשלום ועוד קטגוריה חינמית:

| קטגוריה | מתי משתמשים | חיוב |
|----------|-------------|---------|
| Utility (שירות) | עדכונים טרנזקציוניים שהמשתמש מצפה להם (אישור הזמנה, משלוח, קבלת תשלום, תזכורת תור) | חינם בתוך חלון שירות פתוח של 24 שעות שהמשתמש פתח; מחוץ לחלון, מחויב לפי הודעת תבנית |
| Authentication (אימות) | OTP וקודי אימות | מחויב לפי הודעת תבנית authentication |
| Marketing (שיווק) | מבצעים, הצעות, ניוזלטרים, החזרת לקוחות | מחויב לפי הודעת תבנית marketing (לרוב הקטגוריה היקרה ביותר) |
| Service (שירות חופשי) | תגובות חופשיות בתוך חלון שירות 24 שעות | חינם, נספר כשיחת שירות |

מודל התמחור הישן ("conversation-based" של 24 שעות לפי קטגוריה) הוצא משימוש ב-1 ביולי 2025 והוחלף בחיוב לפי הודעת תבנית עבור utility, authentication ו-marketing, בתוספת קצבה חינמית לכל WABA. תוודאו את התעריפים הספציפיים לישראל בדף התמחור של Meta לפני שאתם מצטטים מספרים ללקוח, מאחר והם משתנים לפי מדינה ומתעדכנים תקופתית.

**חלונות שליחה חינמיים מעבר לחלון השירות הסטנדרטי של 24 שעות:**
- **חלון שירות לקוחות (CSW) של 24 שעות**: נפתח כשהמשתמש שולח הודעה נכנסת. תגובות חופשיות, תבניות utility וחיוב חינמי בתוך החלון.
- **חלון 72 שעות חינמי לאחר Click-to-WhatsApp (CTWA)**: נפתח כשהמשתמש לוחץ על מודעת CTWA בפייסבוק או באינסטגרם. הודעות בכל קטגוריה חינמיות למשך 72 שעות. דפוס רכישת לקוחות נפוץ מאוד בישראל.
- **תבניות authentication מחויבות גם בתוך ה-CSW** (בניגוד ל-utility שחינמית בחלון). מלכודת שתופסת מוצרי OTP ישראליים (בנקים, ארנקים דיגיטליים).
- **קצבה חינמית**: 1,000 שיחות שירות חינמיות לכל WABA בחודש נכון להיום. בדקו את המספר העדכני בדף התמחור של Meta.

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
    url = f"https://graph.facebook.com/v25.0/{waba_id}/message_templates"
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

**דפוסי דחייה קונקרטיים שראינו בתבניות עבריות:**

| טקסט שנדחה | הסיבה | גרסה שעוברת |
|---|---|---|
| "מבצע!! 20% הנחה רק היום, מהרו!" (ב-UTILITY) | שפה שיווקית וסימני דחיפות בקטגוריית UTILITY | להעביר ל-MARKETING, או לנסח טרנזקציונית: "ההנחה שלך {{1}}% פעילה עד {{2}}." |
| "תזכורת: יש לך תור ב-{{1}}" עם דוגמה `["מחר"]` | פלייסהולדר עמום, לא ערך אמיתי | להשתמש בדוגמה אמיתית כמו `["מרפאת השיניים ד\"ר כהן, 15.06.2026 בשעה 10:00"]` |
| Body עם 6+ משתנים ו-30 תווי טקסט קבועים | יחס דמוי ספאם של משתנים לטקסט | להפחית ל-3 משתנים לכל היותר, להוסיף מילות קישור טבעיות |
| "{{1}}{{2}}" בלי מפריד ובלי קוד שפה | חסר footer ולא ברור באיזו שפה | להגדיר במפורש `language: "he"` ולהוסיף שורת footer כמו "להסרה השיבו 'הסר'" |

### שלב 3: שליחת הודעות

**שליחת הודעת תבנית:**
```python
def send_template_message(phone_number_id: str, access_token: str,
                          to: str, template_name: str, language: str,
                          parameters: list):
    """Send a WhatsApp template message."""
    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"
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
    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"
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

### שלב 3.5: דירוג איכות וחימום מספר

WhatsApp מקצה לכל מספר עסקי דירוג איכות (ירוק, צהוב, אדום). מטא מעריכה מחדש את הדירוג כל 6 שעות לפי דיווחי ספאם, שיעור חסימה, ויחס דחיית תבניות. דירוג צהוב או אדום מגביל את כמות המשתמשים שאפשר לפנות אליהם ב-24 שעות, ודירוג אדום מתמשך עלול לעצור שליחה לחלוטין.

**חימום מספר ישראלי חדש (30 הימים הראשונים קריטיים):**

1. **ימים 1-7**: שולחים רק תבניות UTILITY ללקוחות שביצעו opt-in ומצפים להן (אישור הזמנה, OTP). בלי שיווק.
2. **ימים 7-14**: מתחילים אצוות שיווק קטנות (50-200 נמענים), רק למשתמשים שביצעו opt-in ב-30 הימים האחרונים.
3. **ימים 14-30**: סקיילינג הדרגתי. עוצרים מיד אם האיכות יורדת לצהוב.
4. **תמיד**: שורת opt-out ברורה בתבניות שיווק ("להסרה השיבו 'הסר'") וטיפול בהסרות בתוך דקות (חוסמים את ה-wa_id ברשימת השליחה).

**כשהאיכות יורדת לצהוב**: עוצרים שיווק ל-48 שעות, שולחים רק UTILITY למשתמשים פעילים, בודקים תבניות אחרונות לסטייה שיווקית, ועוברים על מקור ה-opt-in של הסגמנט שנפגע.

**מגבלות שליחה מאז אוקטובר 2025 חלות לפי Business Portfolio ולא לפי מספר טלפון**, כלומר העברת קמפיין למספר חדש לא תאפס את המגבלה אם המספר החדש נמצא תחת אותו portfolio. portfolio חדש מתחיל בתקרה יומית נמוכה (~250 שיחות שיווק למשתמשים ייחודיים נכון להיום) ומתקדם לפי הערכת מטא ברמת ה-portfolio של ניצול ואיכות. התייחסו לטבלת השכבות הישנה לפי מספר טלפון (1k → 10k → 100k → unlimited) כ-legacy. בדקו את התקרה הנוכחית שלכם ב-Business Manager → WhatsApp Manager → Insights.

### שלב 4: תזמון ועמידה בתקנות בישראל

שליחת WhatsApp מסחרי בישראל כפופה לתיקון 40 לחוק התקשורת (בזק ושידורים), הידוע כחוק הספאם, ומאז 14 באוגוסט 2025 גם לתיקון 13 לחוק הגנת הפרטיות, שהחמיר את החובות על מי שמעבד מידע אישי וקירב את הדין הישראלי לרגולציית ה-GDPR. שיווק ב-WhatsApp דורש opt-in מפורש מראש בדיוק כמו SMS, ועיבוד לא חוקי של מספרי טלפון יכול להוביל לקנסות מנהליים מצד הרשות להגנת הפרטיות.

**לוח זמנים לשליחה בשוק הישראלי** (הגבלות יום שישי 14:00 ויום שבת 20:00 בקוד למטה הן היוריסטיקה שמרנית. שעות הכניסה והיציאה האמיתיות של שבת משתנות ב-30-60 דקות לפי עונה וערים. לשימוש בייצור, גזרו את שעות הכניסה והיציאה מ-API בסגנון Hebcal לפי מיקום המשתמש):
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

### שלב 4.5: מעבר לתבניות (Flows, שיחות קוליות, קטלוג, CTWA)

פיצ'רים נפוצים של 2025-2026 שעסקים ישראליים שואלים עליהם, לפי עדיפות:

- **WhatsApp Flows**: טפסים נטיביים מרובי-שלבים (איסוף לידים, קביעת תור, סקרים) שמופיעים בתוך הצ'אט. רק ב-Cloud API. מחליף הרבה דפוסים של "טופס Google מקושר מ-WhatsApp". שימושי לקבלת לקוחות בקופות חולים ומרפאות, ליווי לידים בנדל"ן, הזמנת מקום במסעדות.
- **Click-to-WhatsApp ads (CTWA)**: מודעות פייסבוק או אינסטגרם שפותחות צ'אט עם העסק. פותחות את חלון 72 השעות החינמי שתואר למעלה. ערוץ הרכישה בתשלום הדומיננטי בישראל ל-WhatsApp.
- **WhatsApp Business Calling API**: שיחות קוליות ממספר עסקי מאומת. הוכרז ביולי 2025, עם הרחבה לרמת SMB בשלבים דרך BSPs לאורך 2026. הכיסוי לפי מדינה ולפי BSP אינו אחיד. בדקו במסמכי ה-calling API הרשמיים ובמסך ה-BSP שלכם מה הזמינות הנוכחית בישראל לפני שאתם מתכננים flow שתלוי בשיחות. תמחור נפרד מהודעות (תעריפי Meta business calling).
- **קטלוג ומסחר**: קטלוגי מוצרים וכרטיסי מוצר בצ'אט. שימו לב: WhatsApp Pay לא זמין בישראל (המוצר הושק רק בברזיל, הודו וסינגפור). תהליך תשלום חייב להפנות לעמוד תשלום משלכם (קארדקום, טרנזילה, פלאקארד, ביט, Apple/Google Pay וכו').
- **העברת מספר טלפון בין BSPs**: חייבים להסיר את ה-PIN של אימות דו-שלבי לפני ההעברה. צריך לתכנן חלון תחזוקה כי הודעות שבתעבורה עלולות להידלף. תיעוד מזהה מספר הטלפון במקור לפני התחלת ההעברה.
- **תמיכה ב-On-Premises API הסתיימה (הגרסה הסופית פגה ב-23 באוקטובר 2025).** יש להעביר deployments ישנים מ-On-Prem ל-Cloud API או ל-gateway של BSP. אל תמליצו על מסלול On-Prem למשתמשים חדשים.

**הגבלת עוזרי AI כלליים (בתוקף מ-15 בינואר 2026):** מטא כבר לא מאשרת צ'אטבוטים מבוססי AI לשימוש כללי ב-WhatsApp Business. בוטים ייעודיים (שירות לקוחות, קביעת תורים, שאלות על מוצרים, סטטוס הזמנות) ממשיכים להיות מותרים. זה משפיע על שוק העטיפות הישראליות של ChatGPT ל-WhatsApp.

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
- Vonage WhatsApp: https://developer.vonage.com/en/messages/concepts/whatsapp
- Gupshup WhatsApp: https://www.gupshup.io/channels/whatsapp
- AiSensy (BSP, פופולרי בעסקים קטנים): https://www.aisensy.com/
- Sinch WhatsApp: https://www.sinch.com/products/messaging/whatsapp/
- אוטומציות Monday.com: https://support.monday.com/hc/en-us/categories/115000091445
- סקירת WhatsApp Flows: https://developers.facebook.com/docs/whatsapp/flows
- WhatsApp Business Calling API: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/calling
- הודעת סיום תמיכה ל-On-Premises API (הגרסה הסופית פגה ב-23 באוקטובר 2025): https://developers.facebook.com/docs/whatsapp/on-premises/sunset

## מלכודות נפוצות

- מספרי טלפון ישראליים ל-WhatsApp API חייבים להשתמש בקידומת 972 ללא האפס המוביל: `+972521234567`, לא `+9720521234567`. סוכנים כוללים את האפס המיותר לעיתים קרובות, מה שגורם לשגיאת "המספר לא נמצא ב-WhatsApp".
- תבניות הודעות בעברית חייבות לעבור בדיקה של Meta. תבניות UTILITY עם שפה שיווקית נדחות לעיתים קרובות (היה צריך MARKETING). תבניות עם טקסט עברי בבלוקי קוד או בלי דוגמאות למשתנים גם נדחות.
- עסקים ישראליים ששולחים שיווק ב-WhatsApp חייבים לעמוד בתיקון 40 לחוק התקשורת (חוק הספאם), ומאז אוגוסט 2025 גם בתיקון 13 לחוק הגנת הפרטיות. נדרשת הסכמה מפורשת מראש (opt-in), לא רק "קשר עסקי קיים".
- ל-WhatsApp Business יש חלון שירות לקוחות של 24 שעות. אחרי 24 שעות מאז ההודעה האחרונה של המשתמש, אפשר לשלוח רק תבניות מאושרות מראש, ובהתאם לקטגוריה הן יחויבו לפי הודעת תבנית במודל התמחור החדש (מיולי 2024).
- טקסט עברי במשתני תבנית עלול לשבור את עיצוב ההודעה כשהוא מעורב עם מספרים או אנגלית. תשתמשו בתווי Unicode isolate (U+2066 עד U+2069) סביב תוכן מעורב כיוונים, או תעצבו תבניות כך שהמשתנים לא יכילו טקסט מעורב.
- תמחור לפי תבנית (מ-1 ביולי 2025): קטגוריות utility/authentication/marketing מחויבות לפי הודעת תבנית, לא לפי שיחת 24 שעות. יש קצבה חינמית לכל WABA. תבדקו תמיד את דף התמחור של Meta לפני שאתם מצטטים תעריפים ישראליים ללקוח. התעריפים משתנים.
- **תקרת תדירות לתבניות שיווק למשתמש (הטמעה הדרגתית)**: מטא מבצעת deploy של תקרת תדירות לתבניות שיווק כדי להפחית ספאם בשווקים נבחרים. נכון להיום התקרה נאכפת על משתמשים עם קידומת הודו (+91); מטא הודיעה על הרחבה אבל נמענים ישראלים (+972) אינם כפופים לתקרה קשיחה מתועדת נכון לעדכון זה. בדקו את היקף ההטמעה בדפי התמחור/מדיניות של Meta לפני שאתם מניחים שהתקרה בתוקף לקמפיין הישראלי שלכם, ותכננו את ה-opt-in כאילו תקרה כזו מגיעה.
- **מגבלות שליחה הן ברמת Business Portfolio מאז אוקטובר 2025**, לא ברמת מספר טלפון. הוספת מספר שני תחת אותו portfolio לא תכפיל את התקרה היומית.
- **תבניות authentication מחויבות גם בתוך חלון השירות של 24 שעות**, בניגוד ל-utility שחינמית בחלון. מוצרי OTP ישראליים (בנקים, ארנקים דיגיטליים, אימות זהות) מפספסים את זה לעיתים קרובות.
- **קידומות נייד ישראליות שמקובלות ב-WhatsApp**: 050 (פלאפון), 051 (We4G), 052 (סלקום), 053 (HOT Mobile), 054 (פרטנר), 055 (מפעילים וירטואליים), 058 (גולן טלקום). רגקס אימות שמחריג 051 ידחה מנויים אמיתיים.

## פתרון בעיות

### שגיאה: "התבנית נדחתה"
סיבה: התבנית מפרה את מדיניות WhatsApp או שיש בה בעיות עיצוב.
פתרון: תוודאו שהטקסט בעברית מעוצב כראוי, אין תוכן אסור (הימורים, תוכן למבוגרים, מוצרים מפוקחים), שיש דוגמאות ריאליות למשתנים, ושהקטגוריה תואמת את התוכן (UTILITY חייבת להיות טרנזקציונית, MARKETING חייבת להיות שיווקית).

### שגיאה: "שליחת ההודעה נכשלה"
סיבה: מספר לא תקין, הנמען לא ב-WhatsApp, חריגה ממגבלת קצב, או ניסיון שליחת טקסט חופשי מחוץ לחלון.
פתרון: תוודאו פורמט `+972` בלי אפס מוביל, תבדקו שלנמען יש WhatsApp, תכבדו את מגבלות הקצב (Cloud API ברירת מחדל כ-80 הודעות/שנייה למספר עסקי, סקיילינג עד ~1,000 הודעות/שנייה בחשבונות Unlimited; מגבלות שיחה יומיות חלות לפי Business Portfolio מאז אוקטובר 2025). אם אתם מחוץ לחלון 24 שעות, עברו לתבנית מאושרת. אם הכשל הוא על תבנית שיווק והנמען עשה opt-in כנדרש, חשדו בתקרה המתגלגלת של 7 ימים למשתמש.

### שגיאה: "ה-webhook לא מקבל הודעות"
סיבה: כתובת webhook לא אומתה, אפליקציית Meta לא רשומה לשדה `messages`, או אימות חתימה נכשל.
פתרון: תוודאו שכתובת ה-webhook היא HTTPS, שטוקן האימות תואם, שאפליקציית Meta רשומה לשדה `messages` ב-WABA, ושההנדלר שלכם מאמת את `X-Hub-Signature-256` מול ה-App secret.
