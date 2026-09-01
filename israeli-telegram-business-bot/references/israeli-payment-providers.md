# Israeli payment providers for a Telegram business bot

Reference list for Phase 7 Option 1 (external payment links). None of these needs a
Telegram-specific integration: the bot sends a link or opens the provider's page inside a Mini App.

Pick on two axes: does it also issue the compliant invoice, and does it have an API a bot can drive.

**The two capability columns are a practitioner summary, not a sourced guarantee.** Provider feature sets and pricing change without notice, and only the Bit and PayBox rows are backed by an evidence entry. Confirm invoicing and API availability with the provider before you build against it. Cardcom is a mainstream Israeli solek that belongs in this comparison and is not yet listed here.

| Provider | Issues the invoice? | Bot-drivable API? | Notes |
|---|---|---|---|
| Green Invoice (חשבונית ירוקה) | Yes | Yes | Payment links with an automatic invoice. Best default when the owner has no accounting system |
| iCount | Yes | Yes | Invoicing with payment links |
| Rivhit (רווחית) | Yes | Yes | Payment collection with accounting integration |
| PayMe | No | Yes | Simple payment pages. Also powers Bit acceptance on platforms such as Wix |
| Meshulam | No | Yes | Payment clearing aimed at small businesses |
| Tranzila (טרנזילה) | No | Yes | Veteran Israeli processor. ILS, with hosted-iframe and API integration routes. Confirm the current API version and the available integration routes against Tranzila's own docs before coding |
| Bit (ביט) | No | Merchant portal only | Widely used Israeli P2P payment app operated by Bank Hapoalim, with a merchant developer portal at `developer.bitpay.co.il` |
| PayBox (פייבוקס) | No | No | Digital wallet acquired by Israel Discount Bank in 2017 |

## Bit: what the terms actually say

Bit is ILS-only and single-payment only, so it suits low-ticket sales (food, beauty) and not
recurring billing. Bit's own terms say business acceptance is subject to the limits and conditions
agreed between the bank and the business, so get the actual per-transaction and monthly ceilings
from the provider rather than assuming a published number. Bit also states that the payee is
required to issue a lawful tax invoice.

## PayBox: treat as a manual step

Businesses can receive payments online and in store using QR codes or payment links, but there is
no public merchant API a bot can drive. The bot can send the link; a human reconciles.

## Why the invoice column matters

Collecting money through the bot does not change the business's tax obligations. If the owner uses
a bare payment link from a provider that does not invoice, they must still issue the document
separately. That is why Green Invoice, iCount and Rivhit lead the list: they produce the payment
link and the compliant invoice in one step, so the bot never becomes a channel that takes money
without paperwork.

## Telegram's own provider list

Telegram publishes no public provider list. The payments page says only that bots can "Accept
payments from over 200 countries using more than 20 providers", and the actual set is whatever
@BotFather offers your bot under Bot Settings > Payments. As of 2026-09-01 no Israeli solek is
named anywhere in the payments documentation, and Stripe remains the documented reference provider
(the TEST MODE / LIVE MODE tokens). Check the live menu in @BotFather before committing, since
Telegram adds providers over time.
