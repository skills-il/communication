# WhatsApp Business Platform: 2026 changes an Israeli integration must handle

Checked against Meta developer docs on 4 November 2026. Every item below links to its source. Re-check the linked page before quoting a date or a price to a customer.

## 1. Pricing since 1 October 2026: service messages are no longer free

Meta now has five message categories: marketing, utility and authentication (template messages), and service and Meta Business Agent (non-template messages, which can only be sent inside an open 24-hour customer service window). Meta Business Agent was introduced on 1 July 2026 for non-template replies powered by Meta's own Business Agent platform; a reply written by people or by a third-party AI is a service message.

| Message | Before 1 October 2026 | Since 1 October 2026 |
|---|---|---|
| Service (non-template) replies inside the 24h customer service window | Free since 1 November 2024 | Charged per message. Every business phone number gets 1,000 free service messages a month, charged from the 1,001st. Unused free messages do not roll over, and the tier resets monthly by the Messaging account's time zone. |
| Utility template sent in response to a user inside the window | Free since 1 July 2025 | Charged per message. In status webhooks the pricing type for these changed from `free_customer_service` to `regular`. |
| Any message inside a free entry point window (opened when you reply, inside the customer service window, to a user who wrote from a Click-to-WhatsApp ad on the Android or iOS app; open for up to 7 days from that reply) | Free | Still free for marketing, utility, authentication and service. Meta Business Agent messages are charged even here. |
| Marketing, authentication, utility outside the window | Charged per template message | Charged per template message |
| Meta Business Agent replies | Not offered before July 2026 | One per-token charge since 1 August 2026 covering AI processing and delivery |

What to change in an Israeli integration:

- A support or "where is my order" chat is a cost centre above 1,000 replies a month per number. Budget for it, and never describe in-window replies as free in a proposal.
- **Check the payment method.** A Messaging account with no payment method gets its service messages delivered within the free tier and not after it, so replies can stop reaching customers from the 1,001st of the month with nothing visible in your own logs. Error `131042` is the payment-method error. Under the new account model (section 8) each Messaging account has its own payment method.
- The free-tier count is per business phone number, so a portfolio with several numbers gets 1,000 per number.
- **Government bodies and community non-profits.** From 1 October 2026 to 31 December 2027, service messages stay free beyond the monthly free tier for organizations Meta has identified as eligible (government departments and agencies, and community non-profits such as public health, crisis response, disaster relief and non-partisan civic engagement). Do not assume an Israeli עמותה qualifies: Meta reports eligibility through a `subtype` webhook field (from 12 October 2026) and the `service_pricing_policy` field (from 23 October 2026).
- The free tier and the October changes do not apply to "AI Providers", which have their own pricing policy, effective 16 February 2026.
- **General-purpose AI assistants.** Under WhatsApp's Terms of Service, since 15 January 2026 "AI Providers" may offer general-purpose AI assistants on the Platform only where Meta is legally required to permit it. A bot scoped to your own business (support, bookings, order status) is a different use case.

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

More BSUID mechanics worth knowing:

- **Recovering a phone number.** A `REQUEST_CONTACT_INFO` button can be added to utility and marketing templates or sent as an interactive message; the user's shared contact arrives in a contacts webhook carrying `from_user_id`.
- **Identity changes.** When a user changes number, a `system` message of type `user_changed_number` arrives (it also regenerates the BSUID); when only the BSUID changes and no phone can be shared, the type is `user_changed_user_id`. Both carry `previous_user_id`, which is how you join the new identity to the record you already have (section 11).
- **Parent BSUIDs** let a managed business with several portfolios use one identifier across them; ask Meta to enroll.
- **Business usernames** can be reserved from 29 June 2026. Adopting one does not hide the business phone number.

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
- If you reconcile your bill from status webhooks, note that since 1 October 2026 a utility message sent inside the window reports pricing type `regular` (it used to be `free_customer_service`), and service messages change type once the monthly free tier is used up. Re-read the pricing page for the current values before relying on them.
- Verify `X-Hub-Signature-256` against your app secret on the raw request body before trusting the payload.

Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview

## 5. Template pausing and utility recategorization

- A template whose quality drops is paused automatically: 3 hours the first time, 6 hours the second, and disabled the third. A paused template cannot be sent, so automation that depends on it must stop and fall back.
- Misclassifying marketing as utility triggers an escalating ladder: a **warning** (after which utility-to-marketing changes become instant), **rate limiting** (utility volume capped per rolling 24 hours, excess rejected, for at least 7 days), a **utility restriction** (approved utility templates recategorized to `MARKETING` and new ones blocked, 7 days, or 30 for repeat violations), and a **business portfolio level restriction** across every Messaging account (30 days). The practical result is rejected or marketing-priced order updates and, from 2027, the Marketing Messages API endpoint (section 9) for them.
- Templates paused during Template Pacing do not unpause on their own; unpause them with `POST /{template_id}/unpause` or in WhatsApp Manager.

Sources: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-pausing and https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization

## 6. Additional error codes

| Code | Meaning | What to do |
|---|---|---|
| 131050 | The user stopped marketing messages from your business | Suppress permanently. Do not retry |
| 131048 | Sending restricted because too many previous messages were blocked or flagged as spam | Stop campaigns and check quality in WhatsApp Manager |
| 131056 | Too many messages from your number to the same recipient in a short period | Wait and retry, and batch order-status bursts |
| 131042 | Payment method error | Fix billing on the Messaging account |
| 131063 | The template is MARKETING but marketing templates are disabled on Cloud API for this account | Send it through the Marketing Messages API (section 9) |
| 130472 | Not sent as part of a Meta marketing message experiment | A resend gets the same error, so do not retry (source: support/experiments) |
| 130403 | Your business has blocked the user | Unblock the user first; do not retry |
| 132015 | The template is paused for low quality | Edit it and resend after re-approval |
| 132016 | The template was paused too many times and is permanently disabled | Create a new template |

Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes

## 7. Onboarding a number that is already on the WhatsApp Business app

Embedded Signup can onboard a number that is still in use on the WhatsApp Business app. The business keeps using the app for one-to-one chats, WhatsApp keeps message history in sync between the app and the Platform, and the business is offered the option to share its chat history. Do not tell a small Israeli business that moving to the Platform necessarily wipes its chats. Confirm with the BSP that its signup flow supports this.

Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users

## 8. The new account model: WhatsApp account plus Messaging account

From 23 September 2026, reaching all businesses by mid-October 2026, Meta split the WhatsApp Business account (WABA) in two:

- **WhatsApp account (WAAC):** holds a single business phone number (and later a business username), the business profile and the catalog. It is always owned by the client or direct developer, and it can be shared with several partners.
- **Messaging account:** holds templates, billing and payment methods, and webhook subscriptions. Each partner working with a client gets its own Messaging account. Existing WABA IDs now denote Messaging account IDs.

What stays the same: Cloud API endpoints and payloads, phone number IDs, access tokens, template workflows, business verification, and messaging limits at the business portfolio level. When several partners share one number they share its throughput and the portfolio's messaging limit.

What changes for an Israeli business:

- **Moving a number from one Solution Partner to another is not supported in the new model.** The client shares its WhatsApp account with the new partner instead. The number does not move and conversations are uninterrupted. Do not plan a "BSP migration" project; plan a share.
- **Templates do not follow you to a new partner.** They belong to the Messaging account they were created in. Recreate them, or copy them with the Template Migration API, and expect migrated templates' quality rating and messaging tier to reset to baseline, with a ramp-up of roughly 2 to 4 weeks. Avoid switching partners right before a holiday campaign.
- **`messaging_account_id`.** Send it on Messages API calls whenever your access token has messaging access to more than one Messaging account on the same number, because Meta otherwise cannot tell which account to bill. It is optional during rollout, and `paid_messaging_account_id` remains as a deprecated alias; Meta asks integrators to migrate to `messaging_account_id` by 31 December 2026. Meta plans a new Graph API version in the first half of 2027 that requires it for multi-Messaging-account setups, and a mandatory transition in the first half of 2028 in which APIs that take a phone number ID must use the WAAC ID instead.
- Meta Business Suite shows separate **WhatsApp Accounts** and **Messaging Accounts** tabs once a business is migrated. Until then WhatsApp Manager still shows the old WABA view, so the docs can be ahead of what the client sees.

Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/account-model-evolution/

## 9. Marketing Messages API: Cloud API stops carrying marketing in 2027

- Cloud API will stop supporting marketing messages on **13 October 2027**. After that date a marketing send to `/messages` produces an error. Service, authentication and utility messages stay on Cloud API.
- A Messaging account created on or after **13 April 2027** cannot send marketing messages through Cloud API at all.
- Marketing goes to `POST /<PHONE_NUMBER_ID>/marketing_messages` (the Marketing Messages API for WhatsApp), which has a similar technical schema and the same billing model as Cloud API. To start, accept its Terms of Service in the App Dashboard (WhatsApp > Quickstart). Meta says most integrations take about two weeks, so do not leave it to the month before a deadline.
- Features only it offers include message time-to-live expiry dates, useful for a holiday sale that must not arrive late.
- **Route by the template's latest category, not the category you submitted.** Meta can change a UTILITY template to MARKETING after approval. Keep a map of Messaging account, template name, language and latest category; update it from the `template_category_update` webhook only after the completed notification. Send MARKETING to `/marketing_messages` and everything else to `/messages`.
- Once fully onboarded, setting `disable_marketing_messages_on_cloud_api` to `true` makes `/messages` reject marketing templates with error `131063`. Refresh the category and retry through `/marketing_messages`.
- **Max price.** On the Marketing Messages API you can set a maximum price per marketing message delivery, and Meta charges that price or lower. It entered open beta on 1 October 2026. Meta's stated plan is general availability in Q2 2027, when max price becomes required in eligible geographies and fixed published marketing rates apply only on Cloud API.
- **Israel's position.** Meta lists the places where Marketing Messages API delivery optimizations are switched off, and where per-user marketing limits are also not active: the European Economic Area, the United Kingdom, Japan, South Korea, Nigeria, South Africa and Thailand. Israel is not on that list, so per-user marketing limits apply to Israeli recipients.

Sources: https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/overview, https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/route-template-messages, https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/get-started and https://developers.facebook.com/documentation/business-messaging/whatsapp/marketing-messages/pricing

## 10. Onboarding and registration changes

- **Embedded Signup v2 and v3, and their public preview versions, were deprecated on 15 October 2026.** Requests for them, or with no or an invalid version, are served as v4. The latest Embedded Signup version is v5. If a BSP or agency flow still passes `v2` or `v3`, check that what it gets on v4 is what it expects.
- **The 6-digit two-step verification PIN is being deprecated for eligible Cloud API numbers**, rolling out with the account model. If the Two-step verification tab is missing in WhatsApp Manager, there is no PIN to create or reset. Keep sending a valid 6-digit `pin` on `POST /<BUSINESS_PHONE_NUMBER_ID>/register` until Meta announces an API change.

Sources: https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/versions and https://developers.facebook.com/documentation/business-messaging/whatsapp/account-model-evolution/

## 11. A webhook handler for an Israeli CRM

Deduplicate on the message ID (Meta retries for up to 7 days), handle statuses and in-WhatsApp opt-outs, keep both identifiers, and merge records when a user's BSUID changes. Verify `X-Hub-Signature-256` (`sha256=` followed by the HMAC-SHA256 of the raw body, keyed with your app secret) before calling this.

```python
SEEN_IDS: set = set()  # use a persistent store in production

def webhook_handler(event: dict) -> dict:
    """Handle a WhatsApp webhook: messages, delivery statuses and opt-outs."""
    for entry in event.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            if change.get("field") == "user_preferences":
                # User stopped or resumed marketing inside WhatsApp:
                # write it to the same suppression list as 'הסר' replies.
                # record_marketing_preference(value)
                continue
            if change.get("field") != "messages":
                continue
            for status in value.get("statuses", []):
                # sent / delivered / read / failed for an order update.
                # status.get("errors") carries codes such as 131049 / 131050;
                # on "failed" the contacts block is omitted.
                # update_delivery_status(status["id"], status["status"])
                pass
            contact = (value.get("contacts") or [{}])[0]
            for msg in value.get("messages", []):
                if msg["id"] in SEEN_IDS:
                    continue
                SEEN_IDS.add(msg["id"])
                if msg.get("type") == "system":
                    sysmsg = msg.get("system", {})
                    if sysmsg.get("type") in ("user_changed_number", "user_changed_user_id"):
                        # Join the new identity to the record already on file.
                        # merge_customer(old_bsuid=sysmsg.get("previous_user_id"),
                        #                new_bsuid=sysmsg.get("user_id"),
                        #                new_phone=sysmsg.get("wa_id"))  # wa_id may be absent
                        pass
                    continue
                crm_data = {
                    # Phone can be missing for users with a username
                    "phone": msg.get("from") or contact.get("wa_id"),
                    "bsuid": msg.get("from_user_id") or contact.get("user_id"),
                    "message": msg.get("text", {}).get("body", ""),
                    "timestamp": msg["timestamp"],
                    "type": msg["type"],
                    "wa_message_id": msg["id"],
                }
                # update_crm(crm_data)
    return {"status": "ok"}
```

Sources: https://developers.facebook.com/documentation/business-messaging/whatsapp/business-scoped-user-ids and https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/create-webhook-endpoint
