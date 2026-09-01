---
name: israeli-cv-builder
description: "Not legal advice. Generate a ready-to-send Israeli CV (korot chayim / קורות חיים) in Hebrew, English, or both: one page by default, reverse chronological, a military or national service section, dugri (direct) language, metrics-driven bullets, plus an optional Israeli cover letter (michtav mukdam / מכתב מקדים). Use when writing a CV for Israel, building a resume for AllJobs, Drushim, JobMaster, JobNet or LinkedIn Israel, preparing a bilingual tech CV, or drafting an Israeli-style cover letter. Automatically omits age, marital status and religion, grounds on which the Equal Employment Opportunities Law 1988 prohibits discrimination, and omits the photo as market convention. Do NOT use for job market research (use israeli-job-market), tech interview prep (use israeli-tech-interview-prep), salary negotiation (use israeli-tech-salary-negotiator), LinkedIn strategy (use israeli-linkedin-strategy), employer-side screening (use israeli-hr-recruitment-automator), or employment contract review."
license: MIT
allowed-tools: ''
compatibility: Works with Claude, Claude Code, ChatGPT, Cursor, and any agent supporting markdown output. No API keys required.
---

# Israeli CV Builder

## Legal notice

This skill is a free information tool operated by an AI model. It formats a CV and an optional cover letter from details the user supplies, and it summarises published Israeli employment-law rules in order to explain which personal details to leave off the document. It produces no legal opinion, and no lawyer reviews or approves its output at any stage. The legal summaries are general information about published statutes, not advice on the user's own case, and an AI model can err, omit a provision, or state a rule wrongly. Do not rely on anything here as the basis for a claim, for a complaint to the Equal Employment Opportunities Commission, or for any step in a dispute with an employer. It is not a substitute for advice that takes account of the particular circumstances and needs of each person, and anyone facing an actual discrimination question should consult a lawyer.

## Problem
Israeli job seekers waste hours rewriting CVs because the local conventions differ from American and European formats: one page by default, reverse chronological, a military or national service section Israeli recruiters expect to find, dugri (direct) language, and a firm market convention of no photo, no age, and no marital status. Most online CV builders default to US templates that either get rejected by Israeli HR or push the candidate into volunteering exactly the data the Equal Employment Opportunities Law 1988 makes costly for an employer to hold. This skill produces a ready-to-send Israeli CV in Hebrew and/or English in one pass, plus an optional tailored cover letter.

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
| Military / national service | If the candidate served | Unit type, role, rank, dates. Israeli recruiters look for it. Many citizens do not serve, so never treat its absence as an anomaly |
| Education | Yes | Degree, institution, year. Below work experience unless recent grad or student |
| Languages | Yes | With proficiency level (native / fluent / professional / basic) |
| Technical skills | Tech roles | Ordered by recency and depth |
| Generate cover letter? | Yes/No | Ask explicitly. Default to No unless user says yes |

### Step 2: Enforce Equal Employment Law Compliance

Under Employment (Equal Opportunities) Law 5748-1988, section 2(א), an Israeli employer may not **discriminate** among employees or job applicants on grounds of sex, sexual orientation, personal status, pregnancy, fertility treatments, IVF treatments, parenthood, age, race, religion, nationality, country of origin (ארץ מוצא), place of residence (מקום מגורים), worldview (השקפה), political party, or reserve service, in hiring, terms of employment, promotion, vocational training, dismissal or severance pay, and retirement-related benefits. The reserve-service ground also covers the reserve service of a spouse or of a child's other parent, including its frequency or duration.

**Get the mechanism right, because agents routinely state it wrong.** The Law does not, as a general rule, make the *question* an offence. What it does is evidential, and that is the real reason to keep this data off the CV:

- **Section 9(ג)**: once it is proved the employer demanded such information, directly or indirectly, the burden shifts to the employer to prove it did not discriminate.
- **Section 15(ד)**: the same demand raises a rebuttable presumption of guilt in a criminal proceeding.
- **Section 21(ג) limits all of it**: the Law, except section 7, does not apply to an employer of fewer than six employees, and the headcount includes manpower-contractor workers placed with that employer. A candidate applying to a very small Israeli business gets none of this machinery, which is a reason to keep the data off the CV rather than to rely on the Law afterwards.

So volunteering age, marital status, or a photo hands the employer information it had every incentive not to hold, and throws away the candidate's later evidential advantage. Never tell a user "it is illegal for them to ask" as a blanket statement, because as a rule it is not. Two genuine prohibitions on asking do exist, and they sit elsewhere:

| Prohibition | Source | What it means for the CV |
|---|---|---|
| Military profile (פרופיל צבאי) | Section 2א of this Law. The employer may not demand it, nor use it if it reaches them, and may not penalise a refusal to hand it over. (The Shin Bet and the Mossad as employers are carved out.) | NEVER put the profile number on the CV in either language. It is the IDF numeric medical-fitness code, and it is separate from the unit and role, which do belong on the CV |
| Criminal record | Criminal Information and Rehabilitation of Offenders Law, 5779-2019 (חוק המידע הפלילי ותקנת השבים) | The Law controls who may receive criminal information. Where an employer may get it at all, the route runs through the police with the candidate's prior written consent, not through the CV. Do not add a "no criminal record" line, and do not advise the user to volunteer one |

**Disability sits in a different statute and is NOT in the section 2(א) list.** Employment discrimination on grounds of disability is governed by the Equal Rights for Persons with Disabilities Law, 5758-1998, section 8(א), which covers acceptance for employment including admission tests. Section 8(ה) defines discrimination to INCLUDE failing to make the accommodations a person with a disability needs in order to be employed, and expressly counts recruitment tests, working hours, equipment and job requirements among those accommodations, subject only to a "disproportionate burden" limit. There is no employee-count threshold. Practical rule for the CV: do not put a disability on it, and raise any accommodation the candidate needs for an interview or an admission test separately and in writing, once a process is under way.

**NEVER include any of these on an Israeli CV, even if the user provides them:**

| Field | Reason | What to do |
|-------|--------|------------|
| Date of birth | Age is a protected ground. Section 9(ג) bites when the EMPLOYER demands the information, so volunteering it hands over the data and forfeits that burden shift | Omit silently. Do not mention |
| Photograph | Market convention plus bias avoidance. No Israeli statute regulates CV photographs, but a photo puts age, sex, and ethnicity in front of the employer | Omit for EN. For HE, omit by default and only include if user explicitly requests AND the role is non-tech (acting, hospitality) |
| Military profile (פרופיל צבאי) | The employer may not lawfully demand it (section 2א), so there is no reason to supply it unasked | Omit. Keep unit, role, rank, dates |
| Marital status | Personal status is a protected ground | Omit |
| Number of children / parental status | Parenthood is a protected ground | Omit |
| Pregnancy, fertility or IVF treatment | Pregnancy, fertility treatments and IVF treatments are three separate protected grounds under s.2(א) | Omit. Never mention it in the CV or the cover letter |
| Religion | Protected ground | Omit |
| Teudat Zehut (ID number) | Privacy risk, no legitimate reason on a CV | Omit |
| Home address | Place of residence is a protected ground; city only is sufficient for commute signaling | Keep city, drop street |
| Nationality / country of origin | Both are protected grounds; only include if the role genuinely requires work-permit clarification | Default off |

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

4. Military / National Service (if the candidate served)
   - Unit name or type (e.g., "Intelligence Corps, Unit 8200", "Armored Corps, 7th Brigade")
   - Role and rank (e.g., "Team Leader, Sergeant First Class")
   - Dates (YYYY - YYYY)
   - 1-2 bullets on transferable skills (leadership, cleared projects at declassified level, systems maintained)
   - Confidentiality is governed by the discharge undertaking and the unit security officer, not by the candidate's judgment. Default to the corps name (Intelligence Corps, Armored Corps). Name a specific unit or role only where it is already public and permitted
   - National service (שירות לאומי / שירות אזרחי) belongs here under its own name
   - If the candidate did not serve, omit the section. Never write "did not serve" or "exempt" and never explain the gap

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
- Avoid formal biblical Hebrew. Use modern tech Israeli Hebrew: "פיתחתי", "הובלתי", "שיפרתי", not "הנני מתכבד" or "התכבדתי"

### Step 6: Generate the Output

Output the CV as clean markdown that converts well to .docx via pandoc or Word paste. Use H1 for name, H2 for section headers, H3 for company names. Bullets with `- ` prefix. Dates right-aligned via trailing spaces (markdown does not enforce alignment, the user formats in Word after).

Give the user three things:
1. The CV in markdown
2. The pandoc command to convert to .docx, **which is not the same command for the two languages**:
   ```bash
   # English
   pandoc cv.md -o cv.docx
   # Hebrew: dir must be passed as METADATA (-M). Plain `pandoc cv_he.md -o cv_he.docx`
   # produces a left-to-right document, and `-V dir=rtl` is a silent no-op.
   pandoc cv_he.md -M dir=rtl -M lang=he -o cv_he.docx
   ```
3. A list of target keywords from the job description that were included (so the user sees the ATS tailoring)

Do not use markdown tables for Hebrew CV layout. Pandoc does not emit `w:bidiVisual` for tables, so table columns mirror wrongly in Word even with `-M dir=rtl` (pandoc issue #7695, open). Use headings and bullets, which do respect the flag.

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

1. **Including a photo on English CVs**. Agents default to "professional CVs look nicer with a photo", which is wrong for Israel. Omit always for EN, by default for HE. State the reason accurately: it is market convention plus bias avoidance. It is NOT an ATS limitation (modern parsers handle images fine) and it is NOT a statutory rule, since no Israeli law regulates CV photographs.

2. **Listing date of birth because the user mentioned it**. Even if the user writes "I'm 34 years old", never put age or birth date on the CV. Silently drop it. Do not justify this by telling the user "it is illegal to ask your age". The Equal Employment Opportunities Law 1988 prohibits discriminating on age, and makes demanding the information shift the burden of proof onto the employer (section 9(ג)), which is a different and more defensible thing to say.

3. **Using formal biblical Hebrew instead of modern tech Hebrew**. Agents pull from religious or legal corpora and produce "הנני מתכבד להגיש" instead of "שלום, אני {שם}". Israeli tech HR reads it as tone-deaf. Use direct modern Israeli phrasing.

4. **Inventing military unit names**. If the user says "I was in intelligence", do NOT guess they were in 8200. Ask, or write the corps name "חיל המודיעין / Intelligence Corps", which is the safe default. Inventing a specific unit is a credibility-killer if the user is called on it in an interview.

5. **Translating word-for-word between Hebrew and English**. Hebrew bullets and English bullets are not the same text in two languages. They use different verb structures and idioms. Regenerate each language independently from the same source facts.

6. **Keeping US-format phone numbers or addresses**. If the user copy-pastes a US-style resume, the agent often leaves "+1 (555) 123-4567" and "123 Main St, San Francisco, CA 94102" in place. Convert to Israeli phone format and drop the street address (city only).

7. **Padding junior CVs to 2 pages**. Juniors with no experience think more words = better. They do not. Israeli HR prefers a tight 1-page CV with 3 strong bullets over a 2-page CV with 10 weak ones.

8. **Writing the military profile into the military section**. If the user volunteers "profile 97", drop it. Section 2א bars the employer from demanding the profile at all, so putting it on the CV gives away something they could not lawfully have asked for. Unit, role, rank, and dates stay.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Employment (Equal Opportunities) Law, 5748-1988 (Hebrew, Nevo) | https://www.nevo.co.il/law_html/law01/p214m1_001.htm | The authority. Section 2(א) grounds, section 2א military profile, sections 9 and 15 burden of proof and presumption |
| Employment (Equal Opportunities) Law 5748-1988 (unofficial English rendering) | https://www.icj.org/wp-content/uploads/2013/05/Israel-Employment-Equal-Opportunities-Law-5748-1988-eng.pdf | Readable English, but current only to roughly 2004. Its section 2(a) is missing pregnancy, fertility treatments, IVF, parenthood, and place of residence. Never cite it as the list of protected grounds |
| Equal Rights for Persons with Disabilities Law, 5758-1998 | https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%A9%D7%95%D7%95%D7%99%D7%95%D7%9F_%D7%96%D7%9B%D7%95%D7%99%D7%95%D7%AA_%D7%9C%D7%90%D7%A0%D7%A9%D7%99%D7%9D_%D7%A2%D7%9D_%D7%9E%D7%95%D7%92%D7%91%D7%9C%D7%95%D7%AA | Section 8(א) hiring discrimination and section 8(ה) accommodation duty, which is where disability lives (it is NOT in the 1988 Law) |
| Equal Employment Opportunities Commission (נציבות שוויון הזדמנויות בעבודה) | https://www.gov.il/he/departments/units/equal-opportunities-at-work-unit | The civil enforcement body, under the Ministry of Economy and Industry. Complaint channels and current guidance |
| Israeli Employment Service: full guide to writing a CV | https://campus.gov.il/course/taasuka-gov-career-cvbuilding101-he/ | Free official Hebrew course on CV writing from שירות התעסוקה |
| Nefesh B'Nefesh: Israeli Resume Do's and Don'ts | https://www.nbn.org.il/aliyah-inspiration/nbn-blogger-network/nbn-employment-blog/writing-your-israeli-resume-the-dos-and-donts/ | Aliyah-specific CV guidance for olim |
| Anglo-List: Preparing a stand-out resume for Israel | https://anglo-list.com/your-israel-resume/ | Tone, length, and section order. Commercial and undated, treat as convention not authority |

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| CV is 2 pages for a junior | Too many bullets per role, too much padding in summary | Cut summary to 3 lines, max 3 bullets per role, drop any role under 6 months unless directly relevant |
| Hebrew CV reads as translated English | Word-for-word translation from EN draft | Regenerate HE from source facts, not from EN text. Use active Israeli tech verbs |
| User insists on including age | They are older and want to front-load experience | Warn once about EEO Law, then respect choice only for personal copy, never for the ATS-submitted version |
| Military section is empty | The candidate did not serve. Common for Arab citizens, Haredi candidates, anyone with a medical or other exemption, and olim | Omit the section entirely. Do not write "Did not serve" or "Exempt" and do not explain the gap. If they did שירות לאומי or שירות אזרחי, list it here under its own name. Otherwise replace with a "Volunteer / Community" section if relevant |
| Phone number has wrong format | Copied from a US resume | EN: `+972-XX-XXX-XXXX`. HE: `0XX-XXX-XXXX` |
| Cover letter is too long | Default verbosity | Cut to 3 paragraphs, max 250 words EN / 200 words HE. Rewrite paragraph 2 to link 2 achievements to 2 company needs |
| Hebrew .docx opens left-aligned in Word | `pandoc cv_he.md -o cv_he.docx` emits no `w:bidi`, so Word treats the paragraphs as LTR. `-V dir=rtl` does nothing at all, because the docx writer reads `dir` from metadata, not from a template variable | Re-run as `pandoc cv_he.md -M dir=rtl -M lang=he -o cv_he.docx`. Verify in Microsoft Word, not LibreOffice, which hides Word-only RTL bugs |
| Hebrew table columns are mirrored in Word | Pandoc does not emit `w:bidiVisual` for tables (issue #7695, open); `-M dir=rtl` does not fix it | Do not use markdown tables in a Hebrew CV. Use headings and bullets |
