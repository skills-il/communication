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
| Date of birth | NEVER | Age is a protected ground under s.2(א). Nothing bans a candidate from stating it, but volunteering it forfeits the s.9(ג) burden shift. See the section 21 applicability limits in `eeo-compliance-checklist.md`: none of this binds an employer of fewer than six employees |
| Photo | NEVER in EN | Market convention and bias avoidance, not a statutory rule. HE: only if user explicitly requests AND role is non-tech |
| Marital status | NEVER | Personal status is a protected ground under s.2(א). Same reasoning as date of birth |
| Military profile | NEVER | The employer may not lawfully demand it, or use it in the matters listed in s.2(א)(1) to (6) (s.2א), subject to the section 21 limits in `eeo-compliance-checklist.md`. Unit, role, rank and dates are fine |
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
בניתי, שחררתי, הובלתי, פיתחתי, העברתי, הקמתי, אוטומטתי, הקטנתי, שיפרתי, ניהלתי, חנכתי, תכננתי, שילבתי, ייעלתי, חיזקתי, שיכתבתי

**Rules:**
- 3-5 bullets per role maximum
- Each bullet on one line. If it wraps to two lines on the printed page, shorten it
- Past tense for past roles, present tense ONLY for current role
- Quantify at least 2 bullets per role (team size, % improvement, money saved, users affected)
- Avoid generic bullets ("worked on backend systems") that could apply to any engineer

## Military / National Service (if the candidate served)

Single block, 4-6 lines total.

```
{Unit Name / Type}                  {Role} ({Rank})
                                    {Start year} - {End year}

- {Transferable skill achieved}
- {Leadership or scale data if declassified}
```

**What may be written is not the candidate's judgment call.** It is governed by the
confidentiality undertaking (התחייבות לשמירת סודיות) signed at discharge and by the unit's
security officer (קצין ביטחון). For alumni of intelligence, special-operations and technology
units the unit name or even the role title can itself be the protected item. The safe default is
the corps name alone.

**Corps-level names, safe for anyone:**
- `Intelligence Corps` / `חיל המודיעין`
- `Armored Corps` / `שריון`
- `Air Force, technical` / `חיל האוויר - חימוש וטכני`
- `Golani Brigade` / `חטיבת גולני`
- `Combat Medic` / `חובש קרבי`

A specific unit, formation or role title may be named only where it already appears in official
public IDF material and the candidate's own undertaking permits it. When in any doubt, write the
corps name and tell the candidate to check with their קצין ביטחון.

**NEVER:**
- Invent unit numbers, formations or roles the candidate did not serve in
- Name a unit, system, operation, location or code name on the candidate's say-so alone
- List casualty counts or sensitive statistics

**If the candidate did not serve:**
Many Israeli citizens do not do military service, including Arab citizens, Haredi candidates,
and anyone with a medical or other exemption. Some did שירות לאומי or שירות אזרחי instead, which
is a real credential and belongs in this section under its own name. Otherwise omit the section
entirely. Never write "Did not serve" or "Exempt", and never explain the gap: the reason is
almost always a ground protected under s.2(א), and stating it invites exactly the inference the
section protects against. Replace with a "Volunteer / Community Service" section where the
candidate has equivalent experience.

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
| 4 | Experience (if any) | Education | Military / national (brief) |
| 5 | Projects / Open Source | Military / national | Education |
| 6 | Military / national | Skills | Skills |
| 7 | Skills | Languages | Languages |
| 8 | Languages | | |

Military moves up for seniors because it is usually shorter and tech HR skims past it to get to scale and leadership signals.
