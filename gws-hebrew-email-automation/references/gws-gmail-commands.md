# Google Workspace CLI (gws): Gmail Commands Reference

`gws` is a community Rust binary distributed as the npm package `@googleworkspace/cli`. It is **not** an officially supported Google product. All command shapes in this reference come from the canonical SKILL.md files in `googleworkspace/cli`:

- https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-send/SKILL.md
- https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-triage/SKILL.md
- https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-watch/SKILL.md
- https://github.com/googleworkspace/cli/blob/main/README.md

## Installation

```bash
# npm (auto-downloads the right binary from GitHub Releases)
npm install -g @googleworkspace/cli

# Homebrew (macOS / Linux)
brew install googleworkspace-cli

# Prebuilt binaries
# https://github.com/googleworkspace/cli/releases
```

Verify with `gws --version`.

## Authentication

```bash
# First-time setup: creates a GCP project, enables APIs,
# provisions a Desktop OAuth client. Needs the gcloud CLI.
gws auth setup

# Subsequent logins. Filter scopes to avoid the ~25-scope cap
# on unverified (testing-mode) OAuth apps.
gws auth login --scopes gmail

# Check current auth status
gws auth status
```

Tokens are encrypted at rest (AES-256-GCM) and refreshed automatically. There is no separate `gws auth refresh` command.

## Two surfaces: `+helpers` and Discovery methods

`gws` exposes two kinds of Gmail commands side by side:

| Surface | Prefix | How it works |
|---------|--------|--------------|
| Helpers | `+` | Hand-crafted subcommands for common workflows |
| Discovery | none | Auto-generated from Google's Discovery Service at runtime, one subcommand per API method |

Helper commands always start with `+` (`gws gmail +send`), which is how they are distinguished from Discovery methods (`gws gmail users messages send`). Omitting the `+` on a helper errors with "unknown subcommand".

Run `gws gmail --help` to see both surfaces together.

## `gws gmail +send`: Send an email

```bash
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi!'
```

| Flag | Required | Description |
|------|----------|-------------|
| `--to` | yes | Recipient email address(es), comma-separated |
| `--subject` | yes | Email subject |
| `--body` | yes | Email body (plain text by default) |
| `--cc` | no | CC address(es), comma-separated |
| `--bcc` | no | BCC address(es), comma-separated |
| `--from` | no | Sender address for a configured send-as alias |
| `--attach` / `-a` | no | Attach a file (repeat for multiple, 25 MB total limit) |
| `--html` | no | Treat `--body` as HTML |
| `--draft` | no | Save as a Gmail draft instead of sending |
| `--dry-run` | no | Print the request that would be sent without executing it |

**Notes**
- **No `--schedule` flag exists.** Gmail's scheduled send is only available in the Gmail web and mobile UI. For deferred delivery, save the message with `--draft` and schedule from Gmail.
- `--html` accepts fragment tags (`<p>`, `<b>`, `<a>`, `<br>`, etc.), no `<html>`/`<body>` wrapper needed.
- `--from` only works for aliases that are already configured as send-as addresses in your Gmail settings.

## `gws gmail +triage`: Unread inbox summary

```bash
gws gmail +triage
gws gmail +triage --max 5 --query 'from:boss'
gws gmail +triage --labels
```

| Flag | Default | Description |
|------|---------|-------------|
| `--max` | 20 | Maximum messages to show |
| `--query` | `is:unread` | Gmail search query |
| `--labels` | off | Include label names per message |

**`+triage` is read-only.** It prints a table and never modifies the mailbox. To apply labels, use the Discovery sequence below.

## `gws gmail +watch`: Stream new emails as NDJSON

```bash
gws gmail +watch --project my-gcp-project --label-ids INBOX --once
gws gmail +watch --project my-gcp-project --cleanup --output-dir ./incoming
```

| Flag | Default | Description |
|------|---------|-------------|
| `--project` | (none) | GCP project ID for Pub/Sub resources |
| `--subscription` | (none) | Existing Pub/Sub subscription (skip setup) |
| `--topic` | (none) | Existing Pub/Sub topic with Gmail push permission |
| `--label-ids` | (none) | Comma-separated Gmail label IDs to filter (e.g., `INBOX`, `UNREAD`) |
| `--max-messages` | 10 | Max messages per pull batch |
| `--poll-interval` | 5 | Seconds between pulls |
| `--msg-format` | `full` | `full`, `metadata`, `minimal`, or `raw` |
| `--once` | off | Pull once and exit |
| `--cleanup` | off | Delete created Pub/Sub resources on exit |
| `--output-dir` | (none) | Write each message as a JSON file in this directory |

**Notes**
- Requires Google Pub/Sub on the same GCP project.
- Filtering is by **label IDs only**, there is no `--from` or sender-domain filter.
- Gmail watch registrations expire after 7 days and must be renewed.

## Discovery-surface Gmail commands used in this skill

Helpers do not cover labels, filters, or per-message modifications. Use the Discovery surface for those.

### Labels

```bash
# Create a label
gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "בנקאות", "labelListVisibility": "labelShow", "messageListVisibility": "show"}'

# List labels
gws gmail users labels list --params '{"userId": "me"}'

# Delete a label
gws gmail users labels delete --params '{"userId": "me", "id": "Label_1234567890"}'
```

### Messages

```bash
# List messages matching a Gmail search query
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:leumi.co.il", "maxResults": 50}'

# Apply labels to a single message
gws gmail users messages modify \
  --params '{"userId": "me", "id": "MESSAGE_ID"}' \
  --json '{"addLabelIds": ["Label_1234567890"], "removeLabelIds": ["UNREAD"]}'

# Fetch a full message
gws gmail users messages get \
  --params '{"userId": "me", "id": "MESSAGE_ID", "format": "full"}'
```

### Filters (persistent auto-labeling)

```bash
# Create a filter
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "leumi.co.il OR bankhapoalim.co.il"},
    "action": {"addLabelIds": ["Label_1234567890"]}
  }'

# List filters
gws gmail users settings filters list --params '{"userId": "me"}'

# Delete a filter
gws gmail users settings filters delete --params '{"userId": "me", "id": "FILTER_ID"}'
```

Full filter schema: https://developers.google.com/gmail/api/reference/rest/v1/users.settings.filters

## Output format

Every `gws` command prints structured JSON on stdout (helpers that default to tables accept `--format json`). Pipe to `jq` to extract fields:

```bash
gws gmail users messages list --params '{"userId":"me","q":"is:unread"}' | jq -r '.messages[].id'
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | API error (Google returned 4xx/5xx) |
| 2 | Auth error (credentials missing/expired/invalid) |
| 3 | Validation error (bad arguments, unknown service, invalid flag) |
| 4 | Discovery error (could not fetch the API schema) |
| 5 | Internal error |

## Rate limits

| Account type | Daily send limit | Note |
|--------------|-----------------|------|
| Consumer Gmail (`@gmail.com`) | 100 recipients/day | Messages with many recipients count per-recipient |
| Google Workspace | 2,000 recipients/day | Business/Enterprise tiers |

Gmail API also applies per-user quota units per second. For bulk `users messages modify` loops, add a small `sleep` between calls or process in batches.

## Common error patterns

| Error message | Likely cause | Fix |
|---------------|-------------|-----|
| `unknown subcommand: send` | Missing `+` on a helper | Use `gws gmail +send` |
| `Access blocked` (403) during login | Account not in Test users list or too many scopes | Add email to Test users; use `--scopes gmail` |
| `accessNotConfigured` | Gmail API not enabled on GCP project | Open the `enable_url` from the error and click Enable |
| `redirect_uri_mismatch` | OAuth client is not a Desktop app | Recreate the OAuth client with type Desktop app |
| `Label not found` when modifying a message | Passed label name instead of `id` | Use the `id` returned by `users labels create` or `users labels list` |
