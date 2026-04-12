---
name: israeli-cv-builder
description: "Generate a ready-to-send Israeli CV (korot chayim / קורות חיים) in Hebrew, English, or both: 1-page reverse chronological, mandatory military service section, dugri (direct) language, metrics-driven bullets, plus an optional Israeli cover letter (michtav mukdam / מכתב מקדים). Use when writing a CV for Israel, building a resume for AllJobs, Drushim, JobMaster or LinkedIn Israel, preparing a bilingual tech CV, or drafting an Israeli-style cover letter. Automatically omits personal data prohibited by the Equal Employment Opportunities Law 1988 (age, photo, marital status, religion) to prevent discrimination risk. Do NOT use for job market research (use israeli-job-market), tech interview prep (use israeli-tech-interview-prep), salary negotiation (use israeli-tech-salary-negotiator), LinkedIn strategy (use israeli-linkedin-strategy), employer-side screening (use israeli-hr-recruitment-automator), or employment contract review."
license: MIT
allowed-tools: ''
compatibility: Works with Claude, Claude Code, ChatGPT, Cursor, and any agent supporting markdown output. No API keys required.
---

# Israeli CV Builder

## Problem
Israeli job seekers waste hours rewriting CVs because the local conventions differ from American and European formats: 1-page reverse chronological, a mandatory military service section that tech HR scans first, dugri (direct) language, and a strict no-photo / no-age / no-marital-status rule under the Equal Employment Opportunities Law 1988. Most online CV builders default to US templates that either get rejected by Israeli HR or expose the candidate to discrimination claims. This skill produces a ready-to-send Israeli CV in Hebrew and/or English in one pass, plus an optional tailored cover letter.

## Instructions

### Step 1: Collect Inputs

Ask the user for the minimum viable inputs. Do not require everything up front, fill gaps with reasonable defaults and flag what is missing.

| Input | Required | Notes |
|-------|----------|-------|
| Target language | Yes | `he`, `en`, or `both`. If applying to Israeli startup with English website, offer `both` |
| Target role / job description | Yes | Paste full listing or describe the role. Drives keyword tailoring |
| Full name, phone, email, city | Yes | Phone in `+972-XX-XXX-XXXX` format for EN, `0XX-XXX-XXXX` for HE |
| LinkedIn URL | Recommended | Standard on Israeli tech CVs |
| GitHub / portfolio URL | Tech roles only | Put next to LinkedIn |
| Work history | Yes | Company, role, dates, 3-5 bullet achievements each |
| Military service | If Israeli citizen | Unit type, role, rank, dates. Critical for Israeli HR |
| Education | Yes | Degree, institution, year. Below work experience unless recent grad or student |
| Languages | Yes | With proficiency level (native / fluent / professional / basic) |
| Technical skills | Tech roles | Ordered by recency and depth |
| Generate cover letter? | Yes/No | Ask explicitly. Default to No unless user says yes |

### Step 2: Enforce Equal Employment Law Compliance

Under Employment (Equal Opportunities) Law 5748-1988, Israeli employers cannot make hiring decisions based on age, gender, race, religion, marital status, parental status, sexual orientation, political affiliation, or reserve duty. Asking for these on a CV exposes the employer to discrimination claims.

**NEVER include any of these on an Israeli CV, even if the user provides them:**

| Field | Reason | What to do |
|-------|--------|------------|
| Date of birth | Age discrimination risk under Law 5748-1988 | Omit silently. Do not mention |
| Photograph | ATS-unfriendly for EN CVs; invites appearance, age, gender, and ethnicity bias | Omit for EN. For HE, omit by default and only include if user explicitly requests AND the role is non-tech (acting, hospitality) |
| Marital status | Protected under Law 5748-1988 | Omit |
| Number of children / parental status | Protected | Omit |
| Religion | Protected | Omit |
| Teudat Zehut (ID number) | Privacy risk, no legitimate reason on a CV | Omit |
| Home address | City only is sufficient for commute signaling | Keep city, drop street |
| Nationality / citizenship | Only include if role requires work permit clarification | Default off |

If the user insists on including one of these (e.g., "I want a photo"), warn them once with the reason, then respect their choice for the Hebrew version only. Never add a photo to the English version.

### Step 3: Build CV Skeleton

Use this structure for both languages. Content is tailored per role, the skeleton stays constant.

```
1. Header
   - Full name (large, top center or top left)
   - City (not full address) | Phone | Email | LinkedIn | GitHub (tech only)

2. Professional Summary (3-4 lines max)
   - Years of experience + domain + 2-3 standout strengths
   - Must include 2-3 keywords from the target job description

3. Work Experience (reverse chronological)
   - Company name, role, dates (MM/YYYY - MM/YYYY or "Present")
   - City (Tel Aviv, Herzliya, Petah Tikva, remote, etc.)
   - 3-5 bullet points per role
   - Each bullet: action verb + what + quantified result
   - Example: "Reduced deployment time from 45min to 6min by migrating CI from CircleCI to GitHub Actions (saved 80 eng-hours/month)"

4. Military Service (Israeli citizens only)
   - Unit name or type (e.g., "Intelligence Corps, Unit 8200", "Armored Corps, 7th Brigade")
   - Role and rank (e.g., "Team Leader, Sergeant First Class")
   - Dates (YYYY - YYYY)
   - 1-2 bullets on transferable skills (leadership, cleared projects at declassified level, systems maintained)
   - NEVER include classified info. If uncertain, list only role title and skill area

5. Education
   - Institution, degree, major, year of graduation
   - Honors (cum laude, magna cum laude / בהצטיינות)
   - Relevant thesis or final project for recent grads only

6. Skills (for tech roles)
   - Languages: Python, Go, TypeScript, ...
   - Frameworks: React, Django, NestJS, ...
   - Infrastructure: AWS, Kubernetes, Terraform, ...
   - Tools: Git, Docker, Datadog, ...
   - Order by depth and recency, not alphabetical

7. Languages
   - Hebrew: Native / Fluent / Professional / Basic
   - English: ...
   - Additional languages only if at professional level or above

8. Additional (optional, only if space allows and relevant)
   - Open source contributions (with repo links)
   - Speaking engagements at local meetups (TLV Dev, Big Things, etc.)
   - Certifications (AWS, Azure, Google Cloud, CISSP)
```

### Step 4: Apply Israeli Tone and Format Rules

| Rule | What it means | Example |
|------|--------------|---------|
| Dugri language | Direct, no fluff, no marketing speak | Bad: "Spearheaded synergistic cross-functional initiatives". Good: "Led 4-person team to ship feature X in Q3" |
| Quantify everything | Numbers beat adjectives | Bad: "Improved performance significantly". Good: "Reduced p95 latency from 800ms to 120ms" |
| Keywords from job posting | ATS-friendly tailoring | If posting mentions "Kafka", include it in skills AND in a bullet if relevant |
| 1 page for juniors and mid-level | Senior (10+ yrs) may use 2 pages | Ruthlessly cut internships, student jobs if you have 5+ years experience |
| Active verbs | Past tense for past roles, present for current | Built, launched, migrated, owned, scaled, automated, shipped |
| No first person pronouns | Bullets start with verb, not "I" | Bad: "I built a pipeline". Good: "Built a pipeline that processed 10M events/day" |

### Step 5: Language-Specific Rules

**English CV:**
- Left-to-right (LTR) layout
- Phone format: `+972-50-123-4567`
- Dates: `MM/YYYY - MM/YYYY` or `Jan 2023 - Present`
- NO photograph ever
- Use American English spelling only if the role is at a US HQ startup. Otherwise British English is also fine
- Military unit names in English (e.g., "8200 Intelligence Unit")

**Hebrew CV:**
- Right-to-left (RTL) layout
- Phone format: `050-123-4567` (no country code needed)
- Dates in Gregorian calendar: `01/2023 - היום`
- Use gender-neutral phrasing where possible. When impossible, match the user's gender. Never assume
- Military unit names in Hebrew: "מודיעין - יחידה 8200", "שריון - חטיבה 7"
- Photo omitted by default
- Avoid formal biblical Hebrew. Use modern tech Israeli Hebrew: "פיתחתי", "הובלתי", "שיפרתי", not "ביצעתי" or "הוויתי"

### Step 6: Generate the Output

Output the CV as clean markdown that converts well to .docx via pandoc or Word paste. Use H1 for name, H2 for section headers, H3 for company names. Bullets with `- ` prefix. Dates right-aligned via trailing spaces (markdown does not enforce alignment, the user formats in Word after).

Give the user three things:
1. The CV in markdown
2. A one-line pandoc command to convert to .docx: `pandoc cv.md -o cv.docx`
3. A list of target keywords from the job description that were included (so the user sees the ATS tailoring)

### Step 7: Optional Cover Letter (only if user said yes)

Ask ONCE in Step 1 whether to generate a cover letter. If yes, output it AFTER the CV in a separate code block.

**Israeli cover letter rules:**

- 3-4 short paragraphs maximum. Israeli HR skims, they do not read
- No "Dear Hiring Manager" filler. Open with hook: why this specific role, this specific company
- Paragraph 1: Why them. One sentence on why this company specifically (product, mission, recent news)
- Paragraph 2: Why you. 2-3 sentences tying your top 2 achievements to their stated needs
- Paragraph 3: Concrete next step. "Happy to walk through my work on X in a 20-min call"
- Sign off: "Thanks, {Name}" in EN. "תודה, {שם}" in HE
- No more than 250 words in EN, no more than 200 in HE
- No passive voice. No "I would be thrilled to". No "I am writing to apply for"

## Bundled Resources

### References

| File | Purpose |
|------|---------|
| `references/israeli-cv-structure.md` | Full section-by-section Israeli CV template with field-level notes |
| `references/cover-letter-templates.md` | 3 Israeli cover letter templates (tech IC, manager, career changer) in HE and EN |
| `references/eeo-compliance-checklist.md` | Equal Employment Opportunities Law 1988 checklist for what to exclude from a CV |

### Scripts

| File | Purpose |
|------|---------|
| `scripts/cv_keyword_extractor.py` | Extracts ATS keywords from a pasted job description for CV tailoring |

## Recommended MCP Servers

This skill is standalone and does not require an MCP server. The CV is generated entirely from user-provided inputs.

| MCP | When to pair | Purpose |
|-----|--------------|---------|
| None required | N/A | Skill is self-contained. For market research and salary benchmarks, use the `israeli-job-market` skill separately before this one |

## Gotchas

These are the most common mistakes AI agents make when writing Israeli CVs. Each item reflects a real failure mode observed in practice.

1. **Including a photo on English CVs**. US ATS systems cannot parse photos and Israeli EEO law makes photos a discrimination risk. Agents default to "professional CVs look nicer with a photo" which is wrong for Israel. Always omit for EN, omit by default for HE.

2. **Listing date of birth because the user mentioned it**. Even if the user writes "I'm 34 years old", never put age or birth date on the CV. Silently drop it. Asking age on a job application is illegal under the Equal Employment Opportunities Law 1988.

3. **Using formal biblical Hebrew instead of modern tech Hebrew**. Agents pull from religious or legal corpora and produce "הנני מתכבד להגיש" instead of "שלום, אני {שם}". Israeli tech HR reads it as tone-deaf. Use direct modern Israeli phrasing.

4. **Inventing military unit names**. If the user says "I was in intelligence", do NOT guess they were in 8200. Ask or write the generic "חיל המודיעין / Intelligence Corps". Inventing a specific unit is a credibility-killer if the user is called on it in an interview.

5. **Translating word-for-word between Hebrew and English**. Hebrew bullets and English bullets are not the same text in two languages. They use different verb structures and idioms. Regenerate each language independently from the same source facts.

6. **Keeping US-format phone numbers or addresses**. If the user copy-pastes a US-style resume, the agent often leaves "+1 (555) 123-4567" and "123 Main St, San Francisco, CA 94102" in place. Convert to Israeli phone format and drop the street address (city only).

7. **Padding junior CVs to 2 pages**. Juniors with no experience think more words = better. They do not. Israeli HR prefers a tight 1-page CV with 3 strong bullets over a 2-page CV with 10 weak ones.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Employment (Equal Opportunities) Law 5748-1988 (official English text) | https://www.icj.org/wp-content/uploads/2013/05/Israel-Employment-Equal-Opportunities-Law-5748-1988-eng.pdf | Protected categories that must NOT appear on a CV |
| Wikipedia: Employment (Equal Opportunities) Law, 1988 | https://en.wikipedia.org/wiki/Employment_(Equal_Opportunities)_Law,_1988 | Overview of the law and its amendments |
| Nevo legal database: Equal Opportunities Law text | https://www.nevo.co.il/law_html/law01/055_002.htm | Hebrew source of the law |
| Nefesh B'Nefesh: Israeli Resume Do's and Don'ts | https://www.nbn.org.il/aliyah-inspiration/nbn-blogger-network/nbn-employment-blog/writing-your-israeli-resume-the-dos-and-donts/ | Aliyah-specific CV guidance for olim |
| JobMob: Israeli CV translation tips | https://jobmob.co.il/blog/israeli-cv-translation-tips/ | Converting foreign resumes to Israeli format |
| Anglo-List: Preparing a stand-out resume for Israel | https://anglo-list.com/your-israel-resume/ | Tone, length, and section order |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| CV is 2 pages for a junior | Too many bullets per role, too much padding in summary | Cut summary to 3 lines, max 3 bullets per role, drop any role under 6 months unless directly relevant |
| Hebrew CV reads as translated English | Word-for-word translation from EN draft | Regenerate HE from source facts, not from EN text. Use active Israeli tech verbs |
| User insists on including age | They are older and want to front-load experience | Warn once about EEO Law, then respect choice only for personal copy, never for the ATS-submitted version |
| Military section is empty because user is oleh chadash | Did not serve in IDF | Omit the section entirely. Do not write "Did not serve". Replace with a "Volunteer / Community" section if relevant |
| Phone number has wrong format | Copied from a US resume | EN: `+972-XX-XXX-XXXX`. HE: `0XX-XXX-XXXX` |
| Cover letter is too long | Default verbosity | Cut to 3 paragraphs, max 250 words EN / 200 words HE. Rewrite paragraph 2 to link 2 achievements to 2 company needs |
