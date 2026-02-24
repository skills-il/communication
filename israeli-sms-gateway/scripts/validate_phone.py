#!/usr/bin/env python3
"""Validate and normalize Israeli phone numbers.

Usage:
    python validate_phone.py <phone_number>
    python validate_phone.py 054-1234567
    python validate_phone.py +972541234567
    python validate_phone.py "054 123 4567"

Returns the normalized international format (+972XXXXXXXXX) if valid,
or an error message if the number is invalid.
"""

import re
import sys


def validate_israeli_phone(phone: str) -> tuple[bool, str]:
    """Validate and normalize an Israeli phone number.

    Accepts various formats:
        - Local: 054-1234567, 054 123 4567, 0541234567
        - International: +972541234567, 972-54-1234567
        - With country code: +972-54-123-4567

    Args:
        phone: Phone number string in any common format.

    Returns:
        Tuple of (is_valid, result) where result is either the normalized
        international format or an error message.
    """
    # Remove spaces, dashes, parentheses, dots
    clean = re.sub(r'[\s\-\(\)\.]', '', phone)

    # Handle +972 prefix
    if clean.startswith('+972'):
        clean = '0' + clean[4:]
    elif clean.startswith('972'):
        clean = '0' + clean[3:]

    # Validate mobile: 05X-XXXXXXX (10 digits total)
    # Israeli mobile prefixes: 050, 051, 052, 053, 054, 055, 056, 058
    if re.match(r'^05[0-8]\d{7}$', clean):
        international = '+972' + clean[1:]
        return True, international

    # Validate landline: 0X-XXXXXXX (9-10 digits total)
    # Area codes: 02 (Jerusalem), 03 (Tel Aviv), 04 (Haifa), 08 (South), 09 (Sharon)
    if re.match(r'^0[2-9]\d{7,8}$', clean):
        international = '+972' + clean[1:]
        return True, international

    return False, "Invalid Israeli phone number"


def get_phone_type(phone: str) -> str:
    """Determine if the phone number is mobile or landline.

    Args:
        phone: Normalized phone number starting with 0.

    Returns:
        String indicating phone type.
    """
    clean = re.sub(r'[\s\-\(\)\.]', '', phone)
    if clean.startswith('+972'):
        clean = '0' + clean[4:]
    elif clean.startswith('972'):
        clean = '0' + clean[3:]

    if re.match(r'^05[0-8]', clean):
        return "mobile"
    elif re.match(r'^0[2-9]', clean):
        area_codes = {
            '02': 'Jerusalem',
            '03': 'Tel Aviv',
            '04': 'Haifa / North',
            '08': 'South / Be\'er Sheva',
            '09': 'Sharon / Netanya',
        }
        prefix = clean[:2]
        region = area_codes.get(prefix, 'Unknown region')
        return f"landline ({region})"
    return "unknown"


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_phone.py <phone_number>")
        print("Example: python validate_phone.py 054-1234567")
        sys.exit(1)

    phone = sys.argv[1]
    is_valid, result = validate_israeli_phone(phone)

    if is_valid:
        phone_type = get_phone_type(phone)
        print(f"Valid: {result} ({phone_type})")
    else:
        print(f"Invalid: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
