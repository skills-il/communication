# WhatsApp Business Platform: 2026 changes an Israeli integration must handle

Checked against Meta developer docs on 13 September 2026. Every item below links to its source. Re-check the linked page before quoting a date or a price to a customer.

## 1. Pricing from 1 October 2026: service messages are no longer free

| Message | Until 30 September 2026 | From 1 October 2026 |
|---|---|---|
| Non-template (service) replies inside the 24h customer service window | Free since 1 November 2024 | Charged per message. Every business phone number gets 1,000 free service messages a month, charged from the 1,001st. Unused free messages do not roll over. |
| Utility template sent in response to a user inside the window | Free since 1 July 2025 | Charged per message |
| Any message inside the 72h free entry point window opened by a Click-to-WhatsApp ad | Free | Still free |
| Marketing, authentication, utility outside the window | Charged per template message | Charged per template message |

What to change in an Israeli integration:

- A support or "where is my order" chat is now a cost centre above 1,000 replies a month per number. Budget for it, and do not describe in-window replies as free in a proposal.
- Make sure a payment method is attached to the WhatsApp Business account before 1 October. Meta's own pages disagree on what happens without one: the pricing page says the first 1,000 service messages a month are delivered and delivery stops from the 1,001st, while the non-template messages page says service-message delivery stops from 1 October 2026. Either way, replies can silently stop reaching customers. Error `131042` is the payment-method error.
- The free-tier count is per business phone number, so a portfolio with several numbers gets 1,000 per number.

Sources: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing and https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing/non-template-messages

## 2. Business-scoped user IDs (BSUID) and usernames

WhatsApp users can adopt a username. When they do, their phone number may be missing from your webhooks. Meta's page states that supporting BSUIDs is required for all partners and directly-integrated businesses.

- BSUIDs began appearing in webhooks in early April 2026, and sending to a BSUID is supported from July 2026.
- In a messages webhook the BSUID is in `user_id`. If the user has a username, `wa_id` can be missing. A user who has not adopted a username arrives with both the phone number and the BSUID.
- In a status webhook the BSUID is in `contacts[].user_id` and `statuses[].recipient_user_id`. On a `failed` status the `contacts` block is omitted entirely.
- To send to a BSUID, put it in `"recipient"` instead of `"to"`. If both a phone number and a BSUID are sent, the phone number takes precedence.
- A BSUID is scoped to one business portfolio, and it is regenerated if the user changes their phone number.
- A BSUID cannot be used for one-tap, zero-tap or copy-code authentication templates.

Store both identifiers on the CRM record. Do not key an order or a Monday.com item on phone number alone:

```python
def identify_sender(value: dict, msg: dict) -> dict:
    """Return every identifier the webhook actually carried for this sender."""
    contact = (value.get("contacts") or [{}])[0]
    return {
        "phone": msg.get("from") or contact.get("wa_id"),  # may be None for username users
        "bsuid": contact.get("user_id"),
    }
```

Confirm the exact field names against the messages webhook reference before shipping, because Meta has been extending these payloads throughout 2026.

Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids

## 3. In-WhatsApp marketing opt-out

A user can stop marketing messages from your business inside WhatsApp itself, without replying "הסר".

- Subscribe to the `user_preferences` webhook. It fires when a user stops marketing messages and when they resume them.
- A send to such a user fails with error `131050`: the recipient has chosen to stop receiving marketing messages from your business. Do not retry.
- Write both events into the same suppression list that holds "הסר" replies. That list is the refusal record the Israeli section 30A obligations depend on, so an opt-out that arrives through WhatsApp must not be lost.

Sources: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/user_preferences and https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes

## 4. Webhook reliability for order updates

- If your endpoint returns anything other than HTTP 200, Meta retries with decreasing frequency for up to 7 days, and these retries can produce duplicate notifications. Return 200 quickly and deduplicate on the message ID.
- Handle `statuses` as well as `messages`. Delivery failures such as `131049` and `131050` arrive there, not as a synchronous send error. Each status carries `id`, `status`, `timestamp`, `recipient_id` and, since the BSUID rollout, `recipient_user_id`.
- If you reconcile your bill from status webhooks, note that the `type` field in the `pricing` object changes on 1 October 2026 for service messages and for utility messages sent in response to users inside the window. Re-read the pricing page for the new values before relying on them.
- Verify `X-Hub-Signature-256` against your app secret on the raw request body before trusting the payload.

Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview

## 5. Template pausing and utility recategorization

- A template whose quality drops is paused automatically: 3 hours the first time, 6 hours the second, and disabled the third. A paused template cannot be sent, so automation that depends on it must stop and fall back.
- A WABA that sends promotional content under UTILITY can be put under a utility restriction: all its approved utility templates are recategorized to `MARKETING` and new utility templates are blocked, for 7 days (30 days for repeat violations). The practical result is marketing prices and the per-user marketing cap on your order updates.

Sources: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pausing and https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization

## 6. Additional error codes

| Code | Meaning | What to do |
|---|---|---|
| 131050 | The user stopped marketing messages from your business | Suppress permanently. Do not retry |
| 131048 | Sending restricted because too many previous messages were blocked or flagged as spam | Stop campaigns and check quality in WhatsApp Manager |
| 131056 | Too many messages from your number to the same recipient in a short period | Wait and retry, and batch order-status bursts |
| 131042 | Payment method error | Fix billing on the WhatsApp Business account |

Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes

## 7. Onboarding a number that is already on the WhatsApp Business app

Embedded Signup can onboard a number that is still in use on the WhatsApp Business app. The business keeps using the app for one-to-one chats, WhatsApp keeps message history in sync between the app and the Platform, and the business is offered the option to share its chat history. Do not tell a small Israeli business that moving to the Platform necessarily wipes its chats. Confirm with the BSP that its signup flow supports this.

Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users
