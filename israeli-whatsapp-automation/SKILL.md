---
name: israeli-whatsapp-automation
description: >-
  Build WhatsApp automation flows for the Israeli market including chatbots,
  auto-reply sequences, and campaign scheduling with Shabbat and holiday
  awareness. Use when user asks about WhatsApp chatbot development in Israel,
  automated WhatsApp responses in Hebrew, scheduling WhatsApp campaigns around
  Shabbat ("luchot zmanim"), Israeli holiday-aware messaging automation
  ("otomatizatzya"), WhatsApp bot integration with Monday.com or HubSpot
  Israel, or building order confirmation and appointment reminder flows. Covers
  chatbot conversation design, Shabbat-aware timing logic, Hebrew auto-reply
  patterns, Israeli consumer opt-in for automated messages, and CRM
  integration. Do NOT use for WhatsApp Business API setup (use
  israeli-whatsapp-business instead).
license: MIT
allowed-tools: 'Bash(python:*) Bash(curl:*) WebFetch'
compatibility: >-
  Requires WhatsApp Business API access (Cloud API or on-premise). Python 3.9+
  for automation scripts. Network access required.
metadata:
  author: skills-il
  version: 1.0.0
  category: communication
  tags:
    he:
      - ווטסאפ
      - אוטומציה
      - צ'אטבוט
      - שיווק
      - ישראל
    en:
      - whatsapp
      - automation
      - chatbot
      - marketing
      - israel
  display_name:
    he: אוטומציית ווטסאפ ישראלית
    en: Israeli WhatsApp Automation
  display_description:
    he: >-
      בניית תהליכי אוטומציה לווטסאפ בשוק הישראלי כולל צ'אטבוטים, תגובות
      אוטומטיות, תזמון קמפיינים ותזמון מודע לשבת וחגים
    en: >-
      Build WhatsApp automation flows for the Israeli market including chatbots,
      auto-reply sequences, and campaign scheduling with Shabbat and holiday
      awareness. Use when user asks about WhatsApp chatbot development in
      Israel, automated WhatsApp responses in Hebrew, or scheduling WhatsApp
      campaigns around Shabbat. Do NOT use for WhatsApp Business API setup
      (use israeli-whatsapp-business instead).
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli WhatsApp Automation

## Instructions

### Step 1: Design Chatbot Conversation Flows

Design Hebrew chatbot flows that match Israeli communication patterns. Israeli users expect direct, informal communication with quick resolution.

**Common Israeli chatbot flow structure:**

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

**Build interactive message for chatbot menu:**
```python
import requests

def send_chatbot_menu(phone_number_id: str, access_token: str,
                      to: str, menu_items: list) -> dict:
    """Send an interactive list message as chatbot menu."""
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

### Step 2: Implement Shabbat and Holiday-Aware Scheduling

Israeli automation MUST respect Shabbat (Friday evening through Saturday evening) and Jewish holidays. Messages sent during these times are seen as disrespectful and cause high unsubscribe rates.

```python
from datetime import datetime, time, timedelta
import pytz

# Major Jewish holidays (approximate Gregorian dates -- update annually)
# These are the eves when holidays begin (messages should stop before sunset)
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
    """Check if datetime falls during Shabbat (Friday 16:00 to Saturday 20:00 Israel time)."""
    israel_tz = pytz.timezone("Asia/Jerusalem")
    local = dt.astimezone(israel_tz)
    day = local.weekday()  # 0=Monday, 4=Friday, 5=Saturday

    # Friday after 16:00 (before sunset, conservative)
    if day == 4 and local.time() >= time(16, 0):
        return True
    # Saturday before 20:00
    if day == 5 and local.time() < time(20, 0):
        return True
    return False

def is_jewish_holiday(dt: datetime, holidays: list = None) -> tuple[bool, str]:
    """Check if date falls on a Jewish holiday."""
    if holidays is None:
        holidays = JEWISH_HOLIDAYS_2026
    date_str = dt.strftime("%Y-%m-%d")
    for start, end, name in holidays:
        if start <= date_str <= end:
            return True, name
    return False, ""

def get_next_valid_send_time(dt: datetime = None) -> datetime:
    """Calculate the next valid time to send a message in Israel."""
    israel_tz = pytz.timezone("Asia/Jerusalem")
    if dt is None:
        dt = datetime.now(israel_tz)
    else:
        dt = dt.astimezone(israel_tz)

    max_attempts = 14  # Prevent infinite loop (max 2 weeks ahead)
    for _ in range(max_attempts):
        if is_shabbat(dt):
            # Move to Saturday 20:00
            if dt.weekday() == 4:  # Friday
                dt = dt + timedelta(days=1)
            dt = dt.replace(hour=20, minute=0, second=0, microsecond=0)
            continue

        holiday, name = is_jewish_holiday(dt)
        if holiday:
            dt = dt + timedelta(days=1)
            dt = dt.replace(hour=9, minute=0, second=0, microsecond=0)
            continue

        # Business hours: 09:00-20:00
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
    """Schedule a batch of messages respecting Shabbat and holidays."""
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

### Step 3: Build Auto-Reply Sequences

Set up automated response sequences for common Israeli business scenarios.

**Order confirmation flow:**
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

### Step 4: Israeli Consumer Opt-In for Automated Messages

Automated WhatsApp messages are subject to the same Chok HaSpam rules as other commercial messages. Additional considerations for automation:

```python
def validate_automation_consent(phone: str, consent_db: dict,
                                 automation_type: str) -> dict:
    """Validate consent for automated WhatsApp messages."""
    record = consent_db.get(phone)
    if not record:
        return {"allowed": False, "reason": "No consent record found"}

    if not record.get("is_active", False):
        return {"allowed": False, "reason": "Consent was revoked"}

    channels = record.get("channels", [])
    if "whatsapp" not in channels:
        return {"allowed": False, "reason": "No WhatsApp consent (only: " + ", ".join(channels) + ")"}

    # Transactional messages (order updates) have broader permission
    if automation_type == "transactional":
        return {"allowed": True, "reason": "Transactional messages permitted for existing customers"}

    # Marketing automation requires explicit marketing consent
    if automation_type == "marketing":
        if not record.get("marketing_consent", False):
            return {"allowed": False, "reason": "No marketing consent for automated messages"}

    return {"allowed": True, "reason": "Consent verified"}

def build_opt_in_flow() -> dict:
    """Generate WhatsApp opt-in flow for Israeli compliance."""
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

### Step 5: CRM Integration Patterns

**Monday.com automation integration:**
```python
def monday_com_whatsapp_automation(board_id: str, api_key: str) -> dict:
    """Configure Monday.com automation triggers for WhatsApp messages."""
    automations = {
        "new_lead": {
            "trigger": "When status changes to 'New Lead'",
            "action": "Send WhatsApp welcome template",
            "template": "welcome_lead_he",
            "timing": "Immediate (within business hours)"
        },
        "follow_up": {
            "trigger": "When date arrives (follow-up column)",
            "action": "Send WhatsApp follow-up template",
            "template": "follow_up_he",
            "timing": "09:00 on the scheduled date"
        },
        "deal_won": {
            "trigger": "When status changes to 'Deal Won'",
            "action": "Send WhatsApp thank-you + next steps",
            "template": "deal_won_he",
            "timing": "Immediate (within business hours)"
        },
        "inactive_reminder": {
            "trigger": "When last_activity_date > 30 days ago",
            "action": "Send WhatsApp re-engagement",
            "template": "reengagement_he",
            "timing": "10:00 on next business day"
        }
    }
    return automations

def hubspot_israel_whatsapp_config() -> dict:
    """HubSpot Israel WhatsApp automation configuration."""
    return {
        "workflow_triggers": [
            {
                "name": "Lead nurture sequence",
                "trigger": "Contact property 'lifecycle_stage' = 'Lead'",
                "delay": "1 day",
                "template": "nurture_step1_he",
                "check_shabbat": True
            },
            {
                "name": "Post-purchase feedback",
                "trigger": "Deal property 'dealstage' = 'Closed Won'",
                "delay": "3 days",
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

### Step 6: Message Queue and Rate Management

```python
from collections import deque

class IsraeliMessageQueue:
    """Message queue with Shabbat-aware scheduling and rate limiting."""

    def __init__(self, rate_per_second: int = 80):
        self.queue = deque()
        self.rate_per_second = rate_per_second
        self.sent_count = 0

    def enqueue(self, message: dict) -> dict:
        """Add message to queue with scheduling check."""
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
        """Return queue statistics."""
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

## Examples

### Example 1: Restaurant Reservation Bot
User says: "Build a WhatsApp chatbot for my restaurant that handles reservations in Hebrew"
Actions:
1. Design conversation flow: greeting, party size, date/time, confirmation
2. Add Shabbat awareness (restaurant may be closed Friday night/Saturday)
3. Create Hebrew auto-reply templates for each step
4. Set up confirmation and reminder sequences
Result: Hebrew chatbot with reservation flow, Shabbat-aware scheduling, and automated reminders.

### Example 2: E-commerce Automation
User says: "Set up automated WhatsApp notifications for our online store orders"
Actions:
1. Create order confirmation, shipping, and delivery notification flows
2. Configure Shabbat and holiday message pausing
3. Add review request 3 days after delivery
4. Integrate with shipping provider webhooks (Cheetah, HFD, Israel Post)
Result: Complete order lifecycle automation with Israeli timing compliance.

### Example 3: Campaign Scheduling
User says: "Schedule a WhatsApp marketing campaign to 5,000 customers avoiding Shabbat"
Actions:
1. Validate opt-in consent for all recipients
2. Calculate send schedule respecting Shabbat, holidays, and business hours
3. Set rate limiting (avoid exceeding API limits)
4. Queue messages with automatic pause/resume around restricted times
Result: Fully scheduled campaign with Shabbat-aware timing and consent verification.

### Example 4: Monday.com Integration
User says: "When a deal closes in Monday.com, automatically send a WhatsApp thank-you in Hebrew"
Actions:
1. Set up Monday.com automation trigger on deal status change
2. Create Hebrew thank-you template with customer name and deal details
3. Add Shabbat check before sending (queue if during Shabbat)
4. Log sent message back to Monday.com board as update
Result: CRM-triggered WhatsApp automation with Israeli business hours compliance.

## Bundled Resources

### References
- `references/automation-patterns.md` -- Common Israeli WhatsApp automation patterns including chatbot flow templates, auto-reply sequences for order management, appointment systems, and delivery notifications. Includes Hebrew message templates and Shabbat-aware scheduling configurations. Consult when designing automation flows or choosing template patterns.

## Troubleshooting

### Error: "Messages not sending during expected hours"
Cause: Shabbat or holiday detection is pausing the queue.
Solution: Check the holiday calendar configuration. Verify timezone is set to Asia/Jerusalem. Review queue stats to see paused message count.

### Error: "Chatbot not recognizing Hebrew input"
Cause: Hebrew text matching may fail due to Unicode normalization differences.
Solution: Normalize Hebrew input before matching (NFC normalization). Account for common misspellings and transliteration variants. Use keyword-based matching rather than exact string matching.

### Error: "CRM webhook not triggering WhatsApp message"
Cause: Monday.com or HubSpot webhook configuration issue, or message queued due to timing restrictions.
Solution: Verify webhook URL is reachable and returns 200. Check if the message was queued due to Shabbat/holiday timing. Review CRM automation logs for trigger conditions.

### Error: "Rate limit exceeded"
Cause: Sending too many messages per second via the WhatsApp Cloud API.
Solution: WhatsApp Cloud API allows 80 messages/second. Implement rate limiting in your queue. For large campaigns, spread sends over multiple hours within business hours.
