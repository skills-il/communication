---
name: israeli-customer-support-automator
description: Deploy and configure customer support automation for Israeli businesses. Categorizes Hebrew support tickets, manages complaints per Consumer Protection Law 1981 (14-day returns, cooling-off periods), configures SLA with Israeli hours (Sunday-Thursday), and generates Hebrew canned responses for multi-channel support. Use when user asks to "set up customer support", "automate ticket routing", "sherut lakokhot", "handle complaints", or configure helpdesk for Israeli companies. Integrates with Monday.com and Priority ERP. Do NOT use for building chatbots (use hebrew-chatbot-builder), WhatsApp API (use israeli-whatsapp-business), or non-Israeli consumer protection.
license: MIT
allowed-tools: Bash(python3:*)
compatibility: No network required. Python 3.9+ and a shell are needed for scripts/ticket-classifier.py, invoked as python3 (plain "python" does not resolve on current macOS or most Linux images). Hosts that cannot run a shell command can still use every other part of this skill by applying the Step 1 keyword tables by hand instead of running the classifier. Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Gemini CLI.
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
python3 scripts/ticket-classifier.py --text "הכרטיס שלי חויב פעמיים, מבקש זיכוי" --lang he
```

### Step 2: Comply with Israeli Consumer Protection Law

When handling complaints and return requests, ensure full compliance with the Israeli Consumer Protection Law 1981 (chok haganat ha'tzarchan, tashma"b-1981).

**Key provisions for customer support:**

| Provision | Requirement | Law Section |
|---|---|---|
| Remote purchase returns, goods | 14 days from receipt of the goods or from receipt of the Section 14C(b) disclosure document, whichever is later. **Not** from contract signature | Section 14C(c)(1) |
| Remote purchase returns, services | 14 days from the day the transaction was made or from receipt of that document, whichever is later. For a service that is NOT an ongoing transaction the cancellation must be made **at least two non-rest days before** the service date | Section 14C(c)(2) |
| Cancellation of transaction | Consumer can cancel within 14 days; business must refund within 14 days of receiving cancellation notice | Section 14E (14ה) |
| Cancellation fee | Maximum 5% of transaction price or NIS 100, whichever is lower. **No fee at all** when the consumer cancels for cause (defect, non-conformity, late delivery, or any other breach by the dealer) | Section 14E(a)-(b) (14ה) |
| Misleading advertising | Business liable for damage caused by misleading claims | Section 2 |
| Price display | Must display the total price including VAT, in shekels only. 17A (17א) merely DEFINES "total price"; the operative duties are the display duty on goods and the advertising duty | Sections 17B and 17D (17ב, 17ד) |
| Door-to-door sales (rochlut) | Consumer may cancel within 14 days of delivery or of receiving the required details, whichever is later | Section 14 |

**Watch the Hebrew letters.** ג is the THIRD Hebrew letter, so 14ג transliterates to 14C, not 14G. 14ז (14G) is a different section entirely (credit vouchers). Citing "14G" for the remote-purchase cooling-off period sends a customer or a colleague to the wrong provision.

**Cooling-off period exceptions (Section 14C(d), 14ג(ד)).** Five statutory exceptions, and two are routinely misstated: travel and leisure services are excluded only when cancellation falls **within seven non-rest-days before the service date** (a window, not a "specific date"), and "information" under the Computers Law is excluded outright, which is a separate item from recordable goods whose original packaging was opened. Full list in `references/consumer-protection-law.md`.

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

**The remote-sale branch above is not the whole of Israeli returns law.** Five further regimes govern workflows a real support desk runs weekly, and each is a separate enforcement item. They are set out in `references/consumer-protection-law.md`; read that section before configuring intake or an outbound campaign:
- **Section 14I (14ט)**: a cancellation notice must be receivable by phone, in person, registered mail, email, fax and over the internet, and the homepage needs a prominent dedicated cancellation link. You do not get to pick the channel.
- **Section 4C (4ג) and the 2010 Cancellation Regulations**: in-store and non-defect returns, including the presumption that returns are permitted if no policy notice is posted.
- **Section 13D (13ד)**: an ongoing transaction ends within three business days of the cancellation notice, and nothing supplied after that may be charged.
- **Section 16C (16ג)**: the do-not-call registry, which governs marketing CALLS. Section 30A governs messages; a retention calling campaign must check the registry first.
- **Sections 18B(a) and 18C (18ב(א), 18ג)**: free telephone service, publication of the number and hours on every invoice, and agent self-identification on every call.

Consult `references/consumer-protection-law.md` for the full legal reference.

**Privacy Protection Law Amendment 13 (in force 14 August 2025).** Customer-support data is personal information, and a ticket or CRM database is a regulated database. Core duties: a purpose statement and privacy-policy link at every point of collection; retention limited to the purpose; data-subject access and deletion requests answered within 30 days (build a "DSAR" tag to track the clock); sub-processors named in the notice with a signed data-processing addendum; and note that the Privacy Protection Authority now has direct power to impose financial sanctions, calculated by formula rather than capped at a single headline figure, so check the current schedule before quoting a number. Two duties commonly missed: appointing a Privacy Protection Officer where the organisation's profile triggers it, and notifying the Authority of a security incident. The Information Security Regulations, 2017 add a database definition document, access control and logging, and a periodic risk survey. Detail, including the PPA's AI guidance, is in `references/consumer-protection-law.md`.

**Mandatory call recording from 22 March 2027** (Consumer Protection Law Section 16D, 16ד, added by Amendment 74). For the transaction types in the Ninth Schedule at a total price of **NIS 750 or more**, every voice call with the consumer must be recorded in both directions, the consumer must be told at the **start of every call** that it is recorded and that they may request a copy, and the recording must be kept **two years** if a transaction was concluded or **six months** if it was not. On request the dealer must hand over the recording, or a written schedule of call times, within **ten business days**, free of charge for the first request. Note where the sanction attaches: it is failure to DELIVER, not failure to record, that makes the dealer be treated in civil proceedings as having admitted the consumer's version. Three things to design now: a start-of-call announcement in every phone script, a per-call retention clock, and a ticket category with its own ten-business-day SLA for recording requests. This two-year floor also overrides the shorter default retention suggested below. Detail in `references/consumer-protection-law.md`.

**Extended cooling-off for protected groups (Section 14C1, 14ג1).** Standard consumers get 14 days; consumers who are persons with a disability, senior citizens (65+), or new immigrants (within 5 years of receiving their immigrant certificate) get **4 months** to cancel a remote-purchase transaction, provided the transaction involved a conversation between the dealer and the consumer, including a conversation by electronic communication. That conversation condition applies to REMOTE sales (14ג1(ג)) only; for a door-to-door transaction (14ג1(ב)) the four months apply with no such condition. The dealer may demand one document proving the status and no more (14ג1(ד)). Your auto-categorizer should NOT auto-reject return requests beyond day 14 without checking the customer's protected-group status first.

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

**Telephone wait-time obligations. Check first whether they apply to you at all.** The 6-minute human-answer rule is in **Consumer Protection Law Section 18B(a1)** (not in the 2012 regulations), and it binds only a dealer listed in the **Second Schedule**: telephony, internet access, cable and satellite, gas, electricity, water, and ongoing medical-services transactions. There is no employee-count threshold and an ordinary Israeli SME is not covered; banks and insurers are covered by their own statutes. The **2012 Telephone Service Regulations** carry the separate 3-minute announcement (delivered within two minutes of call start) and the 3-hour callback duty, and contain no 6-minute rule. The often-quoted "15% may exceed" and "4.5-minute average" figures are Ministry of Communications supervision metrics for telecom licensees, not statutory consumer caps. They are revised periodically, so read the current figures off the ministry's own page before quoting one to anybody. Full detail, including the systemic-outage carve-out and the callback exceptions, is in `references/consumer-protection-law.md`.

### Step 4: Build Escalation Workflows

Configure a multi-level escalation system for support tickets.

**Escalation levels:**

| Level | Role | Handles | Authority | Response Time |
|---|---|---|---|---|
| L1 | Auto-response / Junior agent | Simple inquiries, password resets, status checks | Send canned responses, basic troubleshooting | Immediate (auto) or 4 hours |
| L2 | Senior agent | Complex issues, billing disputes, returns processing | Issue refunds up to the L2 cap set in your own refund policy, override policies | 8 hours from escalation |
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

The Hebrew escalation-notification template is in `references/hebrew-response-templates.md`.

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

שימו לב: 14 הימים שבחוק הם המועד למסירת הודעת הביטול,
לא למשלוח הפיזי של המוצר.

הזיכוי יבוצע תוך 14 ימים ממועד קבלת הודעת הביטול.

בברכה,
צוות {company_name}
```

**Branch this template on the reason for cancellation before sending it.** The version above fits a **no-fault** cancellation (Section 14E(b)): the consumer returns the goods to the place of business and a fee of up to 5% or NIS 100, whichever is lower, may be charged. If the cancellation is **for cause** (defect, non-conformity, late delivery, or any other breach by the dealer) Section 14E(a) reverses both: the consumer only places the goods at the dealer's disposal **at the place they were delivered** and notifies the dealer, who collects at their own cost, and **no cancellation fee of any kind** may be charged. Section 14E(d) defines cancellation fees as including shipping and packing, so billing return carriage to a for-cause canceller is itself a prohibited fee. Delete the fee line and the shipping instructions in that case. In both branches Section 14E also requires handing the consumer a **copy of the charge-cancellation notice**, not just issuing the refund.


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

Consult `references/hebrew-response-templates.md` for the complete template library.

### Step 6: Configure Multi-Channel Support

Set up support across multiple channels common in the Israeli market.

**Channel configuration:**

| Channel | Popularity in Israel | Best For | Response Format |
|---|---|---|---|
| WhatsApp Business | The dominant messaging channel in Israel | Quick questions, order updates, personal service | Short, conversational Hebrew |
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
- **Per-message pricing (effective 1 July 2025).** Meta switched the WhatsApp Business Platform from conversation-based billing (24-hour windows) to per-message pricing on 1 July 2025. Marketing templates are charged on delivery; utility and authentication templates are charged outside the customer service window. Rates are per country and Meta publishes a downloadable rate card, so read the current Israel row rather than assuming a ratio between categories.
- **Service messages are free today and stop being free on 1 October 2026.** They have not been charged since 1 November 2024. From 1 October 2026 Meta charges per message for all service messages, and also for utility messages sent in response to a user inside an open 24-hour service window. A support operation costed on today's "service is free" assumption will see a new line item from that date. There is also a new Meta Business Agent category, billed per token from 1 August 2026.
- Audit template categories regularly: Meta reclassifies templates (utility to marketing is the common direction, and marketing is the more expensive category), and the business is charged at the category applied at time of use. Most Israeli operations go through a Business Solution Provider, which adds its own markup on top of Meta's rates; confirm that markup with your BSP rather than assuming a figure.

**SMS and WhatsApp marketing consent (Section 30A Communications Law, "chok haspam").** Marketing or promotional messages need **prior explicit written opt-in**; transactional support replies (order status, ticket updates, password resets) are outside the section entirely because they are not a "davar pirsomet" as the statute defines it. The permitted labels are **"פרסומת", "בקשת תרומה" or "תעמולה"**; **"מסחרי" is not in the statute**. An SMS must carry only the advertiser's name and opt-out contact details (Section 30A(e)(2) overrides the general list); an email must carry the word in the **subject line** plus name, address, contact details and a live opt-out URL. A court may award up to **NIS 1,000 per message** without proof of harm. WhatsApp marketing is inside the statute's definition of an electronic message. Tag every outbound channel as "transactional" or "marketing" and gate marketing on a verified opt-in flag. Full detail, including the Section 30A(c) existing-customer route and why it is not the same as the transactional exclusion, is in `references/consumer-protection-law.md`.

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
| Salesforce (incl. Salesforce IL) | Enterprise CRM | API, webhooks |
| HubSpot | SMB CRM | API, native integration |
| Zoho Desk / Zoho CRM | SMB Israeli CRM | API, native integration |
| Jira | Bug tracking | API, webhook on tech tickets |
| Slack / Teams | Internal notifications | Webhook, bot |
| Twilio | SMS/WhatsApp | API |

**Hebrew-NLU support on major helpdesk platforms.** Zendesk and Freshdesk have the most mature Hebrew handling (macros, triggers and intent classification all work in Hebrew); Intercom's Fin handles Hebrew tickets; HelpScout and Front are weaker on Hebrew AI suggestions than on Hebrew tickets. Pricing for the autonomous-agent tiers moves fast and is quoted per resolution or per outcome rather than per seat, so get a written quote from the vendor rather than budgeting from a blog. The per-platform table is in `references/consumer-protection-law.md`.

Pick one tier above your team's volume: agent-assist (drafts, summaries, sentiment) is cheaper and lower-risk; autonomous AI agent (Fin, Zendesk AI Agents) replaces L1 entirely but needs Hebrew QA on a 100-ticket sample before launch.

### Step 8: Measure Customer Satisfaction

Set up customer satisfaction measurement (medidat sipuk lakokhot) with Hebrew-localized surveys.

**CSAT and NPS.** Send a 5-point Hebrew CSAT after resolution and a periodic NPS. Before you wire either up, classify the send: a survey carrying any promotional content, discount or repurchase prompt is advertising and needs Section 30A opt-in, while a plain post-resolution rating is transactional. The Hebrew survey wording is in `references/consumer-protection-law.md`.

**Key metrics dashboard:**

| Metric | Target | Calculation |
|---|---|---|
| CSAT | > 4.0 / 5.0 | Average of post-resolution ratings |
| NPS | > 30 | % Promoters (9-10) minus % Detractors (0-6) |
| First Response Time | Per SLA tier | Time from ticket creation to first agent response |
| Resolution Time | Per SLA tier | Time from ticket creation to resolution |
| First Contact Resolution (FCR) | Above your own measured baseline | % of tickets resolved in first interaction |
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

Result: Return processed in full compliance with Consumer Protection Law 1981, Section 14C (14ג).

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
4. Build metrics dashboard with targets you set from your own baseline (CSAT, NPS, FCR)
5. Define reporting cadence (daily, weekly, monthly, quarterly)
6. Integrate with Monday.com for real-time visibility

Result: Complete satisfaction measurement system with Hebrew surveys and actionable metrics.

## Bundled Resources

### Scripts
- `scripts/ticket-classifier.py` -- Classify Hebrew support tickets by category and priority based on keyword analysis. Supports batch processing from CSV files. Run: `python3 scripts/ticket-classifier.py --help`

### References
- `references/consumer-protection-law.md` -- Key provisions of the Israeli Consumer Protection Law 1981. Covers cooling-off periods, return policies, cancellation fees, warranty obligations, and complaint handling requirements. Consult when handling returns, complaints, or any dispute involving consumer rights.
- `references/hebrew-response-templates.md` -- Ready-to-use Hebrew canned responses for common support scenarios. Includes templates for acknowledgment, refund processing, return instructions, issue resolution, escalation notices, and satisfaction surveys. Consult when creating or customizing support response templates.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Israel Law MCP](https://agentskills.co.il/he/mcp/israel-law) | Query 66 Israeli statutes including Consumer Protection Law provisions directly from the agent, enabling real-time legal reference during complaint handling |
| [Kolzchut (All-Rights)](https://agentskills.co.il/he/mcp/kolzchut) | Search Israel's authoritative rights and entitlements database for consumer rights, return policies, and extended cooling-off eligibility for protected groups |

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Consumer Protection Authority | https://www.gov.il/he/pages/returns | Official return/cancellation policies and consumer rights |
| Kolzchut - Remote Purchase Cancellation | https://www.kolzchut.org.il/he/ביטול_עסקה_שנעשתה_באינטרנט_או_בטלפון | Cooling-off periods, cancellation fees, extended rights for protected groups |
| Kolzchut - Free Telephone Service Right | https://www.kolzchut.org.il/he/מענה_טלפוני_חינם_לצרכן_מאת_ספקי_שירותים | 6-minute human-agent wait cap, 3-hour callback rule, sectors covered |
| Consumer Protection Law (Full Text) | https://www.nevo.co.il/law_html/law00/70305.htm | Full text of the law with all amendments |
| Privacy Protection Authority - AI Guidelines | (search gov.il for "Privacy Protection Authority") | AI/chatbot disclosure obligations under Amendment 13 |
| Section 30A Communications Law (Spam) | https://www.gov.il/en/pages/17052018_7 | Marketing SMS/email consent rules, NIS 1,000 per-message statutory damages |
| Small Claims Court Guide | (search gov.il for "small claims court") | Current maximum claim amount and filing procedures |

## Gotchas

- The 14-day cooling-off period in Israel starts from the delivery date or the date the consumer received the contract terms, whichever is later. Agents may calculate it from the purchase date.
- SLA timers must account for the Israeli work week (Sunday-Thursday). A ticket opened on Friday afternoon should not start its SLA clock until Sunday 08:30.
- The Hebrew word for "complaint" (תלונה) and "query" (שאילתה) are often confused by text classifiers. Auto-categorization should weight escalation keywords like "עורך דין" (lawyer) and "בית משפט" (court) heavily.
- Israeli Consumer Protection Law allows a maximum cancellation fee of 5% of the price or NIS 100, whichever is lower. Agents may use 5% without the 100 NIS cap, overcharging on small transactions.
- WhatsApp is the dominant consumer messaging channel in Israel and the preferred support channel. Agents may default to email-first support strategies that don't match Israeli consumer expectations.
- Protected groups (people with disabilities, citizens 65+, new immigrants within 5 years of receiving their immigrant certificate) get a 4-month cooling-off period on remote purchases, not 14 days. A naive 14-day calculator will wrongly reject these returns. Add a customer-profile check before any auto-rejection.
- The 6-minute phone wait cap runs **from the start of the call** (measured only after any language and region selection), not from the moment the caller reaches the human queue, and it is per call rather than a call-centre average. A long IVR menu does NOT buy you time. It also binds only Second-Schedule sectors, so check applicability before promising it to anyone.
- Marketing SMS without prior opt-in carries up to NIS 1,000 in statutory damages per message (Section 30A Communications Law). Transactional support messages (order updates, ticket replies, password resets) are exempt; marketing blasts are not. Agents may treat all outbound SMS the same.

## Troubleshooting

### Error: "Ticket categorized incorrectly"
Cause: Hebrew keyword detection matched the wrong category (e.g., "payment" matched billing instead of returns)
Solution: Review the keyword detection table in Step 1. Add more specific subcategory keywords. Use the classifier script with `--verbose` flag to see matching details: `python3 scripts/ticket-classifier.py --text "..." --verbose`

### Error: "SLA timer not pausing on weekends"
Cause: Business hours configuration does not account for Shabbat (Saturday) and the Israeli work week
Solution: Verify the business hours config in Step 3. Ensure Friday is set to close at 13:00 (or fully closed) and Saturday is marked as non-business. Check that the timezone is set to Asia/Jerusalem.

### Error: "Return request rejected but customer is within 14-day period"
Cause: The 14-day period was calculated from the order date instead of from receipt of the goods or receipt of the Section 14C(b) disclosure document, whichever is later. Note that contract signature is NOT a trigger
Solution: Per Consumer Protection Law Section 14C (14ג), the cooling-off period starts from the later of: (1) delivery date, or (2) the date the consumer received the contract terms and cancellation details. Recalculate accordingly.

### Error: "Escalation notification not reaching supervisor"
Cause: Notification channel is misconfigured or supervisor assignment rules are not matching
Solution: Check the escalation routing rules in Step 4. Verify that supervisor contact details are up to date. Test the notification webhook. For WhatsApp notifications, ensure the supervisor's phone number is registered with WhatsApp Business API.
