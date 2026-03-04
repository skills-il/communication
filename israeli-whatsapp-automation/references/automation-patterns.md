# Israeli WhatsApp Automation Patterns

## Overview

This reference covers common WhatsApp automation patterns for the Israeli market. All patterns account for Shabbat/holiday timing restrictions, Hebrew language requirements, and Israeli consumer communication preferences.

## Chatbot Flow Templates

### Customer Service Bot

A standard Israeli customer service chatbot should handle these top intents:

1. **Order tracking** (maakedav hazmana) -- Most common inquiry
2. **Business hours** (shaot peeilut) -- Must reflect Sunday-Thursday week
3. **Agent handoff** (haabarah lenatzig) -- Israelis often prefer human contact
4. **Returns/exchanges** (hachzarot/hamarot) -- Subject to Israeli Consumer Protection Law
5. **FAQ** (sheelot nefutzot) -- Product-specific auto-replies

### Lead Qualification Bot

For Israeli B2B businesses:

1. Greeting with company identification
2. Qualify: company size, industry, budget range
3. Schedule a call (respect Sunday-Thursday availability)
4. Hand off to sales representative with context

## Auto-Reply Sequence Templates

### E-commerce Order Lifecycle

| Stage | Trigger | Delay | Hebrew Template |
|-------|---------|-------|-----------------|
| Order confirmed | Payment received | Immediate | ההזמנה שלך ({id}) התקבלה! |
| Order shipped | Status update | Immediate | ההזמנה נשלחה! מעקב: {url} |
| Out for delivery | Driver assigned | Immediate | השליח בדרך! הגעה בעוד {minutes} דקות |
| Delivered | Delivery confirmed | Immediate | ההזמנה נמסרה! |
| Review request | After delivery | 3 days | מה חשבת? נשמח לחוות דעת |
| Re-engagement | No purchase | 30 days | שלום! חסרה לנו. הנה הצעה מיוחדת |

### Appointment-Based Business

| Stage | Trigger | Delay | Hebrew Template |
|-------|---------|-------|-----------------|
| Booking confirmed | Appointment created | Immediate | התור נקבע ב-{date} בשעה {time} |
| Day-before reminder | Calendar | 24h before | תזכורת: תור מחר ב-{time} |
| Morning-of reminder | Calendar | 3h before | התור שלך בעוד 3 שעות |
| Post-visit follow-up | Appointment completed | 2h after | תודה! איך היה? |
| Re-booking suggestion | Calendar | 30 days after | הגיע הזמן לתור הבא? |

### Service Business (Repairs, Maintenance)

| Stage | Trigger | Delay | Hebrew Template |
|-------|---------|-------|-----------------|
| Request received | Form/call | Immediate | קיבלנו את הפנייה שלך |
| Technician assigned | Internal | Immediate | הטכנאי {name} יגיע ב-{date} |
| On the way | GPS/manual | Immediate | הטכנאי בדרך! הגעה בעוד {minutes} דקות |
| Job completed | Manual | Immediate | העבודה הושלמה. סה"כ: {amount} ש"ח |
| Satisfaction survey | After completion | 1 day | מה חשבת על השירות? דרג/י 1-5 |

## Shabbat-Aware Scheduling Configuration

### Standard Configuration

```
Business hours: Sunday-Thursday 09:00-20:00, Friday 09:00-13:00
Shabbat block: Friday 16:00 - Saturday 20:00
Holiday block: Eve of holiday through end of holiday
Queue behavior: Messages are queued, not dropped
Resume: Automatic at next valid sending window
```

### Holiday Calendar Notes

Jewish holidays follow the Hebrew calendar and shift dates each Gregorian year. Key holidays to configure:

- **Rosh Hashana** (2 days) -- Usually September/October
- **Yom Kippur** (1 day) -- Complete communication blackout
- **Sukkot** (7 days, first and last are full holidays)
- **Hanukkah** (8 days) -- Not a full holiday, messages OK
- **Purim** (1 day) -- Messages OK but consider timing
- **Pesach** (7 days, first and last are full holidays)
- **Yom HaAtzmaut** -- National holiday, messages usually OK
- **Shavuot** (1 day)

### Timing Best Practices for Israel

- **Best send times**: Sunday-Tuesday 10:00-12:00, 15:00-17:00
- **Avoid**: Thursday evening (pre-Shabbat shopping rush, low engagement)
- **Friday**: Only send before 13:00 (people prepare for Shabbat)
- **Motzaei Shabbat** (Saturday evening): Good engagement after 21:00
- **Post-holiday**: High engagement in first 2 hours after holiday ends

## CRM Integration Patterns

### Monday.com Automations

Common Monday.com + WhatsApp automation recipes:

1. **New lead notification**: Status changes to "New" -> Send welcome WhatsApp
2. **Follow-up reminder**: Date column arrives -> Send follow-up WhatsApp
3. **Deal closed**: Status changes to "Won" -> Send thank-you WhatsApp
4. **Stale lead**: No activity for 14 days -> Send re-engagement WhatsApp
5. **Task assigned**: Person column changes -> Notify assignee via WhatsApp

### HubSpot Israel Workflows

Common HubSpot + WhatsApp automation workflows:

1. **Lead nurture**: New contact -> Wait 1 day -> Send intro WhatsApp
2. **Post-demo**: Meeting completed -> Wait 2 hours -> Send summary WhatsApp
3. **Onboarding**: Deal closed -> Sequence of 5 WhatsApp messages over 14 days
4. **Renewal reminder**: Subscription end date - 30 days -> Send renewal WhatsApp
5. **NPS survey**: 90 days after purchase -> Send satisfaction WhatsApp

## Rate Limiting Guidelines

WhatsApp Business API rate limits:

| Tier | Messages/day | Messages/second | Typical use |
|------|-------------|-----------------|-------------|
| Tier 1 (new) | 1,000 | 80 | Small business |
| Tier 2 | 10,000 | 80 | Growing business |
| Tier 3 | 100,000 | 80 | Enterprise |
| Tier 4 | Unlimited | 80 | Large enterprise |

Tier upgrades happen automatically based on message volume and quality rating.

## Hebrew Message Template Best Practices

1. Keep messages concise (Israeli users prefer brevity)
2. Use informal tone ("at/ata" not "atem" for individual messages)
3. Include emojis sparingly (one per message max in business context)
4. Always provide a clear call-to-action
5. Use NIS (shekel) symbol for pricing
6. Include business name in first message of any sequence
7. Provide opt-out instruction in the first marketing message
