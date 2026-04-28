---
name: israeli-hr-recruitment-automator
description: Employer-side hiring automation for Israeli companies. Generates Hebrew job descriptions compliant with the Equal Employment Opportunities Law 1988, posts to Israeli job boards (AllJobs, Drushim, JobMaster, LinkedIn Israel), screens resumes with Israeli context (military service, academic institutions, tech bootcamps), schedules interviews around Israeli holidays and Shabbat, and generates offer letters with mandatory Israeli employment clauses. Use when user asks to "write a job description", "post a job in Israel", "screen Israeli resumes", "pirsum misra", "srikat meumadim", "michtav ha'a'sa'a", or automate hiring workflows for Israeli companies. Ensures compliance with Israeli anti-discrimination law and mandatory benefits. Do NOT use for job searching (use israeli-job-market), interview preparation (use israeli-tech-interview-prep), salary negotiation (use israeli-tech-salary-negotiator), employment contracts legal review (use israeli-employment-contracts), or freelancer hiring.
license: MIT
allowed-tools: Bash(python:*)
compatibility: No network required for job description generation and offer letter drafting. Python 3.9+ required for helper scripts. Works with Claude Code, Claude.ai, Cursor.
---

# Israeli HR Recruitment Automator

## Instructions

### Step 1: Generate Compliant Hebrew Job Descriptions

When the user needs to create a job posting, generate a Hebrew job description (teur misra) that complies with the Equal Employment Opportunities Law 1988 (chok shivyon hizdamnuyot ba'avoda).

**Anti-discrimination compliance checklist.** The job description MUST NOT:

| Prohibited Criterion | Law Reference | Example of Violation |
|---|---|---|
| Gender | Section 2(a) | "Looking for a male developer" |
| Age | Section 2(a) | "Ages 25-35 only" |
| Marital/parental status | Section 2(a) | "Single candidates preferred" |
| Pregnancy | Section 2(a) | "Not suitable for pregnant women" |
| Sexual orientation | Section 2(a) | Any reference to orientation |
| Ethnicity/nationality | Section 2(a) | "Jewish/Arab candidates only" |
| Country of origin | Section 2(a) | "Born in Israel" |
| Religion | Section 2(a) | "Sabbath-observant only" |
| Political views | Section 2(a) | Any party affiliation requirement |
| Reserve duty | Section 2(a) | "No miluim obligations" |
| Appearance | Section 2(a) | Height, weight, attractiveness requirements |

**Permitted requirements:**
- Genuine occupational qualifications (e.g., Hebrew fluency for a Hebrew content role)
- Security clearance where legally required
- Specific professional certifications or licenses
- Physical fitness requirements tied directly to job duties

**Job description structure (Hebrew template):**

```
כותרת המשרה: [Title]
חברה: [Company name]
מיקום: [Location]
סוג משרה: [Full-time/Part-time/Hybrid]
תחום: [Field]

תיאור התפקיד:
[2-3 paragraphs about the role, team, and company]

דרישות התפקיד:
- [Requirement 1]
- [Requirement 2]

דרישות רצויות (יתרון):
- [Nice-to-have 1]

מה אנחנו מציעים:
- [Benefit 1]
- [Benefit 2]

להגשת מועמדות: [Application instructions]
```

**Key rules:**
- Use gender-neutral language. In Hebrew, use both masculine and feminine forms: "מפתח/ת", "מנהל/ת" or the inclusive plural form
- List "requirements" vs "nice-to-haves" (yitron) separately to avoid discouraging qualified candidates
- Never list age, military unit, or academic institution as a requirement unless it is a genuine occupational qualification
- Include salary range when possible (not legally required but considered best practice)

Consult `references/anti-discrimination-law.md` for the full legal summary.

### Step 2: Post to Israeli Job Boards

After generating the job description, help the user post to Israeli job boards.

**Major Israeli job boards (2026):**

| Platform | URL | API Available | Notes |
|---|---|---|---|
| AllJobs | alljobs.co.il | Yes (employer portal) | Largest Israeli job board, supports Hebrew postings |
| Drushim | drushim.co.il | Yes (employer API) | Strong in tech and startup roles |
| JobMaster | jobmaster.co.il | Limited | General job board |
| LinkedIn Israel | linkedin.com | Yes (LinkedIn API) | International and tech roles, English-friendly |
| Glassdoor Israel | glassdoor.co.il | Via Indeed API | Review-focused, salary transparency |
| Comeet | comeet.com | Yes | Israeli ATS with job board distribution |
| Gethired | gethired.co.il | No | Tech-focused Israeli board |

**Posting workflow:**
1. Adapt the Hebrew job description for each platform's format and character limits
2. For AllJobs: use their structured fields (category, sub-category, region, city)
3. For LinkedIn: create both Hebrew and English versions
4. Set appropriate filters: experience level, job type (misra mle'a / chalkeet), location
5. Track posting IDs for each platform to monitor applications

**Posting tips:**
- AllJobs and Drushim have peak traffic Sunday-Tuesday
- Post by 9:00 AM Israel time for maximum visibility
- Refresh listings every 7-10 days (most boards penalize stale postings)
- Use AllJobs "hot job" promotion for urgent positions

### Step 3: Screen Resumes with Israeli Context

When screening resumes (korot chaim), apply Israeli-specific context to evaluate candidates fairly and accurately.

**Military service (sherut tzva'i) interpretation:**

| Service Type | Typical Duration | What It Indicates |
|---|---|---|
| Combat (kravi) | 32-36 months | Leadership, teamwork, physical resilience |
| Intelligence (modi'in) | 32-36 months | Analytical skills, security clearance |
| Technology (8200, 81, Mamram) | 32-36 months | Technical skills, strong tech foundation |
| Officers (ktzinim) | 36+ months | Management, responsibility |
| National service (sherut leumi) | 12-24 months | Community orientation, social skills |
| No service | N/A | Do NOT assume negative; many exemptions exist |

**IMPORTANT:** Never use military service type or unit as a filtering criterion. It is informational context only. Filtering by military unit violates the Equal Employment Opportunities Law.

**Israeli academic institutions ranking context:**

| Tier | Institutions |
|---|---|
| Research universities | Technion, Hebrew University, Tel Aviv University, Weizmann Institute, Ben-Gurion University, University of Haifa, Bar-Ilan University |
| Colleges (accredited) | IDC Herzliya (Reichman University), Academic College of Tel Aviv-Yafo, Sapir College, Shenkar, Bezalel |
| Tech bootcamps | ITC (Israel Tech Challenge), Coding Academy, Elevation Academy, Masterschool, Appleseeds |
| International (common) | Online degrees from accredited US/EU universities |

**Resume screening best practices:**
- Focus on skills and experience, not institution prestige
- Treat bootcamp graduates equally for relevant technical roles
- Account for career gaps due to military reserve duty (miluim), maternity leave, or gap years (common in Israel after army service)
- Hebrew resumes may use different date formats (DD/MM/YYYY)
- Look for relevant volunteer work and side projects, which are common in the Israeli tech ecosystem

### Step 4: Schedule Interviews with Israeli Calendar Awareness

Schedule interviews while respecting Israeli holidays, Shabbat, and business customs.

**Israeli work week:** Sunday through Thursday (yom rishon through yom chamishi). Friday is a short workday for some companies (until 12:00-14:00). Saturday (Shabbat) is a rest day.

**Key holidays to avoid (2026):**

| Holiday | Hebrew Name | Dates (2026) | Duration |
|---|---|---|---|
| Purim | פורים | Mar 3 | 1 day (Mar 4 in walled cities / Shushan Purim) |
| Pesach | פסח | Apr 1 (eve) - Apr 9 | First seder Apr 1 evening, Yom Tov Apr 2-3 + Apr 8-9; Apr 4-7 chol hamoed |
| Yom HaShoah | יום השואה | Apr 14 | 1 day (siren 10:00) |
| Yom HaZikaron | יום הזיכרון | Apr 20 (eve) - Apr 21 | 1 day (sirens 20:00 prev day, 11:00) |
| Yom Ha'Atzmaut | יום העצמאות | Apr 21 (eve) - Apr 22 | 1 day |
| Shavuot | שבועות | May 21 (eve) - May 22 | 1 day |
| Tisha B'Av | תשעה באב | Jul 23 | Fast day, partial work day in some firms |
| Rosh Hashana | ראש השנה | Sep 12-13 | 2 days |
| Yom Kippur | יום כיפור | Sep 21 | 1 day (fasting, no work) |
| Sukkot | סוכות | Sep 26 - Oct 3 | First/last days Yom Tov (Sep 26 + Oct 3); Sep 27-Oct 2 chol hamoed |
| Hanukkah | חנוכה | Dec 4-12 | 8 days (workdays, school off) |

**Scheduling rules:**
- Never schedule on Shabbat (Friday evening to Saturday evening)
- Avoid scheduling on holiday eves after 13:00
- Prefer Sunday-Thursday, 09:00-17:00 Israel time (IST/IDT, UTC+2/+3)
- Allow 30-minute buffer for Israeli traffic conditions
- For tech companies: many operate flexible hours, confirm company culture first
- Video interviews: use Israel-friendly platforms (Zoom, Google Meet, Teams)

### Step 5: Generate Offer Letters with Mandatory Israeli Clauses

When generating an offer letter (michtav ha'asa'a), include all mandatory employment benefits as required by Israeli labor law.

**Mandatory benefits table (2026):**

| Benefit | Employee Contribution | Employer Contribution | Notes |
|---|---|---|---|
| Minimum wage (sachar minimum) | N/A | NIS 6,443.85 / month, NIS 34.64 / hour | Effective Apr 1, 2026 (3.3% raise from NIS 6,248). Offer letter salary must meet or exceed. |
| Pension (pensia) | 6.0% of salary | 6.5% of salary | Mandatory; retroactive from day 1 after 6 months without prior pension; from day 1 (or 3 months / end of tax year, whichever is first) for employees with prior pension |
| Keren Hishtalmut | 2.5% of salary | 7.5% of salary | Not mandatory but standard in tech sector; tax-exempt after 6 years. 2026 tax-exempt salary ceiling: NIS 15,712 / month |
| Severance (pitzuim) | N/A | 8.33% of salary | Can be included in pension via Section 14 waiver |

**Section 14 waiver (siman 14):** Most employers include a Section 14 waiver (ishur klali le-pi siman 14), which means pension contributions count toward severance. This must be explicitly stated in the offer letter. Without it, the employer may owe full severance on top of pension contributions. **Critical precondition:** Section 14 only takes effect when 100% of pension and severance contributions are deposited from day 1 on the employee's full salary. Partial coverage (e.g., contributions delayed for the 6-month new-employee window, or computed on base salary only) invalidates Section 14 — the employer is then liable for full statutory severance on top of what was deposited.

**Vacation days (yemei chufsha) minimums by seniority:**

| Years of Service | Annual Vacation Days |
|---|---|
| 1-4 | 14 calendar days (10 workdays) |
| 5 | 16 calendar days |
| 6 | 18 calendar days |
| 7 | 21 calendar days |
| 8+ | Additional day per year (up to 28 calendar days) |

**Other mandatory terms:**

| Term | Requirement |
|---|---|
| Sick days (yemei machala) | 1.5 days per month, up to 90 days accumulated |
| Convalescence pay (dmei havra'a) | 5-10 days per year depending on seniority. **2026 private-sector rate: NIS 418 per day** (frozen, same as 2025). Public-sector rate is approximately NIS 471.4 per day. Sample annual entitlements at NIS 418: year 1 = 5 days = NIS 2,090; year 2-3 = 6 days = NIS 2,508; year 4-10 = 7 days = NIS 2,926. |
| Overtime pay (sha'ot nosafot) | 125% for first 2 hours, 150% thereafter |
| Travel expenses (hoza'ot nesi'a) | Public transport reimbursement or set amount |
| Notice period (hodaa mukdemet) | Varies by seniority (1 day per month for first 6 months, then 2.5 days per month) |

**Offer letter structure:**

```
מכתב הצעת עבודה

לכבוד: [Candidate name]
תאריך: [Date]

הרינו שמחים להציע לך את התפקיד [Job title] בחברת [Company name].

פירוט תנאי ההעסקה:

1. תפקיד: [Job title]
2. תאריך תחילת עבודה: [Start date]
3. שכר ברוטו: [Salary] ש"ח לחודש
4. היקף משרה: [Full/Part time]
5. פנסיה: [X]% עובד, [X]% מעסיק
6. קרן השתלמות: [X]% עובד, [X]% מעסיק
7. סעיף 14: [Include Section 14 clause]
8. ימי חופשה: [X] ימים בשנה
9. ימי מחלה: בהתאם לחוק (1.5 ימים לחודש)
10. דמי הבראה: בהתאם לחוק
11. הוצאות נסיעה: [Amount/arrangement]
12. תקופת ניסיון: [X] חודשים
13. תקופת הודעה מוקדמת: [X] ימים
```

Consult `references/mandatory-benefits.md` for the complete benefits reference table.

### Step 6: Run Compliance Checklist

Before finalizing any hiring document, run through this compliance checklist:

**Job Description Compliance:**
- [ ] No gender-specific language (uses inclusive forms)
- [ ] No age requirements or preferences
- [ ] No marital/parental status references
- [ ] No military unit or service type requirements
- [ ] No ethnicity, religion, or national origin references
- [ ] Requirements are genuine occupational qualifications
- [ ] "Requirements" and "nice-to-haves" are clearly separated

**Offer Letter Compliance:**
- [ ] Pension terms specified (minimum 6% + 6.5%)
- [ ] Section 14 clause included (if applicable)
- [ ] Vacation days meet legal minimum for employee's seniority
- [ ] Sick days referenced per law
- [ ] Convalescence pay (dmei havra'a) mentioned
- [ ] Notice period specified
- [ ] Start date and probation period defined
- [ ] Salary stated as gross (bruto)

**Interview Process Compliance:**
- [ ] No questions about marital status, children, or pregnancy plans
- [ ] No questions about religious observance
- [ ] No questions about military unit (may ask about service duration if relevant to experience)
- [ ] No questions about ethnicity or country of origin
- [ ] Reasonable accommodations offered for candidates with disabilities

Run the compliance checker script for automated validation:
```bash
python scripts/job-description-generator.py --validate --input job_description.txt
```

## Examples

### Example 1: Create a Hebrew Job Description for a Software Developer

User says: "Write a job posting for a senior full-stack developer at our Tel Aviv startup"

Actions:
1. Gather role details: tech stack, team size, company stage
2. Generate Hebrew job description using the template from Step 1
3. Run anti-discrimination compliance checklist
4. Use gender-neutral language throughout ("מפתח/ת", "מהנדס/ת")
5. Separate requirements from nice-to-haves
6. Include salary range if provided

Result: A compliant Hebrew job description ready for posting on AllJobs and LinkedIn.

### Example 2: Screen a Batch of Resumes

User says: "I have 50 resumes for a product manager role, help me create a screening framework"

Actions:
1. Define screening criteria based on job requirements (not military unit or institution)
2. Create a scoring rubric: must-haves, nice-to-haves, red flags
3. Account for Israeli-specific resume patterns (army service section, gap years)
4. Flag resumes for phone screening vs rejection with reasons
5. Ensure no candidate is filtered based on protected characteristics

Result: A structured screening framework with a scored shortlist of candidates.

### Example 3: Generate an Offer Letter

User says: "Draft an offer letter for a QA engineer, 18,000 NIS gross, starting March 2026"

Actions:
1. Generate offer letter with all mandatory clauses
2. Calculate pension contributions (6% employee = 1,080 NIS, 6.5% employer = 1,170 NIS)
3. Include Section 14 waiver clause
4. Set vacation days to legal minimum (14 calendar days for year 1-4)
5. Add sick days, convalescence pay, and travel expense terms
6. Set notice period per seniority

Result: Complete offer letter in Hebrew with all legally required terms.

### Example 4: Post to Multiple Job Boards

User says: "Post our DevOps engineer position to AllJobs and LinkedIn"

Actions:
1. Adapt the Hebrew job description for AllJobs format (structured fields)
2. Create an English version for LinkedIn
3. Select appropriate categories and filters on each platform
4. Recommend posting time (Sunday morning for maximum visibility)
5. Provide tracking instructions for monitoring applications

Result: Job posted on both platforms with tracking details.

## Bundled Resources

### Scripts
- `scripts/job-description-generator.py` -- Generate compliant Hebrew job descriptions from structured input. Validates against anti-discrimination rules and outputs formatted markdown. Run: `python scripts/job-description-generator.py --help`

### References
- `references/anti-discrimination-law.md` -- Summary of the Equal Employment Opportunities Law 1988 (chok shivyon hizdamnuyot ba'avoda). Lists all protected characteristics, permitted exceptions, enforcement mechanisms, and penalties. Consult when writing job descriptions or screening criteria.
- `references/mandatory-benefits.md` -- Complete table of mandatory employment benefits in Israel for 2026. Includes pension rates, keren hishtalmut, vacation days by seniority, sick days, convalescence pay, overtime rules, and notice periods. Consult when drafting offer letters or employment terms.

## Gotchas

- Israeli job descriptions must use gender-inclusive Hebrew (e.g., "מפתח/ת" not "מפתח"). The Equal Employment Opportunities Law 1988 prohibits gender-specific job postings. Agents may generate masculine-only Hebrew forms.
- Military service type and unit (e.g., 8200, Mamram) must never be used as screening criteria, even though they appear on most Israeli resumes. Filtering by unit violates anti-discrimination law.
- Pension contributions in Israel are mandatory from day 1 (or after 6 months for first-time employees). The minimum is 6% employee + 6.5% employer. Agents may use outdated lower rates from pre-2017 regulations.
- Section 14 (Siman 14) waiver is standard in Israeli tech but must be explicitly stated in the offer letter. Without it, employers owe full severance on top of pension contributions. Agents may omit this critical clause.
- Israeli convalescence pay (dmei havra'a) is a mandatory annual benefit with a fixed per-day rate (updated yearly). Agents unfamiliar with Israeli labor law may omit it entirely from offer letters.


## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Equal Employment Opportunities Law (Nevo) | https://www.nevo.co.il/law_html/law00/72482.htm | Full text of Law 1988 with all amendments through 2025 |
| Kol Zchut, hiring obligations | https://www.kolzchut.org.il/he/חוק_שוויון_ההזדמנויות_בעבודה | Employer duties, mandatory notice to employee, recent amendments |
| Israel Ministry of Economy and Industry | https://www.gov.il/he/departments/ministry_of_economy_and_industry | Minimum wage, mandatory benefits, equal pay |
| Israel Equal Employment Opportunities Commission | https://www.gov.il/he/departments/equal_employment_opportunities_commission | EEOC complaint statistics, guidance, enforcement |
| AllJobs | https://www.alljobs.co.il | Job posting formats, category structure |
| Drushim | https://www.drushim.co.il | Alternative job board, posting conventions |

## Troubleshooting

### Error: "Job description flagged for discrimination"
Cause: The description contains language that references a protected characteristic (gender, age, marital status, military unit, etc.)
Solution: Review the anti-discrimination checklist in Step 1. Replace specific language with neutral alternatives. Use "mefateach/et" instead of gendered forms. Remove age ranges and military unit references.

### Error: "Missing mandatory clause in offer letter"
Cause: The offer letter does not include one or more required employment terms (pension, Section 14, vacation days, sick days, convalescence pay)
Solution: Compare against the mandatory benefits table in Step 5 and add the missing clause. Run: `python scripts/job-description-generator.py --validate --input offer_letter.txt`

### Error: "Interview scheduled on Israeli holiday"
Cause: The proposed interview date falls on a holiday or Shabbat
Solution: Check the holiday calendar in Step 4. Reschedule to a standard business day (Sunday-Thursday). Avoid holiday eves after 13:00.

### Error: "Candidate screened out by protected criterion"
Cause: Resume screening used military unit, academic institution tier, or personal status as a filter
Solution: Review Step 3 screening guidelines. Military service and institution are context only, never screening criteria. Focus on skills, experience, and job-relevant qualifications.
