# Pre-send compliance checklist for Israeli WhatsApp messaging

Returns the checks to confirm before a send. The legal background for each marketing item is in `israeli-law.md` (section 30א consent routes and mandatory content, Privacy Protection Law direct mail, Amendment 13). For opt-outs that arrive inside WhatsApp itself, see `platform-2026.md` part 3; for which endpoint a marketing template goes to, part 9.

```python
def compliance_checklist(message_type: str, segmented: bool = False) -> list:
    """Return compliance checklist for Israeli WhatsApp messaging."""
    checks = [
        "Consent basis recorded: prior express consent in writing, or the section 30A(c) existing-customer route",
        "Opt-in record stored: who, what, timestamp, channel",
        "Opt-out mechanism included (e.g., reply 'הסר' / 'STOP')",
        "Phone numbers obtained lawfully; the list is treated as a database",
        "Opt-in form gives the section 11 notice: voluntary or not, purpose, controller and contact, "
        "who receives the data (BSP, Meta), access and correction rights",
        "Message sent in appropriate language (Hebrew or English)",
    ]
    if message_type == "marketing":
        checks.extend([
            "Marketing template approved by Meta in MARKETING category",
            "Sent to /marketing_messages if the template's LATEST category is MARKETING "
            "(required for accounts created from 13 April 2027, for everyone from 13 October 2027)",
            "The word 'פרסומת' at the very start of the message (statutory, section 30A(e))",
            "Advertiser name, address and contact details stated in the body",
            "Right to refuse at any time stated, with a simple way to do it",
            "A valid web or email address for refusals, in addition to the 'הסר' reply",
            "If relying on the existing-customer route, the goods are of a similar kind",
            "Customers whose subscription or contract ended are removed (treated as a refusal)",
            "Not sent during Shabbat or Jewish holidays for B2C",
            "List sent abroad only under the transfer regulations (adequate country or a reg. 2 "
            "exception, plus the recipient's written undertaking)",
        ])
        if segmented:
            checks.extend([
                "Direct-mail fields (Privacy Protection Law s.17F): states it is direct mail with "
                "the direct-mail database's registration number, right to be deleted from the "
                "database and where to ask, controller identity, address and data sources",
                "Written deletion requests acted on and confirmed in writing within 30 days",
            ])
    return checks
```
