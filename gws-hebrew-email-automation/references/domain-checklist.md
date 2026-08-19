# Domain coverage checklist: Gmail automation for Israeli freelancers via the gws CLI

Anchor for the Phase 3b.5 / 5.8 expert review. Bootstrapped 2026-08-19 (v1.5.0 cycle).

## Must cover (core)

| Item | Covered in | Why it is core |
|---|---|---|
| Install, `gws auth setup` / `login` / `status`, own GCP project + OAuth client | Step 1 | Nothing else runs without it. gws README documents the flow and the ~25-scope unverified-app cap. |
| Real `+send` / `+triage` / `+watch` flag surface, no invented flags | Step 2, 4, 8, references/gws-gmail-commands.md | Fabricated flags were the original failure this skill was written to avoid. |
| No scheduled-send flag exists; `--draft` is the deferral route | Step 6, Gotchas | Agents hallucinate `--schedule`. |
| Bilingual Hebrew/English business email structure | Step 2 | The skill's headline capability. |
| RTL rendering in HTML mail and in plain text | Gotchas | caniemail records Gmail's `dir` handling as buggy; plain-text bidi has no markup at all. |
| Shekel formatting, VAT rate, עוסק מורשה vs עוסק פטור branch | Step 2, scripts/shekel-formatter.py | An עוסק פטור may not charge VAT; the script assumes מורשה. |
| The email is transport, not the tax invoice (Invoices Model, מספר הקצאה) | Step 2 | A חשבונית מס above the threshold needs an ITA allocation number from approved software. |
| שוטף + N computed as end-of-invoice-month plus N days | Step 3, Gotchas | Drives the escalation stage; the previous cycle had it arithmetically wrong. |
| Payment-reminder escalation ladder | Step 3 | Headline capability. |
| Rule out ניכוי מס במקור before escalating | Step 3 | A client who paid net of withholding has fully performed. |
| Hebrew labelling via `users messages list` + `modify`, with `--page-all` | Step 4, Example 2 | Without pagination the job silently truncates and reports success. |
| Persistent Gmail filters via `users.settings.filters` | Step 5 | There is no `+filter` helper. |
| Israeli business days, erev Shabbat, chag detection | Step 6 | Sunday-Thursday, and the Hebcal parameter traps are non-obvious. |
| Section 30א consent, required elements, damages, fine tiers, the three 30א(ג) conditions and the absence of any time window | Step 7, references/israeli-email-compliance.md | Direct class-action exposure. |
| Gmail sender requirements: SPF/DKIM baseline for all senders, bulk tier above 5,000/day | Step 7, references/israeli-email-compliance.md | Unauthenticated custom-domain sending is why invoices land in spam. |
| Prompt-injection boundary when the agent both reads inbox and holds send rights | Step 7.5 | Step 8 pipes attacker-controlled text into a send-capable agent. |
| BCC for multi-recipient sends | Gotchas | Most common small-business privacy incident in Israel. |
| Gmail API quota units and daily sending limits | Reference Links, Troubleshooting | Rate-limit failures are the top operational error. |

## Should cover (advanced)

| Item | Status |
|---|---|
| Candle-lighting / havdalah times rather than a flat 14:00 Friday cutoff | Documented in Step 6 as the precise route; the flat rule is retained as the default. |
| `+reply` / `+reply-all` / `+forward` / `+read` helpers, including threading reminders onto the original invoice | Listed in references/gws-gmail-commands.md, not yet wired into the Step 3 workflow. Carried in optimization-log.json. |
| Non-interactive auth (`GOOGLE_WORKSPACE_CLI_TOKEN`, `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`) for headless or sandboxed agent hosts | Not covered. Carried in optimization-log.json. |
| Send-as alias and bilingual signature setup | Not covered. Carried. |
| Drive-link fallback above the 25 MB attachment cap | Not covered. Carried. |
| Gmail API 80,000,000 units/day per-project billing threshold and the May 2026 grandfathering split | Not covered. Carried. |
| Workspace trial-account 500/day cap | Not covered. Carried. |

## Out of scope (explicit)

| Item | Rationale (reviewed 2026-08-19) |
|---|---|
| Issuing the invoice itself, allocation-number retrieval, bookkeeping | This is an EMAIL skill. It warns that the invoice is a regulated instrument produced elsewhere and stops there. Invoicing belongs to the accounting-category skills. |
| Zero-rated VAT on exported services (סעיף 30(א)(5) לחוק מע"מ) | A VAT-treatment determination on the user's own facts. Belongs to a tax skill; putting it here would push this skill across the legal-review line it currently sits safely inside. |
| חוק מוסר תשלומים, statutory late-payment interest, תביעות קטנות, הוצאה לפועל | Debt-enforcement advice. The skill deliberately drafts a business reminder and not a מכתב התראה; adding enforcement content would make it emit a lawyer's work product. |
| Non-Jewish Israeli calendars (Eid al-Fitr, Eid al-Adha, Ramadan hours, Christmas) | Real gap, but Hebcal cannot supply them and no equivalent free API was identified. The correct interim behaviour is to ask the recipient's calendar rather than assume; carried in optimization-log.json rather than silently dropped. |
| Non-Gmail providers, Outlook automation, CRM contact management | Stated anti-triggers in the description. |

## Authoritative sources

- `https://github.com/googleworkspace/cli` README and `skills/gws-gmail-*/SKILL.md` (command surface)
- `https://support.google.com/a/answer/81126`, `/14229414`, `/166852`, `/176600` (sender requirements and limits)
- `https://developers.google.com/workspace/gmail/api/reference/quota` (quota units)
- `https://he.wikisource.org/wiki/חוק_התקשורת_(בזק_ושידורים)` (Section 30א consolidated text)
- `https://www.hebcal.com/home/developer-apis` and the live REST endpoint (calendar)
- Israel Tax Authority VAT interpretation directive 1/2025 (VAT rate)
