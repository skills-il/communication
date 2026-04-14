---
name: gws-hebrew-email-automation
description: Gmail automation for Israeli freelancers using the Google Workspace CLI (gws). Use when user asks to draft Hebrew client emails, send payment reminders in Shekels, triage inbox with Hebrew labels, set up Gmail filters for Israeli services, or save drafts for later send that respect Israeli business hours. Key capabilities include bilingual email drafting via gws gmail +send, payment reminder sequences with ILS amounts, Hebrew-aware inbox labeling, and draft-then-send workflows for Shabbat-aware delivery. Do NOT use for non-Gmail email providers, Microsoft Outlook automation, or CRM-level contact management.
license: MIT
allowed-tools: Bash(gws:*) Bash(npx:*) Bash(npm:*) WebFetch Read Write Edit
compatibility: Requires Node.js 18+, a Google Cloud project with the Gmail API enabled, and the Google Workspace CLI (npm install -g @googleworkspace/cli). User must run gws auth setup once (to create OAuth credentials) and gws auth login to grant Gmail scopes. Works with Claude Code, Cursor, GitHub Copilot, Windsurf, OpenCode, Codex, Gemini CLI.
---


# GWS Hebrew Email Automation

## Instructions

### Step 1: Install and Authenticate gws

Before any Gmail command, confirm `gws` is installed and authenticated. `gws` is a community-built Rust binary distributed on npm as `@googleworkspace/cli`. It is not an officially supported Google product, so the user must provide their own Google Cloud project and OAuth client.

```bash
# Check version (latest is 0.22.x)
gws --version

# Install globally if missing
npm install -g @googleworkspace/cli

# First-time setup: walks through GCP project, enables Gmail API,
# creates a Desktop OAuth client. Requires gcloud CLI.
gws auth setup

# Log in and grant Gmail scopes (prompts a browser)
gws auth login --scopes gmail

# Confirm you are authenticated
gws auth status
```

If `gws auth setup` cannot find `gcloud`, open the Google Cloud Console, create a project, enable the Gmail API, create a Desktop-type OAuth client, and save the downloaded JSON to `~/.config/gws/client_secret.json`. Then run `gws auth login --scopes gmail`.

Tokens are encrypted at rest (AES-256-GCM) and refreshed automatically, so there is no separate `refresh` command.

### Step 2: Draft and Send Bilingual Hebrew/English Emails

When the user needs to send a professional email to an Israeli client, compose the email with Hebrew as the primary language and an optional English section below.

**Email structure for Israeli business communication:**

| Section | Language | Guidelines |
|---------|----------|------------|
| Subject line | Hebrew | Keep under 50 characters, include key action item |
| Greeting | Hebrew | Use formal `שלום [שם],` or informal `היי [שם],` |
| Body | Hebrew (primary) | Right-to-left, use native business terms |
| English section | English (optional) | Add below a separator if recipient may need it |
| Signature | Bilingual | Hebrew name first, English below |

**Sending an email with the `+send` helper:**

The `+` prefix marks hand-crafted helper commands in `gws`, they exist alongside the auto-generated Discovery surface and never collide with Discovery method names. Real flags for `gws gmail +send`: `--to`, `--subject`, `--body`, `--cc`, `--bcc`, `--from`, `--attach`/`-a`, `--html`, `--draft`, `--dry-run`.

```bash
gws gmail +send \
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

**Important:** Always run with `--dry-run` first to preview the full request. Remove the flag only after the user confirms the content. For user review before commit, use `--draft` to save the message as a Gmail draft instead of sending.

**Formatting ILS (Shekel) amounts:**
- Use the Shekel abbreviation: `ש"ח` (Shekel Chadash)
- Format: `15,000 ש"ח` (comma-separated thousands, abbreviation after the number)
- For VAT: specify `לא כולל מע"מ` (excluding VAT) or `כולל מע"מ` (including VAT)
- Current Israeli VAT rate: **18%** (raised from 17% on 1 January 2025 per the Arrangements Law). Use `scripts/shekel-formatter.py --vat` to compute the breakdown.

### Step 3: Payment Reminder Email Sequences

For freelancer payment reminders, follow this escalation sequence:

| Stage | Days Overdue | Tone | Subject Prefix |
|-------|-------------|------|---------------|
| Friendly reminder | 1-7 | Polite, casual | תזכורת - |
| Second notice | 8-21 | Professional, firm | תזכורת שנייה - |
| Final notice | 22-30 | Formal, urgent | תזכורת אחרונה - |
| Overdue warning | 30+ | Legal tone | חשבונית באיחור - |

**Example: Friendly payment reminder saved as a draft for user review**

```bash
gws gmail +send \
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
  --draft
```

Save as `--draft`, then have the user open Gmail to review and click Send (or schedule from the Gmail UI).

**Date formatting for Israeli invoices:**
- Use DD.MM.YYYY format (Israeli standard)
- Payment terms: שוטף + 30 (net 30 from end of current month), שוטף + 45, שוטף + 60

### Step 4: Triage the Inbox and Apply Hebrew Labels

The `+triage` helper is a read-only summary, it lists unread messages but does not label anything. To actually apply Hebrew labels to matching emails, combine three Discovery-surface commands: list labels, list messages matching a query, then modify each message to add the label.

**4a. Show an unread inbox summary (read-only):**

```bash
# Default: 20 most recent unread messages in a table
gws gmail +triage

# Narrow by Gmail search query
gws gmail +triage --max 10 --query "from:(leumi.co.il OR bankhapoalim.co.il)"

# Include label names per message
gws gmail +triage --labels
```

Flags accepted by `+triage`: `--max`, `--query`, `--labels`. No `--from` or `--label` flag exists.

**4b. Create a Hebrew label (first time only):**

```bash
gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "בנקאות", "labelListVisibility": "labelShow", "messageListVisibility": "show"}' \
  --dry-run
```

Capture the returned `id` (for example `Label_1234567890`) for the next step.

**4c. List messages matching a Gmail query, then apply the label:**

```bash
# Find bank emails (use Gmail search syntax in `q`)
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:(leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il OR mizrahi-tefahot.co.il)", "maxResults": 50}' \
  | jq -r '.messages[].id' > /tmp/bank-msg-ids.txt

# Apply the label to each matched message
while read -r msg_id; do
  gws gmail users messages modify \
    --params "{\"userId\": \"me\", \"id\": \"$msg_id\"}" \
    --json '{"addLabelIds": ["Label_1234567890"]}' \
    --dry-run
done < /tmp/bank-msg-ids.txt
```

**Label structure for Israeli freelancers:**

| Label (Hebrew) | Label (English) | Suggested `q:` query |
|----------------|-----------------|----------------------|
| בנקאות | Banking | `from:(leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il OR mizrahi-tefahot.co.il OR mercantile.co.il)` |
| חשבוניות | Invoices | `from:(greeninvoice.co.il OR icount.co.il OR ezcount.co.il OR hashavshevet.co.il)` |
| ממשלתי | Government | `from:(gov.il OR taxes.gov.il OR btl.gov.il)` |
| לקוחות/פעיל | Clients/Active | User-defined client domains |
| קבלות | Receipts | `from:(paybox.co.il OR bitpay.co.il OR paypal.com)` |

### Step 5: Create Persistent Gmail Filters

Gmail filters auto-label incoming mail. There is no `gws gmail +filter` helper; use the Discovery-surface `users settings filters create` method with the real Gmail filter schema.

```bash
# Filter: label Israeli banking notifications
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il"},
    "action": {"addLabelIds": ["Label_1234567890"]}
  }' \
  --dry-run

# Filter: archive receipts automatically (skip inbox, apply label)
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "greeninvoice.co.il OR icount.co.il"},
    "action": {"addLabelIds": ["Label_2345678901"], "removeLabelIds": ["INBOX"]}
  }' \
  --dry-run
```

Use `gws gmail users settings filters list --params '{"userId": "me"}'` to audit existing filters and `gws gmail users settings filters delete --params '{"userId": "me", "id": "FILTER_ID"}'` to remove one.

### Step 6: Respect Israeli Business Hours and Shabbat

`gws gmail +send` does **not** have a scheduled-send flag. Gmail's scheduled send is only available in the Gmail web and mobile UIs. To respect Israeli business customs from the CLI, save drafts with `--draft` and let the user review and send (or schedule) them from Gmail.

| Rule | Details |
|------|---------|
| Business days | Sunday through Thursday (ראשון עד חמישי) |
| Business hours | 09:00-18:00 Israel time (IST winter UTC+2 / IDT summer UTC+3) |
| Friday | Work ends early, typically by 13:00-14:00 |
| Erev Shabbat | Do NOT send after 14:00 on Friday |
| Shabbat | Do NOT send from Friday sunset to Saturday night |
| Jewish holidays | Avoid sending on Chagim |

**Recommended workflow:**

```bash
# 1. Check current time in Israel
TZ=Asia/Jerusalem date

# 2. If outside business hours, save as draft for user review
gws gmail +send \
  --to "client@example.com" \
  --subject "עדכון פרויקט" \
  --body "שלום,

מצורף עדכון שבועי לגבי התקדמות הפרויקט..." \
  --draft

# 3. Tell the user: draft was saved. Open Gmail, Drafts,
#    click Schedule send, and pick Sunday 09:00 Israel time.
```

**Before drafting any outgoing email, check:**
1. Is it Friday after 14:00 Israel time? Save as `--draft` and tell the user to schedule for Sunday 09:00.
2. Is it Shabbat (Friday sunset to Saturday night)? Save as `--draft`.
3. Is it after 18:00 on a weekday? Save as `--draft` and suggest next-morning send.
4. Is it a Jewish holiday (check with the user)? Save as `--draft`.

### Step 7: Watch for Incoming Emails (Advanced, Optional)

The `+watch` helper streams new emails as NDJSON using Gmail's push notifications over Google Pub/Sub. It requires a GCP project with Pub/Sub enabled and only filters by **label IDs**, not sender domains. Use it when the user needs real-time reactions (new invoice then Slack ping), not for passive inbox organization.

```bash
# One-off pull: fetch new messages in INBOX once, then exit
gws gmail +watch \
  --project my-gcp-project \
  --label-ids INBOX \
  --once

# Long-running watch with automatic Pub/Sub cleanup
gws gmail +watch \
  --project my-gcp-project \
  --label-ids INBOX,UNREAD \
  --cleanup \
  --output-dir ./incoming
```

Real flags: `--project`, `--subscription`, `--topic`, `--label-ids`, `--max-messages`, `--poll-interval`, `--msg-format`, `--once`, `--cleanup`, `--output-dir`. Gmail watch registrations expire after 7 days and must be renewed. If the user does not already have Pub/Sub set up, skip this step, the basic labeling workflow in Step 4 is sufficient for most freelancers.

## Examples

### Example 1: Israeli Freelancer Sends Payment Reminder

User says: "Send a payment reminder to david@techstartup.co.il for invoice 2045, 12,000 Shekels, it was due 10 days ago"

Actions:
1. Calculate the original due date (10 days ago from today)
2. Determine escalation stage: 8-21 days = "Second notice"
3. Draft Hebrew email with professional, firm tone
4. Format amount as `12,000 ש"ח`
5. Include invoice details
6. Save as `--draft` for user review before sending

```bash
gws gmail +send \
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
  --draft
```

Result: Email saved as a Gmail draft in professional Hebrew with correct Shekel formatting. User opens Gmail, Drafts, Send.

### Example 2: Label Bank Emails with a Hebrew Label

User says: "Organize my inbox, label all bank emails with בנקאות"

Actions:
1. Create the Hebrew label if it does not exist, capture its `id`
2. List unread messages from Israeli banks with `users messages list`
3. For each matched message, apply the label with `users messages modify`
4. Report the count

```bash
# Create label (run once)
LABEL_ID=$(gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "בנקאות"}' | jq -r '.id')

# List bank emails
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:(leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il OR mizrahi-tefahot.co.il)", "maxResults": 50}' \
  | jq -r '.messages[].id' > /tmp/bank-msgs.txt

# Apply label
while read -r id; do
  gws gmail users messages modify \
    --params "{\"userId\": \"me\", \"id\": \"$id\"}" \
    --json "{\"addLabelIds\": [\"$LABEL_ID\"]}"
done < /tmp/bank-msgs.txt

echo "Labeled $(wc -l < /tmp/bank-msgs.txt) bank messages under בנקאות"
```

Result: All matching bank emails carry the בנקאות label in Gmail.

### Example 3: Draft an Email Instead of Sending on Friday Afternoon

User says: "Send a project update to the client, but it's Friday afternoon"

Actions:
1. Check current Israel time: `TZ=Asia/Jerusalem date` shows Friday 15:30 IDT
2. Determine this is after the 14:00 Friday cutoff (Erev Shabbat)
3. Save the message as a Gmail draft rather than sending
4. Tell the user to open Gmail Drafts and click Schedule send for Sunday 09:00

```bash
TZ=Asia/Jerusalem date
# Fri Apr 17 15:30:12 IDT 2026, past 14:00, do not send

gws gmail +send \
  --to "client@example.com" \
  --subject "עדכון שבועי - פרויקט אתר" \
  --body "שלום,

מצורף עדכון שבועי לגבי התקדמות הפרויקט..." \
  --draft
```

Result: Draft saved. User informed that Friday-afternoon sends are deferred, open Gmail Drafts to review and schedule send for Sunday 09:00 Israel time.

## Bundled Resources

### Scripts
- `scripts/shekel-formatter.py` — Format currency amounts to Israeli Shekel (ILS) standard with proper notation and optional 18% VAT breakdown. Run: `python scripts/shekel-formatter.py --help`

### References
- `references/israeli-business-email-templates.md` — Collection of Hebrew email templates for common freelancer scenarios: quotes, invoices, follow-ups, project updates. Consult when drafting professional Hebrew emails for Israeli clients.
- `references/gws-gmail-commands.md` — Quick reference for the real `gws gmail` commands used in this skill (`+send`, `+triage`, `+watch`, plus the Discovery-surface `users.labels`, `users.messages.list/modify`, `users.settings.filters`). Consult when constructing or troubleshooting `gws` calls.

## Recommended MCP Servers

No Gmail or Google Workspace MCP servers are currently listed in the skills-il directory. If a user prefers tool-driven access over CLI commands, point them to `gws auth setup` and the instructions in Step 1, the CLI is the supported path.

## Gotchas

- `gws` helper commands use a `+` prefix (`gws gmail +send`, `gws gmail +triage`, `gws gmail +watch`). Agents trained on other CLI conventions frequently drop the `+` and generate commands that error with "unknown subcommand". Always include the plus sign for helpers.
- `gws gmail +send` has **no** `--schedule` flag. Gmail's scheduled send only exists in the Gmail web and mobile UI. Agents that assume a `--schedule` flag will generate commands that error. Use `--draft` and tell the user to schedule from Gmail if they need deferred delivery.
- `gws gmail +triage` is **read-only**, it shows a table of unread messages but never modifies the mailbox. To actually apply labels, use the Discovery-surface `users messages list` plus `users messages modify` sequence in Step 4. Agents often conflate the two.
- Israeli business days are Sunday through Thursday, not Monday through Friday. Agents may schedule emails for Saturday or assume Friday is a full workday.
- Shekel amounts should be written as `15,000 ש"ח` (abbreviation after the number), not `₪15,000`. Agents may use USD/EUR symbol placement conventions.
- Israeli invoice dates use DD.MM.YYYY format (dot-separated), not DD/MM/YYYY or MM/DD/YYYY.
- The standard Israeli payment term `שוטף + 30` means net 30 from **end of current month**, not 30 days from the invoice date. A 01.01 invoice on שוטף + 30 is due 02.28, not 01.31.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Google Workspace CLI README | https://github.com/googleworkspace/cli/blob/main/README.md | Installation, auth flow, helper command list |
| `gws gmail +send` canonical skill | https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-send/SKILL.md | Exact flags accepted by `+send` |
| `gws gmail +triage` canonical skill | https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-triage/SKILL.md | `+triage` is read-only summary, flags `--max`, `--query`, `--labels` |
| `gws gmail +watch` canonical skill | https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-watch/SKILL.md | Pub/Sub requirements, `--label-ids` (not `--from`) |
| Gmail API `users.settings.filters` | https://developers.google.com/gmail/api/reference/rest/v1/users.settings.filters | Filter criteria/action schema for Step 5 |
| Israeli VAT rate (18% from 1 Jan 2025) | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/represent-info-051224-2/he/vat_represent-info-051224-2.pdf | Israel Tax Authority Interpretation Directive 1/2025: raising VAT from 17% to 18% |

## Troubleshooting

### Error: "gws: command not found"
Cause: `@googleworkspace/cli` is not installed or not on `PATH`.
Solution: Install with `npm install -g @googleworkspace/cli`. Confirm with `gws --version`. You can also download a prebuilt binary from the [GitHub Releases](https://github.com/googleworkspace/cli/releases) page and place it on your `PATH`.

### Error: "Access blocked" or 403 during `gws auth login`
Cause: Your OAuth app is in testing mode and your Google account is not listed as a test user, or you requested too many scopes at once (unverified apps are capped at ~25).
Solution: Open the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) in your GCP project, add your email under Test users, and retry with a narrow scope list: `gws auth login --scopes gmail`.

### Error: `accessNotConfigured`, "Gmail API has not been used in project ..."
Cause: The Gmail API is not enabled on the GCP project tied to your OAuth client.
Solution: Follow the `enable_url` printed in the error to the Cloud Console API library, click Enable, wait ~10 seconds, and retry. `gws auth setup` can also enable required APIs automatically.

### Error: "unknown subcommand: send"
Cause: You typed `gws gmail send` instead of `gws gmail +send`. Helper commands in `gws` use the `+` prefix to distinguish them from auto-generated Discovery methods.
Solution: Add the plus sign: `gws gmail +send --to ... --subject ... --body ...`.

### Error: "Label not found" when applying a label
Cause: The Hebrew label does not exist yet, or you used the label name instead of the label `id`.
Solution: Create the label first with `gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "בנקאות"}'`, capture the returned `id`, and pass that `id` to `addLabelIds` in `users messages modify`.

### Error: "Rate limit exceeded" when labeling many messages
Cause: Gmail API enforces per-user quota units per second, bulk `messages modify` calls in a tight loop can trip this.
Solution: Add a small `sleep 0.1` between `modify` calls or process messages in batches. For daily send limits, consumer Gmail is capped at 100 recipients/day and Google Workspace at 2,000 recipients/day.
