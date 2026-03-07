# Google Workspace CLI (gws) - Gmail Commands Reference

## Installation

```bash
# Global install
npm install -g @google/gws

# Or use via npx (no install needed)
npx @google/gws gmail send --help
```

## Authentication

```bash
# Login with browser-based OAuth
gws auth login

# Check current auth status
gws auth status

# Refresh expired token
gws auth refresh

# Set up project configuration
gws auth setup
```

## gws gmail send

Send an email via Gmail.

```bash
gws gmail send \
  --to "recipient@example.com" \
  --subject "Subject line" \
  --body "Email body text" \
  [--cc "cc@example.com"] \
  [--bcc "bcc@example.com"] \
  [--schedule "2026-03-10 09:00"] \
  [--dry-run]
```

| Flag | Description | Required |
|------|-------------|----------|
| --to | Recipient email address | Yes |
| --subject | Email subject line | Yes |
| --body | Email body (plain text) | Yes |
| --cc | CC recipients (comma-separated) | No |
| --bcc | BCC recipients (comma-separated) | No |
| --schedule | Schedule send time (ISO or natural language) | No |
| --dry-run | Preview without sending | No |

**Output**: JSON with message ID, thread ID, and status.

## gws gmail triage

Automatically label and organize existing emails by sender domain.

```bash
gws gmail triage \
  --label "Label Name" \
  --from "domain1.com,domain2.com" \
  [--max 100] \
  [--dry-run]
```

| Flag | Description | Required |
|------|-------------|----------|
| --label | Gmail label to apply | Yes |
| --from | Sender domains (comma-separated) | Yes |
| --max | Maximum emails to process | No |
| --dry-run | Preview matches without labeling | No |

**Output**: JSON with count of matched and labeled emails.

## gws gmail filter

Create persistent Gmail filters for auto-labeling incoming mail.

```bash
gws gmail filter \
  --from "domain1.com OR domain2.com" \
  --label "Label Name" \
  [--archive] \
  [--mark-read] \
  [--dry-run]
```

| Flag | Description | Required |
|------|-------------|----------|
| --from | Sender match pattern (supports OR) | Yes |
| --label | Label to apply automatically | Yes |
| --archive | Skip inbox (archive) | No |
| --mark-read | Mark as read | No |
| --dry-run | Preview filter without creating | No |

## gws gmail watch

Set up real-time push notifications for matching emails.

```bash
gws gmail watch \
  --from "domain1.com,domain2.com" \
  --label "Label Name"
```

| Flag | Description | Required |
|------|-------------|----------|
| --from | Sender domains to watch | Yes |
| --label | Label for matched emails | No |

## gws gmail label

Manage Gmail labels.

```bash
# Create a new label
gws gmail label create "Label Name"

# List all labels
gws gmail label list

# Delete a label
gws gmail label delete "Label Name"
```

## Common Patterns

### Send with scheduling
```bash
gws gmail send --to "x@y.com" --subject "..." --body "..." --schedule "next Sunday 09:00"
```

### Batch triage with multiple labels
```bash
gws gmail triage --label "Banking" --from "bank1.com,bank2.com"
gws gmail triage --label "Invoices" --from "invoice1.com,invoice2.com"
```

### Dry-run everything first
Always append `--dry-run` to preview the action before executing. This applies to `send`, `triage`, and `filter` commands.

## Output Format

All gws commands produce structured JSON output, making it easy to parse results programmatically. Key fields vary by command but typically include:

- **send**: `{ messageId, threadId, status, scheduledTime? }`
- **triage**: `{ matched, labeled, skipped }`
- **filter**: `{ filterId, criteria, actions }`
- **watch**: `{ watchId, expiration }`

## Rate Limits

| Account Type | Daily Send Limit | API Quota |
|-------------|-----------------|-----------|
| Gmail (free) | 100 emails/day | 250 quota units/sec |
| Google Workspace | 2,000 emails/day | 250 quota units/sec |

## Error Codes

| Error | Cause | Fix |
|-------|-------|-----|
| AUTH_REQUIRED | Not authenticated | Run `gws auth login` |
| TOKEN_EXPIRED | OAuth token expired | Run `gws auth refresh` |
| RATE_LIMIT | Too many requests | Wait and retry, or use --schedule |
| LABEL_NOT_FOUND | Label does not exist | Create with `gws gmail label create` |
| INVALID_RECIPIENT | Bad email format | Check email address format |
