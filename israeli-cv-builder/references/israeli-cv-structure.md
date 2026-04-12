# Israeli CV Structure Reference

Full section-by-section template for an Israeli CV with field-level notes. Applies to both Hebrew and English, RTL/LTR layout varies.

## Header Block

| Field | Include? | Notes |
|-------|----------|-------|
| Full name | Required | H1, largest text on the page |
| City | Required | Just city name. No street. Tel Aviv, Herzliya, Haifa, Petah Tikva, Be'er Sheva, Jerusalem, Remote |
| Phone | Required | EN: `+972-50-123-4567`. HE: `050-123-4567` |
| Email | Required | Personal email, not work email. Gmail preferred for professional tone |
| LinkedIn | Recommended | Full URL `linkedin.com/in/username`, not just "LinkedIn" |
| GitHub | Tech roles | Full URL. Only include if the profile is active and presentable |
| Personal website | Optional | Only if it hosts a portfolio worth seeing |
| Date of birth | NEVER | Prohibited by EEO Law 1988 |
| Photo | NEVER in EN | HE: only if user explicitly requests AND role is non-tech |
| Marital status | NEVER | Prohibited |
| ID number | NEVER | Privacy risk |

## Professional Summary

3-4 lines. Written in third person or no-person (no "I"). Must contain:
- Years of experience in the target domain
- 2-3 core strengths with domain keywords
- 1 standout data point (scale managed, team size, product impact)

**English example:**
> Backend engineer with 6 years building payment systems at fintech startups. Owned Stripe and Tranzila integrations at Scale of 1M+ monthly transactions. Focus on Go, Postgres, and event-driven architectures on AWS.

**Hebrew example:**
> מהנדס/ת backend עם 6 שנות ניסיון בבניית מערכות תשלומים בסטארטאפים פינטק. הובלתי אינטגרציות Stripe ו-Tranzila בסקיילים של מיליון+ טרנזקציות בחודש. התמחות ב-Go, Postgres וארכיטקטורות אירועים על AWS.

## Work Experience

Reverse chronological. Most recent on top.

**Per role block:**

```
{Company Name}        {Role}
{City}                {Start} - {End or Present}

- {Action verb} {what} {quantified result}
- {Action verb} {what} {quantified result}
- {Action verb} {what} {quantified result}
```

**Action verb bank (English):**
Built, launched, shipped, migrated, owned, scaled, automated, reduced, improved, led, mentored, architected, designed, debugged, rolled out, open-sourced, integrated, optimized, hardened, ported, refactored

**Action verb bank (Hebrew):**
בניתי, שחררתי, הובלתי, פיתחתי, העברתי, הקמתי, אוטמתתי, הקטנתי, שיפרתי, ניהלתי, חנכתי, תכננתי, אינטגרציה, ייעלתי, חיזקתי, שיכתבתי

**Rules:**
- 3-5 bullets per role maximum
- Each bullet on one line. If it wraps to two lines on the printed page, shorten it
- Past tense for past roles, present tense ONLY for current role
- Quantify at least 2 bullets per role (team size, % improvement, NIS saved, users affected)
- Avoid generic bullets ("worked on backend systems") that could apply to any engineer

## Military Service (Israeli citizens)

Single block, 4-6 lines total.

```
{Unit Name / Type}                  {Role} ({Rank})
                                    {Start year} - {End year}

- {Transferable skill achieved}
- {Leadership or scale data if declassified}
```

**Unit name examples:**
- `8200 Intelligence Unit` / `מודיעין - יחידה 8200`
- `Sayeret Matkal` / `סיירת מטכ"ל`
- `Golani Brigade` / `חטיבת גולני`
- `Air Force Ground Crew` / `חיל האוויר - חימוש וטכני`
- `Armored Corps, 7th Brigade` / `שריון - חטיבה 7`
- `Intelligence Corps` / `חיל המודיעין` (use when specific unit is classified)
- `Combat Medic` / `חובש קרבי`

**NEVER:**
- Invent unit numbers you did not serve in
- Include specific classified operations or code names
- List casualty counts or sensitive statistics

**If oleh chadash / did not serve:**
Omit the section entirely. Do not write "Did not serve" or "Exempt". Replace with a "Volunteer / Community Service" section if the candidate has equivalent experience.

## Education

```
{Institution Name}                   {Degree, Major}
{City}                               {Graduation Year}
- {Honor or thesis if relevant}
```

**Honors:**
- English: `cum laude`, `magna cum laude`, `summa cum laude`
- Hebrew: `בהצטיינות`, `בהצטיינות יתרה`

**Place education:**
- Below work experience if you have 2+ years of work
- Above work experience if you are a student or recent grad (< 1 year post-degree)

## Skills (Tech Roles)

Grouped by category, not alphabetical. Order within each group: by depth and recency.

```
Languages: Go, Python, TypeScript, Rust
Frameworks: React, Next.js, NestJS, FastAPI
Data: Postgres, Redis, Kafka, ClickHouse
Infrastructure: AWS, Docker, Kubernetes, Terraform, GitHub Actions
Tools: Git, Datadog, Sentry, PagerDuty
```

**Rules:**
- Do not list skills you could not answer 3 questions about in an interview
- Do not pad with obvious skills ("Microsoft Word") unless the role specifically asks
- Group Hebrew CV skills the same way, keep English technology names in English

## Languages

```
Hebrew: Native
English: Fluent (TOEFL 110)
Russian: Basic
```

Proficiency levels (from top to bottom):
- Native / שפת אם
- Fluent / רהוטה
- Professional working / מקצועית
- Conversational / שיחתית
- Basic / בסיסית

Only list additional languages (beyond Hebrew and English) if at Professional or above. Basic French does not help on a tech CV.

## Section Order Summary

| Order | Junior (0-2 yrs) | Mid (3-7 yrs) | Senior (8+ yrs) |
|-------|------------------|----------------|------------------|
| 1 | Header | Header | Header |
| 2 | Summary | Summary | Summary |
| 3 | Education | Experience | Experience |
| 4 | Experience (if any) | Education | Military (brief) |
| 5 | Projects / Open Source | Military | Education |
| 6 | Military | Skills | Skills |
| 7 | Skills | Languages | Languages |
| 8 | Languages | | |

Military moves up for seniors because it is usually shorter and tech HR skims past it to get to scale and leadership signals.
