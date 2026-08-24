---
name: israeli-job-market
description: Not legal advice and not employment-law advice. Aggregate Israeli job market data, optimize Hebrew CVs, benchmark salaries, and track employment trends. Use when user asks about job searching in Israel, Israeli CV writing, Hebrew resume, salary expectations in Israel, AllJobs, Drushim, JobMaster, JobNet, LinkedIn Israel, Israeli job interviews, or Israeli employment benefits. Covers major job platforms, salary data, and Israeli workplace culture. Do NOT use for international job markets outside Israel or immigration/visa work permits (see separate skill).
license: MIT
allowed-tools: WebFetch
compatibility: Requires network access for job platform data. No API keys needed for public job listings.
---

# Israeli Job Market

## Legal notice

This is a free information tool operated by an AI model. It aggregates public information on recruitment platforms, published salary data, CV and interview conventions, and general rules of Israeli employment law, with no involvement, review, or approval by a licensed advocate. Its output is not legal advice and not a legal opinion, only general information: it does not examine your employment contract, the collective agreement or extension order that applies to you, or your specific circumstances, and those are exactly the facts that determine how any rule actually applies to you. Amounts, rates, and deadlines change over time, and an AI model may err, omit data, or present a wrong conclusion.

Do not rely on the output as a basis for waiving a right, signing a contract or a termination arrangement, filing a claim, or approaching the Labour Court. It is not a substitute for advice that takes into account the particular data and needs of each person, and before taking any step or signing any document you should consult an advocate specialising in employment law. All use of the output is at the user's sole responsibility.

## Instructions

### Step 1: Identify User Need
Determine which job market service the user needs:

| Service | When | Key Platforms |
|---------|------|--------------|
| Job search | Looking for positions | AllJobs, Drushim, JobMaster, LinkedIn |
| CV optimization | Preparing applications | Hebrew/English CV standards |
| Salary benchmark | Negotiating or planning | AllJobs survey, CBS, Glassdoor |
| Market trends | Career planning | CBS data, startup ecosystem reports |
| Interview prep | Upcoming interviews | Israeli culture, common practices |

### Step 2: Job Search Guidance

**Platform selection by sector:**

| Sector | Best Platform | Why |
|--------|--------------|-----|
| Tech / Startups | LinkedIn Israel, Drushim | English-friendly, tech focus |
| Government / Public | Civil-service tenders at ejobs.gov.il (נציבות שירות המדינה); municipal jobs on each municipality's own site | State jobs are published as מכרזים with a formal application form, deadline and scoring, not as CV-by-email listings. taasuka.gov.il is the Employment Service (unemployment registration and placement), NOT the publisher of state jobs. |
| General market | AllJobs | Largest listing volume |
| Entry level | JobMaster, AllJobs | Broadest coverage |
| Senior / Executive | LinkedIn, headhunters | Network-driven hiring |
| Staffing / Contract | SQLink, Matrix, Ness | IT staffing specialists |

**Search tips for Israeli platforms:**
- Search in both Hebrew and English -- many listings are in Hebrew only
- Filter by region: Gush Dan (Tel Aviv metro), Haifa, Jerusalem, Be'er Sheva, remote
- "Mishra" (mishra) = position, "Maskoret" (maskoret) = salary
- Check "drushim" (drushim) literally means "wanted/needed"

### Step 3: Hebrew CV Optimization

**Israeli CV structure (recommended order):**

```
1. Personal Details
   - Full name, phone (+972), email
   - LinkedIn profile URL
   - City of residence (commute matters in Israel)
   - Optional: Date of birth, photo

2. Professional Summary
   - 2-3 sentences, role-focused
   - Include years of experience and key expertise

3. Work Experience
   - Reverse chronological
   - Company name, role title, dates
   - 3-5 bullet points per role with achievements
   - Quantify results (percentages, revenue, team size)

4. Military Service
   - Unit, role, rank, dates
   - Relevant skills or leadership experience
   - Tech units: specify technologies used

5. Education
   - Degree, institution, graduation year
   - Relevant coursework or thesis (if recent graduate)

6. Technical Skills
   - Programming languages, tools, certifications

7. Languages
   - Hebrew: native/fluent, English: level, others
```

**CV tips for Israeli market:**
- Keep to 1-2 pages (Israel prefers concise CVs)
- Military service section is expected for ages 21-35
- Include a professional photo (head and shoulders, professional attire)
- Hebrew CV for Israeli companies, English for multinational/tech
- Mention "Keren Hishtalmut" expectations in salary discussion, not on CV

### Step 4: Salary Benchmarking

**Salary lookup guidance:**

```python
# Israeli salary context helper
israeli_salary_data = {
    "currency": "NIS (New Israeli Shekel)",
    "pay_frequency": "Monthly gross (bruto)",
    "average_wage_btl_benefits": 13769,   # NIS/month, National Insurance Law s.2 (benefits base), from 01.01.2026
    "average_wage_btl_contributions": 13566,  # NIS/month, National Insurance Law s.1 (contributions base), from 01.01.2026
    "average_wage_cbs_per_post": 14374,   # NIS/month gross per employee post, CBS, April 2026 data
    "minimum_wage_monthly": 6443.85,      # NIS/month full-time, from 01.04.2026
    "minimum_wage_hourly": 35.40,         # NIS/hour, from 01.04.2026
    # Indicative planning ranges compiled by this skill from market reporting, NOT survey data.
    # Do not quote them as published benchmarks. Verify per company on levels.fyi before using a number in a negotiation.
    "tech_ranges": {  # Tel Aviv / Gush Dan, gross monthly NIS, indicative
        "junior_developer": (18000, 26000),
        "mid_developer": (26000, 40000),
        "senior_developer": (38000, 60000),
        "staff_engineer": (55000, 85000),
        "team_lead": (45000, 65000),
        "engineering_manager": (55000, 80000),
        "vp_engineering": (65000, 110000),
        "product_manager": (28000, 55000),
        "senior_pm": (40000, 70000),
        "data_scientist": (30000, 58000),
        "ai_engineer": (35000, 70000),  # New band, premium for LLM/genAI experience
        "ml_research_engineer": (40000, 80000),
        "devops_engineer": (30000, 55000),
        "security_engineer": (35000, 65000),
    },
    "benefits_value": {
        "pension": "18.5% of salary total under the mandatory-pension extension order: 6% employee, 6.5% employer tagmulim, 6% employer severance component. Ask whether the offer is under Section 14 of the Severance Pay Law, which decides whether the accrued severance component is yours on any exit or only on dismissal.",
        "keren_hishtalmut": "7.5% employer (2.5% employee) -- tax-free savings",
        "vacation_days": "Statutory minimum accrues by seniority under the Annual Leave Law; tech offers usually exceed it. Check the current ladder before quoting a number.",
        "sick_days": "Accrues monthly under the Sick Pay Law up to a statutory cap, and unused days carry over. Check the current accrual rate and cap before quoting a number.",
        "meal_vouchers": "Common, partially tax-exempt",
        "company_car": "Common for senior roles, taxed as benefit",
        "annual_bonus": "Varies by company and there is no published Israeli benchmark. Ask the employer for the historical payout range.",
    }
}
```

**Statutory floor and the two "average wage" numbers.** Minimum wage is 6,443.85 NIS/month for a
full-time post and 35.40 NIS/hour, in force since 01.04.2026; no further national step is published,
so do not promise one. Three different "average wage" figures circulate and they are not
interchangeable: Bituach Leumi uses 13,769 NIS as the benefits base (National Insurance Law s.2)
and 13,566 NIS as the contributions base (s.1), both from 01.01.2026, while the CBS figure of
14,374 NIS (April 2026) is gross pay per employee post and runs higher. The CBS series is monthly and moves, so re-check it rather than quoting April 2026 indefinitely. State which one you mean
whenever you benchmark against "the average wage".

**Where to research salaries:**
1. levels.fyi (filter by Israel) -- best source for FAANG IL R&D + senior tech compensation incl. equity
2. AllJobs salary survey: alljobs.co.il/salary
3. Glassdoor Israel: glassdoor.com (filter by Israel)
4. Ethosia salary report (annual, free PDF) -- Israeli tech-focused
5. CBS wage statistics: data.gov.il (search for wage data)
6. LinkedIn Salary Insights: available for premium users
7. Geektime salary surveys: geektime.co.il (annual deep-dive)

**Top employers in Israel (2026 snapshot):**

| Tier | Examples | Notes |
|---|---|---|
| FAANG IL R&D | Google IL, Meta IL, Amazon IL (incl. AWS), Apple IL, Microsoft IL, Nvidia IL, Intel IL | Highest base + RSUs. Hiring tightened post-2023 but bouncing back, esp. AI/infra. Intel IL trimmed in 2024-2025; Nvidia and Microsoft expanding. |
| Israeli unicorns + scaleups | Wiz, Mobileye, Wix, monday.com, Lemonade, Riskified, Rapyd, Lightricks, Fiverr, Gong, JFrog, Cellebrite, Verbit, Tipalti, Snyk, Trax, Pagaya | Wiz was acquired by Google in a deal reported at about $32 billion, announced in March 2025 and completed on 11 March 2026, and Wiz keeps its brand inside Google Cloud. Mid-2026 Wix and Lemonade are stable; Riskified and Lightricks did rounds of layoffs in 2024-2025 then resumed selective hiring. |
| AI-native (post-2023 wave) | AI21 Labs, Run:ai, Pinecone IL ops, Aporia, Hour One, D-ID | Premium pay for LLM/agent expertise. Many founded by 8200/Talpiot alumni. |
| Mid-tier startups | Series B-C SaaS, fintech, cybersec | Typically lower base than unicorns, often traded off against a higher equity percentage. Ask the candidate to benchmark the specific offer. |
| Banks + insurance | Bank Hapoalim, Bank Leumi, Discount, Mizrahi-Tefahot, Migdal, Harel, Phoenix, Clal | Stable, structured ladders, lower base for tech but pension generous. Backend Java/.NET dominant. |
| Government + defense | IDF MAMRAM, Rafael, IAI, Elbit, Mossad/Shabak (cleared), Israel Police, Bituach Leumi tech | Lower base but pension + cleared-job premium (cleared roles can switch to defense unicorns). |

**Market context as of mid-2026.** The Israeli tech market contracted in late 2023 and 2024 (layoff
waves at Wix, Lightricks, Riskified, Cellebrite, Snyk, JFrog and many Series-B startups), and hiring
resumed through 2025. The 2026 picture is a split market rather than a recovery: the Israel
Innovation Authority's 2026 human-capital survey found firms hiring an average of 8% of headcount
in H1 against 2.8% laid off, with hardware companies expanding while software companies contract.
The share of companies that cut hiring after adopting AI tools tripled within half a year, from 3%
to 10%, and the squeeze falls hardest on junior roles. National unemployment was 2.9% (seasonally
adjusted, April 2026), so the labour market overall stays tight even where tech hiring does not.
Reservist call-ups remain a live factor in interviews. Senior AI engineering commands
a clear premium over general senior-engineer bands, but no public Israeli survey states a reliable
range for it, so check levels.fyi per company rather than quoting a figure.

**IDF unit signals on a CV** (Israeli tech recruiters scan for these):

| Unit | Signal | Effect on hiring |
|---|---|---|
| 8200 | Signals intelligence / cyber | Strong signal for cyber, data, ML; common founder pedigree |
| Mamram | Central computing unit (IDF) | Strong backend/infra signal; Mamram course alumni network |
| Talpiot | Elite STEM officer track | Top-tier signal, very small alumni pool, often founder track |
| 9900 | Visual intel / geospatial | Strong CV/imagery/ML signal |
| Unit 81 | Special-ops technology | Niche but respected for hardware/embedded |
| Maglan / Sayeret Matkal / Shayetet 13 | Combat special forces | Leadership signal; often paired with later tech training |
| Atuda | Academic deferral track | Common for engineers; signals degree completed before service |

If a candidate didn't serve (foreign-born, exempt, or chose not to), it's not a deal-breaker for most tech roles, but recruiters may ask about it. Cleared positions (Rafael, IAI, defense unicorns) typically require Israeli citizenship and IDF service.

**Bootcamps and alternative pipelines:**

| Bootcamp | Focus | Notes |
|---|---|---|
| ITC (Israel Tech Challenge) | Data science, software engineering | Top-tier, English-language, popular with olim |
| Coding Academy by John Bryce | Full-stack | Largest by volume |
| HackerU / ThriveDX | Cyber, full-stack | Hebrew + English tracks. Verify the provider is still operating and the specific track is still running before recommending it; this group has been the subject of financial-distress reporting. |
| She Codes | Free women's coding community | Strong signal for entry roles |
| Wix Academy / monday Academy | Internal pipelines | Often hire grads directly |

### Step 5: Israeli Interview Culture

**What to expect:**
- Interviews are relatively informal compared to US/Europe
- Direct communication style ("dugri") is appreciated
- Technical interviews similar to global standards (coding, system design)
- Culture fit matters -- Israeli teams value collaboration and initiative
- Hebrew small talk expected, but technical discussion often in English
- "Why Israel?" for olim (immigrants) is a common question
- Salary negotiation is expected -- first offer is usually negotiable
- Background check: may include military service verification

**Notice period is graduated, not a flat 30 days.** Under the Advance Notice Law a monthly-paid
employee owes one day of notice for each of the first six months of employment, two and a half days
for each further full month up to the end of the first year, and a full month only from the second
year. Daily and hourly employees are on their own ladder. So a candidate five months into a job owes
five calendar days, not a month. The statutory period is a floor that a contract can lengthen, and
it can be waived or bought out by agreement, so ask what the contract actually says before promising
a start date.

**Common questions specific to Israel:**
- "Tell me about your military service" (for younger candidates)
- "Why are you leaving your current company?" (direct, expected)
- "What are your salary expectations?" (asked early in process)
- "When can you start?" (notice period is graduated, see below)

## Examples

### Example 1: Job Search
User says: "I'm a senior Python developer looking for jobs in Tel Aviv"
Actions:
1. Recommend LinkedIn Israel + Drushim for tech roles
2. Suggest search terms: "Python developer", "Backend developer", "Senior developer"
3. Filter: Gush Dan region, 5+ years experience
4. Provide the indicative senior-developer range from Step 4 (38,000-60,000 NIS/month), flagged as indicative and to be checked per company
Result: Curated platform recommendations with salary context.

### Example 2: CV Review
User says: "Can you help me write a Hebrew CV for Israeli companies?"
Actions:
1. Follow Step 3 structure
2. Ask about military service background
3. Ensure Hebrew formatting (RTL), proper section headers
4. Include photo guidance and personal details per Israeli norms
Result: Structured Hebrew CV following Israeli conventions.

### Example 3: Salary Negotiation
User says: "I got an offer for 28,000 NIS as a mid-level developer, is that fair?"
Actions:
1. Check against the indicative mid-developer range from Step 4 (26,000-40,000)
2. Factor in location (Tel Aviv premium vs periphery)
3. Calculate total compensation including benefits
4. Advise on negotiation approach
Result: Contextual salary analysis with negotiation guidance.

## Bundled Resources

### References
- `references/domain-checklist.md` -- Internal coverage contract for this skill: what a complete Israeli job-market workflow must cover, what it should cover, and what is explicitly routed to a sibling skill. Consult when deciding whether a question is in scope.
- `references/israeli-cv-template.md` -- Standard Israeli CV templates in both English and Hebrew formats with section-by-section structure, including personal details, professional summary, work experience, military service, education, skills, and languages. Covers photo guidelines, Hebrew RTL formatting notes, and Israeli hiring conventions. Consult when helping users write or optimize CVs for the Israeli job market.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| levels.fyi (Israel filter) | https://www.levels.fyi/?country=105 | FAANG IL + senior tech compensation incl. equity |
| Geektime | https://www.geektime.co.il | Daily Israeli tech news, hiring/layoff coverage, annual salary surveys |
| Calcalist Tech | https://www.calcalist.co.il/Tech | Hebrew tech business news, funding rounds, layoff announcements |
| TheMarker Tech | https://www.themarker.com/technation | Hebrew tech and business news |
| AllJobs | https://www.alljobs.co.il | Largest Hebrew job board, salary survey at /salary |
| Drushim | https://www.drushim.co.il | Hebrew job board, strong tech listings |
| Ethosia salary report | https://www.ethosia.co.il | Annual Israeli tech salary PDF (free) |
| CBS wage data | https://www.cbs.gov.il | Official wage statistics by sector and occupation |
| Bituach Leumi reservist pay | https://www.btl.gov.il/benefits/Reserve_Service/Pages/default.aspx | Miluim compensation rules and employer indemnification |
| Bituach Leumi average wage | https://www.btl.gov.il/Mediniyut/GeneralData/Pages/שכר%20ממוצע.aspx | The s.1 and s.2 average-wage figures and their effective date |
| Kol Zchut minimum wage | https://www.kolzchut.org.il/he/שכר_מינימום | Current monthly / hourly minimum wage and youth rates |

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Israeli CBS MCP](https://agentskills.co.il/he/mcps/developer-tools/israeli-cbs) | Queries Central Bureau of Statistics series directly, so wage and employment figures can be pulled live instead of quoted from a static table |
| [Kolzchut (All-Rights)](https://agentskills.co.il/he/mcps/government-services/kolzchut) | Looks up Israeli employment rights (minimum wage, notice, severance, reservist protections) from the All-Rights knowledge base |

## Related Skills

Adjacent questions belong to other skills in this directory: unemployment benefit eligibility and registering at the Employment Service bureau go to `israeli-unemployment-benefits-navigator`, drafting the CV itself to `israeli-cv-builder`, reserve-duty administration to `israeli-miluim-manager`, and offer-stage negotiation tactics to `israeli-tech-salary-negotiator`.

## Gotchas

- Israeli salaries are always quoted as monthly gross (bruto), not annual. Agents may convert to annual figures and confuse candidates who expect monthly numbers.
- Keren Hishtalmut (education fund) adds approximately 10% to total compensation (7.5% employer + 2.5% employee) and is tax-free after 6 years. Agents may omit this significant benefit when comparing Israeli offers to international ones.
- The Israeli work week runs Sunday to Thursday, so Sunday is the first working day and Thursday is the last. Agents trained on a Monday-to-Friday week routinely mistime follow-ups, interview scheduling, and "end of week" commitments by a day or two.
- Israeli CVs commonly include a photo, date of birth, and military service section. Agents trained on US resume conventions may flag these as inappropriate when they are standard practice in Israel.
- "Shotef + 30" payment terms mean net 30 from end of month, not net 30 from invoice date, and agents frequently misinterpret it. Freelancers negotiating terms should also look at חוק מוסר תשלומים לספקים, which sets statutory payment deadlines rather than leaving timing purely to the contract.
- Miluim (reserve duty) days are paid via Bituach Leumi. Topping that up to full salary is still not a legal obligation, so candidates evaluating offers should ask explicitly: "Do you supplement Bituach Leumi reservist pay to my full salary, and is that contractual or at managerial discretion?" What changed is the employer's side: under the 2026 arrangement the state indemnifies employers at 20% of a reservist employee's wage on a permanent basis, no longer conditional on the service being classed as emergency service. The same arrangement extends protection from dismissal to two months instead of one for an employee who served more than 60 reserve days, and gives spouses of reservists with children up to age 14 up to 8 paid absence days a year.
- Taking a role through a staffing firm is not the same as taking it through a services contractor, and the difference is worth asking about. A koach-adam agency worker placed with the same end employer for more than nine consecutive months becomes an employee of that end employer, with earlier seniority carried across. Two exclusions matter here: the rule does not apply to computing roles, which is exactly the population the IT staffing firms serve, and it does not bite at all if the engagement is structured as a services contract rather than a manpower placement. Ask which of the two the contract is.
- Israel has NO law requiring a salary range in a job posting, and agents routinely assert one because several US states and the EU Pay Transparency Directive do. What Israel has is a reporting duty added to the Equal Pay Law (חוק שכר שווה לעובדת ולעובד) that makes employers of more than 518 employees publish an annual gender pay-gap report and give each employee their own group's gap figure. That is a retrospective disclosure, not a posting requirement. A candidate can still ask for the band in the screening call, but should not claim an entitlement to it.
- LinkedIn premium "Salary Insights" for Israel has weak coverage outside the top FAANG/Israeli-unicorn population. For mid-market roles, prefer the AllJobs salary survey, Ethosia annual report, or Geektime surveys.

## Troubleshooting

### Issue: "Job listings are all in Hebrew"
Cause: Most Israeli companies post in Hebrew
Solution: Use browser translation, search LinkedIn for English listings, or focus on multinational companies operating in Israel.

### Issue: "No response to applications"
Cause: Israeli market is network-driven; cold applications have lower response rates. Separately, silence is often a breach rather than a signal.
Solution: Use LinkedIn connections, attend meetups (Meetup.com Israel), ask for referrals. Israeli tech community is tight-knit -- warm introductions significantly increase response rate. Also tell the candidate their statutory right: at a workplace with more than 25 employees, an employer running a screening process must give a candidate who sat an interview or screening test written notice of the progress of the process at least once every two months, and written notice of rejection within 14 days of someone else being hired for that role. Catering roles and jobs offered for 30 days or less are exempt, as is anyone who never actually interviewed. A labour court may award the candidate compensation for a breach even with no proven financial loss.

### Issue: "Salary seems low compared to US"
Cause: Israeli salaries are lower in absolute terms but include mandatory benefits
Solution: Calculate total compensation including pension (18.5% total, of which 12.5% is the employer: 6.5% tagmulim plus 6% severance), Keren Hishtalmut (7.5% employer plus 2.5% employee), and other benefits. Also factor in lower healthcare costs and different cost of living.