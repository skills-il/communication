#!/usr/bin/env python3
"""
Israeli Hebrew Support Ticket Classifier

Classifies Hebrew support tickets by category and priority based on keyword
analysis. Supports single ticket classification and batch processing from CSV.

Usage:
    python ticket-classifier.py --text "הכרטיס שלי חויב פעמיים" --lang he
    python ticket-classifier.py --file tickets.csv --output classified.csv
    python ticket-classifier.py --text "I was charged twice" --lang en
"""

import argparse
import csv
import json
import re
import sys
from typing import Optional


# Category definitions with Hebrew and English keywords
CATEGORIES = {
    'billing': {
        'name_he': 'חיוב',
        'name_en': 'Billing',
        'keywords_he': [
            'חיוב', 'חשבונית', 'תשלום', 'זיכוי', 'החזר כספי', 'חויב',
            'כרטיס אשראי', 'העברה בנקאית', 'PayPal', 'ביט', 'פייבוקס',
            'חיוב כפול', 'חיוב שגוי', 'סכום', 'מחיר', 'הנחה', 'קופון',
            'חשבון', 'יתרה', 'חוב', 'תשלומים',
        ],
        'keywords_en': [
            'charge', 'invoice', 'payment', 'refund', 'credit', 'billing',
            'credit card', 'overcharge', 'double charge', 'price', 'discount',
            'coupon', 'balance', 'debt', 'installment',
        ],
        'default_priority': 'medium',
    },
    'technical': {
        'name_he': 'תקלה טכנית',
        'name_en': 'Technical',
        'keywords_he': [
            'לא עובד', 'תקלה', 'באג', 'נתקע', 'שגיאה', 'קריסה',
            'איטי', 'נפל', 'לא נטען', 'מסך שחור', 'לא מגיב',
            'עדכון', 'גרסה', 'תאימות', 'אינטגרציה', 'API',
            'לא מתחבר', 'ניתוק', 'הודעת שגיאה',
        ],
        'keywords_en': [
            'not working', 'bug', 'error', 'crash', 'slow', 'down',
            'loading', 'black screen', 'unresponsive', 'update', 'version',
            'compatibility', 'integration', 'disconnect', 'error message',
        ],
        'default_priority': 'high',
    },
    'returns': {
        'name_he': 'החזרות',
        'name_en': 'Returns',
        'keywords_he': [
            'החזרה', 'החלפה', 'ביטול עסקה', 'תקופת צינון', 'ביטול',
            'להחזיר', 'רוצה להחליף', 'לא מתאים', 'לא כמו בתמונה',
            'פגום', 'שבור', 'לא שלם', 'חסר', 'הגנת הצרכן',
            'זכות ביטול', '14 ימים', 'אריזה מקורית',
        ],
        'keywords_en': [
            'return', 'exchange', 'cancel', 'cancellation', 'cooling off',
            'defective', 'broken', 'damaged', 'wrong item', 'missing',
            'consumer protection', '14 days', 'refund',
        ],
        'default_priority': 'high',
    },
    'complaints': {
        'name_he': 'תלונות',
        'name_en': 'Complaints',
        'keywords_he': [
            'תלונה', 'אי שביעות רצון', 'לא מקובל', 'דורש פיצוי',
            'מתלונן', 'גרוע', 'נורא', 'חוצפה', 'בושה', 'אכזבה',
            'עורך דין', 'בית משפט', 'תביעה', 'הרשות להגנת הצרכן',
            'פיצוי', 'נזק', 'הפליה', 'יחס מזלזל',
        ],
        'keywords_en': [
            'complaint', 'dissatisfied', 'unacceptable', 'compensation',
            'terrible', 'horrible', 'disgrace', 'lawyer', 'court',
            'sue', 'consumer authority', 'damage', 'discrimination',
        ],
        'default_priority': 'high',
    },
    'general': {
        'name_he': 'שאלה כללית',
        'name_en': 'General Inquiry',
        'keywords_he': [
            'מידע', 'שאלה', 'מחיר', 'שעות פעילות', 'זמינות',
            'כמה עולה', 'איפה', 'מתי', 'איך', 'האם אפשר',
            'קטלוג', 'מבצע', 'מלאי', 'סניף', 'כתובת',
        ],
        'keywords_en': [
            'information', 'question', 'price', 'hours', 'availability',
            'how much', 'where', 'when', 'how', 'catalog',
            'promotion', 'sale', 'stock', 'branch', 'address',
        ],
        'default_priority': 'low',
    },
    'account': {
        'name_he': 'חשבון',
        'name_en': 'Account',
        'keywords_he': [
            'סיסמה', 'כניסה', 'חשבון', 'הרשמה', 'מנוי',
            'שכחתי סיסמה', 'לא מצליח להיכנס', 'נחסם', 'אימות',
            'פרופיל', 'עדכון פרטים', 'מחיקת חשבון', 'דוא"ל',
            'שם משתמש', 'אבטחה', 'דו-שלבי',
        ],
        'keywords_en': [
            'password', 'login', 'account', 'register', 'subscription',
            'forgot password', 'locked', 'verification', 'profile',
            'update details', 'delete account', 'email', 'username',
            'security', 'two-factor',
        ],
        'default_priority': 'medium',
    },
    'shipping': {
        'name_he': 'משלוח',
        'name_en': 'Shipping',
        'keywords_he': [
            'משלוח', 'מעקב', 'חבילה', 'הגעה', 'כתובת',
            'לא הגיע', 'עיכוב', 'שליח', 'דואר', 'חבילה פגומה',
            'מספר מעקב', 'שינוי כתובת', 'איסוף', 'נקודת חלוקה',
        ],
        'keywords_en': [
            'shipping', 'tracking', 'package', 'delivery', 'address',
            'not arrived', 'delay', 'courier', 'mail', 'damaged package',
            'tracking number', 'address change', 'pickup', 'delivery point',
        ],
        'default_priority': 'medium',
    },
}

# Priority escalation keywords
PRIORITY_ESCALATION = {
    'critical': {
        'he': ['עורך דין', 'בית משפט', 'תביעה', 'הרשות להגנת הצרכן', 'משטרה', 'הונאה'],
        'en': ['lawyer', 'court', 'lawsuit', 'consumer authority', 'police', 'fraud'],
    },
    'high': {
        'he': ['דחוף', 'מיידי', 'חירום', 'פיצוי', 'נזק', 'פגום', 'שבור'],
        'en': ['urgent', 'immediate', 'emergency', 'compensation', 'damage', 'defective', 'broken'],
    },
}


def classify_ticket(
    text: str,
    lang: str = 'he',
    verbose: bool = False,
) -> dict:
    """Classify a support ticket by category and priority.

    Args:
        text: The ticket text to classify.
        lang: Language of the text ('he' for Hebrew, 'en' for English).
        verbose: If True, include matching details in the result.

    Returns:
        Dict with category, priority, confidence, and optional match details.
    """
    text_lower = text.lower() if lang == 'en' else text
    scores: dict[str, dict] = {}

    for cat_id, cat_data in CATEGORIES.items():
        keywords = cat_data[f'keywords_{lang}']
        matches = []
        score = 0

        for keyword in keywords:
            keyword_lower = keyword.lower() if lang == 'en' else keyword
            if keyword_lower in text_lower:
                matches.append(keyword)
                # Longer keyword matches are more specific and worth more
                score += len(keyword.split())

        scores[cat_id] = {
            'score': score,
            'matches': matches,
            'match_count': len(matches),
        }

    # Sort by score descending
    sorted_categories = sorted(
        scores.items(),
        key=lambda x: (x[1]['score'], x[1]['match_count']),
        reverse=True,
    )

    # Determine category
    if sorted_categories[0][1]['score'] > 0:
        best_cat_id = sorted_categories[0][0]
        best_cat_data = sorted_categories[0][1]
    else:
        best_cat_id = 'general'
        best_cat_data = scores['general']

    # Determine priority
    priority = CATEGORIES[best_cat_id]['default_priority']

    # Check for priority escalation keywords
    for prio_level in ['critical', 'high']:
        prio_keywords = PRIORITY_ESCALATION[prio_level][lang]
        for keyword in prio_keywords:
            keyword_check = keyword.lower() if lang == 'en' else keyword
            if keyword_check in text_lower:
                priority = prio_level
                break
        if priority == prio_level:
            break

    # Calculate confidence
    total_keywords = len(CATEGORIES[best_cat_id][f'keywords_{lang}'])
    if total_keywords > 0 and best_cat_data['match_count'] > 0:
        confidence = min(best_cat_data['match_count'] / 3.0, 1.0)
    else:
        confidence = 0.1

    result = {
        'category': best_cat_id,
        'category_name_he': CATEGORIES[best_cat_id]['name_he'],
        'category_name_en': CATEGORIES[best_cat_id]['name_en'],
        'priority': priority,
        'confidence': round(confidence, 2),
    }

    if verbose:
        result['matched_keywords'] = best_cat_data['matches']
        result['score'] = best_cat_data['score']
        result['all_scores'] = {
            k: {'score': v['score'], 'matches': v['matches']}
            for k, v in sorted_categories
            if v['score'] > 0
        }

    return result


def process_csv(
    input_file: str,
    output_file: str,
    text_column: str = 'text',
    lang: str = 'he',
) -> int:
    """Process a CSV file of tickets and classify each one.

    Args:
        input_file: Path to input CSV file.
        output_file: Path to output CSV file.
        text_column: Name of the column containing ticket text.
        lang: Language of the tickets.

    Returns:
        Number of tickets processed.
    """
    count = 0

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        if text_column not in reader.fieldnames:
            print(
                f'Error: Column "{text_column}" not found in CSV. '
                f'Available columns: {", ".join(reader.fieldnames)}',
                file=sys.stderr,
            )
            sys.exit(1)

        fieldnames = list(reader.fieldnames) + [
            'classified_category',
            'classified_category_he',
            'classified_priority',
            'classified_confidence',
        ]

        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                text = row.get(text_column, '')
                if not text:
                    continue

                result = classify_ticket(text, lang=lang)
                row['classified_category'] = result['category']
                row['classified_category_he'] = result['category_name_he']
                row['classified_priority'] = result['priority']
                row['classified_confidence'] = result['confidence']
                writer.writerow(row)
                count += 1

    return count


def main():
    parser = argparse.ArgumentParser(
        description='Classify Hebrew support tickets by category and priority.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Classify a single Hebrew ticket:
    %(prog)s --text "הכרטיס שלי חויב פעמיים, מבקש זיכוי" --lang he

  Classify with verbose output:
    %(prog)s --text "לא מצליח להיכנס לחשבון, שכחתי סיסמה" --lang he --verbose

  Classify an English ticket:
    %(prog)s --text "I was charged twice for my order" --lang en

  Batch classify from CSV:
    %(prog)s --file tickets.csv --output classified.csv --text-column ticket_text

  Show category list:
    %(prog)s --list-categories

Categories: billing, technical, returns, complaints, general, account, shipping
Priorities: critical, high, medium, low
        """,
    )

    # Input mode
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('--text', help='Single ticket text to classify')
    input_group.add_argument('--file', help='CSV file with tickets to classify')
    input_group.add_argument(
        '--list-categories',
        action='store_true',
        help='List all categories with their keywords',
    )

    # Options
    parser.add_argument(
        '--lang',
        choices=['he', 'en'],
        default='he',
        help='Language of the ticket text (default: he)',
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed matching information',
    )
    parser.add_argument(
        '--output',
        help='Output CSV file (required with --file)',
    )
    parser.add_argument(
        '--text-column',
        default='text',
        help='Column name containing ticket text in CSV (default: text)',
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format for single ticket (default: text)',
    )

    args = parser.parse_args()

    # List categories mode
    if args.list_categories:
        print('Available categories:')
        print()
        for cat_id, cat_data in CATEGORIES.items():
            print(f'  {cat_id}')
            print(f'    Hebrew: {cat_data["name_he"]}')
            print(f'    English: {cat_data["name_en"]}')
            print(f'    Default priority: {cat_data["default_priority"]}')
            print(f'    Hebrew keywords ({len(cat_data["keywords_he"])}): '
                  f'{", ".join(cat_data["keywords_he"][:5])}...')
            print(f'    English keywords ({len(cat_data["keywords_en"])}): '
                  f'{", ".join(cat_data["keywords_en"][:5])}...')
            print()
        sys.exit(0)

    # Single ticket mode
    if args.text:
        result = classify_ticket(args.text, lang=args.lang, verbose=args.verbose)

        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f'Category:    {result["category"]} ({result["category_name_he"]} / {result["category_name_en"]})')
            print(f'Priority:    {result["priority"]}')
            print(f'Confidence:  {result["confidence"]}')

            if args.verbose and 'matched_keywords' in result:
                print(f'Score:       {result["score"]}')
                print(f'Matched:     {", ".join(result["matched_keywords"])}')
                if result.get('all_scores'):
                    print('All scores:')
                    for cat, data in result['all_scores'].items():
                        print(f'  {cat}: score={data["score"]}, '
                              f'matches=[{", ".join(data["matches"])}]')

        sys.exit(0)

    # Batch CSV mode
    if args.file:
        if not args.output:
            parser.error('--file requires --output')

        try:
            count = process_csv(
                args.file,
                args.output,
                text_column=args.text_column,
                lang=args.lang,
            )
            print(f'Classified {count} tickets. Output: {args.output}')
        except FileNotFoundError:
            print(f'Error: File not found: {args.file}', file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f'Error: {e}', file=sys.stderr)
            sys.exit(1)

        sys.exit(0)

    # No input provided
    parser.print_help()
    sys.exit(1)


if __name__ == '__main__':
    main()
