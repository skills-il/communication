---
name: israeli-customer-support-automator
description: Deploy and configure customer support automation for Israeli businesses. Categorizes Hebrew support tickets, manages complaints per Consumer Protection Law 1981 (14-day returns, cooling-off periods), configures SLA with Israeli hours (Sunday-Thursday), and generates Hebrew canned responses for multi-channel support. Use when user asks to "set up customer support", "automate ticket routing", "sherut lakokhot", "handle complaints", or configure helpdesk for Israeli companies. Integrates with Monday.com and Priority ERP. Do NOT use for building chatbots (use hebrew-chatbot-builder), WhatsApp API (use israeli-whatsapp-business), or non-Israeli consumer protection.
license: MIT
allowed-tools: Bash(python:*)
compatibility: No network required for ticket classification and template generation. Python 3.9+ required for the classifier script. Works with Claude Code, Claude.ai, Cursor.
---

# Israeli Customer Support Automator

## Instructions

### Step 1: Categorize and Route Hebrew Support Tickets

Set up ticket categorization (miyun krartisim) to classify incoming Hebrew support requests. Each ticket should be categorized by type and priority.

**Category taxonomy:**

| Category | Hebrew | Subcategories | Typical Priority |
|---|---|---|---|
| Billing | חיוב | Incorrect charge, refund request, payment method, invoice question | Medium-High |
| Technical | תקלה טכנית | Bug report, feature not working, integration issue, performance | High |
| Returns | החזרות | Product return, exchange, cooling-off cancellation | High (time-sensitive) |
| Complaints | תלונות | Service complaint, product complaint, escalation request | High |
| General inquiry | שאלה כללית | Product info, pricing, availability, hours | Low |
| Account | חשבון | Login issues, password reset, profile update, subscription | Medium |
| Shipping | משלוח | Tracking, delivery delay, damaged package, address change | Medium |

**Routing rules:**

| Priority | Response Target | Assignment |
|---|---|---|
| Critical | 1 hour | L3 supervisor, immediate alert |
| High | 4 business hours | L2 agent, queue priority |
| Medium | 8 business hours | L1 agent, standard queue |
| Low | 24 business hours | L1 agent or auto-response |

**Hebrew keyword detection for auto-categorization:**

| Keywords (Hebrew) | Auto-Category |
|---|---|
| חיוב, חשבונית, תשלום, זיכוי, החזר כספי | Billing |
| לא עובד, תקלה, באג, נתקע, שגיאה, קריסה | Technical |
| החזרה, החלפה, ביטול עסקה, תקופת צינון | Returns |
| תלונה, אי שביעות רצון, לא מקובל, דורש פיצוי | Complaints |
| מידע, שאלה, מחיר, שעות פעילות, זמינות | General inquiry |
| סיסמה, כניסה, חשבון, הרשמה, מנוי | Account |
| משלוח, מעקב, חבילה, הגעה, כתובת | Shipping |

Run the classifier script for automated ticket categorization:
```bash
python scripts/ticket-classifier.py --text "הכרטיס שלי חויב פעמיים, מבקש זיכוי" --lang he
```

### Step 2: Comply with Israeli Consumer Protection Law

When handling complaints and return requests, ensure full compliance with the Israeli Consumer Protection Law 1981 (chok haganat ha'tzarchan, tashma"b-1981).

**Key provisions for customer support:**

| Provision | Requirement | Law Section |
|---|---|---|
| Remote purchase returns | 14 days cooling-off period from delivery or contract signing (whichever is later) | Section 14G |
| Cancellation of transaction | Consumer can cancel within 14 days; business must refund within 14 days of receiving cancellation notice | Section 14G |
| Cancellation fee | Maximum 5% of transaction price or NIS 100, whichever is lower | Section 14G |
| Defective product | Right to repair, replacement, or refund; no time limit for manufacturing defects | Section 11 |
| Misleading advertising | Business liable for damage caused by misleading claims | Section 2 |
| Receipt requirement | Must provide receipt for every transaction over NIS 24 | Section 14B |
| Price display | Must display prices including VAT | Section 17A |
| Warranty | Must honor written warranty terms; minimum periods vary by product type | Section 10 |
| Door-to-door sales | Extended cooling-off period; customer can cancel even after 14 days in some cases | Section 14A |

**Cooling-off period exceptions (Section 14G(d)):**
- Perishable goods
- Goods produced or altered specifically for the consumer
- Information products that have been opened (software, recordings)
- Accommodation, travel, or entertainment services for a specific date

**Complaint handling workflow:**

```
Complaint received
    |
    v
Categorize (billing/product/service)
    |
    v
Check if within 14-day cooling-off period
    |
    +--> YES: Process return/cancellation immediately
    |         Refund within 14 days of notice
    |         May charge cancellation fee (max 5% or NIS 100)
    |
    +--> NO: Check if defective product
              |
              +--> YES: Offer repair/replacement/refund
              |         No time limit for manufacturing defects
              |
              +--> NO: Standard complaint workflow
                       Acknowledge -> Investigate -> Resolve
                       Escalate if unresolved within SLA
```

Consult `references/consumer-protection-law.md` for the full legal reference.

### Step 3: Configure SLA Management with Israeli Business Hours

Set up SLA timers that respect Israeli business hours and holidays.

**Israeli business hours configuration:**

| Parameter | Value |
|---|---|
| Business days | Sunday through Thursday (yom rishon through yom chamishi) |
| Standard hours | 08:30 - 17:30 IST (Israel Standard Time, UTC+2) / IDT (UTC+3 during DST) |
| Friday | 08:30 - 13:00 (optional; some businesses closed) |
| Saturday (Shabbat) | Closed |
| Holiday eves | Close at 13:00 |

**SLA tiers:**

| Tier | First Response | Resolution | Applicable To |
|---|---|---|---|
| Premium | 1 business hour | 4 business hours | Enterprise customers, legal complaints |
| Standard | 4 business hours | 1 business day | Regular customers, billing issues |
| Basic | 8 business hours | 2 business days | General inquiries, low-priority |
| Informational | 1 business day | 3 business days | Product questions, feature requests |

**SLA calculation rules:**
- SLA clock starts when ticket is created during business hours
- Tickets created outside business hours: clock starts at next business day opening (08:30)
- Tickets created on Friday after 13:00: clock starts Sunday 08:30
- Tickets created on Shabbat or holidays: clock starts next business day 08:30
- Consumer Protection Law complaints: always use Premium SLA regardless of customer tier
- Pause SLA clock when waiting for customer response (status: "awaiting customer")

**Holiday SLA adjustments.** During the following periods, extend SLAs by 1 business day:
- Rosh Hashana, Yom Kippur, Sukkot, Pesach (multi-day holidays with reduced staffing)
- Days between holidays when many employees take vacation (gashranim)

### Step 4: Build Escalation Workflows

Configure a multi-level escalation system for support tickets.

**Escalation levels:**

| Level | Role | Handles | Authority | Response Time |
|---|---|---|---|---|
| L1 | Auto-response / Junior agent | Simple inquiries, password resets, status checks | Send canned responses, basic troubleshooting | Immediate (auto) or 4 hours |
| L2 | Senior agent | Complex issues, billing disputes, returns processing | Issue refunds up to NIS 500, override policies | 8 hours from escalation |
| L3 | Supervisor / Team lead | Legal complaints, high-value disputes, VIP customers | Full refund authority, compensation offers | 4 hours from escalation |
| L4 | Management | Regulatory complaints, PR-sensitive issues, legal threats | Policy changes, legal consultation | 2 hours from escalation |

**Auto-escalation triggers:**

| Trigger | Escalate To | Reason |
|---|---|---|
| Customer mentions "lawyer" (עורך דין) or "court" (בית משפט) | L3 | Potential legal action |
| Customer mentions "Consumer Protection Authority" (הרשות להגנת הצרכן) | L3 | Regulatory complaint |
| Ticket unresolved past SLA | Next level | SLA breach |
| Customer requests supervisor | L3 | Customer demand |
| 3+ tickets from same customer in 7 days | L2 | Recurring issue pattern |
| Negative sentiment detected | L2 | Customer frustration |
| Ticket involves amount > NIS 1,000 | L2 | High-value transaction |
| Social media complaint (public) | L3 | PR sensitivity |

**Escalation notification template (Hebrew):**

```
[הסלמת כרטיס]
מספר כרטיס: {ticket_id}
לקוח: {customer_name}
סיבת הסלמה: {reason}
רמה נוכחית: L{current} -> L{next}
תיאור: {description}
היסטוריה: {interaction_count} אינטראקציות
SLA נותר: {sla_remaining}
```

### Step 5: Create Hebrew Canned Response Templates

Build a library of canned responses (tshuvot mugdarot meirosh) in Hebrew for common support scenarios.

**Response templates by category:**

**Acknowledgment (aishur kabala):**
```
שלום {customer_name},

תודה שפנית אלינו. קיבלנו את פנייתך (מספר כרטיס: {ticket_id}).
נחזור אליך בהקדם, לכל המאוחר תוך {sla_hours} שעות עבודה.

בברכה,
צוות {company_name}
```

**Refund processed (zikui butzah):**
```
שלום {customer_name},

בהמשך לפנייתך, ביצענו זיכוי בסך {amount} ש"ח לכרטיס האשראי שלך.
הזיכוי יופיע בחשבונך תוך 3-5 ימי עסקים.

מספר אסמכתא: {reference_id}

נשמח לעמוד לרשותך בכל שאלה נוספת.

בברכה,
צוות {company_name}
```

**Return instructions (hora'ot lehachzara):**
```
שלום {customer_name},

בהתאם לבקשתך להחזרת המוצר, להלן ההוראות:

1. ארזו את המוצר באריזתו המקורית
2. צרפו את החשבונית / אישור ההזמנה
3. שלחו לכתובת: {return_address}
   או הביאו לסניף הקרוב: {branch_address}

שימו לב: ההחזרה חייבת להתבצע תוך 14 ימים ממועד קבלת המוצר,
בהתאם לחוק הגנת הצרכן.

לאחר קבלת המוצר, הזיכוי יבוצע תוך 14 ימים.

בברכה,
צוות {company_name}
```

**Issue resolved (ba'aya nitpera):**
```
שלום {customer_name},

שמחים לעדכן שהבעיה שדיווחת עליה (כרטיס {ticket_id}) טופלה.

{resolution_details}

אם הבעיה חוזרת או שיש לך שאלות נוספות, אל תהסס/י לפנות אלינו.

נשמח אם תוכל/י לדרג את חוויית השירות:
{satisfaction_survey_link}

בברכה,
צוות {company_name}
```

**Escalation notice to customer (hodaat haslama):**
```
שלום {customer_name},

פנייתך (כרטיס {ticket_id}) הועברה לטיפול מנהל/ת צוות שלנו
שיצור/תיצור איתך קשר בהקדם.

אנו מתייחסים לפנייתך ברצינות ונעשה כל שביכולתנו לפתור את העניין.

בברכה,
צוות {company_name}
```

Consult `references/hebrew-response-templates.md` for the complete template library.

### Step 6: Configure Multi-Channel Support

Set up support across multiple channels common in the Israeli market.

**Channel configuration:**

| Channel | Popularity in Israel | Best For | Response Format |
|---|---|---|---|
| WhatsApp Business | Very high (90%+ adoption) | Quick questions, order updates, personal service | Short, conversational Hebrew |
| Email | High | Formal complaints, documentation, detailed issues | Structured, formal Hebrew |
| Phone | High | Urgent issues, elderly customers, complex problems | Script-guided conversation |
| Website chat | Medium | Browser-based inquiries, guided troubleshooting | Chatbot + agent handoff |
| Facebook/Instagram | Medium | Public complaints, product questions, social engagement | Public-facing, diplomatic |
| SMS | Low (replaced by WhatsApp) | Automated notifications, appointment reminders | Brief, transactional |

**Channel-specific guidelines:**

**WhatsApp:**
- Use WhatsApp Business API for automated responses
- Keep messages under 500 characters
- Use emoji sparingly (common in Israeli business WhatsApp)
- Support Hebrew text direction (RTL)
- Send order updates and tracking proactively
- Business hours auto-reply for after-hours messages

**Email:**
- Use professional Hebrew templates
- Include ticket number in subject line
- Attach relevant documents (invoices, receipts)
- Response time: per SLA tier
- Auto-acknowledge receipt within 1 hour

**Social media:**
- Respond publicly to acknowledge, then move to private message (hodaa pratit) for details
- Never share personal or order information in public replies
- Response tone: professional but personable
- Escalate negative viral posts to L3 immediately
- Monitor brand mentions using social listening tools

### Step 7: Integrate with Israeli CRM Tools

Connect support workflows with CRM and ERP systems commonly used by Israeli businesses.

**Monday.com integration:**
- Create support board with ticket pipeline (New -> In Progress -> Waiting -> Resolved -> Closed)
- Map ticket categories to Monday.com groups
- Set up automations: auto-assign by category, SLA deadline notifications, escalation triggers
- Use Monday.com API for bi-directional sync
- Configure Hebrew column names and status labels

**Priority ERP integration:**
- Sync customer data (customer number, billing history, orders)
- Auto-create service calls (kriut sherut) from support tickets
- Link tickets to invoices and orders for billing disputes
- Pull product warranty information for defect claims
- Export support metrics to Priority reporting

**Other common integrations:**

| Tool | Use Case | Integration Method |
|---|---|---|
| Salesforce | Enterprise CRM | API, webhooks |
| HubSpot | SMB CRM | API, native integration |
| Jira | Bug tracking | API, webhook on tech tickets |
| Slack / Teams | Internal notifications | Webhook, bot |
| Twilio | SMS/WhatsApp | API |

### Step 8: Measure Customer Satisfaction

Set up customer satisfaction measurement (medidat sipuk lakokhot) with Hebrew-localized surveys.

**CSAT (Customer Satisfaction Score):**

Post-resolution survey (Hebrew):
```
מה מידת שביעות הרצון שלך מהטיפול בפנייה?
1 - לא מרוצה כלל
2 - לא מרוצה
3 - ניטרלי
4 - מרוצה
5 - מרוצה מאוד
```

**NPS (Net Promoter Score):**

Periodic survey (Hebrew):
```
בסולם של 0 עד 10, עד כמה סביר שתמליץ/י על {company_name} לחבר/ה או עמית/ה?
0 (לא סביר כלל) -------- 10 (סביר מאוד)
```

**Key metrics dashboard:**

| Metric | Target | Calculation |
|---|---|---|
| CSAT | > 4.0 / 5.0 | Average of post-resolution ratings |
| NPS | > 30 | % Promoters (9-10) minus % Detractors (0-6) |
| First Response Time | Per SLA tier | Time from ticket creation to first agent response |
| Resolution Time | Per SLA tier | Time from ticket creation to resolution |
| First Contact Resolution (FCR) | > 60% | % of tickets resolved in first interaction |
| Ticket Volume | Trend analysis | Total tickets per day/week/month |
| Escalation Rate | < 15% | % of tickets escalated beyond L1 |
| Customer Effort Score (CES) | > 4.0 / 5.0 | "How easy was it to resolve your issue?" |

**Reporting cadence:**
- Daily: Ticket volume, first response time, open ticket count
- Weekly: CSAT trend, escalation rate, channel distribution
- Monthly: NPS, FCR, SLA compliance rate, top complaint categories
- Quarterly: Customer journey analysis, process improvement recommendations

## Examples

### Example 1: Set Up Ticket Routing for an E-Commerce Company

User says: "I need to set up customer support automation for my online store in Israel"

Actions:
1. Configure ticket categorization based on Hebrew keyword detection (Step 1)
2. Set up Consumer Protection Law compliance for returns (14-day cooling-off period, Step 2)
3. Configure SLA timers with Sunday-Thursday business hours (Step 3)
4. Build escalation workflow with auto-triggers for legal keywords (Step 4)
5. Generate Hebrew canned responses for order inquiries, returns, and refunds (Step 5)
6. Set up WhatsApp Business and email channels (Step 6)

Result: Fully configured support system with Hebrew templates, Israeli law compliance, and multi-channel routing.

### Example 2: Handle a Consumer Protection Complaint

User says: "A customer wants to return a product they bought online 10 days ago"

Actions:
1. Verify the purchase is within the 14-day cooling-off period (it is, 10 < 14 days)
2. Check if the product falls under cooling-off exceptions (perishable, custom-made, opened software)
3. If not excepted: process return immediately, send return instructions template
4. Calculate cancellation fee (max 5% of price or NIS 100, whichever is lower)
5. Issue refund within 14 days of receiving cancellation notice
6. Document the interaction for compliance records

Result: Return processed in full compliance with Consumer Protection Law 1981, Section 14G.

### Example 3: Create an Escalation Workflow

User says: "A customer posted a complaint on Facebook tagging our company and threatening to go to the Consumer Protection Authority"

Actions:
1. Auto-escalate to L3 (mentions regulatory authority)
2. Respond publicly on Facebook: acknowledge and invite to private message
3. Assign to supervisor with 2-hour SLA
4. Document the public post for PR monitoring
5. Prepare resolution offer per company policy
6. Follow up via private channel (WhatsApp or email)

Result: Public complaint managed with appropriate escalation, regulatory risk mitigated.

### Example 4: Set Up CSAT Measurement

User says: "I want to measure customer satisfaction for our support team"

Actions:
1. Create Hebrew CSAT survey template (5-point scale)
2. Configure auto-send after ticket resolution
3. Set up NPS survey for monthly distribution
4. Build metrics dashboard with targets (CSAT > 4.0, NPS > 30, FCR > 60%)
5. Define reporting cadence (daily, weekly, monthly, quarterly)
6. Integrate with Monday.com for real-time visibility

Result: Complete satisfaction measurement system with Hebrew surveys and actionable metrics.

## Bundled Resources

### Scripts
- `scripts/ticket-classifier.py` -- Classify Hebrew support tickets by category and priority based on keyword analysis. Supports batch processing from CSV files. Run: `python scripts/ticket-classifier.py --help`

### References
- `references/consumer-protection-law.md` -- Key provisions of the Israeli Consumer Protection Law 1981. Covers cooling-off periods, return policies, cancellation fees, warranty obligations, and complaint handling requirements. Consult when handling returns, complaints, or any dispute involving consumer rights.
- `references/hebrew-response-templates.md` -- Ready-to-use Hebrew canned responses for common support scenarios. Includes templates for acknowledgment, refund processing, return instructions, issue resolution, escalation notices, and satisfaction surveys. Consult when creating or customizing support response templates.

## Gotchas

- The 14-day cooling-off period in Israel starts from the delivery date or the date the consumer received the contract terms, whichever is later. Agents may calculate it from the purchase date.
- SLA timers must account for the Israeli work week (Sunday-Thursday). A ticket opened on Friday afternoon should not start its SLA clock until Sunday 08:30.
- The Hebrew word for "complaint" (תלונה) and "query" (שאילתה) are often confused by text classifiers. Auto-categorization should weight escalation keywords like "עורך דין" (lawyer) and "בית משפט" (court) heavily.
- Israeli Consumer Protection Law allows a maximum cancellation fee of 5% or 100 NIS, whichever is lower. Agents may use 5% without the 100 NIS cap, overcharging on small transactions.
- WhatsApp has over 90% adoption in Israel and is the preferred support channel. Agents may default to email-first support strategies that don't match Israeli consumer expectations.

## Troubleshooting

### Error: "Ticket categorized incorrectly"
Cause: Hebrew keyword detection matched the wrong category (e.g., "payment" matched billing instead of returns)
Solution: Review the keyword detection table in Step 1. Add more specific subcategory keywords. Use the classifier script with `--verbose` flag to see matching details: `python scripts/ticket-classifier.py --text "..." --verbose`

### Error: "SLA timer not pausing on weekends"
Cause: Business hours configuration does not account for Shabbat (Saturday) and the Israeli work week
Solution: Verify the business hours config in Step 3. Ensure Friday is set to close at 13:00 (or fully closed) and Saturday is marked as non-business. Check that the timezone is set to Asia/Jerusalem.

### Error: "Return request rejected but customer is within 14-day period"
Cause: The 14-day period was calculated from the order date instead of the delivery date (or contract signing, whichever is later)
Solution: Per Consumer Protection Law Section 14G, the cooling-off period starts from the later of: (1) delivery date, or (2) the date the consumer received the contract terms and cancellation details. Recalculate accordingly.

### Error: "Escalation notification not reaching supervisor"
Cause: Notification channel is misconfigured or supervisor assignment rules are not matching
Solution: Check the escalation routing rules in Step 4. Verify that supervisor contact details are up to date. Test the notification webhook. For WhatsApp notifications, ensure the supervisor's phone number is registered with WhatsApp Business API.
