#!/usr/bin/env python3
"""Validate email campaign HTML against Israeli anti-spam law (Chok HaSpam).

Checks:
  - Hebrew unsubscribe link presence
  - RTL markup correctness
  - Required legal text
  - Consent record completeness (optional)

Usage:
  python check_email.py --html campaign.html
  python check_email.py --html campaign.html --consent-db consents.json
  python check_email.py --help
"""

import argparse
import json
import re
import sys
from pathlib import Path


def check_rtl_markup(html: str) -> list[dict]:
    """Check for proper RTL markup in HTML email."""
    issues = []

    if 'dir="rtl"' not in html and "dir='rtl'" not in html:
        issues.append({
            "severity": "error",
            "rule": "rtl-direction",
            "message": "Missing dir=\"rtl\" attribute. Hebrew emails must set RTL direction on root element."
        })

    if "text-align: right" not in html and "text-align:right" not in html:
        issues.append({
            "severity": "warning",
            "rule": "rtl-text-align",
            "message": "Missing text-align: right. Hebrew content should default to right-aligned."
        })

    if 'lang="he"' not in html and "lang='he'" not in html:
        issues.append({
            "severity": "warning",
            "rule": "lang-attribute",
            "message": "Missing lang=\"he\" attribute. Set language for accessibility and rendering."
        })

    if 'charset' not in html.lower():
        issues.append({
            "severity": "error",
            "rule": "charset",
            "message": "Missing charset declaration. Use UTF-8 for Hebrew content."
        })

    return issues


def check_unsubscribe(html: str) -> list[dict]:
    """Check for mandatory Hebrew unsubscribe mechanism."""
    issues = []

    hebrew_unsub_patterns = [
        r"הסרה",
        r"להסרה",
        r"הסרת מרשימה",
        r"הסרה מרשימת התפוצה",
        r"ביטול רישום",
        r"אינך מעוניין",
        r"אינך מעוניינת",
        r"להפסיק לקבל",
    ]

    has_hebrew_unsub = any(
        re.search(pattern, html) for pattern in hebrew_unsub_patterns
    )

    if not has_hebrew_unsub:
        issues.append({
            "severity": "error",
            "rule": "hebrew-unsubscribe",
            "message": "Missing Hebrew unsubscribe text. Israeli law requires unsubscribe mechanism in Hebrew."
        })

    unsub_link = re.search(r'<a[^>]*href=["\'][^"\']*unsub[^"\']*["\']', html, re.IGNORECASE)
    if not unsub_link:
        unsub_link = re.search(r'<a[^>]*href=["\'][^"\']*remove[^"\']*["\']', html, re.IGNORECASE)

    if not unsub_link and not has_hebrew_unsub:
        issues.append({
            "severity": "error",
            "rule": "unsubscribe-link",
            "message": "No unsubscribe link found. Every commercial email must include a functional unsubscribe link."
        })

    return issues


def check_legal_requirements(html: str) -> list[dict]:
    """Check for required legal text under Israeli law."""
    issues = []

    has_business_id = bool(re.search(r'\d{9}', html))
    if not has_business_id:
        issues.append({
            "severity": "warning",
            "rule": "business-id",
            "message": "No 9-digit business registration number found. Recommended for commercial emails."
        })

    nis_pattern = re.search(r'(NIS|ש"ח|שקל|ILS)', html)
    price_pattern = re.search(r'\d+([.,]\d+)?', html)
    if nis_pattern and not re.search(r'(מע"מ|VAT|כולל מע)', html):
        issues.append({
            "severity": "warning",
            "rule": "vat-notice",
            "message": "Prices found but no VAT notice. Israeli law requires clear pricing including VAT."
        })

    return issues


def check_consent_records(consent_file: str) -> list[dict]:
    """Validate consent database completeness."""
    issues = []

    try:
        with open(consent_file, "r", encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        issues.append({
            "severity": "error",
            "rule": "consent-file",
            "message": f"Consent file not found: {consent_file}"
        })
        return issues
    except json.JSONDecodeError:
        issues.append({
            "severity": "error",
            "rule": "consent-format",
            "message": f"Invalid JSON in consent file: {consent_file}"
        })
        return issues

    if not isinstance(records, list):
        records = [records]

    required_fields = ["email", "consented_at", "consent_method", "consent_source"]

    for i, record in enumerate(records):
        for field in required_fields:
            if field not in record or not record[field]:
                issues.append({
                    "severity": "error",
                    "rule": "consent-field",
                    "message": f"Record {i}: Missing required field '{field}'"
                })

        if record.get("is_active") is False:
            issues.append({
                "severity": "warning",
                "rule": "consent-revoked",
                "message": f"Record {i} ({record.get('email', 'unknown')}): Consent was revoked. Do NOT send."
            })

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Validate email campaign against Israeli anti-spam law (Chok HaSpam)"
    )
    parser.add_argument(
        "--html",
        required=True,
        help="Path to email campaign HTML file"
    )
    parser.add_argument(
        "--consent-db",
        help="Path to consent records JSON file (optional)"
    )
    args = parser.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        print(f"Error: HTML file not found: {args.html}")
        sys.exit(1)

    html_content = html_path.read_text(encoding="utf-8")

    all_issues = []
    all_issues.extend(check_rtl_markup(html_content))
    all_issues.extend(check_unsubscribe(html_content))
    all_issues.extend(check_legal_requirements(html_content))

    if args.consent_db:
        all_issues.extend(check_consent_records(args.consent_db))

    errors = [i for i in all_issues if i["severity"] == "error"]
    warnings = [i for i in all_issues if i["severity"] == "warning"]

    print(f"\nIsraeli Email Compliance Check: {args.html}")
    print("=" * 60)

    if not all_issues:
        print("PASS: All checks passed.")
        sys.exit(0)

    for issue in errors:
        print(f"  ERROR [{issue['rule']}]: {issue['message']}")

    for issue in warnings:
        print(f"  WARN  [{issue['rule']}]: {issue['message']}")

    print(f"\nSummary: {len(errors)} error(s), {len(warnings)} warning(s)")

    if errors:
        print("FAIL: Fix errors before sending campaign.")
        sys.exit(1)
    else:
        print("PASS (with warnings): Review warnings before sending.")
        sys.exit(0)


if __name__ == "__main__":
    main()
