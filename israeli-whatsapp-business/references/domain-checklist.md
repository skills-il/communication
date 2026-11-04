# Domain checklist: WhatsApp Business Platform for Israeli SMBs and e-commerce

Scope: an Israeli business sending transactional (order, shipping, appointment) and marketing (holiday promotion) messages through the Cloud API, directly or via a BSP. Meta sources below were re-fetched with curl on 2026-11-04 (Meta answers a desktop-browser User-Agent with HTTP 400, so the fetch used curl's default User-Agent). Israeli statutory items were read on 2026-11-04 against the consolidated statute text on Hebrew Wikisource and the Amendment 13 publication in Reshumot.

Source keys used below:
- [PRICE] https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- [PRICE26] https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/non-template-messages
- [BSUID] https://developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids
- [TCAT] https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization
- [TPAUSE] https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pausing
- [LIMITS] https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits
- [PERUSER] https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits
- [WHOV] https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview
- [WHPREF] https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/user_preferences
- [ERR] https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes
- [AME] https://developers.facebook.com/documentation/business-messaging/whatsapp/account-model-evolution/
- [MMAPI] https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview
- [MMROUTE] https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/route-template-messages
- [MMGS] https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/get-started
- [MMPRICE] https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/pricing
- [ESVER] https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/versions
- [CALLPRICE] https://developers.facebook.com/documentation/business-messaging/whatsapp/calling/pricing
- [AUTHTPL] https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates
- [TPLOV] https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview
- [TRANSFER] Privacy Protection (Transfer of Data to Databases Abroad) Regulations, 2001: https://he.wikisource.org/wiki/%D7%AA%D7%A7%D7%A0%D7%95%D7%AA_%D7%94%D7%92%D7%A0%D7%AA_%D7%94%D7%A4%D7%A8%D7%98%D7%99%D7%95%D7%AA_(%D7%94%D7%A2%D7%91%D7%A8%D7%AA_%D7%9E%D7%99%D7%93%D7%A2_%D7%90%D7%9C_%D7%9E%D7%90%D7%92%D7%A8%D7%99_%D7%9E%D7%99%D7%93%D7%A2_%D7%A9%D7%9E%D7%97%D7%95%D7%A5_%D7%9C%D7%92%D7%91%D7%95%D7%9C%D7%95%D7%AA_%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94)
- [COMMLAW] Communications (Bezeq and Broadcasts) Law, section 30א: https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%AA%D7%A7%D7%A9%D7%95%D7%A8%D7%AA_(%D7%91%D7%96%D7%A7_%D7%95%D7%A9%D7%99%D7%93%D7%95%D7%A8%D7%99%D7%9D)
- [PENAL] Penal Law, section 61: https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%A2%D7%95%D7%A0%D7%A9%D7%99%D7%9F
- [PRIVLAW] Privacy Protection Law: https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%92%D7%A0%D7%AA_%D7%94%D7%A4%D7%A8%D7%98%D7%99%D7%95%D7%AA
- [A13] Privacy Protection Law (Amendment 13), Sefer HaChukim 3287: https://fs.knesset.gov.il/25/law/25_lsr_4810658.pdf

## Must cover (core)

1. **App vs Platform decision, with Coexistence.** A number already on the WhatsApp Business app can enter the Coexistence flow in Embedded Signup. Do not assert that onboarding always loses chat history. [CHANGELOG]
2. **Embedded Signup version.** v2 and v3 (and their public previews) were deprecated on 15 October 2026 and are served as v4; the latest version is v5. [ESVER]
3. **Number migration limits.** Migrating a business phone number from one Solution Partner to another is not supported in the new account model; the client shares its WhatsApp account with the new partner instead. [AME]
4. **Graph API version.** Use the current version (v26.0 as of 2026-11-04) and never hardcode it without a check. [SEND]
5. **Recipient identity: phone AND BSUID.**
   - Store `user_id` (BSUID) from every messages and status webhook.
   - Do not key the CRM on phone alone: a phone may be absent when the user has a username.
   - BSUIDs are scoped to a business portfolio and regenerate on a phone change.
   - Send with `recipient` for a BSUID. When both are sent, the phone takes precedence. `wa_id` may be omitted from send responses. [BSUID]
6. **Phone format.** Use E.164 without a leading zero after 972. Also support non-Israeli customers for transactional sends. [SEND]
7. **2026 pricing model.**
   - Five categories: marketing, utility, authentication (templates), service and Meta Business Agent (non-template). [PRICE]
   - Since 1 Oct 2026, service messages are charged, with 1,000 free per business phone number per month and no rollover. [PRICE] [PRICE26]
   - Since 1 Oct 2026, utility templates inside the CSW are charged. [PRICE26]
   - Without a payment method, service messages are delivered within the free tier and not after it. [PRICE]
   - The free entry point window: opened by replying inside the CSW to a user who wrote from a Click-to-WhatsApp ad on the Android or iOS app, open for up to 7 days from that reply, free for everything except Meta Business Agent messages. [PRICE]
   - Eligible governments and community non-profits keep service messages free beyond the tier through 31 Dec 2027. [PRICE]
   - Pricing changes only on the 1st of a quarter. [PRICE]
8. **Template authoring.** [TPLOV]
   - Hebrew language code `he`. [TLANG]
   - Example values are required for every parameter.
   - Positional vs named `parameter_format`, with named parameters in lowercase and underscores. [TOV]
9. **Template sending with all components.** Body, header and button parameters (for example a dynamic tracking URL for shipping updates). [TMSG]
10. **Category discipline.**
    - Utility vs marketing rules.
    - The utility-abuse restriction recategorizes all utility templates to MARKETING for 7 or 30 days, and can escalate to the whole portfolio. [TCAT]
11. **Template pausing.** Low quality pauses a template for 3h, then 6h, then disables it. Automation must halt and fall back. [TPAUSE]
12. **Messaging limits.**
    - Limits are set per portfolio.
    - Read the current limit from `whatsapp_business_manager_messaging_limit`, not the deprecated `messaging_limit_tier`. [LIMITS]
13. **Per-user marketing cap.**
    - It applies to Israel; the exclusions are the EEA, UK, Japan, South Korea, Nigeria, South Africa and Thailand. [MMGS]
    - WhatsApp does not currently deliver marketing templates to US +1 numbers. [PERUSER]
14. **Marketing opt-out inside WhatsApp.**
    - Consume the `user_preferences` webhook (stop and resume) into the store's own suppression list.
    - Treat error 131050 as a permanent do-not-retry. [WHPREF] [ERR]
15. **Webhook endpoint correctness.**
    - Verify `X-Hub-Signature-256` with HMAC-SHA256 and the app secret. [WHEP]
    - Return 200 fast.
    - Deduplicate by message ID, because Meta retries for up to 7 days and duplicates occur. [WHOV]
16. **Status webhooks for order updates.**
    - Handle sent, delivered, read and failed statuses.
    - Read `errors` and the `pricing` object; utility in the CSW reports `regular` since 1 Oct 2026, no longer `free_customer_service`.
    - Failed statuses omit the contacts block. [WHSTATUS] [PRICE] [BSUID]
17. **Error handling map.** At minimum, map these codes to actions:
    - 131047 (window closed)
    - 131026 (undeliverable)
    - 130429 (throughput)
    - 131049 (per-user cap, wait 24h)
    - 131050 (opted out)
    - 131048 (spam restriction)
    - 131056 (pair rate limit)
    - 131042 (payment method)
    - 130472 (experiment)
    - 131063 (marketing disabled on Cloud API, resend via the Marketing Messages API)
    - 130403 (the business blocked the user)
    - 132015 / 132016 (template paused / permanently disabled)

    Source: [ERR]
18. **Israeli commercial-message law, section 30א of the Communications Law.** [COMMLAW] [PENAL] Cover:
    - prior express written consent, or the 30א(ג) existing-customer route (purchase or negotiation with notice, chance to refuse, similar kind);
    - refusal at any time, by the channel the advert came on, and the deemed refusal when an ongoing relationship ends (30א(ד));
    - mandatory content (30א(ה)): the word פרסומת at the start, advertiser name, address and contact details, the right to refuse with a simple way to do it, and for an electronic message a valid internet address for refusals;
    - exposure: up to NIS 1,000 per advertisement without proof of damage, the presumption of knowledge (30א(י)), criminal fines under Penal Law 61(א)(4) and 61(א)(3), and the officers' supervision duty (30א(ח)).

    WhatsApp is not named; treat it as covered and as an electronic message.
19. **Privacy Protection Law and Amendment 13.** [PRIVLAW] [A13] Cover:
    - Amendment 13 in force since 14 August 2025;
    - the customer phone list as a database, with provenance and opt-in records;
    - direct mail (17ו): a segmented campaign must state it is direct mail, the right to deletion and an address, and the controller's identity, address and sources; written deletion requests confirmed within 30 days;
    - the section 11 notice on the opt-in form;
    - registration of list-broker databases over 10,000 people (8א), and transfer abroad under the 2001 transfer regulations (BSP and CRM processors). [TRANSFER]
20. **Marketing Messages API and the Cloud API marketing sunset.** New Messaging accounts from 13 April 2027 cannot send marketing on Cloud API, and all Cloud API marketing sends error from 13 October 2027. Route by the template's latest category using the `template_category_update` webhook. [MMAPI] [MMROUTE]
21. **Account model.** WhatsApp account (number, profile, catalog) vs Messaging account (templates, billing, webhooks); templates do not follow a partner change and migrated templates' quality and tier reset for roughly 2 to 4 weeks. [AME]

## Should cover (advanced)

1. **Marketing Messages API features.** Delivery optimization, time-to-live, measurement. (The routing and sunset are Must-cover item 20.) [MMAPI]
2. **Max price for marketing.** Expressed as `bid_amount` per 1,000 deliveries in `optimization_spec`. Open beta from 1 October 2026; GA planned for Q2 2027, when it becomes required in eligible geographies. [MMPRICE]
3. **REQUEST_CONTACT_INFO.** A button on utility and marketing templates, or an interactive message, to recover a phone for username users; the shared contact arrives with `from_user_id`. [BSUID]
4. **Business username.** Reserve and adopt one from 29 June 2026. It does not hide the business phone number. [BSUID]
5. **Parent BSUIDs.** For managed businesses with multiple portfolios. [BSUID]
6. **`messaging_account_id`.** Send it when the token reaches more than one Messaging account on a number; it affects billing attribution. Required for multi-Messaging-account setups in the new Graph API version planned for H1 2027, and on all versions from H1 2028. [AME]
7. **Groups API.** Programmatic group creation and management (not re-verified on 2026-11-04; check eligibility and pricing on the Groups page before relying on it). [CHANGELOG]
8. **Meta Business Agent per-token pricing.** From 1 Aug 2026, and the AI Providers pricing policy. [PRICE26] [CHANGELOG]
9. **Authentication templates.**
   - Fixed, non-customizable preset text with an optional security disclaimer and expiry warning, and a one-tap, copy-code or zero-tap button; the code is sent as the body parameter and the URL button parameter. [AUTHTPL]
   - BSUIDs are not usable for one-tap, zero-tap or copy-code templates. [BSUID]
10. **Calling API pricing.** User-initiated calls are free; business-initiated calls are charged in six-second pulses by destination country and volume tier. Recording, transcription and voicemail extras were not re-verified on 2026-11-04. [CALLPRICE]
11. **Webhook mutual TLS.** Webhooks support mTLS. [WHOV]
12. **BSP selection.** Covers Messaging account ownership, local invoicing and template tooling. This is a business judgement: Meta docs only confirm the ownership and Coexistence mechanics. [CHANGELOG]

## Out of scope (explicit)

Each row was re-litigated on 2026-11-04: would an ordinary user ask for it, and has it become capturable?

- Personal WhatsApp and unofficial automation (web-client bots, unofficial libraries). Users do ask, and the skill answers it by routing them away: these are not the Business Platform. Unchanged.
- In-chat payments. Meta's Payments API docs cover India and Brazil only, not Israel. The skill answers the question (redirect to the store's own Israeli payment provider).
- On-Premises API (end of support). Answered in one line in Step 4.5.
- General-purpose AI chatbot products on WhatsApp. Restricted by WhatsApp's terms; Step 4.5 says so.
- A binding legal opinion on whether section 30א, or the direct-mail rules, reach a specific campaign. Users will ask; the skill gives the statutory rules in `israeli-law.md` and routes the judgement to counsel.
- Buying or renting phone lists. The skill says not to, with the 8א registration reason.
- Non-Israeli spam regimes (TCPA, GDPR ePrivacy), beyond noting that US marketing templates are not delivered.
- Jewish holiday and Shabbat time computation as an authoritative source. Users plausibly ask why a chag send went out; the script still knows only Friday and Saturday heuristics. The skill now says so explicitly and points to a Hebcal-style source. Capturing a holiday table in the script remains a deferred item.

## Authoritative sources

Fetched and confirmed on 2026-11-04: every key in the source list at the top. Meta pages were read with curl's default User-Agent; the statute texts on Hebrew Wikisource were read as raw wikitext, and Amendment 13 from the Knesset PDF.

Items tagged [CHANGELOG], [TMSG], [TOV], [TLANG], [WHEP] or [WHSTATUS] point at Meta pages that were not re-read on 2026-11-04. The WhatsApp changelog page served by curl stopped at 12 May 2026 and the rendered page failed to load, so items sourced only to it should be re-verified before relying on them.
