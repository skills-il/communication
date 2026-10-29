# Domain coverage checklist: israeli-telegram-business-bot

Scope: walk an Israeli small-business owner from zero to a working Telegram bot that books
appointments, takes orders, answers FAQs and sends compliant broadcasts. The skill spans four
independently-drifting surfaces (Telegram Bot API, Israeli spam law, Israeli privacy law, Israeli
tax/invoicing) plus a volatile payment-provider market, so check all five every cycle.

Last reviewed: 2026-10-29 (v1.5.0).

## Must cover (core)

| # | Item | Why it is core |
|---|------|----------------|
| 1 | Current Bot API version and release date, plus whether anything the skill relies on changed | The version banner at the top of `core.telegram.org/bots/api`. Still 10.3 on 2026-10-29; 10.2/10.3 additions used: disabled inline buttons, Mini App origin lock |
| 2 | Every BotFather command the skill names, confirmed still present and still called the same | The business toggle is the live example: `Secretary Mode` on `/bots/features`, still `Business Mode` on `/bots` |
| 3 | The rule that a bot cannot start a conversation, and its consequence that every broadcast audience is built one Start press at a time | `core.telegram.org/bots`. It is the single fact that decides Telegram vs WhatsApp |
| 4 | Rate limits: per chat, per group, free broadcast, paid broadcast rate, per-message Stars cost, and both paid-broadcast eligibility thresholds | `core.telegram.org/bots/faq`. All six verified 2026-09-01 |
| 5 | Payments: ILS min and max per invoice from `currencies.json`, and the fact that Telegram publishes NO public provider list | The prior wording claimed Israeli soleks were absent from an "official list" that does not exist |
| 6 | Telegram Stars scope: digital goods only, currency tag XTR, mandatory `/paysupport`, `provider_token` for physical goods only | `core.telegram.org/bots/payments-stars`. The `/paysupport` duty is an obligation, not a nicety |
| 7 | Deep links: the 64-character payload cap, the allowed charset, and the `/start bizChat<user_chat_id>` manage link for connected bots | `core.telegram.org/bots/features#deep-linking`. A bot that parses only its own payloads ignores the manage entry point |
| 8 | Section 30a: the four mandatory elements (prior explicit consent, the פרסומת label, sender name/address/contact, a working opt-out in the same medium at the recipient's election), the NIS 1,000 statutory damages, and the honest scope hedge that instant messaging is not named in the statute | The compliant template lives in `references/business-bot-templates.md`. A promotion template that omits any element is a breach on its face |
| 9 | Privacy: the bot's customer list is a מאגר מידע; a typical SMB need not register (s.8א) or appoint a privacy officer (s.17ב1); the s.11 notice at collection; access and correction; basic security; data held abroad (2001 Regulations) | Statute text on he.wikisource.org (post-Amendment 13). A ready Hebrew notice is in `references/compliance-and-security.md` |
| 10 | Invoicing: that collecting money through the bot does not change tax obligations, and that the חשבוניות ישראל allocation number applies to tax invoices issued to BUSINESS customers deducting input VAT | Without the scope qualifier, consumer-facing businesses (the skill's main audience) think they need a number they do not |
| 11 | Israeli calendar: Sunday-Thursday week, Friday short day, Shabbat closed, Israel festival day-counts (NOT diaspora), Chol HaMoed and erev chag as short days, and Yom HaZikaron | Hebcal's `i=on` flag selects the Israel schedule and returns Chol HaMoed and erev entries separately |
| 12 | Troubleshooting causes that are verified, not guessed. One token, one consumer: two pollers make each other fail (commonly logged as 409, a code Telegram does not document), polling fails while a webhook is set, and a second webhook platform silently takes over (n8n's Telegram Trigger registers a webhook). The fix uses each platform's disconnect button, never the token in a browser or a chat | A troubleshooting row is a diagnosis the agent quotes verbatim to the user. 1.5.0 corrected the earlier claim that BotPress, n8n and ManyChat all long-poll |
| 13a | Connected-bot limits: the owner picks which chats the bot may access, and `can_reply` covers only private chats with an incoming message in the last 24 hours, so reminders and broadcasts need a standalone bot | `core.telegram.org/bots/api#businessbotrights`. Missing until 1.5.0, which meant the recommended Option A silently could not send reminders |
| 13b | Token handling: storage, never into a chat (including an AI chat) or a browser address bar, the webhook secret for self-hosting, and the full incident checklist after `/token` | `core.telegram.org/bots/features`, `core.telegram.org/bots/api#setwebhook` |
| 13c | Deposits and the distance-transaction cancellation right (s.14ג, the 5% / NIS 100 cap in s.14ה, the disclosure duties) | Consumer Protection Law. A forfeit-on-any-cancellation deposit is unlawful for a timely cancellation |
| 13d | The weekly closed day is owner-configurable (Friday, Saturday or Sunday), with non-Jewish holidays entered by hand | Added 1.5.0 (was row 16) |
| 13 | Reference-file integrity: every pointer in SKILL.md and SKILL_HE.md resolves to a section that exists in the target file, and every reference file appears in Bundled Resources in BOTH languages | This row exists because the 1.4.0 restructuring broke both, and nothing else caught it |

## Should cover (advanced)

| # | Item | Status |
|---|------|--------|
| 14 | Direct marketing (דיוור ישיר) under ss.17ד-17ו (17ג was repealed): the labelling duty, the deletion right, naming the data source | Covered 1.5.0 in `references/compliance-and-security.md`, with the honest caveat that whether a segmented promotion to own customers is direct mail is not settled |
| 15 | Data-subject access and correction built INTO the bot (/mydata), and the Data Security Regulations tier for a customer table of this shape | Covered 1.5.0. A full deletion workflow is still owner-defined |
| 16 | Non-Jewish calendars: Friday-as-closed, Ramadan hours, Eid, Christmas and Easter | Covered 1.5.0 as an owner setting (row 13d). No authoritative date source is named for Islamic holidays, so the owner enters them |
| 17 | Provider table: invoice and API claims sourced per row | Morning, Grow, Cardcom, Bit and PayBox evidenced 2026-10-29. iCount, Rivhit, PayMe and Tranzila rows still practitioner summary |
| 19 | s.30a(ג) existing-customer route (details given during a purchase, notice, chance to refuse, similar products only) | Covered 1.5.0 |
| 18 | First-instance case law applying s.30a to WhatsApp broadcasts, which bears on the instant-messaging scope hedge | Not covered. Deferred |

## Out of scope (explicit)

| Item | Rationale |
|------|-----------|
| Writing bot code in Node.js or Python | Routed to `telegram-bot-builder` in the description. This skill is the no-code path. Reviewed 2026-10-29 |
| WhatsApp Business automation | Routed to `israeli-whatsapp-business`. Reviewed 2026-10-29 |
| Voice bots and IVR | Routed to `hebrew-voice-bot-builder`. Reviewed 2026-10-29 |
| Helpdesk and support-ticket routing | Routed to `israeli-customer-support-automator`. Reviewed 2026-10-29 |
| Lead-generation marketing chatbots | Routed to `hebrew-chatbot-builder`. Reviewed 2026-10-29 |

## Authoritative sources

- Bot API and changelog: https://core.telegram.org/bots/api
- Bot features (BotFather, deep linking, privacy mode, Secretary Mode): https://core.telegram.org/bots/features
- Bot FAQ (rate limits): https://core.telegram.org/bots/faq
- Payments and ILS limits: https://core.telegram.org/bots/payments and https://core.telegram.org/bots/payments/currencies.json
- Telegram Stars: https://core.telegram.org/bots/payments-stars
- Telegram Business (Premium scope, chat links): https://core.telegram.org/api/business
- Communications Law s.30a: https://www.nevo.co.il/law_html/law01/032_002.htm
- Privacy Protection Authority: `gov.il/he/departments/the_privacy_protection_authority` (Cloudflare-blocks automated fetches; the privacy facts in this skill are evidenced against the statute text instead)
- Privacy Protection Law, Consumer Protection Law, Data Security Regulations (statute text): https://he.wikisource.org
- Business bot rights and webhook secret: https://core.telegram.org/bots/api
- Israel Tax Authority (חשבוניות ישראל): `gov.il/he/departments/israel_tax_authority` (Cloudflare-blocks automated fetches). The allocation-number rule itself is s.38(א1) of the VAT Law, on he.wikisource.org
