# Domain Checklist: israeli-personal-assistant

Scope: a judgment/knowledge layer for Israeli daily life and work (calendar, Hebrew communication norms, business-obligation reminders). NOT live API integration. Category: communication.

## Must cover (core)

- **Israeli work week** Sunday-Thursday; Friday short day (cutoff ~13:00); Saturday no business; Erev Chag follows the Friday rule.
- **Jewish holidays in Israel** (one yom tov per holiday, not the diaspora two-day pattern): Yom Kippur, Rosh Hashana, Sukkot + Chol HaMoed + Shmini Atzeret/Simchat Torah (combined), Pesach + Chol HaMoed, Shavuot, Purim. Current-cycle Gregorian dates, with the explicit reminder that dates shift each year (fetch from HebCal).
- **National observances** (working days, cultural weight): Yom HaShoah, Yom HaZikaron, Yom HaAtzmaut, Yom Yerushalayim, Iron Swords Memorial Day (24 Tishrei, Knesset 2024).
- **Recurring business obligations**: VAT reporting/payment (15th of following month; bi-monthly up to the turnover threshold, monthly above), Bituach Leumi + income-tax advances (15th monthly), annual return (spring), 102 employer reports (February).
- **Invoicing change (2024-2026)**: חשבוניות ישראל allocation-number regime and its stepping threshold.
- **VAT rate** current value.
- **Hebrew communication norms**: directness, anti-patterns (archaic/over-formal/passive), tone per channel, opener conventions.
- **Israeli formatting**: DD/MM/YYYY dates, ₪ symbol-first, phone formats, ת.ז./ח.פ. 9 digits, 7-digit postcode.
- **Scheduling intelligence**: Shabbat/Erev-Chag cutoffs, Chol HaMoed reduced availability, August vacation, observance sensitivity.

## Should cover (advanced)

- Hebrew date alongside Gregorian in the morning brief; HebCal API for date conversion.
- Invoice follow-up cadence templates.
- Seasonal business patterns by quarter.
- Pairing pointers to live-integration skills (shabbat-aware-scheduler, gws-hebrew-email-automation).

## Out of scope (explicit)

- Live calendar API integration / event creation (shabbat-aware-scheduler).
- Automated email sending (gws-hebrew-email-automation).
- VAT/income-tax/payroll calculation (accounting skills).
- Legal document drafting (legal-tech skills).

## Authoritative sources

- HebCal (holiday dates, Hebrew date conversion, i=on for Israel).
- Israel Tax Authority / gov.il (VAT rate, reporting cycle threshold, allocation-number regime, deadlines).
- Bituach Leumi (btl.gov.il) advance-payment dates.
