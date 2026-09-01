# Domain coverage checklist: israeli-telegram-business-bot

Scope: walk an Israeli small-business owner from zero to a working Telegram bot that books
appointments, takes orders, answers FAQs and sends compliant broadcasts. The skill spans four
independently-drifting surfaces (Telegram Bot API, Israeli spam law, Israeli privacy law, Israeli
tax/invoicing) plus a volatile payment-provider market, so check all five every cycle.

Last reviewed: 2026-09-01 (v1.4.0).

## Must cover (core)

| # | Item | Why it is core |
|---|------|----------------|
| 1 | Current Bot API version and release date, plus whether anything the skill relies on changed | The version banner at the top of `core.telegram.org/bots/api`. Drifted this cycle (10.2 to 10.3) |
| 2 | Every BotFather command the skill names, confirmed still present and still called the same | The business toggle is the live example: `Secretary Mode` on `/bots/features`, still `Business Mode` on `/bots` |
| 3 | The rule that a bot cannot start a conversation, and its consequence that every broadcast audience is built one Start press at a time | `core.telegram.org/bots`. It is the single fact that decides Telegram vs WhatsApp |
| 4 | Rate limits: per chat, per group, free broadcast, paid broadcast rate, per-message Stars cost, and both paid-broadcast eligibility thresholds | `core.telegram.org/bots/faq`. All six verified 2026-09-01 |
| 5 | Payments: ILS min and max per invoice from `currencies.json`, and the fact that Telegram publishes NO public provider list | The prior wording claimed Israeli soleks were absent from an "official list" that does not exist |
| 6 | Telegram Stars scope: digital goods only, currency tag XTR, mandatory `/paysupport`, `provider_token` for physical goods only | `core.telegram.org/bots/payments-stars`. The `/paysupport` duty is an obligation, not a nicety |
| 7 | Deep links: the 64-character payload cap, the allowed charset, and the `/start bizChat<user_chat_id>` manage link for connected bots | `core.telegram.org/bots/features#deep-linking`. A bot that parses only its own payloads ignores the manage entry point |
| 8 | Section 30a: the four mandatory elements (prior explicit consent, the פרסומת label, sender name/address/contact, a working opt-out in the same medium at the recipient's election), the NIS 1,000 statutory damages, and the honest scope hedge that instant messaging is not named in the statute | The compliant template lives in `references/business-bot-templates.md`. A promotion template that omits any element is a breach on its face |
| 9 | Privacy: that the bot's customer list is a מאגר מידע, that Amendment 13 reshaped the regime, and that a US no-code host transfers Israeli customer data abroad | Do not quote thresholds or privacy-officer triggers from memory; route to the Authority |
| 10 | Invoicing: that collecting money through the bot does not change tax obligations, and that the חשבוניות ישראל allocation number applies to tax invoices issued to BUSINESS customers deducting input VAT | Without the scope qualifier, consumer-facing businesses (the skill's main audience) think they need a number they do not |
| 11 | Israeli calendar: Sunday-Thursday week, Friday short day, Shabbat closed, Israel festival day-counts (NOT diaspora), Chol HaMoed and erev chag as short days, and Yom HaZikaron | Hebcal's `i=on` flag selects the Israel schedule and returns Chol HaMoed and erev entries separately |
| 12 | Troubleshooting causes that are verified, not guessed. In particular 409 Conflict has TWO causes (a webhook is set, or two pollers share one token) and only one is fixed by `deleteWebhook` | A troubleshooting row is a diagnosis the agent quotes verbatim to the user |
| 13 | Reference-file integrity: every pointer in SKILL.md and SKILL_HE.md resolves to a section that exists in the target file, and every reference file appears in Bundled Resources in BOTH languages | This row exists because the 1.4.0 restructuring broke both, and nothing else caught it |

## Should cover (advanced)

| # | Item | Status |
|---|------|--------|
| 14 | Direct marketing (דיוור ישיר) under the Privacy Protection Law ss.17ג-17ו: the deletion right, the duty to state that the message comes from a direct-marketing database, and to name the data source | Not covered. Deferred. It is a regime independent of s.30a, so a bot that satisfies s.30a can still fail it |
| 15 | Data-subject access, correction and deletion routes built INTO the bot (a delete command), and the Data Security Regulations security tier for a customer table of this shape | Not covered. Deferred |
| 16 | Non-Jewish calendars: Friday-as-closed, Ramadan hours, Eid, Christmas and Easter for businesses serving Arab-Israeli and Christian-Israeli customers | Not covered. Deferred. The Sunday-Thursday assumption is currently hardcoded into the booking logic with no escape hatch |
| 17 | Cardcom in the provider table, and a source for each provider row's invoice/API claims | Partially covered. Only Bit and PayBox rows are evidenced |
| 18 | First-instance case law applying s.30a to WhatsApp broadcasts, which bears on the instant-messaging scope hedge | Not covered. Deferred |

## Out of scope (explicit)

| Item | Rationale |
|------|-----------|
| Writing bot code in Node.js or Python | Routed to `telegram-bot-builder` in the description. This skill is the no-code path. Reviewed 2026-09-01 |
| WhatsApp Business automation | Routed to `israeli-whatsapp-business`. Reviewed 2026-09-01 |
| Voice bots and IVR | Routed to `hebrew-voice-bot-builder`. Reviewed 2026-09-01 |
| Helpdesk and support-ticket routing | Routed to `israeli-customer-support-automator`. Reviewed 2026-09-01 |
| Lead-generation marketing chatbots | Routed to `hebrew-chatbot-builder`. Reviewed 2026-09-01 |

## Authoritative sources

- Bot API and changelog: https://core.telegram.org/bots/api
- Bot features (BotFather, deep linking, privacy mode, Secretary Mode): https://core.telegram.org/bots/features
- Bot FAQ (rate limits): https://core.telegram.org/bots/faq
- Payments and ILS limits: https://core.telegram.org/bots/payments and https://core.telegram.org/bots/payments/currencies.json
- Telegram Stars: https://core.telegram.org/bots/payments-stars
- Telegram Business (Premium scope, chat links): https://core.telegram.org/api/business
- Communications Law s.30a: https://www.nevo.co.il/law_html/law01/032_002.htm
- Privacy Protection Authority: https://www.gov.il/he/departments/the_privacy_protection_authority
- Israel Tax Authority (חשבוניות ישראל): https://www.gov.il/he/departments/israel_tax_authority
