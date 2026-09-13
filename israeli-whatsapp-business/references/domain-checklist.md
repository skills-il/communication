# Domain checklist: WhatsApp Business Platform for Israeli SMBs and e-commerce

Scope: an Israeli business sending transactional (order, shipping, appointment) and marketing (holiday promotion) messages through the Cloud API, directly or via a BSP. Every source below was fetched with curl on 2026-09-13. Israeli statutory items are marked **[source not re-fetched]** where the checklist author could not fetch them. The Kol-Zchut spam-law page and the Privacy Protection Authority page were both read in a browser on 2026-09-13 during the update.

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

## Must cover (core)

1. **App vs Platform decision, with Coexistence.** A number already on the WhatsApp Business app can enter the Coexistence flow in Embedded Signup. Do not assert that onboarding always loses chat history. [CHANGELOG]
2. **Embedded Signup version.** v2 is deprecated on 8 October 2026, so integrate with v4. [CHANGELOG]
3. **Number migration limits.** Phone-number migration is not supported for accounts on the new WhatsApp account model. [CHANGELOG]
4. **Graph API version.** Use the current version (v26.0 as of 2026-09-13) and never hardcode it without a check. [SEND]
5. **Recipient identity: phone AND BSUID.**
   - Store `user_id` (BSUID) from every messages and status webhook.
   - Do not key the CRM on phone alone: a phone may be absent when the user has a username.
   - BSUIDs are scoped to a business portfolio and regenerate on a phone change.
   - Send with `recipient` for a BSUID. When both are sent, the phone takes precedence. `wa_id` may be omitted from send responses. [BSUID]
6. **Phone format.** Use E.164 without a leading zero after 972. Also support non-Israeli customers for transactional sends. [SEND]
7. **2026 pricing model.**
   - Per-message pricing for marketing, utility and authentication templates. [PRICE]
   - From 1 Oct 2026, service messages are charged, with 1,000 free per business phone number per month and no rollover. [PRICE26]
   - From 1 Oct 2026, utility templates inside the CSW are charged. [PRICE26]
   - Without a payment method, delivery stops after 1,000 service messages a month. [PRICE26]
   - The 72h free entry point window from click-to-WhatsApp ads remains. [PRICE]
   - Pricing changes only on the 1st of a quarter. [PRICE]
8. **Template authoring.**
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
    - It applies to Israel; the exclusions are the EEA, UK, Japan and South Korea.
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
    - Read `errors` and the `pricing` object; the pricing `type` values change on 1 Oct 2026.
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
    - blocked user

    Source: [ERR]
18. **Israeli commercial-message law, section 30A of the Communications Law.** **[source not re-fetched]** Cover:
    - the consent basis, or the existing-customer route;
    - the mandatory advertisement label, advertiser identity and contact details, and the refusal method;
    - the statutory compensation exposure.

    Treat WhatsApp as covered. Cross-check with the Nevo or Knesset statute text and kolzchut before publishing.
19. **Privacy Protection Law Amendment 13.** **[source not re-fetched]** Cover:
    - the customer phone list as a database;
    - provenance and opt-in records;
    - transfer abroad (BSP and CRM processors).

    Verify on the Privacy Protection Authority site manually.

## Should cover (advanced)

1. **Marketing Messages API** . Delivery optimization, time-to-live, measurement, and BSUID `recipient` support. [MMAPI] [CHANGELOG]
2. **Max price for marketing.**
   - `optimization_spec` replaced `bid_spec` after 31 July 2026.
   - A template can switch between rate card pricing and max price.
   - `per_message_bid_multiplier` exists.
   - The feature is Limited Beta. [CHANGELOG]
3. **Contact book and REQUEST_CONTACT_INFO interactive message.** Use these to recover a phone for username users, and handle `from_user_id` in contacts webhooks. [BSUID] [CHANGELOG]
4. **Business username.** Reserve and adopt one from 29 June 2026. It does not hide the business phone number. [BSUID]
5. **Parent BSUIDs.** For managed businesses with multiple portfolios. [BSUID]
6. **`messaging_account_id`.** Send it when the token reaches more than one Messaging account on a number; it affects billing attribution. [CHANGELOG]
7. **Groups API.** Available to Official Business Accounts, with a separate group service pricing type. [CHANGELOG] [PRICE]
8. **Meta Business Agent per-token pricing.** From 1 Aug 2026, and the AI Providers pricing policy. [PRICE26] [CHANGELOG]
9. **Authentication templates.**
   - iOS keyboard autofill is on by default from 15 June 2026.
   - BSUIDs are not usable for one-tap, zero-tap or copy-code templates. [CHANGELOG] [BSUID]
10. **Calling API extras.** Call recording, transcription, voicemail (alpha) and BSUID fields in calling webhooks. [CHANGELOG]
11. **Webhook mutual TLS.** [WHOV]
12. **BSP selection.** Covers WABA ownership, local invoicing and template tooling. This is a business judgement: Meta docs only confirm the ownership and Coexistence mechanics. [CHANGELOG]

## Out of scope (explicit)

- Personal WhatsApp and unofficial automation (web-client bots, unofficial libraries). These are not the Business Platform.
- WhatsApp Pay and in-chat payments (not offered in Israel). Checkout redirects to the store's own Israeli payment provider.
- On-Premises API (end of support).
- General-purpose AI chatbot products on WhatsApp.
- Drafting a binding legal opinion on whether section 30A reaches WhatsApp. Flag it and recommend counsel.
- Buying or renting phone lists.
- Non-Israeli spam regimes (TCPA, GDPR ePrivacy), beyond noting that US marketing templates are not delivered.
- Jewish holiday and Shabbat time computation as an authoritative source. Use a calendar library, and note that no official source was fetched for this checklist.

## Authoritative sources

Fetched and confirmed on 2026-09-13:
- [PRICE], [PRICE26], [BSUID], [CHANGELOG], [SEND], [TMSG], [TOV], [TLANG], [TCAT], [TPAUSE], [LIMITS], [PERUSER], [WHOV], [WHEP], [WHSTATUS], [WHPREF], [ERR], [MMAPI] (full URLs in the source key list at the top)
- Graph API changelog (versions): https://developers.facebook.com/docs/graph-api/changelog

Israeli law. These must be checked manually, because automated fetch failed on 2026-09-13:
- Kolzchut, compensation for advertisements sent without consent (spam law): https://www.kolzchut.org.il/he/%D7%A4%D7%99%D7%A6%D7%95%D7%99_%D7%91%D7%92%D7%99%D7%9F_%D7%9E%D7%A9%D7%9C%D7%95%D7%97_%D7%93%D7%91%D7%A8%D7%99_%D7%A4%D7%A8%D7%A1%D7%95%D7%9E%D7%AA_%D7%9C%D7%9C%D7%90_%D7%94%D7%A1%D7%9B%D7%9E%D7%94_%D7%A9%D7%9C_%D7%94%D7%A0%D7%9E%D7%A2%D7%9F_(%D7%97%D7%95%D7%A7_%D7%94%D7%A1%D7%A4%D7%90%D7%9D) (verified in a browser on 2026-09-13; the older `?curid=14302` link returns 404)
- Privacy Protection Authority: https://www.gov.il/he/departments/the_privacy_protection_authority (Cloudflare challenge)


Note: items tagged [CHANGELOG], [SEND], [TMSG], [TOV], [TLANG], [WHEP], [WHSTATUS] or [MMAPI] point at Meta pages that were not re-read in a browser during the 2026-09-13 update. Re-verify those items before relying on them.
