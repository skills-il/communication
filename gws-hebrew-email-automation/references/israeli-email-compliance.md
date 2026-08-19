# Israeli Email Compliance and Gmail Deliverability

Detailed reference for Step 7 of SKILL.md. Consult before automating any outbound that goes to more than a handful of recipients.

Before automating any outbound that goes to more than a handful of recipients, gate the workflow on Israel's anti-spam rules and Gmail's 2024-2025 bulk-sender rules.

**Israel's spam law (Section 30A of the Communications Law (Broadcasting and Telecommunications), 5742-1982):**

- "Davar pirsomet" (advertising content) cannot be sent via email, SMS, fax, or automated dialer **without explicit prior consent** of the recipient. Consent must be in writing (an opt-in checkbox or signed form, not pre-checked).
- Statutory damages: **up to 1,000 NIS per offending message**, awarded without proof of actual harm. Damages are cumulative, so a 500-recipient blast can expose the sender to 500,000 NIS in a class action.
- Criminal fine: sending without consent (Section 30A(f)(1)) carries a fine under Penal Law Section 61(a)(4), **226,000 NIS**. Sending an advertisement that omits the required details (Section 30A(f)(2)) is the lower tier, Penal Law Section 61(a)(3), **75,300 NIS**. These ceilings are updated by order of the Minister of Justice under Penal Law Section 64, not automatically every year, so check the current figure before quoting one.
- Every message must include:
  - The word `פרסומת` (advertisement) at the start of the subject line.
  - The sender's full name, full street address, and contact details.
  - The recipient's right to opt out at any time, and for an electronic message specifically, **a valid live internet address of the advertiser for submitting the opt-out** (Section 30A(e)(1)(c)(1)). A reply-to-stop instruction alone does not satisfy this for email. The opt-out must be honored.
- **Transactional messages are outside the section entirely**, because they fail the definition of "davar pirsomet" in Section 30A(a)(1) (a message distributed commercially whose purpose is to encourage a purchase or other spending). An order confirmation, a ticket reply, or a password reset is not advertising. This is a definitional exclusion, not an exemption you have to qualify for.
- **The existing-customer route (Section 30A(c)) is a different thing**: it permits sending *actual advertising* without prior consent, and only when all three conditions hold together: (1) the recipient gave their details to the advertiser during a purchase or during negotiations for one, AND was told the details would be used to send advertising; (2) the advertiser gave them an opportunity to refuse and they did not; (3) the advertisement relates to a product or service **of a similar kind** to the one in (1). **There is no time window in the statute** - no six months, no twelve. Do not tell a user their consent has "expired" or that they are covered because a purchase was recent. Under Section 30A(d)(2), in an ongoing-supply contract the recipient is deemed to have opted out when the contract ends.

**Authentication baseline for EVERY sender, not just bulk.** Google's sender guidelines set requirements that apply to all senders at any volume: SPF **or** DKIM on the sending domain, a valid reverse-DNS (PTR) record, TLS for transmission, RFC 5322-conformant formatting, no impersonation of Gmail From: addresses, and a spam rate kept under 0.3%. A freelancer sending twenty invoices a month from `@mydomain.co.il` is inside this tier. It matters most for `gws gmail +send --from`: sending as a custom-domain alias whose domain has no SPF or DKIM alignment is the single most common reason a freelancer's invoices land in spam, and an invoice nobody saw is exactly the failure this skill exists to prevent. Set up SPF or DKIM before sending anything from a custom address.

**Additional bulk-sender rules (Gmail, in force since February 2024, enforcement ramped up November 2025):**

The table below ADDS to the baseline above once the user sends more than 5,000 messages/day to gmail.com addresses (e.g., a newsletter blast from `@yourdomain.co.il`):

| Requirement | What to set up |
|-------------|----------------|
| SPF | DNS TXT record authorizing the sending IPs |
| DKIM | DNS TXT record with the public key, signing keys configured on the sending domain |
| DMARC | DNS TXT record at `_dmarc.yourdomain.co.il`, policy at least `p=none` for monitoring (move to `quarantine`/`reject` after audit) |
| RFC 8058 one-click unsubscribe | Both `List-Unsubscribe: <https://...>, <mailto:...>` AND `List-Unsubscribe-Post: List-Unsubscribe=One-Click` headers |
| Spam complaint rate | Below 0.1% (red line at 0.3%) |
| Unsubscribe turnaround | Honor unsubscribe requests within **48 hours** |
| Visible unsubscribe link | In the email body |

A `gws gmail +send --html` blast from a Workspace account is subject to all of the above once you cross 5,000/day to Gmail addresses. The CLI does **not** add `List-Unsubscribe` headers automatically; you must build them into your `--body` HTML or use a transactional ESP (Resend, SendGrid, Mailgun) for the actual blast.

**Practical workflow before drafting any outbound that resembles marketing:**

1. Ask the user: is this message advertising content (offer, promotion, newsletter)? If yes, confirm the recipient has explicit written consent on file.
2. If marketing, prefix the subject with `פרסומת - ...` and append the sender's full details + a `הסרה` (unsubscribe) instruction to the body.
3. If volume is >100/day, recommend the user move the blast to a transactional ESP rather than `gws gmail +send` (Gmail's daily limit and authentication burden are not built for marketing volume).
