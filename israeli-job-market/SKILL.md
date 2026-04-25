---
name: israeli-job-market
description: Aggregate Israeli job market data, optimize Hebrew CVs, benchmark salaries, and track employment trends. Use when user asks about job searching in Israel, Israeli CV writing, Hebrew resume, salary expectations in Israel, AllJobs, Drushim, JobMaster, JobNet, LinkedIn Israel, Israeli job interviews, or Israeli employment benefits. Covers major job platforms, salary data, and Israeli workplace culture. Do NOT use for international job markets outside Israel or immigration/visa work permits (see separate skill).
license: MIT
version: 1.1.0
allowed-tools: Bash(python:*) WebFetch
compatibility: Requires network access for job platform data. No API keys needed for public job listings.
---

# Israeli Job Market

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
| Government / Public | Israeli Employment Service (taasuka.gov.il) | Official government jobs |
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
    "average_national": 13500,  # NIS/month average wage (CBS, all sectors, 2026)
    "tech_ranges": {  # Tel Aviv / Gush Dan, gross monthly NIS, 2026 bands
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
        "pension": "6% employee + 6.5% employer (mandatory)",
        "keren_hishtalmut": "7.5% employer (2.5% employee) -- tax-free savings",
        "vacation_days": "12-20 days/year depending on seniority",
        "sick_days": "18 days/year (accumulate)",
        "meal_vouchers": "Common, partially tax-exempt",
        "company_car": "Common for senior roles, taxed as benefit",
        "annual_bonus": "Varies, 1-3 months typical in tech",
    }
}
```

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
| Israeli unicorns + scaleups | Wiz, Mobileye, Wix, monday.com, Lemonade, Riskified, Rapyd, Lightricks, Fiverr, Gong, JFrog, Cellebrite, Verbit, Tipalti, Snyk, Trax, Pagaya | Wiz acquired by Google in 2024 for ~$32B (still operates as Wiz). Mid-2026 Wix and Lemonade are stable; Riskified and Lightricks did rounds of layoffs in 2024-2025 then resumed selective hiring. |
| AI-native (post-2023 wave) | AI21 Labs, Run:ai (acquired by Nvidia 2024), Pinecone IL ops, Aporia, Hour One, D-ID | Premium pay for LLM/agent expertise. Many founded by 8200/Talpiot alumni. |
| Mid-tier startups | Series B-C SaaS, fintech, cybersec | Expect 10-25% lower base than unicorns, often higher equity %. |
| Banks + insurance | Bank Hapoalim, Bank Leumi, Discount, Mizrahi-Tefahot, Migdal, Harel, Phoenix, Clal | Stable, structured ladders, lower base for tech but pension generous. Backend Java/.NET dominant. |
| Government + defense | IDF MAMRAM, Rafael, IAI, Elbit, Mossad/Shabak (cleared), Israel Police, Bituach Leumi tech | Lower base but pension + cleared-job premium (cleared roles can switch to defense unicorns). |

**Post-October-2023 / 2024-2026 market context.** The Israeli tech market took a hit in late 2023 after the war began and global rate hikes; 2024 saw layoff waves at Wix, Lightricks, Riskified, Cellebrite, Snyk, JFrog and many Series-B startups. By H2 2025 hiring resumed, biased toward AI engineering, infra, and security roles. Reservist call-ups (miluim) remain a real factor in interviews; many employers ask about expected reserve days and supplement the Bituach Leumi reservist pay. Base salary growth was muted in 2024 but AI roles broke out, with $250k-$400k total comp packages now common for senior AI engineers at top firms.

**IDF unit signals on a CV** (Israeli tech recruiters scan for these):

| Unit | Signal | Effect on hiring |
|---|---|---|
| 8200 | Signals intelligence / cyber | Strong signal for cyber, data, ML; common founder pedigree |
| Mamram | Central computing unit (IDF) | Strong backend/infra signal; Mamram course alumni network |
| Talpiot | Elite STEM officer track | Top-tier signal, very small alumni pool, often founder track |
| 9900 | Visual intel / geospatial | Strong CV/imagery/ML signal |
| 81 / Matzpen | Special-ops tech | Niche but respected for hardware/embedded |
| Maglan / Sayeret Matkal / Shayetet 13 | Combat special forces | Leadership signal; often paired with later tech training |
| Atuda | Academic deferral track | Common for engineers; signals degree completed before service |

If a candidate didn't serve (foreign-born, exempt, or chose not to), it's not a deal-breaker for most tech roles, but recruiters may ask about it. Cleared positions (Rafael, IAI, defense unicorns) typically require Israeli citizenship and IDF service.

**Bootcamps and alternative pipelines:**

| Bootcamp | Focus | Notes |
|---|---|---|
| ITC (Israel Tech Challenge) | Data science, software engineering | Top-tier, English-language, popular with olim |
| Coding Academy by John Bryce | Full-stack | Largest by volume |
| HackerU / ThriveDX | Cyber, full-stack | Hebrew + English tracks |
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

**Common questions specific to Israel:**
- "Tell me about your military service" (for younger candidates)
- "Why are you leaving your current company?" (direct, expected)
- "What are your salary expectations?" (asked early in process)
- "Can you start in 30 days?" (standard notice period)

## Examples

### Example 1: Job Search
User says: "I'm a senior Python developer looking for jobs in Tel Aviv"
Actions:
1. Recommend LinkedIn Israel + Drushim for tech roles
2. Suggest search terms: "Python developer", "Backend developer", "Senior developer"
3. Filter: Gush Dan region, 5+ years experience
4. Provide salary range: 36,000-55,000 NIS/month for senior Python
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
1. Check against benchmarks (mid-dev range: 25,000-38,000)
2. Factor in location (Tel Aviv premium vs periphery)
3. Calculate total compensation including benefits
4. Advise on negotiation approach
Result: Contextual salary analysis with negotiation guidance.

## Bundled Resources

### Scripts
- `scripts/salary_calculator.py` -- Estimates Israeli salary ranges by role, industry, and experience level, computes gross-to-net approximation for job offers, and compares benefits packages (pension, keren hishtalmut, vacation days) against Israeli labor law minimums. Run: `python scripts/salary_calculator.py --help`

### References
- `references/israeli-cv-template.md` -- Standard Israeli CV templates in both English and Hebrew formats with section-by-section structure, including personal details, professional summary, work experience, military service, education, skills, and languages. Covers photo guidelines, Hebrew RTL formatting notes, and Israeli hiring conventions. Consult when helping users write or optimize CVs for the Israeli job market.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| levels.fyi (Israel filter) | https://www.levels.fyi/?country=120 | FAANG IL + senior tech compensation incl. equity |
| Geektime | https://www.geektime.co.il | Daily Israeli tech news, hiring/layoff coverage, annual salary surveys |
| Calcalist Tech | https://www.calcalist.co.il/Tech | Hebrew tech business news, funding rounds, layoff announcements |
| TheMarker Tech | https://www.themarker.com/technation | Hebrew tech and business news |
| AllJobs | https://www.alljobs.co.il | Largest Hebrew job board, salary survey at /salary |
| Drushim | https://www.drushim.co.il | Hebrew job board, strong tech listings |
| Ethosia salary report | https://www.ethosia.co.il | Annual Israeli tech salary PDF (free) |
| CBS wage data | https://www.cbs.gov.il | Official wage statistics by sector and occupation |
| Bituach Leumi reservist pay | https://www.btl.gov.il/benefits/Reserves | Miluim compensation rules (relevant for 2024-2026 candidates) |

## Gotchas

- Israeli salaries are always quoted as monthly gross (bruto), not annual. Agents may convert to annual figures and confuse candidates who expect monthly numbers.
- Keren Hishtalmut (education fund) adds approximately 10% to total compensation (7.5% employer + 2.5% employee) and is tax-free after 6 years. Agents may omit this significant benefit when comparing Israeli offers to international ones.
- The Israeli tech job market peaks Sunday-Tuesday for job postings. Agents may recommend posting on Mondays (which is already the 3rd day of the Israeli work week).
- Israeli CVs commonly include a photo, date of birth, and military service section. Agents trained on US resume conventions may flag these as inappropriate when they are standard practice in Israel.
- "Shotef + 30" payment terms mean net 30 from end of month, not net 30 from invoice date. This is the most common freelancer payment term in Israel and agents frequently misinterpret it.

## Troubleshooting

### Issue: "Job listings are all in Hebrew"
Cause: Most Israeli companies post in Hebrew
Solution: Use browser translation, search LinkedIn for English listings, or focus on multinational companies operating in Israel.

### Issue: "No response to applications"
Cause: Israeli market is network-driven; cold applications have lower response rates
Solution: Use LinkedIn connections, attend meetups (Meetup.com Israel), ask for referrals. Israeli tech community is tight-knit -- warm introductions significantly increase response rate.

### Issue: "Salary seems low compared to US"
Cause: Israeli salaries are lower in absolute terms but include mandatory benefits
Solution: Calculate total compensation including pension (6% employee + 6.5% employer), Keren Hishtalmut (7.5%), and other benefits. Also factor in lower healthcare costs and different cost of living.