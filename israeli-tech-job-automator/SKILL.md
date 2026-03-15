---
name: israeli-tech-job-automator
description: >-
  Automates tech job searching across Israeli platforms (AllJobs, Drushim,
  LinkedIn Israel, JobMaster) with CV optimization for Hebrew/English
  bilingual resumes, salary benchmarking against Israeli tech market data,
  interview preparation for Israeli companies, and application tracking.
  Use when user asks to "find tech jobs in Israel", "optimize my CV for
  Israeli market", "salary benchmarking Israel", "khipus avoda" (Hebrew
  transliteration), or needs help with Israeli job platforms, bilingual
  resume formatting, or interview prep. Do NOT use for non-Israeli job
  markets, recruitment agency management, or HR system administration.
license: MIT
allowed-tools: 'Bash(python:*)'
compatibility: 'No special requirements. Works with Claude Code, Cursor, Windsurf.'
metadata:
  author: skills-il
  version: 1.0.0
  category: communication
  tags:
    he:
      - חיפוש עבודה
      - קורות חיים
      - שכר הייטק
      - ראיונות עבודה
      - הייטק ישראלי
      - ישראל
    en:
      - job-search
      - cv-optimization
      - tech-salary
      - job-interviews
      - israeli-tech
      - israel
  display_name:
    he: "אוטומציית חיפוש עבודה בהייטק הישראלי"
    en: Israeli Tech Job Automator
  display_description:
    he: "אוטומציה של חיפוש עבודה בפלטפורמות ישראליות (AllJobs, דרושים, LinkedIn), אופטימיזציית קורות חיים בעברית/אנגלית, השוואת שכר בהייטק הישראלי, והכנה לראיונות בחברות ישראליות."
    en: >-
      Automates tech job searching across Israeli platforms (AllJobs, Drushim,
      LinkedIn Israel, JobMaster) with CV optimization for Hebrew/English
      bilingual resumes, salary benchmarking against Israeli tech market data,
      interview preparation for Israeli companies, and application tracking.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
---

# Israeli Tech Job Automator

Comprehensive automation for tech job searching in the Israeli market. This skill covers everything from finding positions on Israeli job platforms to optimizing your bilingual CV, benchmarking salaries, and preparing for interviews at Israeli tech companies.

## Israeli Job Platforms

### AllJobs (alljobs.co.il)

Israel's largest general job board with significant tech listings.

**Strengths:**
- Largest database of Israeli job listings
- Strong presence across all sectors (not just tech)
- Hebrew-first interface, comfortable for local candidates
- Employer reviews and salary estimates
- Resume database for passive job seekers

**Profile Optimization:**
- Complete your profile in Hebrew (primary) and English (secondary)
- Upload CV in both languages
- Set job alerts with specific technology keywords
- Use Hebrew technology terms alongside English ones (e.g., "פיתוח Full Stack" AND "Full Stack Development")
- Enable "visible to employers" for passive search

**Search Tips:**
- Filter by "הייטק" (hi-tech) industry category
- Use English technology terms for better results (React, Python, AWS)
- Filter by region: Tel Aviv (תל אביב), Herzliya (הרצליה), Ra'anana (רעננה) for top tech hubs
- Set salary filter above 15,000 NIS to filter out non-tech roles

### Drushim (drushim.co.il)

Popular Israeli job aggregator with strong tech focus.

**Strengths:**
- Aggregates listings from company career pages
- Good filtering by technology stack
- Salary estimates based on market data
- Company profiles with employee reviews
- Mobile app with push notifications

**Profile Optimization:**
- Create a detailed tech profile with your stack
- List specific frameworks and tools (not just languages)
- Set technology-specific alerts
- Follow companies you are interested in for updates

**Search Tips:**
- Use the "הייטק" (Hi-Tech) category for targeted results
- Filter by experience level: "ג'וניור" (Junior), "מידלבל" (Mid-level), "סניור" (Senior)
- Use advanced search to combine technology + location + experience
- Check "חברות מגייסות" (Hiring Companies) section for active employers

### LinkedIn Israel

The dominant professional network for Israeli tech.

**Strengths:**
- Essential for Israeli tech networking
- Most Israeli tech companies post here
- Strong recruiter activity in Israeli market
- Easy to connect with Israeli tech community
- English-first, which works well for international companies in Israel

**Profile Optimization:**
- Write headline in English (Israeli tech recruiters search in English)
- Add Hebrew summary in addition to English
- List Israeli military tech units if applicable (8200, Mamram, etc.)
- Include Israeli tech ecosystem keywords (startup, scale-up, exit)
- Get endorsements from Israeli colleagues for key skills
- Join Israeli tech groups (Israeli High-Tech, Tel Aviv Startups)

**Search Tips:**
- Use "Israel" location filter
- Search for specific company names rather than generic titles
- Set job alerts for specific technologies + Israel
- Check "Easy Apply" for quick applications
- Follow Israeli tech recruiters for early access to positions

### JobMaster (jobmaster.co.il)

Israeli job platform with good tech coverage.

**Strengths:**
- Clean interface with good search capabilities
- Strong in the central Israel tech corridor
- Direct employer listings (fewer recruiter postings)
- Salary range transparency on many listings

**Profile Optimization:**
- Upload bilingual CV
- Set detailed preferences for technology, location, and salary range
- Enable email alerts for matching positions

### ATS Platforms Used by Israeli Startups

Many Israeli startups use international ATS platforms for their career pages:

| Platform | Used By | Tips |
|----------|---------|------|
| Comeet | Israeli startups, scale-ups | Apply directly, reference employee names |
| Lever | Mid-size Israeli tech companies | Tailored cover letter helps |
| Greenhouse | Larger Israeli tech companies | Follow company career pages |
| Workday | Enterprise companies with IL offices | Formal application process |
| BreezyHR | Smaller Israeli startups | Quick application, often founder reviews |

## CV Optimization

### Israeli CV Conventions

Israeli tech CVs have specific conventions that differ from US and European formats:

**Format Guidelines:**
- **Length**: 1-2 pages (1 page for junior, 2 for senior/lead)
- **Photo**: Not required and often discouraged. Israel's Employment (Equal Opportunities) Law prohibits discrimination based on appearance, making photo requests in hiring legally risky. Including a photo is your choice, but it is not expected
- **Personal details**: Name, phone (+972 format), email, LinkedIn URL, GitHub/portfolio
- **No marital status**: Do not include marital status, number of children, or date of birth (anti-discrimination law)
- **Military service**: Include if relevant tech experience (Unit 8200, Mamram, C4I, etc.). Non-combat service can be listed briefly or omitted
- **Education**: List degrees with institution name. Israeli universities are well-known locally, so no need to explain them
- **Languages**: List Hebrew (native), English (fluent/professional), and any other languages

**Section Order (recommended):**
1. Contact information
2. Professional summary (2-3 sentences)
3. Technical skills (categorized: languages, frameworks, tools, cloud)
4. Work experience (reverse chronological)
5. Military service (if tech-relevant)
6. Education
7. Certifications and courses (optional)
8. Languages

### Bilingual CV Strategy

Most Israeli tech candidates need two CV versions:

**Hebrew CV:**
- Use for positions at Israeli companies posting in Hebrew
- AllJobs, Drushim, and government sector roles
- Right-aligned text, Hebrew fonts (David, Arial Hebrew, Heebo)
- Technology names stay in English (React, Python, AWS)
- Job titles can be in Hebrew or English depending on the company

**English CV:**
- Use for international companies with Israel offices
- LinkedIn, Greenhouse, Lever applications
- Multinational companies (Google, Microsoft, Meta Israel offices)
- Startups targeting international markets

**Bilingual tips:**
- Keep both versions synchronized in content
- Technology terms always in English in both versions
- Company names in their original language
- Dates in international format (Jan 2024, not ינואר 2024) even in Hebrew CV
- Do not translate job titles literally (e.g., "ראש צוות" = "Team Lead", not "Head of Team")

### ATS-Friendly Formatting

```
DO:
- Use standard section headers
- Use standard fonts (Arial, Calibri, Heebo for Hebrew)
- Include exact technology names from the job posting
- Use bullet points, not paragraphs
- Save as PDF with text layer (not scanned image)
- File name: FirstName_LastName_CV.pdf

DO NOT:
- Use tables or columns (ATS may not parse correctly)
- Use headers/footers for important content
- Use images, icons, or graphics
- Use unusual section names
- Submit a Word document with Hebrew text issues
```

### Keyword Optimization for Israeli Tech Roles

Include both the full name and common abbreviations:

```
Backend:
  Node.js, Express, NestJS, Python, Django, FastAPI,
  Java, Spring Boot, Go, Golang, C#, .NET

Frontend:
  React, Next.js, Vue.js, Angular, TypeScript,
  JavaScript, HTML5, CSS3, Tailwind CSS

Mobile:
  React Native, Flutter, Swift, iOS, Kotlin, Android

DevOps/Cloud:
  AWS, GCP, Azure, Docker, Kubernetes, K8s,
  Terraform, CI/CD, Jenkins, GitHub Actions

Data:
  PostgreSQL, MongoDB, Redis, Elasticsearch,
  Kafka, RabbitMQ, SQL, NoSQL

AI/ML:
  Python, TensorFlow, PyTorch, LLM, NLP,
  Computer Vision, Machine Learning, Deep Learning

Israeli-specific:
  Startup experience, Scale-up, 0-to-1, Exit,
  Military tech background, Bilingual (Hebrew/English)
```

## Salary Benchmarking

### Israeli Tech Salary Ranges (2026)

Salary data based on public surveys (Ethosia, Hever Group, LinkedIn Salary Insights). All figures in gross monthly NIS.

#### Software Development

| Role | Junior (0-2 yrs) | Mid (2-5 yrs) | Senior (5-8 yrs) | Lead/Staff (8+ yrs) |
|------|------------------|----------------|-------------------|---------------------|
| Full Stack Developer | 18,000-25,000 | 25,000-35,000 | 35,000-50,000 | 50,000-70,000 |
| Backend Developer | 18,000-25,000 | 25,000-38,000 | 38,000-55,000 | 55,000-75,000 |
| Frontend Developer | 17,000-24,000 | 24,000-34,000 | 34,000-48,000 | 48,000-65,000 |
| Mobile Developer | 18,000-26,000 | 26,000-38,000 | 38,000-55,000 | 55,000-70,000 |
| Embedded Developer | 20,000-28,000 | 28,000-40,000 | 40,000-55,000 | 55,000-75,000 |

#### DevOps and Infrastructure

| Role | Junior (0-2 yrs) | Mid (2-5 yrs) | Senior (5-8 yrs) | Lead/Staff (8+ yrs) |
|------|------------------|----------------|-------------------|---------------------|
| DevOps Engineer | 20,000-28,000 | 28,000-42,000 | 42,000-60,000 | 60,000-80,000 |
| SRE | 22,000-30,000 | 30,000-45,000 | 45,000-65,000 | 65,000-85,000 |
| Cloud Engineer | 20,000-28,000 | 28,000-42,000 | 42,000-58,000 | 58,000-75,000 |

#### Data and AI

| Role | Junior (0-2 yrs) | Mid (2-5 yrs) | Senior (5-8 yrs) | Lead/Staff (8+ yrs) |
|------|------------------|----------------|-------------------|---------------------|
| Data Engineer | 20,000-28,000 | 28,000-42,000 | 42,000-60,000 | 60,000-80,000 |
| Data Scientist | 22,000-30,000 | 30,000-45,000 | 45,000-65,000 | 65,000-85,000 |
| ML Engineer | 22,000-32,000 | 32,000-48,000 | 48,000-70,000 | 70,000-90,000 |
| AI/LLM Engineer | 25,000-35,000 | 35,000-55,000 | 55,000-80,000 | 80,000-100,000 |

#### Management

| Role | Junior (0-2 yrs mgmt) | Mid (2-5 yrs mgmt) | Senior (5+ yrs mgmt) |
|------|----------------------|--------------------|--------------------|
| Team Lead | 40,000-55,000 | 55,000-70,000 | 70,000-85,000 |
| Engineering Manager | 50,000-65,000 | 65,000-80,000 | 80,000-100,000 |
| VP Engineering | N/A | 70,000-90,000 | 90,000-130,000 |
| CTO (startup) | N/A | 60,000-85,000 | 80,000-120,000+ |

#### Security

| Role | Junior (0-2 yrs) | Mid (2-5 yrs) | Senior (5-8 yrs) | Lead/Staff (8+ yrs) |
|------|------------------|----------------|-------------------|---------------------|
| Security Engineer | 20,000-28,000 | 28,000-42,000 | 42,000-60,000 | 60,000-80,000 |
| Security Researcher | 22,000-32,000 | 32,000-48,000 | 48,000-68,000 | 68,000-90,000 |
| CISO | N/A | N/A | 60,000-80,000 | 80,000-120,000 |

### Equity and Stock Options

Israeli startups commonly offer equity through the 102 ESOP (Employee Stock Option Plan) tax track:

**102 Capital Gains Track (Trustee):**
- Most common for Israeli tech employees
- Options held by a trustee for minimum 24 months
- Taxed at 25% capital gains rate (vs. up to 50% marginal income tax)
- The company does NOT get a tax deduction (trade-off for the employee's lower tax rate)

**Key terms to understand:**
- **Strike price**: The price you pay to exercise options
- **Vesting schedule**: Typically 4 years with 1-year cliff
- **Exercise window**: How long after leaving to exercise (standard: 90 days, some companies offer extended windows)
- **409A valuation**: The fair market value at time of grant (for US-incorporated companies with Israel offices)

**Evaluating equity offers:**
```
Questions to ask:
1. What percentage of the company do my options represent (fully diluted)?
2. What is the current 409A/fair market value?
3. What is the most recent fundraising valuation?
4. What is the vesting schedule? (Standard: 4-year, 1-year cliff)
5. Is it the 102 capital gains track (trustee)?
6. What happens to my options if acquired? (Single vs. double trigger)
7. What is the exercise window after departure?
8. How many funding rounds have occurred (dilution impact)?
```

### Benefits Package Comparison

Standard Israeli tech benefits to negotiate and compare:

| Benefit | Legal Minimum | Good Package | Excellent Package |
|---------|--------------|--------------|-------------------|
| Pension (employer) | 6.5% | 6.5% | 7-8% |
| Pension (employee) | 6% | 6% | 6-7% |
| Keren Hishtalmut (employer) | Not mandatory | 7.5% | 7.5% |
| Keren Hishtalmut (employee) | Not mandatory | 2.5% | 2.5% |
| Vacation days | 12-20 (by seniority) | 18-22 | 24-30 |
| Sick days | 18/year (1.5/month) | 18/year | Unlimited (trust-based) |
| Convalescence pay | 5-10 days (by seniority) | 5-10 days (by seniority) | 5-10 days (by seniority) |
| Work from home | Not mandatory | 2-3 days/week | Full flexibility |
| Education budget | Not standard | 5,000-10,000 NIS/year | 15,000+ NIS/year |
| Meals/food | Not mandatory | Cibus/10bis card | Cibus + office meals |
| Phone allowance | Not mandatory | Company phone | Phone + internet |
| Car allowance | Not mandatory | Rare for non-mgmt | 3,000-5,000 NIS/month |
| Annual bonus | Not standard | 1-2 months | 2-4 months |

**Keren Hishtalmut explained:**
This is a unique Israeli tax-advantaged savings fund. The employer contributes 7.5% and the employee 2.5% of salary (up to a ceiling). After 6 years (3 for specific purposes), withdrawals are tax-free. This is essentially an additional 7.5% salary bonus. Always negotiate for this benefit.

## Interview Preparation

### Israeli Tech Interview Culture

Israeli tech interviews tend to be direct and informal compared to US or European standards:

**Cultural norms:**
- First-name basis from the start, even with the CEO
- Direct communication style. Interviewers ask pointed questions, and you should give straightforward answers
- It is acceptable (and expected) to push back on interview questions or challenge assumptions
- "Chutzpah" (confidence, assertiveness) is valued, but do not confuse it with arrogance
- Interviewers genuinely want to see how you think, not just the right answer
- Hebrew small talk before the interview is common and appreciated
- Showing genuine curiosity about the company and product is important

### Common Israeli Interview Process

Most Israeli tech companies follow this structure:

**Stage 1: HR/Recruiter Screen (30-45 min)**
- Usually in Hebrew (unless the company is English-first)
- Background overview, motivation, salary expectations
- Cultural fit assessment
- They will ask about military service background (this is normal in Israel)
- Be prepared to share salary expectations early (Israelis are direct about money)

**Stage 2: Technical Interview (60-90 min)**
- Coding challenge (live or take-home)
- System design (for senior roles)
- Technology-specific deep dive
- Often conducted in English for international companies
- Whiteboard or shared editor (CoderPad, HackerRank)

**Stage 3: Team Fit / Cultural Interview (45-60 min)**
- Meet potential teammates
- Discuss work style and collaboration
- Often more relaxed, might include coffee or lunch
- May be conducted in Hebrew

**Stage 4: Hiring Manager / CTO Interview (30-60 min)**
- Strategic discussion about the role
- Architecture and technical vision
- May include a live problem-solving exercise
- This is where negotiation begins indirectly

**Stage 5: Offer and Negotiation**
- Initial offer usually by phone or email
- Always negotiate (it is expected in Israeli culture)
- Focus negotiation on: base salary, equity, keren hishtalmut percentage, vacation days, flexibility
- Reference check may happen before or after offer

### Negotiation Norms in Israel

```
DO:
- Research market rates before the interview (use this skill's salary data)
- Share your current compensation when asked (it is common in Israel)
- Negotiate multiple components, not just salary
- Ask for the offer in writing before making a decision
- Request 3-5 days to consider (longer is unusual in the fast Israeli market)
- Mention competing offers if you have them (this is expected)

DO NOT:
- Over-negotiate after accepting (this burns bridges in the small Israeli market)
- Bluff about competing offers you do not have (the market is small, people talk)
- Delay more than a week to respond (Israeli hiring moves fast)
- Focus only on salary (total compensation matters more)
- Undervalue keren hishtalmut (it is a significant tax-advantaged benefit)
```

### Common Technical Interview Questions (Israeli Focus)

**System design (for senior roles):**
- Design a payment processing system for the Israeli market (Shva integration, shekel transactions)
- Design a notification system supporting Hebrew/English with RTL layout
- Scale an application for Israeli traffic patterns (Sunday-Thursday work week, Jewish holidays)

**Coding challenges:**
- Standard LeetCode-style problems (arrays, strings, trees, graphs)
- Israeli companies tend to favor practical problems over pure algorithmic ones
- Be prepared for Hebrew variable names in pair programming sessions

**Architecture discussions:**
- Microservices vs. monolith (Israeli startups often start monolith, scale to microservices)
- Multi-region deployment considerations (Israeli data sovereignty)
- Event-driven architecture patterns

## Application Tracking

### Tracking Template

Use this template to track your job applications across Israeli platforms:

```
# Application Tracker

## Active Applications

| Company | Role | Platform | Applied | Status | Next Step | Contact | Follow-up Date |
|---------|------|----------|---------|--------|-----------|---------|----------------|
| Example Ltd | Senior BE | LinkedIn | 2026-03-10 | Phone Screen | HR Call 3/15 | Yael (HR) | 2026-03-15 |
| Startup X | Full Stack | Comeet | 2026-03-08 | Technical | Coding Test | David (CTO) | 2026-03-14 |

## Status Legend
- Applied: Application submitted
- Phone Screen: HR/recruiter call scheduled or completed
- Technical: Technical interview stage
- Team Fit: Cultural/team interview
- Offer: Received offer
- Negotiation: Negotiating terms
- Accepted: Offer accepted
- Declined: Position declined
- Rejected: Not selected

## Follow-up Rules
- After applying: Follow up after 5 business days if no response
- After phone screen: Send thank you email within 24 hours
- After technical: Follow up after 3 business days
- After team fit: Follow up after 3 business days
- During offer: Respond within 3-5 business days
```

### Follow-up Timing for Israeli Companies

Israeli business culture is fast-paced. Appropriate follow-up timing:

- **After submitting application**: 3-5 business days (keep in mind Sunday-Thursday work week)
- **After phone screen**: Same day thank-you email, follow up after 3 days if no update
- **After technical interview**: Thank-you within 24 hours, follow up after 3-5 days
- **After final interview**: Follow up after 3 days if no response
- **Negotiation phase**: Respond to offers within 3-5 days (do not delay longer)

**Note on Israeli calendar:** Remember that the Israeli work week runs Sunday to Thursday. Friday is a short day (many offices close by 14:00). Do not send follow-up emails on Friday afternoon or Saturday (Shabbat). Major Jewish holidays (Rosh Hashana, Yom Kippur, Sukkot, Pesach) slow hiring significantly.

### Referral Networking on LinkedIn Israel

The Israeli tech market is small and heavily referral-driven:

```
Networking Strategy:
1. Identify target companies
2. Search for 1st and 2nd degree connections at each company
3. Reach out with a personal message (Hebrew or English, match their profile language)
4. Be specific about the role you are interested in
5. Ask for an informational call, not a direct referral
6. After the call, ask if they would be comfortable referring you
7. Most Israeli companies offer referral bonuses (3,000-15,000 NIS),
   so employees are generally happy to refer good candidates

Message Template (English):
"Hi [Name], I noticed you work at [Company] as [Role]. I'm exploring
[specific role/team] and would love to hear about your experience there.
Would you have 15 minutes for a quick call? Happy to share insights
about [your current domain] in return."

Message Template (Hebrew):
"היי [שם], ראיתי שאתה עובד/ת ב-[חברה] בתפקיד [תפקיד]. אני בודק/ת
אפשרות ל-[תפקיד ספציפי] ואשמח לשמוע על החוויה שלך שם. יש לך
15 דקות לשיחה קצרה? אשמח לשתף תובנות מ-[התחום שלך] בתמורה."
```

## Legal Rights for Job Seekers

### Israeli Employment Law Basics

Key legal rights you should know as a tech job seeker in Israel:

**Trial Period:**
- No statutory maximum, but most companies use 3-6 months
- Same rights and benefits apply during the trial period
- Either party can terminate with shorter notice during the trial
- Pension contributions are mandatory (retroactive from day one after a 6-month waiting period for new employees without prior pension insurance)

**Notice Period:**
- First 6 months: 1 day per month of employment
- Months 7-12: 6 days plus 2.5 days per additional month worked
- After first year: 1 month notice
- Most senior tech roles negotiate 1-3 months notice in the contract
- Notice period is mutual (you cannot be forced to leave immediately unless cause exists)
- Garden leave: employer may send you home during notice period (still paid)

**Non-Compete Limitations:**
- Israeli courts generally do not enforce broad non-compete clauses
- Non-competes are enforceable only if they are:
  - Limited in scope (specific competitors, not entire industry)
  - Limited in time (typically up to 12 months)
  - Compensated (some courts require additional compensation for non-compete periods)
  - Protecting a legitimate business interest (trade secrets, customer relationships)
- The Supreme Court has repeatedly ruled in favor of employee mobility
- Non-solicitation clauses (of clients/employees) are more enforceable than non-compete

**Overtime and Work Hours:**
- Standard work week: 42 hours (since 2018 reform)
- Tech employees in "trust positions" (senior roles, managers) are often exempt from overtime tracking
- Flex time and WFH policies vary by company

**Termination Rights:**
- Severance pay ("pitzuim"): 1 month salary per year of employment
- Most Israeli tech companies use "Section 14" arrangement (severance deposited monthly to pension fund)
- Unused vacation days must be paid upon termination
- Keren hishtalmut becomes available per the fund's terms

**Pension and Social Benefits (from day one):**
- Pension: employer 6.5%, employee 6% (of salary up to ceiling)
- Severance contribution: 8.33% (part of pension, "Section 14")
- Disability insurance: typically included in pension package
- Keren hishtalmut: common in tech, 7.5% employer + 2.5% employee (up to a ceiling)

## Running the Tools

Use the included scripts for CV analysis and salary benchmarking:

```bash
# Analyze your CV and get improvement suggestions
python scripts/cv-optimizer.py --cv /path/to/your-cv.pdf --role "Senior Backend Developer"

# Quick salary lookup
python scripts/salary-benchmark.py --role "full-stack" --experience 5
python scripts/salary-benchmark.py --role "devops" --experience 3 --format json

# List all available roles
python scripts/salary-benchmark.py --list-roles
```

Refer to the `references/` directory for detailed platform guides and salary data.
