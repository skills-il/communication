# Choosing between direct Cloud API and a BSP

The BSPs listed in SKILL.md Step 1 are not interchangeable. This is business judgement rather than a Meta rule: Meta's documentation confirms only the ownership and onboarding mechanics (`platform-2026.md` section 8).

| Question | Why it matters in Israel |
|---|---|
| Who is billed by Meta? | Some BSPs pass Meta's rate through at cost plus a platform fee; others resell at a markup. Ask for their Israel country rate, not a global average. |
| Do they invoice as an Israeli vendor? | A local invoice with VAT is far easier for an Israeli accountant than a foreign one needing self-assessment. Some BSPs bill from abroad only. |
| Who owns the Messaging account? | The lock-in question, changed by the account model Meta rolled out from 23 September 2026. The WhatsApp account that holds your number is always yours and can be shared with several partners, and moving a number between partners is no longer supported, so you add or switch a BSP by sharing the number rather than migrating it. What stays with the partner is the **Messaging account**: templates, billing and analytics. Leaving a BSP means recreating or migrating templates, and migrated templates restart their quality rating and messaging tier (roughly 2 to 4 weeks to rebuild). Prefer a Messaging account owned by your business. If the BSP extends you credit on a Messaging account you own, that account cannot be shared with another partner. |
| How good is template management? | You will submit and resubmit Hebrew templates constantly, and a weak template UI multiplies that work. |
| Is there Hebrew support on Israeli hours? | A foreign support desk is painful when sending is paused on a Sunday, a working day in Israel. |

Direct Cloud API is cheaper and removes the lock-in question, but you own token rotation, webhook hosting and retry logic yourself.

Vendor pages (each confirms the vendor offers WhatsApp Business Platform access; check Israeli coverage and invoicing yourself):
- 360dialog (BSP): https://www.360dialog.com/whatsapp-business-api
- MessageBird/Bird (BSP): https://bird.com/
- Twilio WhatsApp Business: https://www.twilio.com/en-us/messaging/channels/whatsapp
- Infobip WhatsApp: https://www.infobip.com/whatsapp-business
- Vonage WhatsApp: https://developer.vonage.com/en/messages/concepts/whatsapp
- Gupshup WhatsApp: https://www.gupshup.io/whatsapp
- AiSensy (BSP): https://www.aisensy.com/
- Sinch WhatsApp: https://www.sinch.com/products/messaging/whatsapp/
