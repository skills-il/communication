---
name: israeli-sms-gateway
description: Integrate with Israeli SMS gateway providers for business messaging, OTP, and notifications. Use when user asks about sending SMS in Israel, Israeli SMS providers, phone number validation (Israeli format), Hebrew SMS segment cost, OTP implementation, bulk SMS, sender ID rules, or SMS marketing compliance. Covers 019 SMS, InforUMobile, SMS4Free, and international providers with Israeli support. Do NOT use for WhatsApp Business API (see separate skill) or non-Israeli telecom.
license: MIT
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires API key from chosen SMS provider. Network access required.
---

# Israeli SMS Gateway

## Instructions

### Step 1: Validate Israeli Phone Number

Use `scripts/validate_phone.py`. It encodes the current numbering plan, which a hand-rolled regex almost always gets wrong in the same three ways: it accepts truncated numbers, it accepts Palestinian networks that share the +972 country code, and it accepts a landline length that does not exist.

The allocation this skill enforces:

| Range | Meaning | Local digits |
|-------|---------|--------------|
| 050, 051, 052, 053, 054, 055, 058 | Israeli mobile | 10 |
| 056 (Ooredoo Palestine), 059 (Jawwal) | Palestinian mobile, rejected | 10 |
| 057 | Retired (Hot mobile used it until November 2014), rejected | 10 |
| 02, 03, 04, 08, 09 | Geographic landline | 9 |
| 072 to 079 | Non-geographic landline and VoIP (070 and 071 are outside the numbering plan) | 10 |

Two traps worth naming explicitly:

1. Write the mobile prefixes as an explicit alternation, never as the character range `05[0-8]`. The range happens to produce almost the right set today, but it silently admits 056 and 057, and the moment someone widens it to `05[0-9]` it admits 059 as well. Both 056 and 059 are Palestinian networks.
2. A landline fallback like `0[2-9]` plus a loose length will re-admit every 05 number the mobile branch just rejected, which defeats every mobile guard above it. Anchor the length and keep 05 out of that branch.

A valid phone number is not the same as a valid SMS destination. Landlines (geographic and 072 to 079) validate as phone numbers but generally cannot receive SMS: Twilio rejects them outright with error 21614. `scripts/send_sms.py` therefore refuses a landline recipient unless you pass `--allow-landline`, and `scripts/validate_phone.py --sms-check` exits 2 for one.

```python
import re

MOBILE_RE = re.compile(r'^(?:050|051|052|053|054|055|058)\d{7}$')
LANDLINE_GEO_RE = re.compile(r'^0(?:2|3|4|8|9)\d{7}$')
LANDLINE_NONGEO_RE = re.compile(r'^07[2-9]\d{7}$')


def validate_israeli_phone(phone: str) -> tuple[bool, str]:
    raw = re.sub(r'[\s\-\(\)\.]', '', phone)
    clean = raw
    if clean.startswith('+972'):
        clean = '0' + clean[4:]
    elif clean.startswith('972'):
        clean = '0' + clean[3:]

    # In +972 form the national trunk 0 is dropped.
    if (raw.startswith('+972') or raw.startswith('972')) and clean.startswith('00'):
        return False, 'Extra leading zero: use +972501234567, not +9720501234567'

    if MOBILE_RE.match(clean):
        return True, '+972' + clean[1:]
    if clean[:3] in ('056', '059'):
        return False, 'Palestinian network (056 Ooredoo, 059 Jawwal), not Israeli'
    if LANDLINE_GEO_RE.match(clean) or LANDLINE_NONGEO_RE.match(clean):
        return True, '+972' + clean[1:]
    return False, 'Invalid Israeli phone number'
```

### Step 2: Estimate Segments Before You Estimate Cost

This is the single most expensive thing to get wrong, and it is arithmetic, not opinion. A carrier bills per SEGMENT, not per send.

| Encoding | Single segment | Per segment when split |
|----------|----------------|------------------------|
| GSM-7 (Latin) | 160 | 153 |
| UCS-2 (Hebrew, or any non-GSM-7 character) | 70 | 67 |

A single Hebrew letter anywhere in the body downgrades the whole message to UCS-2 and cuts capacity by more than half. A 140-character Hebrew message is 3 segments, not 1, so a campaign budgeted from character count alone understates real cost by roughly a factor of two or three. Most emoji do the same thing and cost two units each. So do Word-style smart quotes, en dashes and non-breaking spaces pasted into Latin copy: they are outside GSM-7 and silently force the whole message to UCS-2.

Run the estimate before you send:

```bash
python scripts/send_sms.py --estimate \
    --message "שלום, ההזמנה שלך יצאה למשלוח" \
    --price-per-segment 0.09 --recipients 5000
```

`segment_count()` in `scripts/send_sms.py` is importable if you want the same arithmetic inside your own budgeting code.

### Step 3: Choose Provider

| Provider | Best For | API Type | Pricing note |
|----------|----------|----------|--------------|
| 019 SMS (019 Telecom) | Israeli enterprise, banks | REST, XML or JSON, sandbox available | Package-based, quote required |
| InforUMobile | Marketing, bulk campaigns | REST JSON | Package-based, quote required |
| SMS4Free | Startups, dev/test | REST JSON | Package-based, free trial allowance on signup |
| ActiveTrail | Marketing automation | REST | SMS campaigns inside its marketing platform |
| Twilio | Global apps targeting +972 | REST | Published per-segment rate, see below |
| Vonage | Multi-region apps | REST | Volume pricing |
| Bird | Multi-channel | REST | Volume pricing |

Israeli package pricing is quoted per account and is not reliably published, so this skill does not print a per-message figure for the local providers. Ask for a written quote and confirm whether it is priced per message or per SEGMENT, because for Hebrew traffic those differ by two to three times.

OTP and marketing traffic have different provider requirements, so choose per use case rather than once:

- OTP: speed and reach matter most. Check that the provider offers a voice fallback for kosher numbers, keep the template short and purely transactional, and verify the sender ID before launch.
- Marketing: the refusal path matters most. Prefer a sender the recipient can reply to, or a provider with a built-in removal mechanism, plus delivery reports you can reconcile. Compare Twilio's published per-segment rate below against local package quotes before defaulting a recurring Hebrew campaign to it.

Twilio does publish Israel rates: outbound is priced at $0.2575 and inbound at $0.0075, per SEGMENT, not per message. Verify before budgeting, since carrier surcharges move.

Bird is the company formerly called MessageBird; the rename completed before 2025, so treat "MessageBird" in older tutorials as the same vendor.

### Step 4: Send SMS

**InforUMobile (JSON REST, the current v2 contract):**

Authorization is HTTP Basic over `username:API-token`. Note it is the API TOKEN, not the account password, and the header value must be genuinely base64-encoded. The body is envelope-wrapped under a top-level `Data` key. Responses carry `StatusId` and `StatusDescription`.

```python
import base64
import os
import requests


def send_sms_inforu(to: str, message: str, sender: str) -> dict:
    """Send SMS via the InforU v2 JSON endpoint."""
    creds = f'{os.environ.get("INFORU_USER", "")}:{os.environ.get("INFORU_API_TOKEN", "")}'
    token = base64.b64encode(creds.encode("utf-8")).decode("ascii")

    response = requests.post(
        "https://capi.inforu.co.il/api/v2/SMS/SendSms",
        headers={
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json={
            "Data": {
                "Message": message,
                "Recipients": [{"Phone": to}],  # local form, e.g. 0541234567
                "Settings": {"Sender": sender},
            }
        },
        timeout=15,
    )
    return response.json()  # StatusId 1 = accepted
```

InforU's SMS examples only ever show the recipient in local form (`0541234567`), so send that rather than `972...`. The documented API rate limit is 30 calls per second; calls above it return `-429` (HTTP 429 Too Many Requests), so a bulk loop needs a throttle.

**SMS4Free (JSON REST v2):**

The live endpoint is `https://api.sms4free.co.il/ApiSMS/v2/SendSMS`. Two things break naive code here:

- The old `www.sms4free.co.il/ApiSMS/SendSMS` address now redirects to the homepage. It is dead as an API.
- v1 and v2 return different types. v1 replies with a bare integer body; v2 replies with a JSON envelope carrying `status` and `message`. Code that tests `response.text == "1"` is wrong against v2, and against v1 it misreports failure on any successful multi-recipient send, because a positive value is the count accepted rather than the literal 1.

SMS4Free's developer documentation publishes the status table: a positive value is the number of recipients accepted, `0` is a general error, `-1` wrong key, username or password, `-2` invalid sender, `-3` no recipients found, `-4` insufficient balance, `-5` message content not valid, `-6` sender number has not passed first-time verification. An HTTP 200 is not confirmation by itself; always check `status`, and surface the API's `message` alongside it. Credentials are three fields passed in the body: `user` (the mobile number used at signup), `pass` (the account password), and `key` (the personal API key from the account's API page). On the free trial the sender is locked to the signup number, so a custom sender fails with `-2` until a package is bought.

**019 SMS:** documented at https://docs.019sms.co.il/sms/ with the base address `https://019sms.co.il/api`, XML or JSON, and token authentication. It also exposes a SANDBOX at `https://019sms.co.il/api/test`, which mirrors the real request without performing the action. Use it to validate request formatting before you spend credits; it is the most useful thing on this list for a developer and the most commonly missed.

The providers disagree on both the recipient format and what "success" looks like, so never reuse one provider's parser for another:

| Provider | Recipient format | Success signal |
|----------|------------------|----------------|
| InforU | Local, `0541234567` (the only form its SMS examples show) | `StatusId` 1 |
| SMS4Free | `05XXXXXXXX`, `9725XXXXXXXX` or `+9725XXXXXXXX` | `status` greater than 0 (the recipient count) |
| 019 SMS | `5xxxxxxx` or `05xxxxxxx` | `status` 0 |
| Twilio | E.164, `+972541234567` | HTTP 201 |

**Twilio:** standard Programmable Messaging. Israel has operational rules that silently swallow traffic if ignored, listed under Gotchas.

### Step 5: Delivery Reports (DLR)

There is no delivery-status flag in the bundled script; delivery status is a separate provider call or webhook. Where to look:

- InforU: poll https://capi.inforu.co.il/api/v2/PullData with a `Data.Type` of `DeliveryNotificationSMS` and a batch size, or have InforU push each report to your own URL by setting `Settings.DeliveryNotificationUrl` on the send.
- SMS4Free: pass `returnUrl` and `usermsgid` on the send; SMS4Free then POSTs `to`, `status` and `msgId` form-encoded to that URL. Common statuses: 1 delivered, 5 not delivered, 6 kosher number.
- 019 SMS: see the API documentation linked above.
- Twilio: a `StatusCallback` webhook on the message.

### Step 6: OTP Hardening

The skill markets OTP as a primary use case, so treat the security controls as mandatory rather than optional:

- Rate-limit per destination number, not only per IP or per account.
- Cap verification attempts per code, then invalidate the code.
- Give every code a short TTL and delete it on first successful use so it cannot be replayed.
- Compare with a constant-time comparison, never with `==` on the raw string.
- Never write the code to logs, analytics, or error trackers.
- Make the send idempotent: key it on a request ID so a retried HTTP call resends the SAME code instead of generating a new one. Without this, a retry loop becomes both a duplicate-charge generator and a duplicate-code generator, and the user gets several valid codes at once.

The same idempotency rule applies to bulk sends: key each recipient send so a partial-failure retry does not bill and deliver the batch twice.

### Step 7: Compliance Checklist (Chok HaSpam + Privacy Law Amendment 13)

Israeli commercial SMS is governed by Section 30A of the Communications (Bezeq and Broadcasts) Law, known as Chok HaSpam, and, since 14 August 2025, by Amendment 13 to the Privacy Protection Law, which raised obligations on processors of personal data.

An SMS is a דבר פרסומת when its PURPOSE is commercial: the statute defines it as a message distributed commercially whose purpose is to encourage the purchase of a product or service, or to encourage spending money in another way. It also covers a message to the general public requesting a donation or carrying propaganda (תעמולה), but the statute defines תעמולה to EXCLUDE any political message, election propaganda included. A third limb catches a message to the general public that invites the recipient to call a specific phone number to receive some message.

Before sending commercial SMS:

- [ ] Recipient gave explicit prior written opt-in (active choice, not a pre-ticked box), OR you meet the existing-customer route in the next item
- [ ] Existing-customer route, all conditions together: the recipient gave their details during a purchase or during negotiations toward one; you told them at that point that the details would be used to send advertising; you gave them an opportunity to refuse and they did not; and the advertising concerns a product or service of a SIMILAR KIND to that purchase. Miss any one and you are back to needing fresh opt-in.
- [ ] Opt-in record stored: who, what they consented to, when, on which channel
- [ ] Message content: for SMS specifically the statute requires the advertiser's name and the contact details for sending a refusal notice. The broader list that applies to other channels (the word פרסומת at the start, plus name, address, and contact details, plus the right to refuse) is reduced for short messages to only the name and the refusal contact details. Adding the word פרסומת is common practice and harmless in substance, but the SMS clause itself lists only those two items.
- [ ] Opt-out is free apart from the cost of sending the refusal itself, and the recipient chooses whether to refuse in writing or BY THE SAME CHANNEL the advertisement arrived on. A reply of `עצור` to an SMS must therefore actually work, not merely a link. A recipient cannot reply to an alphanumeric (text) sender ID at all, so a marketing message sent from one needs a reply number or the provider's built-in removal mechanism in the body.
- [ ] Refusals honoured; sending after a refusal removes any good-faith defence
- [ ] Ongoing subscriptions: ending the contract counts as a refusal notice by itself
- [ ] Phone numbers obtained lawfully under Privacy Law Amendment 13 (purpose limitation, data minimisation, security), with the section 11 notice given when the number was collected
- [ ] Direct mail (דיוור ישיר) under the Privacy Protection Law, a SEPARATE regime from Chok HaSpam: a personal approach to a person based on belonging to a population group defined by one or more characteristics of people in a database (for example "customers who bought in the last year" or "customers in Haifa"). Section 17ו(א) then requires EVERY approach to contain, clearly and prominently: a statement that it is direct mail (plus the registration number of the database used for direct-mail services, where one is registered; since Amendment 13 registration is required only in narrower cases, such as a database whose main purpose is passing personal data to others, so many businesses mailing their own customers have no number to cite), notice of the recipient's right to be deleted from the database with the address for that request, and the identity and address of the database controller and the sources it got the data from. Unlike Chok HaSpam, there is no shorter SMS version of this list, so fitting it into an SMS (in the body or via a link) is a judgment call to make with counsel. Under section 23כו(ג), added by Amendment 13, the Privacy Protection Authority may impose a financial sanction of 50 NIS (indexed: 51.18 NIS in 2026) multiplied by the number of recipients, with a minimum of 30,000 NIS (30,710 NIS in 2026); the same per-person sanction covers collecting a number without the section 11 notice. Whether an unsegmented send to the whole customer list is direct mail is debated, so do not assume it is not.
- [ ] No transfer abroad of recipient lists without adequate protection
- [ ] Sending during reasonable hours (avoid Shabbat for religious recipients, avoid late night)
- [ ] Penalty awareness: where an advertisement was sent KNOWINGLY, a court MAY award damages not dependent on proof of loss, up to 1,000 NIS per advertisement. It is a discretionary ceiling and not an automatic tariff. Two things make it worse in practice: an advertiser is PRESUMED to have acted knowingly unless it proves otherwise, and that presumption cannot be rebutted at all in three cases: the message went out after a refusal; the advertiser previously sent that recipient an unlawful advertisement, even unknowingly; or the number came from a randomly generated list. For a recurring monthly campaign the second case means one bad send taints every later one to that recipient.
- [ ] Criminal and personal exposure: sending without consent is also a criminal offence carrying a fine, and the company's manager and whoever is responsible for marketing must supervise to prevent it. If the company commits the offence, those officers are presumed to have breached that duty unless they show they did everything possible.

## Examples

### Example 1: Send OTP
User says: "Send a verification code to an Israeli mobile number."
Result: Generate a 6-digit code, send via the provider API, apply the hardening controls in Step 6, and expire the code in your backend after 5 to 10 minutes.

On the legal side, be careful with the common claim that OTP and service messages are simply exempt. There is no express service-message carve-out in the statute. The test is the message's PURPOSE, so a genuine transactional message the user themselves triggered is outside the definition, but the moment that message carries a logo, a slogan, a promotion, or a marketing link it can become a דבר פרסומת and fall back under the opt-in rule. Keep transactional messages purely transactional.

### Example 2: Format Phone Number
User says: "Convert 054-1234567 to international format."
Result: `+972541234567`. Note the trunk 0 is dropped, so `+9720541234567` is wrong.

### Example 3: Bulk Marketing SMS
User says: "Send a promotional SMS to my customer list about a holiday sale."
Actions:
1. Validate every number with `scripts/validate_phone.py` and drop Palestinian prefixes.
2. Run the segment estimate on the FINAL copy and budget from segments, not characters.
3. Filter the list against your unsubscribe table and your opt-in or existing-customer record.
4. Include the advertiser's name and a working opt-out on the same channel. If the list was selected from your customer database by a characteristic, also include the direct-mail details from Step 7.
5. Schedule for Israeli business hours (avoid Shabbat from Friday afternoon to Saturday evening, avoid Jewish holidays for B2C).
6. Send with per-recipient idempotency keys and reconcile the DLR feed back into your CRM.
Result: a campaign checked against the Chok HaSpam and Privacy Law items in Step 7, with a cost figure that matches the invoice.

## Bundled Resources

### Scripts
- `scripts/send_sms.py`: Sends SMS via SMS4Free, Twilio, or InforUMobile, and computes GSM-7 vs UCS-2 segment counts and estimated cost via `--estimate`. Credentials come from CLI arguments or environment variables (SMS_API_KEY, TWILIO_ACCOUNT_SID, and so on), and each provider's host is fixed in the code. It refuses landline recipients unless `--allow-landline` is passed. It does NOT poll delivery status; see Step 5. Run: `python scripts/send_sms.py --help`
- `scripts/validate_phone.py`: Validates and normalizes Israeli phone numbers from any common format to +972 international format, distinguishes mobile from geographic and non-geographic landline, and rejects Palestinian and retired prefixes with an explanatory message. `--sms-check` exits 2 for a valid landline, since landlines are not SMS destinations. Run: `python scripts/validate_phone.py --help`

## Reference Links

- Communications (Bezeq and Broadcasts) Law, full text including Section 30A: https://www.nevo.co.il/law_html/law01/032_002.htm
- Compensation for advertising sent without consent, Kol Zchut: https://www.kolzchut.org.il/he/%D7%A4%D7%99%D7%A6%D7%95%D7%99_%D7%91%D7%92%D7%99%D7%9F_%D7%9E%D7%A9%D7%9C%D7%95%D7%97_%D7%93%D7%91%D7%A8%D7%99_%D7%A4%D7%A8%D7%A1%D7%95%D7%9E%D7%AA_%D7%9C%D7%9C%D7%90_%D7%94%D7%A1%D7%9B%D7%9E%D7%94_%D7%A9%D7%9C_%D7%94%D7%A0%D7%9E%D7%A2%D7%9F_%28%D7%97%D7%95%D7%A7_%D7%94%D7%A1%D7%A4%D7%90%D7%9D%29
- Privacy Protection Law Amendment 13, Privacy Protection Authority: https://www.gov.il/he/departments/the_privacy_protection_authority
- Sender ID verification regulation effective 3.1.2021, explained by a provider: https://www.sms4free.co.il/Regulation.html
- 019 SMS API documentation and sandbox: https://docs.019sms.co.il/sms/
- InforUMobile API collection: https://apidoc.inforu.co.il/
- SMS4Free API overview: https://www.sms4free.co.il/SMSByAPI.html
- SMS4Free developer documentation (status codes, DLR webhook): https://www.sms4free.co.il/docs/otp-api.html
- ActiveTrail SMS: https://www.activetrail.co.il/
- Twilio Israel SMS guidelines: https://www.twilio.com/en-us/guidelines/il/sms
- Twilio Israel SMS pricing: https://www.twilio.com/en-us/sms/pricing/il
- Twilio Israel and Palestine prefix geo-permission update: https://www.twilio.com/en-us/changelog/programmable-sms-geo-permissions-israel-and-palestine-prefix-update
- Vonage SMS API: https://developer.vonage.com/en/messaging/sms/overview
- Bird (formerly MessageBird): https://bird.com/
- Israeli numbering plan, Ministry of Communications (edition 4, 2023): https://www.gov.il/BlobFolder/policy/number_policy/en/The_numbering_plan-02-2023.pdf
- Israeli numbering plan, operator prefixes: https://en.wikipedia.org/wiki/Telephone_numbers_in_Israel
- GSM-7 vs UCS-2 encoding reference: https://en.wikipedia.org/wiki/GSM_03.38

## Gotchas

- Israeli mobile numbers are 10 digits starting 05X. Agents validate against US 10-digit formats, or keep the leading zero when converting to +972. The correct form drops it.
- 056 and 059 are Palestinian networks (Ooredoo Palestine and Jawwal) sharing the +972 country code. A regex written as `05[0-9]`, or as the range `05[0-8]`, quietly accepts them. Twilio routes those two prefixes through the Palestine geo-permission rather than Israel, under a different rate card and policy.
- The landline branch of a validator is where mobile guards go to die. `0[2-9]\d{7,8}` accepts a truncated 9-digit mobile as a valid landline, so an agent that "validated" the number still sends to a number that cannot receive it.
- Hebrew is UCS-2: 70 characters in one segment, 67 per segment once split. Cost models built on the 160-character Latin figure understate Hebrew campaigns by two to three times. One Hebrew character in an otherwise Latin message downgrades the whole message.
- Sender ID in Israel is NOT a government registry, and there is no Ministry of Communications portal to apply to. The duties sit with your provider, in two layers. First, under a Ministry of Communications regulation effective 3.1.2021 aimed at preventing sender spoofing, a sender ID that is a real mobile or landline NUMBER needs a one-time ownership verification before the first send (Latin-text sender IDs, withheld senders and provider-supplied virtual numbers are exempt from that NUMBER check). Second, under the Ministry's anti-phishing reform decided in October 2022, a business distributing SMS through a bulk-sending system must pass strong identity verification with the provider, for example a video call with identity documents plus verification of the paying credit card; providers report that textual (alphanumeric) sender names have been restricted this way since 25.4.2023. Budget time for this onboarding before a launch. International providers additionally require their own pre-registration for alphanumeric IDs, which Twilio lists as taking about a week for Israel.
- Twilio Israel operational rules that make messages vanish with no obvious error: short codes are NOT SUPPORTED in Israel; international traffic submitted over local long codes is actively blocked by the operators; using a local non-real number as the sender ID (for example a company's fixed-line number) is not allowed and will most probably be rejected by the network operator; and on the Golan and Azi Communications networks numeric sender IDs are replaced by generic alphanumeric ones outside Twilio's platform, so your carefully chosen number is not what the recipient sees.
- Kosher phones (מספר כשר) block SMS. An OTP sent to one is silently lost unless the provider converts it to a voice call: SMS4Free does this automatically and reports DLR status 6 "kosher number". Offer a voice-OTP fallback rather than hard-coding kosher number ranges, which change.
- InforU's SMS product moved to a JSON v2 contract on a different host from the old XML endpoint. Posting the new JSON body to an old address, or sending the API token unencoded in the Basic header, both fail.
- SMS4Free v1 and v2 return different response TYPES from near-identical URLs. Copy the wrong parser and every send looks like a failure.
- Sending on Shabbat is poor B2C practice in Israel and a frequent source of complaints.
- OTP is not automatically exempt from Chok HaSpam. Adding a promotional line or a marketing link to a verification message can convert it into an advertisement.

## Troubleshooting

### Error: "Message not delivered"
Cause: invalid number, carrier blocking, quota exceeded, or a sender ID that has not passed ownership verification.
Solution: re-validate with the bundled script, confirm credentials, and pull the DLR feed (Step 5) rather than guessing from the send response. The send response only says the gateway ACCEPTED the message.

### Error: Messages disappear with a success response (Twilio, Israel)
Cause: usually one of the Israel-specific rules. Short codes are not supported; international traffic over local long codes is blocked by the operators; a local non-real number (such as a company landline) used as the sender ID is rejected by the operator; or the recipient is on Golan or Azi Communications, where numeric sender IDs get swapped for generic alphanumeric ones. If the API itself returned error 21614, the recipient is a landline, which cannot receive SMS.
Solution: switch to a registered alphanumeric sender ID, and route Israeli traffic through an Israeli provider if deliverability matters more than a single global integration.

### Error: "Sender ID rejected"
Cause: a numeric sender ID that has not completed the one-time ownership verification introduced by the 3.1.2021 regulation (SMS4Free status `-6`), an alphanumeric ID used before the account passed the provider's identity verification or pre-registration, or a custom sender on a free trial (SMS4Free status `-2`).
Solution: complete verification with your provider. Numeric mobile senders are verified by a link sent to that handset; numeric landline senders by placing a call from that line. While pre-registration is pending, fall back to the provider's default sender.

### Error: "Hebrew characters garbled in SMS"
Cause: the message was not sent as UCS-2, or was truncated at a Latin length limit.
Solution: send UCS-2 explicitly. Most Israeli providers detect Hebrew automatically. Verify on a real handset rather than a simulator.

### Error: The bill is double the estimate
Cause: budgeting per message rather than per segment on Hebrew traffic.
Solution: run `python scripts/send_sms.py --estimate` on the final copy, and confirm with your provider whether the quote is per message or per segment.

### Error: Users receive several valid OTP codes at once
Cause: a retried send that generates a new code each time.
Solution: make the send idempotent on a request ID as described in Step 6, and invalidate the previous code whenever a new one is legitimately issued.
