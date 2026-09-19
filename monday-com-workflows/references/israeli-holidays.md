# Israeli Holiday Calendar for Sprint Planning

A sprint planner needs three states per date, not two:

| State | Meaning | Which days |
|-------|---------|------------|
| `off` | Statutory day of rest. No work, automations should not fire. | The fixed rest days in section 18A of the Law and Administration Ordinance: both days of Rosh Hashana, Yom Kippur, the first day of Sukkot and Shemini Atzeret, the first and seventh days of Pesach, and Shavuot. Plus Yom Ha'Atzmaut, which the Independence Day Law makes a "יום שבתון". |
| `half` | Erev chag. Many workplaces finish early; plan reduced capacity. | Erev Rosh Hashana, Erev Yom Kippur, Erev Sukkot, Erev Pesach, Erev Shavuot. |
| `policy` | A working day by law, but teams differ. The team lead decides. | Chol hamoed Sukkot and Pesach, Purim, Tisha B'Av, Hanukkah, Yom HaShoah, Yom HaZikaron. |

Ask the team how they treat `policy` days before freezing anything. Freezing all of Hanukkah removes a full working week from a sprint.

Dates below are the Israel schedule (one-day Yom Tov), taken from hebcal with `i=on`, for 2026 through 2028. Never use the Diaspora two-day dates: they mark a working day as a holiday. When a year is missing, fetch it from `https://www.hebcal.com/hebcal?v=1&cfg=json&year=<YEAR>&i=on&maj=on&min=on&mod=on` rather than guessing.

```python
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

def israel_today() -> date:
    """Today's date in Israel. A job on a UTC server that calls date.today()
    sees the previous date for 2-3 hours after Israeli midnight."""
    return datetime.now(ZoneInfo("Asia/Jerusalem")).date()

# (start, end, name, state). Israel schedule, verified against hebcal i=on.
ISRAELI_CALENDAR = {
    2026: [
        ("2026-03-03", "2026-03-03", "Purim", "policy"),
        ("2026-04-01", "2026-04-01", "Erev Pesach", "half"),
        ("2026-04-02", "2026-04-02", "Pesach I", "off"),
        ("2026-04-03", "2026-04-07", "Chol HaMoed Pesach", "policy"),
        ("2026-04-08", "2026-04-08", "Pesach VII", "off"),
        ("2026-04-14", "2026-04-14", "Yom HaShoah", "policy"),
        ("2026-04-21", "2026-04-21", "Yom HaZikaron", "policy"),
        ("2026-04-22", "2026-04-22", "Yom Ha'Atzmaut", "off"),
        ("2026-05-21", "2026-05-21", "Erev Shavuot", "half"),
        ("2026-05-22", "2026-05-22", "Shavuot", "off"),
        ("2026-07-23", "2026-07-23", "Tisha B'Av", "policy"),
        ("2026-09-11", "2026-09-11", "Erev Rosh Hashana", "half"),
        ("2026-09-12", "2026-09-13", "Rosh Hashana", "off"),
        ("2026-09-20", "2026-09-20", "Erev Yom Kippur", "half"),
        ("2026-09-21", "2026-09-21", "Yom Kippur", "off"),
        ("2026-09-25", "2026-09-25", "Erev Sukkot", "half"),
        ("2026-09-26", "2026-09-26", "Sukkot I", "off"),
        ("2026-09-27", "2026-10-02", "Chol HaMoed Sukkot", "policy"),
        ("2026-10-03", "2026-10-03", "Shemini Atzeret", "off"),
        ("2026-12-05", "2026-12-12", "Hanukkah", "policy"),
    ],
    2027: [
        ("2027-03-23", "2027-03-23", "Purim", "policy"),
        ("2027-04-21", "2027-04-21", "Erev Pesach", "half"),
        ("2027-04-22", "2027-04-22", "Pesach I", "off"),
        ("2027-04-23", "2027-04-27", "Chol HaMoed Pesach", "policy"),
        ("2027-04-28", "2027-04-28", "Pesach VII", "off"),
        ("2027-05-04", "2027-05-04", "Yom HaShoah", "policy"),
        ("2027-05-11", "2027-05-11", "Yom HaZikaron", "policy"),
        ("2027-05-12", "2027-05-12", "Yom Ha'Atzmaut", "off"),
        ("2027-06-10", "2027-06-10", "Erev Shavuot", "half"),
        ("2027-06-11", "2027-06-11", "Shavuot", "off"),
        ("2027-08-12", "2027-08-12", "Tisha B'Av", "policy"),
        ("2027-10-01", "2027-10-01", "Erev Rosh Hashana", "half"),
        ("2027-10-02", "2027-10-03", "Rosh Hashana", "off"),
        ("2027-10-10", "2027-10-10", "Erev Yom Kippur", "half"),
        ("2027-10-11", "2027-10-11", "Yom Kippur", "off"),
        ("2027-10-15", "2027-10-15", "Erev Sukkot", "half"),
        ("2027-10-16", "2027-10-16", "Sukkot I", "off"),
        ("2027-10-17", "2027-10-22", "Chol HaMoed Sukkot", "policy"),
        ("2027-10-23", "2027-10-23", "Shemini Atzeret", "off"),
        ("2027-12-25", "2027-12-31", "Hanukkah", "policy"),  # continues to 2028-01-01
    ],
    2028: [
        ("2028-01-01", "2028-01-01", "Hanukkah", "policy"),
        ("2028-03-12", "2028-03-12", "Purim", "policy"),
        ("2028-04-10", "2028-04-10", "Erev Pesach", "half"),
        ("2028-04-11", "2028-04-11", "Pesach I", "off"),
        ("2028-04-12", "2028-04-16", "Chol HaMoed Pesach", "policy"),
        ("2028-04-17", "2028-04-17", "Pesach VII", "off"),
        ("2028-04-24", "2028-04-24", "Yom HaShoah", "policy"),
        ("2028-05-01", "2028-05-01", "Yom HaZikaron", "policy"),
        ("2028-05-02", "2028-05-02", "Yom Ha'Atzmaut", "off"),
        ("2028-05-30", "2028-05-30", "Erev Shavuot", "half"),
        ("2028-05-31", "2028-05-31", "Shavuot", "off"),
        ("2028-08-01", "2028-08-01", "Tisha B'Av", "policy"),
        ("2028-09-20", "2028-09-20", "Erev Rosh Hashana", "half"),
        ("2028-09-21", "2028-09-22", "Rosh Hashana", "off"),
        ("2028-09-29", "2028-09-29", "Erev Yom Kippur", "half"),
        ("2028-09-30", "2028-09-30", "Yom Kippur", "off"),
        ("2028-10-04", "2028-10-04", "Erev Sukkot", "half"),
        ("2028-10-05", "2028-10-05", "Sukkot I", "off"),
        ("2028-10-06", "2028-10-11", "Chol HaMoed Sukkot", "policy"),
        ("2028-10-12", "2028-10-12", "Shemini Atzeret", "off"),
        ("2028-12-13", "2028-12-20", "Hanukkah", "policy"),
    ],
}

def holiday_state(day: date) -> tuple[str, str]:
    """Return (state, name): state is 'off', 'half', 'policy' or 'work'.
    Raises for a year that is not in the table instead of silently
    answering 'work' for every date, which is the failure that matters."""
    rows = ISRAELI_CALENDAR.get(day.year)
    if rows is None:
        raise ValueError(f"No Israeli calendar for {day.year}; add it from hebcal (i=on)")
    for start, end, name, state in rows:
        if date.fromisoformat(start) <= day <= date.fromisoformat(end):
            return state, name
    return "work", ""

def sprint_capacity(start: date, workdays: int = 5, policy_as: float = 1.0,
                    weekend: tuple = (4, 5)) -> float:
    """Capacity of a sprint of `workdays` working days starting at `start`
    (any weekday). Friday and Saturday are skipped by default (weekday 4, 5);
    pass weekend=(5,) for a team that works Fridays.
    off = 0, half = 0.5, policy = policy_as (team choice), work = 1."""
    weights = {"off": 0.0, "half": 0.5, "work": 1.0, "policy": policy_as}
    total, counted, day = 0.0, 0, start
    while counted < workdays:
        if day.weekday() not in weekend:
            total += weights[holiday_state(day)[0]]
            counted += 1
        day += timedelta(days=1)
    return total
```

Notes:

- Erev chag that falls on Friday or Saturday does not reduce a Sunday-Thursday sprint. In 2026 Erev Yom Kippur falls on a Sunday, the first day of the sprint week. In 2027 so does Erev Yom Kippur (10 October).
- Hanukkah dates above are the eight days (the first candle is lit the evening before the first date). Hanukkah 2027 runs into 1 January 2028.
- Jerusalem observes Shushan Purim, the day after Purim (2026-03-04, 2027-03-24, 2028-03-13), not Purim. For a Jerusalem team, move the Purim row one day later.
- Use `israel_today()`, not `date.today()`, in any scheduled job: the server clock is usually UTC.
- monday's native recurring automations ("every Sunday at 09:00") cannot consult this table. To skip a holiday, run the schedule from your own job: check `holiday_state(israel_today())` first, then call the API.
