#!/usr/bin/env python3
"""Validate and normalize Israeli phone numbers.

Usage:
    python validate_phone.py <phone_number>
    python validate_phone.py 054-1234567
    python validate_phone.py +972541234567
    python validate_phone.py "054 123 4567"

Returns the normalized international format (+972XXXXXXXXX) if valid,
or an explanatory error message if the number is invalid.

Numbering plan encoded here (see SKILL.md "Reference Links" for the source):
    Israeli mobile      050 051 052 053 054 055 058   -> 10 local digits
    Palestinian mobile  056 (Ooredoo)  059 (Jawwal)   -> rejected on purpose
    Retired mobile      057                           -> rejected on purpose
    Geographic landline 02 03 04 08 09                -> 9 local digits
    Non-geographic      07N (landline / VoIP)         -> 10 local digits
"""

import argparse
import re
import sys

# Explicit alternation, NOT a character range. `05[0-8]` looks equivalent for
# today's allocation but it is a RANGE over {0,1,2,3,4,5,6,7,8}: it silently
# admits 056 and 057, and anyone who later widens it to 05[0-9] also admits
# 059. Both 056 and 059 are Palestinian networks and 057 is retired, so the
# set is spelled out one prefix at a time and must stay that way.
ISRAELI_MOBILE_PREFIXES = ('050', '051', '052', '053', '054', '055', '058')
PALESTINIAN_MOBILE_PREFIXES = ('056', '059')
RETIRED_MOBILE_PREFIXES = ('057',)

MOBILE_RE = re.compile(r'^(?:050|051|052|053|054|055|058)\d{7}$')
# Geographic landlines are 9 local digits in total: one area-code pair plus
# seven. The old pattern was `0[2-9]\d{7,8}`, which (a) swallowed every 05
# number the mobile branch had just rejected and (b) accepted a 10-digit 03
# number that does not exist. Both bugs are closed by anchoring the length and
# by never letting 05 reach this branch.
LANDLINE_GEO_RE = re.compile(r'^0(?:2|3|4|8|9)\d{7}$')
# Non-geographic landline / VoIP: 07N plus seven digits, 10 local digits.
LANDLINE_NONGEO_RE = re.compile(r'^07\d{8}$')


def normalize(phone: str) -> str:
    """Strip separators and convert any +972 / 972 form to the local 0 form."""
    clean = re.sub(r'[\s\-\(\)\.]', '', phone)
    if clean.startswith('+972'):
        clean = '0' + clean[4:]
    elif clean.startswith('972'):
        clean = '0' + clean[3:]
    return clean


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
        international format or an explanatory error message.
    """
    raw = re.sub(r'[\s\-\(\)\.]', '', phone)
    clean = normalize(phone)

    # The international forms carry the country code, so the national number
    # must NOT also carry its trunk 0. "+9720501234567" is the single most
    # common malformed input and it used to normalize to "00501234567".
    if (raw.startswith('+972') or raw.startswith('972')) and clean.startswith('00'):
        return False, ('Invalid: an extra leading zero. In +972 form the national '
                       'trunk 0 is dropped, so 050-1234567 becomes +972501234567, '
                       'not +9720501234567.')

    if not clean.startswith('0') or not clean[1:].isdigit():
        return False, 'Invalid Israeli phone number: expected digits in local (0...) or +972 form.'

    prefix3 = clean[:3]

    if MOBILE_RE.match(clean):
        return True, '+972' + clean[1:]

    if prefix3 in PALESTINIAN_MOBILE_PREFIXES:
        return False, (f'Rejected: {prefix3} is a Palestinian mobile network '
                       '(056 Ooredoo Palestine, 059 Jawwal), not an Israeli one. '
                       'It shares the +972 country code but routes under a '
                       'different rate card and geo-permission.')

    if prefix3 in RETIRED_MOBILE_PREFIXES:
        return False, (f'Rejected: {prefix3} is not a currently allocated Israeli '
                       'mobile prefix. Hot mobile used it until November 2014.')

    if clean.startswith('05'):
        return False, (f'Invalid Israeli mobile number. Expected one of '
                       f'{", ".join(ISRAELI_MOBILE_PREFIXES)} followed by 7 digits '
                       f'(10 digits in total), got {len(clean)} digits.')

    if LANDLINE_GEO_RE.match(clean):
        return True, '+972' + clean[1:]

    if LANDLINE_NONGEO_RE.match(clean):
        return True, '+972' + clean[1:]

    if clean.startswith('07'):
        return False, ('Invalid non-geographic number. 07N landline and VoIP '
                       'numbers are 10 digits in total.')

    if clean[1] in '23489':
        return False, ('Invalid Israeli landline. Geographic numbers (02, 03, 04, '
                       f'08, 09) are 9 digits in total, got {len(clean)}.')

    return False, 'Invalid Israeli phone number.'


def get_phone_type(phone: str) -> str:
    """Describe a number that already passed validate_israeli_phone.

    Args:
        phone: Phone number in any accepted format.

    Returns:
        String indicating phone type.
    """
    clean = normalize(phone)

    if MOBILE_RE.match(clean):
        return 'mobile'

    if LANDLINE_GEO_RE.match(clean):
        area_codes = {
            '02': 'Jerusalem',
            '03': 'Tel Aviv',
            '04': 'Haifa / North',
            '08': 'South / Be\'er Sheva',
            '09': 'Sharon / Netanya',
        }
        region = area_codes.get(clean[:2], 'Unknown region')
        return f'landline ({region})'

    if LANDLINE_NONGEO_RE.match(clean):
        return 'landline (non-geographic / VoIP)'

    return 'unknown'


def main():
    parser = argparse.ArgumentParser(
        description='Validate and normalize an Israeli phone number to +972 format.',
        epilog='Example: python validate_phone.py 054-1234567',
    )
    parser.add_argument('phone', help='Phone number in local (05X...) or international (+972...) form')
    args = parser.parse_args()

    is_valid, result = validate_israeli_phone(args.phone)

    if is_valid:
        print(f'Valid: {result} ({get_phone_type(args.phone)})')
    else:
        print(f'Invalid: {result}')
        sys.exit(1)


if __name__ == '__main__':
    main()
