# אוטומציית ווטסאפ ישראלית

## הוראות

### שלב 1: עיצוב תהליכי שיחה לצ'אטבוט

עצבו תהליכי צ'אטבוט בעברית שמתאימים לדפוסי תקשורת ישראליים. משתמשים ישראליים מצפים לתקשורת ישירה, לא פורמלית עם פתרון מהיר.

**מבנה תהליך צ'אטבוט ישראלי נפוץ:**

```python
CHATBOT_FLOWS = {
    "greeting": {
        "trigger": ["shalom", "hi", "hey"],
        "response_he": "שלום! איך אפשר לעזור? בחר/י אפשרות:",
        "options": [
            {"id": "1", "text_he": "מעקב הזמנה", "text_en": "Track order", "next": "order_tracking"},
            {"id": "2", "text_he": "שעות פעילות", "text_en": "Business hours", "next": "hours"},
            {"id": "3", "text_he": "דבר/י עם נציג", "text_en": "Speak to agent", "next": "handoff"},
        ]
    },
    "order_tracking": {
        "trigger": ["order", "tracking", "הזמנה", "מעקב"],
        "response_he": "מה מספר ההזמנה שלך?",
        "expects_input": True,
        "input_validation": r"^[A-Z0-9]{6,12}$",
        "next": "order_status_lookup"
    },
    "hours": {
        "trigger": ["hours", "open", "שעות", "פתוח"],
        "response_he": (
            "שעות הפעילות שלנו:\n"
            "ראשון-חמישי: 09:00-18:00\n"
            "שישי: 09:00-13:00\n"
            "שבת: סגור\n\n"
            "צריך/ה עוד משהו?"
        ),
        "next": "greeting"
    },
    "handoff": {
        "trigger": ["agent", "human", "נציג", "אדם"],
        "response_he": "מעביר/ה אותך לנציג. זמן המתנה משוער: כ-3 דקות.",
        "action": "transfer_to_agent"
    }
}
```

**בניית הודעה אינטראקטיבית לתפריט צ'אטבוט:**
```python
import requests

def send_chatbot_menu(phone_number_id: str, access_token: str,
                      to: str, menu_items: list) -> dict:
    """שליחת הודעת רשימה אינטראקטיבית כתפריט צ'אטבוט."""
    url = f"https://graph.facebook.com/v21.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    sections = [{
        "title": "אפשרויות",
        "rows": [
            {"id": item["id"], "title": item["text_he"]}
            for item in menu_items
        ]
    }]
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": "שלום! איך אפשר לעזור?"},
            "action": {
                "button": "בחר/י אפשרות",
                "sections": sections
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### שלב 2: יישום תזמון מודע לשבת וחגים

אוטומציה ישראלית חייבת לכבד שבת (מערב שישי עד מוצאי שבת) וחגים יהודיים. הודעות שנשלחות בזמנים אלה נתפסות כחוסר כבוד וגורמות לשיעורי הסרה גבוהים.

```python
from datetime import datetime, time, timedelta
import pytz

# חגים יהודיים עיקריים (תאריכים גרגוריאניים משוערים -- יש לעדכן מדי שנה)
# אלה הם ערבי החגים שבהם החגים מתחילים (יש להפסיק הודעות לפני השקיעה)
JEWISH_HOLIDAYS_2026 = [
    ("2026-03-01", "2026-03-02", "Purim"),
    ("2026-04-01", "2026-04-09", "Pesach"),
    ("2026-04-28", "2026-04-29", "Yom HaAtzmaut"),
    ("2026-05-21", "2026-05-22", "Shavuot"),
    ("2026-09-11", "2026-09-13", "Rosh Hashana"),
    ("2026-09-20", "2026-09-21", "Yom Kippur"),
    ("2026-09-25", "2026-10-03", "Sukkot"),
]

def is_shabbat(dt: datetime) -> bool:
    """בדיקה אם התאריך נופל בשבת (שישי 16:00 עד שבת 20:00 שעון ישראל)."""
    israel_tz = pytz.timezone("Asia/Jerusalem")
    local = dt.astimezone(israel_tz)
    day = local.weekday()  # 0=שני, 4=שישי, 5=שבת

    # שישי אחרי 16:00 (לפני השקיעה, שמרני)
    if day == 4 and local.time() >= time(16, 0):
        return True
    # שבת לפני 20:00
    if day == 5 and local.time() < time(20, 0):
        return True
    return False

def is_jewish_holiday(dt: datetime, holidays: list = None) -> tuple[bool, str]:
    """בדיקה אם התאריך נופל בחג יהודי."""
    if holidays is None:
        holidays = JEWISH_HOLIDAYS_2026
    date_str = dt.strftime("%Y-%m-%d")
    for start, end, name in holidays:
        if start <= date_str <= end:
            return True, name
    return False, ""

def get_next_valid_send_time(dt: datetime = None) -> datetime:
    """חישוב הזמן התקף הבא לשליחת הודעה בישראל."""
    israel_tz = pytz.timezone("Asia/Jerusalem")
    if dt is None:
        dt = datetime.now(israel_tz)
    else:
        dt = dt.astimezone(israel_tz)

    max_attempts = 14  # מניעת לולאה אינסופית (עד שבועיים קדימה)
    for _ in range(max_attempts):
        if is_shabbat(dt):
            # הזזה לשבת 20:00
            if dt.weekday() == 4:  # שישי
                dt = dt + timedelta(days=1)
            dt = dt.replace(hour=20, minute=0, second=0, microsecond=0)
            continue

        holiday, name = is_jewish_holiday(dt)
        if holiday:
            dt = dt + timedelta(days=1)
            dt = dt.replace(hour=9, minute=0, second=0, microsecond=0)
            continue

        # שעות עסקים: 09:00-20:00
        if dt.time() < time(9, 0):
            dt = dt.replace(hour=9, minute=0, second=0, microsecond=0)
        elif dt.time() >= time(20, 0):
            dt = dt + timedelta(days=1)
            dt = dt.replace(hour=9, minute=0, second=0, microsecond=0)
            continue

        return dt

    return dt

def schedule_campaign(messages: list, start_time: datetime = None,
                      rate_per_hour: int = 500) -> list:
    """תזמון אצווה של הודעות תוך כיבוד שבת וחגים."""
    israel_tz = pytz.timezone("Asia/Jerusalem")
    if start_time is None:
        start_time = datetime.now(israel_tz)

    current_time = get_next_valid_send_time(start_time)
    interval = timedelta(seconds=3600 / rate_per_hour)
    schedule = []

    for msg in messages:
        send_at = get_next_valid_send_time(current_time)
        schedule.append({
            "to": msg["to"],
            "template": msg["template"],
            "scheduled_at": send_at.isoformat(),
            "status": "queued"
        })
        current_time = send_at + interval

    return schedule
```

### שלב 3: בניית רצפי תגובה אוטומטית

הגדירו רצפי תגובה אוטומטית לתרחישים עסקיים ישראליים נפוצים.

**תהליך אישור הזמנה:**
```python
ORDER_CONFIRMATION_FLOW = {
    "step_1_confirmation": {
        "delay_minutes": 0,
        "template": "order_confirmed_he",
        "params": ["order_id", "total_nis", "estimated_delivery"],
        "message_he": "ההזמנה שלך ({order_id}) התקבלה! סה\"כ: {total_nis} ש\"ח. משלוח משוער: {estimated_delivery}"
    },
    "step_2_shipped": {
        "trigger": "status_change_to_shipped",
        "template": "order_shipped_he",
        "params": ["order_id", "tracking_url"],
        "message_he": "ההזמנה ({order_id}) נשלחה! עקוב/י אחרי המשלוח: {tracking_url}"
    },
    "step_3_delivered": {
        "trigger": "status_change_to_delivered",
        "template": "order_delivered_he",
        "params": ["order_id"],
        "message_he": "ההזמנה ({order_id}) נמסרה! מקווים שנהנית. נשמח לשמוע מה חשבת."
    },
    "step_4_review_request": {
        "delay_days": 3,
        "after_step": "step_3_delivered",
        "template": "review_request_he",
        "params": ["customer_name", "product_name"],
        "message_he": "שלום {customer_name}, איך {product_name}? נשמח אם תשאיר/י חוות דעת קצרה."
    }
}

APPOINTMENT_REMINDER_FLOW = {
    "step_1_day_before": {
        "delay_before_appointment": "24h",
        "template": "appointment_reminder_24h_he",
        "params": ["customer_name", "business_name", "date", "time"],
        "message_he": "שלום {customer_name}, תזכורת: יש לך תור ב-{business_name} מחר ({date}) בשעה {time}. אשר/י או בטל/י."
    },
    "step_2_morning_of": {
        "delay_before_appointment": "3h",
        "template": "appointment_reminder_3h_he",
        "params": ["business_name", "time", "address"],
        "message_he": "התור שלך ב-{business_name} בעוד 3 שעות ({time}). כתובת: {address}. צריך/ה לשנות?"
    },
    "step_3_followup": {
        "delay_after_appointment": "2h",
        "template": "appointment_followup_he",
        "params": ["business_name"],
        "message_he": "תודה שביקרת ב-{business_name}! איך היה? נשמח לשמוע."
    }
}

DELIVERY_NOTIFICATION_FLOW = {
    "step_1_out_for_delivery": {
        "trigger": "status_out_for_delivery",
        "template": "delivery_otw_he",
        "params": ["order_id", "eta_window"],
        "message_he": "ההזמנה ({order_id}) בדרך אליך! חלון הגעה משוער: {eta_window}."
    },
    "step_2_arriving": {
        "trigger": "driver_nearby",
        "template": "delivery_arriving_he",
        "params": ["minutes_away"],
        "message_he": "השליח בדרך אליך! זמן הגעה משוער: {minutes_away} דקות."
    },
    "step_3_delivered": {
        "trigger": "delivery_confirmed",
        "template": "delivery_done_he",
        "params": ["order_id"],
        "message_he": "ההזמנה ({order_id}) נמסרה בהצלחה! תודה."
    }
}
```

### שלב 4: הסכמת צרכן ישראלי להודעות אוטומטיות

הודעות ווטסאפ אוטומטיות כפופות לאותם כללי חוק הספאם כמו הודעות מסחריות אחרות. שיקולים נוספים לאוטומציה:

```python
def validate_automation_consent(phone: str, consent_db: dict,
                                 automation_type: str) -> dict:
    """אימות הסכמה להודעות ווטסאפ אוטומטיות."""
    record = consent_db.get(phone)
    if not record:
        return {"allowed": False, "reason": "לא נמצא רישום הסכמה"}

    if not record.get("is_active", False):
        return {"allowed": False, "reason": "ההסכמה בוטלה"}

    channels = record.get("channels", [])
    if "whatsapp" not in channels:
        return {"allowed": False, "reason": "אין הסכמה לווטסאפ (רק: " + ", ".join(channels) + ")"}

    # הודעות טרנזקציוניות (עדכוני הזמנה) בעלות הרשאה רחבה יותר
    if automation_type == "transactional":
        return {"allowed": True, "reason": "הודעות טרנזקציוניות מותרות ללקוחות קיימים"}

    # אוטומציית שיווק דורשת הסכמה מפורשת לשיווק
    if automation_type == "marketing":
        if not record.get("marketing_consent", False):
            return {"allowed": False, "reason": "אין הסכמה לשיווק עבור הודעות אוטומטיות"}

    return {"allowed": True, "reason": "ההסכמה אומתה"}

def build_opt_in_flow() -> dict:
    """יצירת תהליך הסכמה (opt-in) לווטסאפ בתאימות ישראלית."""
    return {
        "initial_message": {
            "he": "ברוכים הבאים! האם תרצה/י לקבל עדכונים מאיתנו בוואטסאפ?",
            "buttons": [
                {"id": "optin_yes", "title": "כן, אשמח"},
                {"id": "optin_no", "title": "לא, תודה"}
            ]
        },
        "confirm_message": {
            "he": "מעולה! תקבל/י מאיתנו עדכוני הזמנות ומבצעים. תמיד אפשר להסיר בהודעת 'הסר'.",
        },
        "opt_out_keywords": ["הסר", "הפסק", "stop", "remove", "הסרה"],
        "opt_out_response": {
            "he": "הוסרת מרשימת התפוצה. לא תקבל/י יותר הודעות שיווקיות."
        }
    }
```

### שלב 5: דפוסי אינטגרציה עם CRM

**אינטגרציית אוטומציה עם Monday.com:**
```python
def monday_com_whatsapp_automation(board_id: str, api_key: str) -> dict:
    """הגדרת טריגרים לאוטומציית Monday.com עבור הודעות ווטסאפ."""
    automations = {
        "new_lead": {
            "trigger": "כשסטטוס משתנה ל-'ליד חדש'",
            "action": "שליחת תבנית ברוכים הבאים בווטסאפ",
            "template": "welcome_lead_he",
            "timing": "מיידי (בתוך שעות עסקים)"
        },
        "follow_up": {
            "trigger": "כשמגיע תאריך (עמודת מעקב)",
            "action": "שליחת תבנית מעקב בווטסאפ",
            "template": "follow_up_he",
            "timing": "09:00 בתאריך המתוזמן"
        },
        "deal_won": {
            "trigger": "כשסטטוס משתנה ל-'עסקה נסגרה'",
            "action": "שליחת תודה + שלבים הבאים בווטסאפ",
            "template": "deal_won_he",
            "timing": "מיידי (בתוך שעות עסקים)"
        },
        "inactive_reminder": {
            "trigger": "כש-last_activity_date > 30 ימים",
            "action": "שליחת הודעת חידוש קשר בווטסאפ",
            "template": "reengagement_he",
            "timing": "10:00 ביום העסקים הבא"
        }
    }
    return automations

def hubspot_israel_whatsapp_config() -> dict:
    """הגדרת אוטומציית ווטסאפ ל-HubSpot ישראל."""
    return {
        "workflow_triggers": [
            {
                "name": "רצף טיפוח לידים",
                "trigger": "מאפיין איש קשר 'lifecycle_stage' = 'Lead'",
                "delay": "יום 1",
                "template": "nurture_step1_he",
                "check_shabbat": True
            },
            {
                "name": "משוב לאחר רכישה",
                "trigger": "מאפיין עסקה 'dealstage' = 'Closed Won'",
                "delay": "3 ימים",
                "template": "feedback_request_he",
                "check_shabbat": True
            },
        ],
        "settings": {
            "timezone": "Asia/Jerusalem",
            "language": "he",
            "shabbat_pause": True,
            "holiday_pause": True,
            "business_hours_only": True,
            "hours_start": "09:00",
            "hours_end": "20:00"
        }
    }
```

### שלב 6: ניהול תור הודעות ומגבלות קצב

```python
from collections import deque

class IsraeliMessageQueue:
    """תור הודעות עם תזמון מודע לשבת והגבלת קצב."""

    def __init__(self, rate_per_second: int = 80):
        self.queue = deque()
        self.rate_per_second = rate_per_second
        self.sent_count = 0

    def enqueue(self, message: dict) -> dict:
        """הוספת הודעה לתור עם בדיקת תזמון."""
        israel_tz = pytz.timezone("Asia/Jerusalem")
        now = datetime.now(israel_tz)

        if is_shabbat(now):
            send_at = get_next_valid_send_time(now)
            message["scheduled_at"] = send_at.isoformat()
            message["status"] = "queued_shabbat"
        else:
            holiday, name = is_jewish_holiday(now)
            if holiday:
                send_at = get_next_valid_send_time(now)
                message["scheduled_at"] = send_at.isoformat()
                message["status"] = f"queued_holiday_{name}"
            else:
                message["scheduled_at"] = now.isoformat()
                message["status"] = "queued"

        self.queue.append(message)
        return message

    def get_queue_stats(self) -> dict:
        """החזרת סטטיסטיקות תור."""
        return {
            "total_queued": len(self.queue),
            "sent": self.sent_count,
            "rate_limit": f"{self.rate_per_second}/sec",
            "shabbat_paused": sum(
                1 for m in self.queue if m.get("status", "").startswith("queued_shabbat")
            ),
            "holiday_paused": sum(
                1 for m in self.queue if m.get("status", "").startswith("queued_holiday")
            )
        }
```

## דוגמאות

### דוגמה 1: צ'אטבוט להזמנת מקום במסעדה
המשתמש אומר: "בנה צ'אטבוט ווטסאפ למסעדה שלי שמטפל בהזמנות מקום בעברית"
פעולות:
1. עצבו תהליך שיחה: ברכה, מספר סועדים, תאריך/שעה, אישור
2. הוסיפו מודעות לשבת (המסעדה עשויה להיות סגורה בשישי בערב/שבת)
3. צרו תבניות תגובה אוטומטית בעברית לכל שלב
4. הגדירו רצפי אישור ותזכורת
תוצאה: צ'אטבוט בעברית עם תהליך הזמנת מקום, תזמון מודע לשבת ותזכורות אוטומטיות.

### דוגמה 2: אוטומציה למסחר אלקטרוני
המשתמש אומר: "הגדירו התראות ווטסאפ אוטומטיות להזמנות בחנות המקוונת שלנו"
פעולות:
1. צרו תהליכי אישור הזמנה, משלוח והודעת מסירה
2. הגדירו השהיית הודעות בשבת ובחגים
3. הוסיפו בקשת חוות דעת 3 ימים אחרי המסירה
4. שלבו עם webhooks של ספקי משלוחים (צ'יטה, HFD, דואר ישראל)
תוצאה: אוטומציה מלאה של מחזור חיי הזמנה עם תאימות תזמון ישראלי.

### דוגמה 3: תזמון קמפיין
המשתמש אומר: "תזמנו קמפיין שיווקי בווטסאפ ל-5,000 לקוחות תוך הימנעות משבת"
פעולות:
1. אמתו הסכמת opt-in לכל הנמענים
2. חשבו לוח זמנים לשליחה תוך כיבוד שבת, חגים ושעות עסקים
3. הגדירו הגבלת קצב (הימנעות מחריגה ממגבלות API)
4. הכניסו הודעות לתור עם השהייה/חידוש אוטומטי בזמנים מוגבלים
תוצאה: קמפיין מתוזמן במלואו עם תזמון מודע לשבת ואימות הסכמה.

### דוגמה 4: אינטגרציית Monday.com
המשתמש אומר: "כשעסקה נסגרת ב-Monday.com, שלח אוטומטית תודה בווטסאפ בעברית"
פעולות:
1. הגדירו טריגר אוטומציה ב-Monday.com על שינוי סטטוס עסקה
2. צרו תבנית תודה בעברית עם שם הלקוח ופרטי העסקה
3. הוסיפו בדיקת שבת לפני שליחה (תור אם בזמן שבת)
4. תעדו הודעה שנשלחה בחזרה ללוח Monday.com כעדכון
תוצאה: אוטומציית ווטסאפ מונעת CRM עם תאימות שעות עסקים ישראליות.

## משאבים מצורפים

### חומרי עזר
- `references/automation-patterns.md` -- דפוסי אוטומציה נפוצים לווטסאפ בישראל כולל תבניות תהליכי צ'אטבוט, רצפי תגובה אוטומטית לניהול הזמנות, מערכות תורים והתראות משלוח. כולל תבניות הודעות בעברית והגדרות תזמון מודעות לשבת. התייעצו בעת עיצוב תהליכי אוטומציה או בחירת דפוסי תבניות.

## פתרון בעיות

### שגיאה: "הודעות לא נשלחות בשעות הצפויות"
סיבה: זיהוי שבת או חג משהה את התור.
פתרון: בדקו את הגדרת לוח החגים. ודאו שאזור הזמן מוגדר ל-Asia/Jerusalem. בדקו סטטיסטיקות תור לראות מספר הודעות מושהות.

### שגיאה: "הצ'אטבוט לא מזהה קלט בעברית"
סיבה: התאמת טקסט עברי עשויה להיכשל עקב הבדלי נורמליזציית Unicode.
פתרון: נרמלו קלט עברי לפני התאמה (נורמליזציית NFC). קחו בחשבון שגיאות כתיב נפוצות ווריאנטים של תעתיק. השתמשו בהתאמה מבוססת מילות מפתח ולא בהתאמת מחרוזת מדויקת.

### שגיאה: "webhook של CRM לא מפעיל הודעת ווטסאפ"
סיבה: בעיית הגדרת webhook ב-Monday.com או HubSpot, או שההודעה בתור עקב מגבלות תזמון.
פתרון: ודאו שכתובת ה-webhook נגישה ומחזירה 200. בדקו אם ההודעה נכנסה לתור עקב שבת/חג. בדקו לוגים של אוטומציית CRM לתנאי הפעלה.

### שגיאה: "חריגה ממגבלת קצב"
סיבה: שליחת יותר מדי הודעות בשנייה דרך WhatsApp Cloud API.
פתרון: WhatsApp Cloud API מאפשר 80 הודעות/שנייה. יישמו הגבלת קצב בתור. לקמפיינים גדולים, פרסו שליחות על פני מספר שעות בתוך שעות עסקים.
