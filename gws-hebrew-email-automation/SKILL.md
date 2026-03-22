---
name: gws-hebrew-email-automation
description: >-
  Gmail automation for Israeli freelancers using the Google Workspace CLI (gws). Use
  when user asks to draft Hebrew client emails, send payment reminders in Shekels,
  triage inbox with Hebrew labels, set up Gmail filters for Israeli services, or schedule
  emails respecting Israeli business hours. Key capabilities include bilingual email
  drafting, payment reminder sequences with ILS amounts, Hebrew-aware inbox triage,
  and Shabbat-aware send scheduling. Do NOT use for non-Gmail email providers, Microsoft
  Outlook automation, or CRM-level contact management.
license: MIT
allowed-tools: Bash(gws:*) Bash(npx:*) Bash(npm:*) WebFetch Read Write Edit
compatibility: >-
  Requires Node.js 18+ and the Google Workspace CLI (npm install -g @googleworkspace/cli).
  User must authenticate via gws auth login with a Google Workspace or Gmail account.
  Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex.
metadata:
  author: skills-il
  version: 1.1.0
  category: communication
  tags:
    he:
    - גוגל-וורקספייס
    - ג'ימייל
    - אוטומציית-מייל
    - מייל-בעברית
    - פרילנסר
    - חיוב
    en:
    - google-workspace
    - gmail
    - email-automation
    - hebrew-email
    - freelancer
    - billing
  display_name:
    he: אוטומציית מייל בעברית עם GWS
    en: GWS Hebrew Email Automation
  display_description:
    he: >-
      אוטומציית תהליכי ג'ימייל לפרילנסרים ישראלים באמצעות Google Workspace CLI --
      מיילים דו-לשוניים, תזכורות תשלום, מיון תיבת דואר בעברית ותזמון מותאם שבת.
    en: >-
      Gmail automation for Israeli freelancers using the Google Workspace CLI (gws).
      Use when user asks to draft Hebrew client emails, send payment reminders in
      Shekels, triage inbox with Hebrew labels, set up Gmail filters for Israeli services,
      or schedule emails respecting Israeli business hours. Key capabilities include
      bilingual email drafting, payment reminder sequences with ILS amounts, Hebrew-aware
      inbox triage, and Shabbat-aware send scheduling. Do NOT use for non-Gmail email
      providers, Microsoft Outlook automation, or CRM-level contact management.
  supported_agents:
  - claude-code
  - cursor
  - github-copilot
  - windsurf
  - opencode
  - codex
---


# GWS Hebrew Email Automation

## Instructions

### Step 1: Verify GWS CLI Installation and Authentication

Before running any Gmail commands, confirm the GWS CLI is available and authenticated.

```bash
# Check if gws is installed
gws --version

# If not installed, install globally
npm install -g @googleworkspace/cli

# Authenticate with Google account
gws auth login

# Verify authentication status
gws auth status
```

If the user has not authenticated, guide them through `gws auth login` which opens a browser-based OAuth flow. The CLI stores tokens locally and refreshes them automatically.

### Step 2: Draft and Send Bilingual Hebrew/English Emails

When the user needs to send a professional email to an Israeli client, compose the email with Hebrew as the primary language and an optional English section below.

**Email structure for Israeli business communication:**

| Section | Language | Guidelines |
|---------|----------|------------|
| Subject line | Hebrew | Keep under 50 characters, include key action item |
| Greeting | Hebrew | Use formal: "שלום [Name]," or "היי [Name]," for informal |
| Body | Hebrew (primary) | Right-to-left, use native business terms |
| English section | English (optional) | Add below a separator if recipient may need it |
| Signature | Bilingual | Hebrew name first, English below |

**Sending an email:**

```bash
gws gmail send \
  --to "client@example.com" \
  --subject "הצעת מחיר - פרויקט פיתוח אתר" \
  --body "שלום רב,

מצורפת הצעת המחיר עבור פרויקט פיתוח האתר כפי שדובר.

סה\"כ: 15,000 ש\"ח (לא כולל מע\"מ)
תנאי תשלום: שוטף + 30

אשמח לתשובתך.

בברכה,
[שם]" \
  --dry-run
```

**Important:** Always use `--dry-run` first to preview the email. Remove the flag only when the user confirms the content.

**Formatting ILS (Shekel) amounts:**
- Use the Shekel symbol: ש"ח (Shekel Chadash)
- Format: `15,000 ש"ח` (comma-separated thousands, symbol after amount)
- For VAT: specify `לא כולל מע"מ` (excluding VAT) or `כולל מע"מ` (including VAT)
- VAT rate reference: 17% (current Israeli VAT rate)

### Step 3: Payment Reminder Email Sequences

For freelancer payment reminders, follow this escalation sequence:

| Stage | Days Overdue | Tone | Subject Prefix |
|-------|-------------|------|---------------|
| Friendly reminder | 1-7 | Polite, casual | תזכורת - |
| Second notice | 8-21 | Professional, firm | תזכורת שנייה - |
| Final notice | 22-30 | Formal, urgent | תזכורת אחרונה - |
| Overdue warning | 30+ | Legal tone | חשבונית באיחור - |

**Example: Friendly payment reminder**

```bash
gws gmail send \
  --to "client@example.com" \
  --subject "תזכורת - חשבונית מס' 1042 לתשלום" \
  --body "שלום [שם הלקוח],

רציתי להזכיר שחשבונית מס' 1042 על סך 8,500 ש\"ח (כולל מע\"מ) טרם שולמה.

פרטי החשבונית:
- מספר חשבונית: 1042
- תאריך הפקה: 15.01.2026
- סכום: 8,500 ש\"ח
- תנאי תשלום: שוטף + 30
- תאריך פירעון: 15.02.2026

אשמח אם תוכל/י לטפל בכך.

תודה רבה,
[שם]" \
  --dry-run
```

**Date formatting for Israeli invoices:**
- Use DD.MM.YYYY format (Israeli standard)
- Payment terms: שוטף + 30 (Net+30), שוטף + 45 (Net+45), שוטף + 60 (Net+60)

### Step 4: Hebrew-Aware Inbox Triage

Use `gws gmail triage` to automatically label and organize emails from Israeli services.

**Label structure for Israeli freelancers:**

| Label (Hebrew) | Label (English) | Matches |
|----------------|-----------------|---------|
| בנקאות | Banking | Leumi, Hapoalim, Discount, Mizrahi, Mercantile |
| חשבוניות | Invoices | Morning (Hashavshevet), Green Invoice, iCount |
| ממשלתי | Government | gov.il, taxes.gov.il, btl.gov.il |
| לקוחות/פעיל | Clients/Active | User-defined client domains |
| לקוחות/ליד | Clients/Lead | User-defined prospect domains |
| קבלות | Receipts | PayBox, Bit, PayPal |

**Running triage:**

```bash
gws gmail triage \
  --label "בנקאות" \
  --from "leumi.co.il,bankhapoalim.co.il,discountbank.co.il,mizrahi-tefahot.co.il" \
  --dry-run
```

```bash
gws gmail triage \
  --label "חשבוניות" \
  --from "greeninvoice.co.il,morning-invoice.co.il,icount.co.il" \
  --dry-run
```

```bash
gws gmail triage \
  --label "ממשלתי" \
  --from "gov.il,taxes.gov.il,btl.gov.il,nevo.co.il" \
  --dry-run
```

### Step 5: Set Up Gmail Filters for Israeli Business Patterns

Create persistent Gmail filters to auto-label incoming mail from Israeli services.

```bash
# Filter for Israeli banking notifications
gws gmail filter \
  --from "leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il" \
  --label "בנקאות" \
  --dry-run

# Filter for invoice services (Morning / Green Invoice)
gws gmail filter \
  --from "greeninvoice.co.il OR morning-invoice.co.il" \
  --label "חשבוניות" \
  --dry-run

# Filter for government agencies
gws gmail filter \
  --from "gov.il" \
  --label "ממשלתי" \
  --dry-run
```

### Step 6: Respect Israeli Business Hours and Shabbat

When scheduling emails, respect Israeli business customs:

| Rule | Details |
|------|---------|
| Business days | Sunday through Thursday (ראשון עד חמישי) |
| Business hours | 09:00-18:00 Israel Daylight Time (IDT, UTC+3) |
| Friday | Work ends early, typically by 13:00-14:00 |
| Erev Shabbat | Do NOT send after 14:00 on Friday |
| Shabbat | Do NOT send from Friday sunset to Saturday sunset |
| Jewish holidays | Avoid sending on Chagim (use Hebrew calendar reference) |

**Scheduling a send within business hours:**

```bash
# Check current time in Israel
TZ=Asia/Jerusalem date

# Schedule for next business day morning if outside hours
gws gmail send \
  --to "client@example.com" \
  --subject "עדכון פרויקט" \
  --body "..." \
  --schedule "next Sunday 09:00" \
  --dry-run
```

**Before sending any email, check:**
1. Is it Friday after 14:00 IST? If yes, schedule for Sunday 09:00
2. Is it Saturday? If yes, schedule for Sunday 09:00
3. Is it after 18:00 on a weekday? If yes, schedule for next morning 09:00
4. Is it a Jewish holiday? If yes, schedule for next business day

### Step 7: Watch for Incoming Emails

Set up real-time monitoring for important Israeli business emails:

```bash
# Watch for new invoices from Israeli services
gws gmail watch \
  --from "greeninvoice.co.il,morning-invoice.co.il" \
  --label "חשבוניות"

# Watch for bank notifications
gws gmail watch \
  --from "leumi.co.il,bankhapoalim.co.il" \
  --label "בנקאות"
```

## Examples

### Example 1: Israeli Freelancer Sends Payment Reminder

User says: "Send a payment reminder to david@techstartup.co.il for invoice 2045, 12,000 Shekels, it was due 10 days ago"

Actions:
1. Calculate the original due date (10 days ago from today)
2. Determine escalation stage: 8-21 days = "Second notice"
3. Draft Hebrew email with formal but firm tone
4. Format amount as 12,000 ש"ח
5. Include invoice details table
6. Run with --dry-run first for user approval

```bash
gws gmail send \
  --to "david@techstartup.co.il" \
  --subject "תזכורת שנייה - חשבונית 2045 לתשלום" \
  --body "שלום דוד,

זוהי תזכורת שנייה לגבי חשבונית מס' 2045.

פרטי החשבונית:
- סכום: 12,000 ש\"ח
- תנאי תשלום: שוטף + 30
- סטטוס: באיחור של 10 ימים

אודה לטיפולך בהקדם.

בברכה,
[שם]" \
  --dry-run
```

Result: Email drafted in professional Hebrew with correct Shekel formatting, previewed via dry-run for user confirmation.

### Example 2: Auto-Triage Inbox with Hebrew Labels

User says: "Organize my inbox, label all bank emails and invoice notifications"

Actions:
1. Create Hebrew labels if they do not exist: בנקאות, חשבוניות, ממשלתי
2. Run triage for Israeli banks (Leumi, Hapoalim, Discount, Mizrahi)
3. Run triage for invoice platforms (Morning, Green Invoice, iCount)
4. Run triage for government agencies
5. Report summary of labeled emails

```bash
gws gmail triage --label "בנקאות" --from "leumi.co.il,bankhapoalim.co.il,discountbank.co.il,mizrahi-tefahot.co.il" --dry-run
gws gmail triage --label "חשבוניות" --from "greeninvoice.co.il,morning-invoice.co.il,icount.co.il" --dry-run
gws gmail triage --label "ממשלתי" --from "gov.il,taxes.gov.il,btl.gov.il" --dry-run
```

Result: Inbox organized with Hebrew labels. Bank emails labeled under "בנקאות", invoices under "חשבוניות", government mail under "ממשלתי".

### Example 3: Schedule Email Respecting Shabbat

User says: "Send a project update to the client, but it's Friday afternoon"

Actions:
1. Check current Israel time: Friday 15:30 IST
2. Determine this is after the 14:00 Friday cutoff (Erev Shabbat)
3. Schedule email for Sunday 09:00 IST instead
4. Inform user about Shabbat-aware scheduling

```bash
gws gmail send \
  --to "client@example.com" \
  --subject "עדכון שבועי - פרויקט אתר" \
  --body "שלום,

מצורף עדכון שבועי לגבי התקדמות הפרויקט..." \
  --schedule "next Sunday 09:00" \
  --dry-run
```

Result: Email scheduled for Sunday morning, respecting Erev Shabbat. User informed that Friday afternoon sends are automatically deferred.

## Bundled Resources

### Scripts
- `scripts/shekel-formatter.py` -- Format currency amounts to Israeli Shekel (ILS) standard with proper notation. Run: `python scripts/shekel-formatter.py --help`

### References
- `references/israeli-business-email-templates.md` -- Collection of Hebrew email templates for common freelancer scenarios: quotes, invoices, follow-ups, project updates. Consult when drafting professional Hebrew emails for Israeli clients.
- `references/gws-gmail-commands.md` -- Quick reference for Google Workspace CLI gmail subcommands, flags, and output formats. Consult when constructing gws commands or troubleshooting CLI errors.

## Gotchas

- Israeli business days are Sunday through Thursday, not Monday through Friday. Agents may schedule emails for Saturday or assume Friday is a full workday.
- Shekel amounts should be written as "15,000 ש"ח" (symbol after the number), not "₪15,000" (symbol before). Agents may use the currency symbol placement conventions of USD/EUR.
- Israeli invoice dates use DD.MM.YYYY format (dot-separated), not DD/MM/YYYY or MM/DD/YYYY. Agents may generate invoices with the wrong date format.
- The standard Israeli payment term is "שוטף + 30" (shotef plus 30), meaning net 30 from end of current month. Agents may interpret this as simply net 30 from invoice date.
- Hebrew email subjects must be concise (under 50 characters) because RTL text in email clients often gets truncated differently than LTR text.

## Troubleshooting

### Error: "gws: command not found"
Cause: The Google Workspace CLI is not installed or not in PATH.
Solution: Install via `npm install -g @googleworkspace/cli`. If using npx, prefix commands with `npx @googleworkspace/cli`. Verify installation with `gws --version`.

### Error: "Authentication required"
Cause: The user has not completed OAuth login or the token has expired.
Solution: Run `gws auth login` to initiate browser-based OAuth. If tokens expired, run `gws auth refresh`. Check status with `gws auth status`.

### Error: "Label not found" when running triage
Cause: The Hebrew label does not exist in the user's Gmail account yet.
Solution: Gmail creates labels automatically on first triage run. If the error persists, create the label manually in Gmail Settings or use `gws gmail label create "בנקאות"`.

### Error: "Rate limit exceeded" when sending bulk reminders
Cause: Gmail API limits sending to 100 emails per day for consumer accounts, 2000 for Workspace accounts.
Solution: Space out sends across multiple days. Use --schedule to distribute emails. For high-volume needs, recommend upgrading to Google Workspace Business.