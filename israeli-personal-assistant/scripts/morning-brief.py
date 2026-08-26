#!/usr/bin/env python3
"""
morning-brief.py

Generates a structured morning brief template for Israeli workdays.

- Fetches the Hebrew date for today (or a given date) from the HebCal API
- Lists upcoming Jewish holidays in the next 30 days
- Checks if today is a short day (Friday or Erev Chag)
- Prints a formatted brief template in both Hebrew and English
- Reminds about recurring business obligations (VAT, Bituach Leumi)

Usage:
    python3 morning-brief.py
    python3 morning-brief.py --date 2026-04-06
    python3 morning-brief.py --lang he
    python3 morning-brief.py --lang en
    python3 morning-brief.py --tasks "Follow up with Rivka, Send invoice 87"

Requirements:
    pip install requests

The script uses only the public HebCal API (https://www.hebcal.com) and
requires no API key or authentication.
"""

import argparse
import sys
from datetime import date, datetime, timedelta

try:
    import requests
except ImportError:
    print("Missing dependencies. Run: pip install requests python-dateutil")
    sys.exit(1)


HEBCAL_API = "https://www.hebcal.com/hebcal"
HEBREW_DAYS = {
    0: "יום שני",
    1: "יום שלישי",
    2: "יום רביעי",
    3: "יום חמישי",
    4: "יום שישי",
    5: "שבת",
    6: "יום ראשון",
}
ENGLISH_DAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

# Titles (Israel scheme) whose EVE is a genuine short day. Minor holidays such as
# Lag BaOmer, Tu BiShvat, Purim and the Chanukah nights are ordinary workdays, and
# treating their eve as a short day is wrong.
YOM_TOV_PREFIXES = (
    "Rosh Hashana",
    "Yom Kippur",
    "Sukkot I",
    "Shmini Atzeret",
    "Pesach I",
    "Pesach VII",
    "Shavuot",
)


# Observances that close Israeli business for the whole day, beyond the yom tov list.
FULL_SHUTDOWN_PREFIXES = ("Yom HaAtzma", "Yom Kippur")

# Iron Swords Memorial Day is fixed at 24 Tishrei but HebCal does NOT return it in
# any category, so it has to be carried here or it silently disappears from every
# brief. Dates are the Gregorian equivalents of 24 Tishrei, moved to Sunday
# 25 Tishrei when 24 Tishrei falls on Shabbat. Derive further years with the HebCal
# converter (hy=<year>&hm=Tishrei&hd=24&h2g=1), never by adding days to a prior year.
IRON_SWORDS_MEMORIAL_DAY = {
    date(2026, 10, 5): ("יום הזיכרון לחללי מלחמת חרבות ברזל", "Iron Swords Memorial Day"),
    date(2027, 10, 25): ("יום הזיכרון לחללי מלחמת חרבות ברזל", "Iron Swords Memorial Day"),
}


def is_yom_tov(title: str) -> bool:
    """True only for a full-shutdown yom tov in the Israeli scheme."""
    title = (title or "").strip()
    if "CH''M" in title or "CH’’M" in title or "Chol HaMoed" in title:
        return False
    return any(title.startswith(prefix) for prefix in YOM_TOV_PREFIXES)


# VAT bi-monthly reporting windows (month pairs and due month)
VAT_PERIODS = [
    {"months": [1, 2], "due_month": 3, "he": "דיווח מע\"מ: ינואר-פברואר", "en": "VAT report: January-February"},
    {"months": [3, 4], "due_month": 5, "he": "דיווח מע\"מ: מרץ-אפריל", "en": "VAT report: March-April"},
    {"months": [5, 6], "due_month": 7, "he": "דיווח מע\"מ: מאי-יוני", "en": "VAT report: May-June"},
    {"months": [7, 8], "due_month": 9, "he": "דיווח מע\"מ: יולי-אוגוסט", "en": "VAT report: July-August"},
    {"months": [9, 10], "due_month": 11, "he": "דיווח מע\"מ: ספטמבר-אוקטובר", "en": "VAT report: September-October"},
    {"months": [11, 12], "due_month": 1, "he": "דיווח מע\"מ: נובמבר-דצמבר", "en": "VAT report: November-December"},
]


def get_hebrew_date_string(target_date: date) -> str:
    """Fetch the Hebrew date string for a specific date via the HebCal converter."""
    try:
        response = requests.get(
            "https://www.hebcal.com/converter",
            params={
                "cfg": "json",
                "gy": target_date.year,
                "gm": target_date.month,
                "gd": target_date.day,
                "g2h": 1,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("hebrew", "")
    except requests.RequestException:
        return ""


def get_upcoming_holidays(target_date: date, days_ahead: int = 30) -> list:
    """Return Jewish holidays in the next `days_ahead` days."""
    end_date = target_date + timedelta(days=days_ahead)
    holidays = []

    # Fetch current and next month if needed
    months_to_fetch = {target_date.month}
    if end_date.month != target_date.month:
        months_to_fetch.add(end_date.month)

    for month in months_to_fetch:
        year = target_date.year if month >= target_date.month else target_date.year + 1
        params = {
            "v": 1,
            "cfg": "json",
            "maj": "on",       # major holidays
            "min": "on",       # minor holidays
            "mod": "on",       # modern/national observances
            "nx": "off",       # no Rosh Chodesh
            "mf": "on",        # minor fasts (Tzom Gedaliah, Tisha B'Av and the rest)
            "i": "on",         # ISRAEL scheme: one yom tov per holiday, not the diaspora two
            "year": year,
            "month": month,
        }
        # Deliberately no "lg" override: the default response carries an English
        # "title" AND a Hebrew "hebrew" field, so each brief can use its own language.
        try:
            response = requests.get(HEBCAL_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            continue

        for item in data.get("items", []):
            item_date_str = item.get("date", "")
            if not item_date_str:
                continue
            try:
                item_date = datetime.strptime(item_date_str[:10], "%Y-%m-%d").date()
            except ValueError:
                continue
            if target_date <= item_date <= end_date:
                category = item.get("category", "")
                if category in ("holiday", "modern", "fast"):
                    holidays.append(
                        {
                            "date": item_date,
                            "title": item.get("title", ""),
                            "hebrew": item.get("hebrew", ""),
                            "category": category,
                        }
                    )

    # HebCal does not carry Iron Swords Memorial Day in any category, so add it here.
    for observance_date, (title_he, title_en) in IRON_SWORDS_MEMORIAL_DAY.items():
        if target_date <= observance_date <= end_date:
            holidays.append(
                {
                    "date": observance_date,
                    "title": title_en,
                    "hebrew": title_he,
                    "category": "modern",
                }
            )

    return sorted(holidays, key=lambda x: x["date"])


def check_shutdown_today(target_date: date, holidays: list) -> tuple:
    """
    Returns (is_shutdown, reason_he, reason_en) for a day on which Israeli business
    does not operate at all: Shabbat, a yom tov, Yom Kippur or Yom HaAtzmaut.

    This is separate from check_short_day(), which answers the EVE question. Without
    it the brief renders Yom Kippur as an ordinary Monday and still prints action
    reminders on it.
    """
    if target_date.weekday() == 5:  # Saturday
        for holiday in holidays:
            if holiday["date"] == target_date and is_yom_tov(holiday["title"]):
                title = holiday.get("hebrew") or holiday["title"]
                return (True, f"שבת ו{title} (סגירה מוחלטת)", f"Shabbat and {holiday['title']} (full shutdown)")
        return (True, "שבת (אין פעילות עסקית)", "Shabbat (no business activity)")

    for holiday in holidays:
        if holiday["date"] != target_date:
            continue
        title_en = holiday["title"]
        if is_yom_tov(title_en) or title_en.startswith(FULL_SHUTDOWN_PREFIXES):
            title = holiday.get("hebrew") or title_en
            return (True, f"{title} (סגירה מוחלטת)", f"{title_en} (full shutdown)")

    return (False, "", "")


def check_short_day(target_date: date, holidays: list) -> tuple:
    """
    Returns (is_short_day, reason_he, reason_en).
    A short day is Friday or any Erev Chag (eve of a major holiday).
    """
    weekday = target_date.weekday()

    if weekday == 4:  # Friday
        return (True, "יום שישי (יום קצר, עד 13:00 בערך)", "Friday (short day, until ~13:00)")

    # Check if tomorrow is a full-shutdown yom tov (Erev Chag). Minor holidays do
    # not shorten the working day, so their eves must not be flagged.
    tomorrow = target_date + timedelta(days=1)
    for holiday in holidays:
        if holiday["date"] == tomorrow and is_yom_tov(holiday["title"]):
            title_he = holiday.get("hebrew", holiday["title"])
            title_en = holiday["title"]
            return (
                True,
                f"ערב {title_he} (יום קצר)",
                f"Erev {title_en} (short day)",
            )

    return (False, "", "")


def get_vat_reminder(target_date: date) -> tuple:
    """Returns (he_reminder, en_reminder) if we are within 7 days of a VAT deadline, else empty strings."""
    month = target_date.month
    day = target_date.day

    for period in VAT_PERIODS:
        if period["due_month"] == month and 8 <= day <= 19:
            return (
                f"חלון דיווח מע\"מ פתוח! {period['he']} - עד ה-15, ובדיווח מקוון עד ה-19 בשעה 18:30"
                " (למדווחים דו-חודשי בלבד; מדווח חודשי מגיש כל חודש, ולעוסק פטור אין דיווח מע\"מ תקופתי)",
                f"VAT filing window open! {period['en']} - due by the 15th, or the 19th at 18:30 when filing online"
                " (bi-monthly filers only; monthly filers report every month, and an osek patur has no periodic VAT report)",
            )

    return ("", "")


def get_bituach_leumi_reminder(target_date: date) -> tuple:
    """
    Returns reminder strings in the run-up to the Bituach Leumi standing-order debit.

    Self-employed contributions are paid on the schedule of the payment vouchers
    Bituach Leumi sends; a standing-order bank debit is taken on the 22nd for the
    PREVIOUS month, and the date shifts around Shabbat and holidays. It is not the 15th.
    """
    day = target_date.day
    if 15 <= day <= 22:
        return (
            "ביטוח לאומי לעצמאי - חיוב הוראת הקבע ב-22 בחודש, עבור החודש הקודם",
            "Bituach Leumi (self-employed) - standing-order debit on the 22nd, for the previous month",
        )
    return ("", "")


def format_date_he(d: date) -> str:
    """Format a date in Israeli format: DD.MM.YYYY"""
    return d.strftime("%d.%m.%Y")


def parse_tasks(tasks_arg: str) -> list:
    """Split a comma-separated task string into a list."""
    if not tasks_arg:
        return []
    return [t.strip() for t in tasks_arg.split(",") if t.strip()]


def build_brief_he(
    target_date: date,
    hebrew_date: str,
    day_name_he: str,
    is_shutdown: bool,
    shutdown_reason_he: str,
    is_short_day: bool,
    short_day_reason_he: str,
    holidays: list,
    vat_reminder: str,
    bl_reminder: str,
    tasks: list,
) -> str:
    lines = []
    lines.append("=" * 50)
    lines.append("סיכום בוקר")
    lines.append("=" * 50)
    lines.append(f"תאריך: {day_name_he}, {format_date_he(target_date)}")
    if hebrew_date:
        lines.append(f"תאריך עברי: {hebrew_date}")
    lines.append("")

    if is_shutdown:
        lines.append(f"[!!] {shutdown_reason_he}")
        lines.append("אין לקבוע פגישות, דדליינים או משלוחים ביום הזה.")
        lines.append("")
    elif is_short_day:
        lines.append(f"[!] שים לב: {short_day_reason_he}")
        lines.append("")

    if holidays:
        lines.append("חגים קרובים (30 הימים הבאים):")
        for h in holidays:
            title = h.get("hebrew") or h["title"]
            lines.append(f"  - {format_date_he(h['date'])}: {title}")
        lines.append("")

    reminders = []
    if not is_shutdown:
        if vat_reminder:
            reminders.append(vat_reminder)
        if bl_reminder:
            reminders.append(bl_reminder)

    if reminders:
        lines.append("תזכורות חובה עסקיות:")
        for r in reminders:
            lines.append(f"  - {r}")
        lines.append("")

    lines.append("משימות פתוחות:")
    if tasks:
        for t in tasks:
            lines.append(f"  [ ] {t}")
    else:
        lines.append("  [ ] הוסיפו משימות עם --tasks \"משימה 1, משימה 2\"")
    lines.append("")

    lines.append("דדליינים קרובים:")
    lines.append("  [ ] הוסיפו דדליינים ידנית")
    lines.append("")

    lines.append("=" * 50)
    return "\n".join(lines)


def build_brief_en(
    target_date: date,
    hebrew_date: str,
    day_name_en: str,
    is_shutdown: bool,
    shutdown_reason_en: str,
    is_short_day: bool,
    short_day_reason_en: str,
    holidays: list,
    vat_reminder: str,
    bl_reminder: str,
    tasks: list,
) -> str:
    lines = []
    lines.append("=" * 50)
    lines.append("Morning Brief")
    lines.append("=" * 50)
    lines.append(f"Date: {day_name_en}, {format_date_he(target_date)}")
    if hebrew_date:
        lines.append(f"Hebrew date: {hebrew_date}")
    lines.append("")

    if is_shutdown:
        lines.append(f"[!!] {shutdown_reason_en}")
        lines.append("Do not schedule meetings, deadlines or deliveries on this day.")
        lines.append("")
    elif is_short_day:
        lines.append(f"[!] Note: {short_day_reason_en}")
        lines.append("")

    if holidays:
        lines.append("Upcoming holidays (next 30 days):")
        for h in holidays:
            lines.append(f"  - {format_date_he(h['date'])}: {h['title']}")
        lines.append("")

    reminders = []
    if not is_shutdown:
        if vat_reminder:
            reminders.append(vat_reminder)
        if bl_reminder:
            reminders.append(bl_reminder)

    if reminders:
        lines.append("Business obligation reminders:")
        for r in reminders:
            lines.append(f"  - {r}")
        lines.append("")

    lines.append("Open tasks:")
    if tasks:
        for t in tasks:
            lines.append(f"  [ ] {t}")
    else:
        lines.append("  [ ] Add tasks with --tasks \"Task 1, Task 2\"")
    lines.append("")

    lines.append("Upcoming deadlines:")
    lines.append("  [ ] Add deadlines manually")
    lines.append("")

    lines.append("=" * 50)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate an Israeli morning brief with Hebrew date and upcoming holidays."
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--lang",
        choices=["he", "en", "both"],
        default="both",
        help="Output language: he, en, or both (default: both)",
    )
    parser.add_argument(
        "--tasks",
        type=str,
        default="",
        help="Comma-separated list of open tasks to include in the brief",
    )
    args = parser.parse_args()

    # Resolve target date
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print(f"Invalid date format: {args.date}. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        target_date = date.today()

    weekday = target_date.weekday()
    day_name_he = HEBREW_DAYS[weekday]
    day_name_en = ENGLISH_DAYS[weekday]

    print(f"Fetching Hebrew date for {target_date}...")
    hebrew_date = get_hebrew_date_string(target_date)

    print("Fetching upcoming holidays...")
    holidays = get_upcoming_holidays(target_date, days_ahead=30)

    is_shutdown, shutdown_reason_he, shutdown_reason_en = check_shutdown_today(
        target_date, holidays
    )
    is_short_day, short_day_reason_he, short_day_reason_en = check_short_day(
        target_date, holidays
    )

    vat_he, vat_en = get_vat_reminder(target_date)
    bl_he, bl_en = get_bituach_leumi_reminder(target_date)

    tasks = parse_tasks(args.tasks)

    print()

    if args.lang in ("he", "both"):
        print(
            build_brief_he(
                target_date,
                hebrew_date,
                day_name_he,
                is_shutdown,
                shutdown_reason_he,
                is_short_day,
                short_day_reason_he,
                holidays,
                vat_he,
                bl_he,
                tasks,
            )
        )

    if args.lang == "both":
        print()

    if args.lang in ("en", "both"):
        print(
            build_brief_en(
                target_date,
                hebrew_date,
                day_name_en,
                is_shutdown,
                shutdown_reason_en,
                is_short_day,
                short_day_reason_en,
                holidays,
                vat_en,
                bl_en,
                tasks,
            )
        )


if __name__ == "__main__":
    main()
