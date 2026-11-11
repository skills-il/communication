# Domain checklist: israeli-sms-gateway

Anchor for the Expert Review. Every row names where the skill covers it. Sources are the ones in `evidence.json`.

## Must cover (core)

- Israeli number validation against the Ministry of Communications numbering plan: mobile 05X (10 digits), geographic 0A (9 digits), non-geographic 072 to 079 (10 digits). Step 1, `scripts/validate_phone.py`.
- Palestinian networks sharing +972 (056, 059) and the retired 057 handled explicitly. Step 1, Gotchas.
- Landlines are valid phone numbers but not SMS destinations. Step 1, `send_sms.py` refuses them by default.
- Segment arithmetic: GSM-7 vs UCS-2, single vs multi-part capacity, per-segment billing. Step 2, `send_sms.py --estimate`.
- Per-provider request shape, recipient format and success signal (InforU, SMS4Free, 019 SMS, Twilio). Steps 3 and 4.
- Delivery reports are separate from the send response, per provider. Step 5.
- OTP hardening: per-destination rate limit, attempt cap, TTL, constant-time compare, no logging, idempotent sends. Step 6.
- Communications Law s.30A: definition of an advertisement (commercial purpose, donation or non-political propaganda, call-a-number limb), prior consent, existing-customer route, SMS content minimum, same-channel refusal, statutory damages and the knowingly presumption. Step 7.
- Privacy Protection Law: lawful collection with the section 11 notice; direct mail (דיוור ישיר) contents under s.17ו(א) and the per-recipient sanction under s.23כו(ג) added by Amendment 13. Step 7, Example 3.
- Chok HaSpam sanctions beyond civil damages: criminal fine and the officers' supervision duty with its presumption; all three no-defence cases of the knowingly presumption. Step 7.
- Sender ID: no government registry; numeric sender ownership verification (3.1.2021); identity verification of the sending business under the 2022 anti-phishing reform. Gotchas, Troubleshooting.
- Twilio Israel silent-failure rules (short codes, long-code international traffic, non-real local sender numbers, Golan/Azi sender swap, landline error 21614). Gotchas, Troubleshooting.

## Should cover (advanced)

- Kosher numbers block SMS; voice-OTP fallback. Gotchas.
- Alphanumeric senders cannot receive replies, which interacts with the same-channel refusal right. Step 7.
- Provider rate limits (InforU documented limit). Step 4.
- Provider choice per use case (OTP vs marketing). Step 3.
- Carve-outs to the call-a-number limb (State bodies, rescue bodies) and the one-time consent request to a business: not yet in the skill, logged for the next cycle.
- Shabbat and holiday sending etiquette for B2C. Step 7, Example 3.

## Out of scope (explicit)

- WhatsApp Business messaging: separate skill `israeli-whatsapp-business`. Reviewed 2026-11-11: a user asking about WhatsApp is routed there by the description.
- Per-message prices of Israeli local providers: not published reliably, quoted per account; the skill tells the user to get a written quote and confirm per-message vs per-segment. Reviewed 2026-11-11: still not capturable from a public source.
- A hard-coded table of kosher number ranges: ranges change and the only list found is an unreferenced Wikipedia section. Reviewed 2026-11-11: the skill points to provider voice fallback instead.
- Exhaustive per-provider error-code tables beyond what each provider publishes: the skill surfaces the provider's own message.
