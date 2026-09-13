# Pre-send compliance checklist for Israeli WhatsApp messaging

Returns the checks to confirm before a send. The legal background for each marketing item is in SKILL.md Step 4 (section 30A consent routes, the section 30A(e) disclosure block, Amendment 13). For opt-outs that arrive inside WhatsApp itself, see `platform-2026.md` part 3.

```python
def compliance_checklist(message_type: str) -> list:
    """Return compliance checklist for Israeli WhatsApp messaging."""
    checks = [
        "Consent basis recorded: explicit opt-in, or the section 30A(c) existing-customer route",
        "Opt-in record stored: who, what, timestamp, channel",
        "Opt-out mechanism included (e.g., reply 'הסר' / 'STOP')",
        "Phone numbers obtained lawfully; the list is treated as a database",
        "Message sent in appropriate language (Hebrew or English)",
    ]
    if message_type == "marketing":
        checks.extend([
            "Marketing template approved by Meta in MARKETING category",
            "Message clearly marked as advertising (common practice; confirm wording with counsel)",
            "Advertiser name, address and contact details stated in the body",
            "Right to refuse and how to exercise it stated in the body",
            "If relying on the existing-customer route, the goods are of the same kind",
            "Not sent during Shabbat or Jewish holidays for B2C",
            "No cross-border list transfer without adequate protection",
        ])
    return checks
```
