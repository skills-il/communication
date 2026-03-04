---
name: israeli-email-compliance
description: >-
  Build compliant email campaigns for the Israeli market with Hebrew RTL
  templates, anti-spam law validation, and deliverability optimization. Use when
  user asks about Israeli email marketing, Hebrew email templates, "Chok
  HaSpam" (Amendment 40) compliance, Israeli ISP deliverability (Bezeq, HOT,
  Partner), opt-in consent management ("haskama mukdemet"), Hebrew unsubscribe
  mechanisms ("hasarat mireshima"), or RTL HTML email formatting. Covers prior
  explicit consent requirements stricter than CAN-SPAM, 14-day cancellation
  rights under Consumer Protection Law, and consent management for overlapping
  email and SMS campaigns. Do NOT use for SMS messaging (use israeli-sms-gateway
  instead) or WhatsApp marketing (use israeli-whatsapp-business instead).
license: MIT
allowed-tools: 'Bash(python:*) WebFetch'
compatibility: >-
  Requires Python 3.9+ for validation script. Network access optional for
  deliverability checks.
metadata:
  author: skills-il
  version: 1.0.0
  category: communication
  tags:
    he:
      - דוא"ל
      - ספאם
      - רגולציה
      - שיווק
      - הסכמה
      - ישראל
    en:
      - email
      - spam
      - regulation
      - marketing
      - consent
      - israel
  display_name:
    he: תאימות דוא"ל ישראלי
    en: Israeli Email Compliance
  display_description:
    he: >-
      בניית קמפיינים תקניים לדוא"ל בשוק הישראלי עם תבניות RTL בעברית, אימות
      חוק הספאם ואופטימיזציית שליחה
    en: >-
      Build compliant email campaigns for the Israeli market with Hebrew RTL
      templates, anti-spam law validation, and deliverability optimization. Use
      when user asks about Israeli email marketing, Hebrew email templates,
      Chok HaSpam compliance, Israeli ISP deliverability, opt-in consent
      management, or RTL HTML email formatting.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Email Compliance

## Instructions

### Step 1: Understand Israeli Anti-Spam Law ("Chok HaSpam")

Amendment 40 to the Communications Law (Telecommunications), 5742-1982, is Israel's anti-spam regulation. Key differences from US CAN-SPAM:

| Requirement | Israel (Chok HaSpam) | US (CAN-SPAM) |
|-------------|----------------------|----------------|
| Consent model | Prior explicit consent ("haskama mukdemet") required BEFORE sending | Opt-out model (send until unsubscribe) |
| Consent format | Written, recorded, or digital with timestamp | No specific format |
| Unsubscribe deadline | Immediate (within 2 business days max) | 10 business days |
| Penalties | Up to 1,000 NIS per message without consent (civil), criminal fines | Up to $46,517 per email |
| Private lawsuits | Recipients can sue for 1,000 NIS per message without proving damages | Must prove damages |

**Exceptions where prior consent is NOT required:**
1. Existing customer who purchased similar products/services in the past year
2. The message clearly relates to a product/service the customer previously purchased
3. The customer was given a clear opportunity to refuse at the time of purchase

### Step 2: Implement Consent Management

```python
from datetime import datetime, timezone
from dataclasses import dataclass, field

@dataclass
class ConsentRecord:
    """Track opt-in consent per Israeli anti-spam law requirements."""
    email: str
    consented_at: str  # ISO 8601 timestamp
    consent_method: str  # "web_form", "written", "verbal_recorded"
    consent_source: str  # URL or description of where consent was given
    ip_address: str = ""
    channels: list = field(default_factory=lambda: ["email"])
    is_active: bool = True
    revoked_at: str = ""

    def to_record(self) -> dict:
        return {
            "email": self.email,
            "consented_at": self.consented_at,
            "method": self.consent_method,
            "source": self.consent_source,
            "ip": self.ip_address,
            "channels": self.channels,
            "active": self.is_active,
            "revoked_at": self.revoked_at
        }

def validate_consent(record: ConsentRecord) -> list:
    """Validate consent record meets Israeli legal requirements."""
    issues = []
    if not record.consented_at:
        issues.append("Missing consent timestamp (required by law)")
    if record.consent_method not in ("web_form", "written", "verbal_recorded"):
        issues.append("Consent method must be verifiable")
    if not record.consent_source:
        issues.append("Must record where consent was obtained")
    return issues
```

**Multi-channel consent management (email + SMS):**
When a user consents to email, that does NOT automatically cover SMS or WhatsApp. Each channel requires separate explicit consent under Chok HaSpam.

### Step 3: Build Hebrew RTL Email Templates

Hebrew emails require proper RTL (right-to-left) markup. Without it, ISPs may flag emails as spam or render them incorrectly.

```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      direction: rtl;
      text-align: right;
      font-family: Arial, Helvetica, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #f4f4f4;
    }
    .container {
      max-width: 600px;
      margin: 0 auto;
      background-color: #ffffff;
      padding: 20px;
    }
    .header { text-align: center; padding: 20px 0; }
    .content { padding: 20px; line-height: 1.8; }
    .unsubscribe {
      text-align: center;
      padding: 20px;
      font-size: 12px;
      color: #666666;
      border-top: 1px solid #eeeeee;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>COMPANY_NAME</h1>
    </div>
    <div class="content">
      <p>MESSAGE_BODY</p>
    </div>
    <div class="unsubscribe">
      <p>
        UNSUBSCRIBE_TEXT_HE
        <a href="UNSUBSCRIBE_URL">UNSUBSCRIBE_LINK_HE</a>
      </p>
      <p>COMPANY_ADDRESS</p>
    </div>
  </div>
</body>
</html>
```

**Critical RTL rules:**
- Always set `dir="rtl"` on the root element
- Use `text-align: right` as default
- Mixed Hebrew/English content: wrap English segments in `<span dir="ltr">`
- Test in both Outlook (common in Israeli enterprises) and Gmail

### Step 4: Israeli ISP Deliverability

Israeli ISPs have specific patterns that affect email deliverability:

| ISP | Email Domain | Notes |
|-----|-------------|-------|
| Bezeq (bezeq.net) | @bezeq.net, @bezequint.net | Conservative spam filters, warm up slowly |
| HOT (hot.net.il) | @hot.co.il, @hotmail.co.il | Monitor bounce rates carefully |
| Partner (012) | @012.net.il | Aggressive rate limiting |
| Cellcom | @cellcom.co.il | Standard deliverability |
| Walla! | @walla.co.il | Popular Israeli webmail, check image rendering |
| Gmail IL | @gmail.com | Standard Google filters, Hebrew subject lines OK |

**Deliverability best practices for Israel:**
1. Warm up new sending IPs gradually (start with 50/day, double weekly)
2. Authenticate with SPF, DKIM, and DMARC
3. Hebrew subject lines: keep under 50 characters (displays truncated on mobile)
4. Send during Israeli business hours: Sunday-Thursday, 09:00-18:00 Israel time
5. Avoid sending Friday afternoon through Saturday evening (Shabbat)

### Step 5: Mandatory Unsubscribe Mechanism

Under Chok HaSpam, every commercial email MUST include a clear, functional unsubscribe mechanism in Hebrew.

```python
def generate_unsubscribe_section(unsub_url: str, company_name: str) -> dict:
    """Generate bilingual unsubscribe section for Israeli emails."""
    return {
        "he": (
            f"אינך מעוניין/ת לקבל הודעות מ-{company_name}? "
            f'<a href="{unsub_url}">לחצ/י כאן להסרה מרשימת התפוצה</a>. '
            "ההסרה תתבצע תוך 2 ימי עסקים."
        ),
        "en": (
            f"Don't want to receive emails from {company_name}? "
            f'<a href="{unsub_url}">Click here to unsubscribe</a>. '
            "Removal will be processed within 2 business days."
        )
    }

def process_unsubscribe(email: str, record: dict) -> dict:
    """Process unsubscribe request per Israeli law requirements."""
    return {
        "email": email,
        "status": "unsubscribed",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "must_complete_by": "2 business days from request",
        "channels_removed": record.get("channels", ["email"]),
        "confirmation_sent": True
    }
```

**Unsubscribe requirements under Chok HaSpam:**
- Must be in Hebrew (or bilingual)
- One-click or single-step process (no login required)
- Must be processed within 2 business days
- Must include List-Unsubscribe header for email clients

### Step 6: Consumer Protection Law Integration

The Israeli Consumer Protection Law grants a 14-day cancellation right ("zchut bitulim") for transactions made via commercial communications:

```python
def cancellation_notice_required(transaction_type: str) -> dict:
    """Check 14-day cancellation requirements for email-driven transactions."""
    rules = {
        "cooling_off_period_days": 14,
        "notice_required": True,
        "applies_to": [
            "Purchases made via email promotions",
            "Subscriptions initiated from email campaigns",
            "Services booked through email offers"
        ],
        "must_include_in_email": [
            "Clear pricing in NIS (including VAT)",
            "Cancellation rights notice in Hebrew",
            "Business registration number",
            "Contact details for cancellation requests"
        ]
    }
    return rules
```

### Step 7: Run Compliance Validation

Use the bundled validation script to check your email campaign:

```bash
python scripts/check_email.py --html campaign.html --consent-db consents.json
```

The script validates:
- Hebrew unsubscribe link presence
- RTL markup correctness
- Required legal text
- Consent record completeness

## Examples

### Example 1: Marketing Campaign Setup
User says: "Create a Hebrew email campaign for our Passover sale"
Actions:
1. Verify consent records exist for all recipients with "email" channel
2. Build RTL Hebrew template with holiday-themed content
3. Add mandatory unsubscribe section in Hebrew
4. Include 14-day cancellation notice for any products offered
5. Schedule for Sunday-Thursday before Passover (avoid Shabbat and Chag)
Result: Compliant Hebrew marketing email with proper consent verification.

### Example 2: Transactional Email Template
User says: "Set up order confirmation emails in Hebrew for our e-commerce site"
Actions:
1. Create RTL HTML template with order details
2. Include business registration number and NIS pricing with VAT
3. Add cancellation rights notice (14-day cooling off)
4. Test rendering on Walla!, Gmail, and Outlook
Result: Legally compliant Hebrew transactional email template.

### Example 3: Consent Migration
User says: "We're moving from Mailchimp to SendGrid, how do we handle Israeli consent records?"
Actions:
1. Export all consent records with timestamps and consent source
2. Map consent fields to new platform (preserve original consent date)
3. Verify each record has required fields (timestamp, method, source)
4. Re-validate against Chok HaSpam requirements
Result: Migrated consent database with full legal compliance preserved.

### Example 4: Multi-Channel Compliance Audit
User says: "We send both emails and SMS to customers, is our consent setup correct?"
Actions:
1. Verify separate consent records exist for each channel
2. Check that email consent does not assume SMS consent
3. Validate unsubscribe mechanisms exist per channel
4. Confirm consent timestamps and sources are recorded
Result: Audit report with per-channel compliance status.

## Bundled Resources

### Scripts
- `scripts/check_email.py` -- Validates email campaign HTML against Israeli anti-spam law requirements. Checks for Hebrew unsubscribe links, RTL markup, required legal text, and consent record completeness. Run: `python scripts/check_email.py --help`

### References
- `references/anti-spam-law.md` -- Summary of Amendment 40 to the Communications Law (Chok HaSpam): consent requirements, penalties, exceptions, enforcement patterns, and comparison with international anti-spam laws. Consult when verifying campaign compliance or advising on consent architecture.

## Troubleshooting

### Error: "No consent record found for recipient"
Cause: Recipient email not in consent database or consent was revoked.
Solution: Verify recipient explicitly opted in. Under Israeli law, you CANNOT send commercial email without prior consent. Check if consent was recorded with timestamp and source.

### Error: "RTL rendering broken in Outlook"
Cause: Outlook uses Word rendering engine which handles RTL inconsistently.
Solution: Add `dir="rtl"` to every table cell individually, not just the wrapper. Use inline styles instead of CSS classes for direction properties.

### Error: "High bounce rate on Israeli ISPs"
Cause: Sending too fast to Israeli ISP domains or poor list hygiene.
Solution: Implement domain-based throttling (max 100/hour for Bezeq, 200/hour for HOT). Remove hard bounces immediately. Warm up gradually on new IPs.
