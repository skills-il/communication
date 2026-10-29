# Israeli payment providers for a Telegram business bot

Reference list for Phase 7 Option 1 (external payment links). None of these needs a
Telegram-specific integration: the bot sends a link or opens the provider's page inside a Mini App.

Pick on two axes: does it also issue the compliant invoice, and does it have an API a bot can drive.

**The two capability columns are a practitioner summary, not a sourced guarantee.** Provider feature sets and pricing change without notice. Evidenced (checked 2026-10-29): Morning's and Grow's automatic documents, Cardcom's hosted-page and document API, Bit's bank-set limits and invoice duty, PayBox's owner. Everything else in the table, including every "Bot-drivable API?" cell, is practitioner summary. Confirm invoicing and API availability with the provider before you build against it.

| Provider | Issues the invoice? | Bot-drivable API? | Notes |
|---|---|---|---|
| Morning (מורנינג, formerly Green Invoice / חשבונית ירוקה) | Yes | Yes | Clearing with an automatic invoice on every transaction. Best default when the owner has no accounting system |
| iCount | Yes | Yes | Invoicing with payment links |
| Rivhit (רווחית) | Yes | Yes | Payment collection with accounting integration |
| PayMe | No | Yes | Simple payment pages. Also powers Bit acceptance on platforms such as Wix |
| Grow (formerly Meshulam / משולם) | Yes | Yes | Clearing aimed at small businesses; issues the document to the customer automatically after payment, and has an API |
| Cardcom (קארדקום) | Yes | Yes | Hosted payment page (LowProfile) API with an attached document, and a separate document-creation endpoint |
| Tranzila (טרנזילה) | No | Yes | Veteran Israeli processor. ILS, with hosted-iframe and API integration routes. Confirm the current API version and the available integration routes against Tranzila's own docs before coding |
| Bit (ביט) | No | Merchant portal only | Widely used Israeli payment app, with a merchant developer portal at `developer.bitpay.co.il` |
| PayBox (פייבוקס) | No | None found | Digital wallet acquired by Israel Discount Bank in 2017 |

## Bit: what the terms actually say

Bit's own terms say business acceptance is subject to the limits and conditions
agreed between the bank and the business, so get the actual per-transaction and monthly ceilings
from the provider rather than assuming a published number. Bit also states that the payee is
required to issue a lawful tax invoice.

## PayBox: treat as a manual step

Businesses can receive payments online and in store using QR codes or payment links, but we found
no public merchant API a bot can drive. The bot can send the link; a human reconciles.

## Why the invoice column matters

Collecting money through the bot does not change the business's tax obligations. If the owner uses
a bare payment link from a provider that does not invoice, they must still issue the document
separately. That is why the providers that produce the payment link and the compliant invoice in one step
lead the list: the bot never becomes a channel that takes money without paperwork.

A deposit is a payment too, and needs its receipt when it is received.

The חשבוניות ישראל allocation number is narrower than it sounds. What triggers it is the RECIPIENT
being a registered dealer who will deduct input VAT on a tax invoice above the current threshold,
not the document type or the business type. A cafe or salon selling to private consumers will
rarely meet it; the same cafe invoicing a company for a catering order above the threshold does.
The threshold falls year on year, so read the current figure off the Tax Authority page rather
than quoting one from memory.

## Telegram's own provider list

Telegram publishes no public provider list. The payments page says only that bots can "Accept
payments from over 200 countries using more than 20 providers", and the actual set is whatever
@BotFather offers your bot under Bot Settings > Payments. As of 2026-10-29 no Israeli solek is
named anywhere in the payments documentation, and Stripe remains the documented reference provider
(the TEST MODE / LIVE MODE tokens). Check the live menu in @BotFather before committing, since
Telegram adds providers over time.
