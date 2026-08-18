#!/usr/bin/env python3
"""Format currency amounts to Israeli Shekel (ILS) standard.

Converts numeric values to properly formatted Israeli Shekel strings
with thousands separators and the standard ILS notation.

Usage:
  python scripts/shekel-formatter.py 15000
  python scripts/shekel-formatter.py 15000 --vat
  python scripts/shekel-formatter.py 8500 --vat --terms 30
  python scripts/shekel-formatter.py --help

Output examples:
  15,000 ש"ח
  15,000 ש"ח (כולל מע"מ)
  15,000 ש"ח (לא כולל מע"מ) | מע"מ: 2,550 ש"ח | סה"כ: 17,550 ש"ח
"""

import argparse
import sys
from decimal import Decimal, ROUND_HALF_UP

# Current Israeli VAT rate (as of 2026)
VAT_RATE = Decimal("0.18")


def format_shekel(amount: Decimal, include_symbol: bool = True) -> str:
    """Format a number as Israeli Shekel amount.

    Args:
        amount: The amount to format
        include_symbol: Whether to append the Shekel symbol

    Returns:
        Formatted string like "15,000" or '15,000 ש"ח'
    """
    # Round to 2 decimal places
    rounded = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Check if it's a whole number
    if rounded == rounded.to_integral_value():
        formatted = f"{int(rounded):,}"
    else:
        integer_part = int(rounded)
        decimal_part = abs(rounded - integer_part).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        decimal_str = str(decimal_part)[2:]  # Remove "0."
        formatted = f"{integer_part:,}.{decimal_str}"

    if include_symbol:
        return f'{formatted} ש"ח'
    return formatted


def calculate_vat(amount: Decimal) -> dict:
    """Calculate VAT for a given amount.

    Args:
        amount: The base amount (before VAT)

    Returns:
        Dict with base, vat, and total amounts
    """
    vat = (amount * VAT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    total = amount + vat
    return {"base": amount, "vat": vat, "total": total}


def format_payment_terms(days: int) -> str:
    """Format payment terms in Hebrew.

    Args:
        days: Number of days (e.g., 30, 45, 60)

    Returns:
        Hebrew payment terms string
    """
    return f"שוטף + {days}"


def main():
    parser = argparse.ArgumentParser(
        description="Format amounts to Israeli Shekel (ILS) standard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s 15000                    # 15,000 ש\"ח\n"
            "  %(prog)s 15000 --vat              # With VAT breakdown\n"
            "  %(prog)s 8500 --vat --terms 30    # With payment terms\n"
            "  %(prog)s 1234.56                  # 1,234.56 ש\"ח\n"
        ),
    )
    parser.add_argument("amount", type=str, help="Amount to format (number)")
    parser.add_argument(
        "--vat", action="store_true", help="Include VAT (18%%) breakdown"
    )
    parser.add_argument(
        "--terms",
        type=int,
        choices=[30, 45, 60, 90],
        help="Payment terms in days",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )

    args = parser.parse_args()

    try:
        amount = Decimal(args.amount.replace(",", ""))
    except Exception:
        print(f"Error: Invalid amount '{args.amount}'", file=sys.stderr)
        sys.exit(1)

    if amount < 0:
        print("Error: Amount must be positive", file=sys.stderr)
        sys.exit(1)

    if args.json:
        import json

        result = {"amount": str(amount), "formatted": format_shekel(amount)}
        if args.vat:
            vat_info = calculate_vat(amount)
            result["vat"] = {
                "rate": str(VAT_RATE),
                "base": format_shekel(vat_info["base"]),
                "vat_amount": format_shekel(vat_info["vat"]),
                "total": format_shekel(vat_info["total"]),
            }
        if args.terms:
            result["payment_terms"] = {
                "days": args.terms,
                "hebrew": format_payment_terms(args.terms),
            }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if args.vat:
            vat_info = calculate_vat(amount)
            print(f'סכום: {format_shekel(vat_info["base"])} (לא כולל מע"מ)')
            print(f'מע"מ (18%): {format_shekel(vat_info["vat"])}')
            print(f'סה"כ: {format_shekel(vat_info["total"])} (כולל מע"מ)')
        else:
            print(format_shekel(amount))

        if args.terms:
            print(f"תנאי תשלום: {format_payment_terms(args.terms)}")


if __name__ == "__main__":
    main()
