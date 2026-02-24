---
name: israeli-job-market
description: >-
  Aggregate Israeli job market data, optimize Hebrew CVs, benchmark salaries,
  and track employment trends. Use when user asks about job searching in Israel,
  Israeli CV writing, Hebrew resume, salary expectations in Israel, AllJobs,
  Drushim, JobMaster, JobNet, LinkedIn Israel, Israeli job interviews, or
  Israeli employment benefits. Covers major job platforms, salary data, and
  Israeli workplace culture. Do NOT use for international job markets outside
  Israel or immigration/visa work permits (see separate skill).
license: MIT
allowed-tools: "Bash(python:*) WebFetch"
compatibility: "Requires network access for job platform data. No API keys needed for public job listings."
metadata:
  author: skills-il
  version: 1.0.0
  category: communication
  tags: [jobs, employment, cv, salary, career, hebrew, israel]
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
| Government / Public | JobNet (jobnet.gov.il) | Official government jobs |
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
    "average_national": 12000,  # NIS/month approximate
    "tech_ranges": {
        "junior_developer": (14000, 20000),
        "mid_developer": (20000, 32000),
        "senior_developer": (30000, 45000),
        "team_lead": (35000, 50000),
        "vp_engineering": (50000, 80000),
        "product_manager": (22000, 40000),
        "data_scientist": (22000, 42000),
        "devops_engineer": (22000, 38000),
    },
    "benefits_value": {
        "pension": "6.5% employer contribution (mandatory)",
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
1. AllJobs salary survey: alljobs.co.il/salary
2. Glassdoor Israel: glassdoor.com (filter by Israel)
3. CBS wage statistics: data.gov.il (search for wage data)
4. LinkedIn Salary Insights: available for premium users

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
4. Provide salary range: 30,000-42,000 NIS/month for senior Python
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
1. Check against benchmarks (mid-dev range: 20,000-32,000)
2. Factor in location (Tel Aviv premium vs periphery)
3. Calculate total compensation including benefits
4. Advise on negotiation approach
Result: Contextual salary analysis with negotiation guidance.

## Bundled Resources

### References
- `references/israeli-cv-template.md` — Standard Israeli CV templates in both English and Hebrew formats with section-by-section structure, including personal details, professional summary, work experience, military service, education, skills, and languages. Covers photo guidelines, Hebrew RTL formatting notes, and Israeli hiring conventions. Consult when helping users write or optimize CVs for the Israeli job market.

## Troubleshooting

### Issue: "Job listings are all in Hebrew"
Cause: Most Israeli companies post in Hebrew
Solution: Use browser translation, search LinkedIn for English listings, or focus on multinational companies operating in Israel.

### Issue: "No response to applications"
Cause: Israeli market is network-driven; cold applications have lower response rates
Solution: Use LinkedIn connections, attend meetups (Meetup.com Israel), ask for referrals. Israeli tech community is tight-knit -- warm introductions significantly increase response rate.

### Issue: "Salary seems low compared to US"
Cause: Israeli salaries are lower in absolute terms but include mandatory benefits
Solution: Calculate total compensation including pension (6.5%), Keren Hishtalmut (7.5%), and other benefits. Also factor in lower healthcare costs and different cost of living.
