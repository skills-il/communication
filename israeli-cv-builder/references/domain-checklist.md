# Domain coverage checklist: israeli-cv-builder

Scope: produce a ready-to-send Israeli CV and an optional cover letter, and decide what personal
data stays off the document. The legal content exists to justify those omissions. It is not a
general Israeli employment-rights reference.

Last reviewed: 2026-09-01 (v1.1.0).

## Must cover (core)

| # | Item | Why it is core |
|---|------|----------------|
| 1 | Section 2(א) protected grounds, complete and current, including השקפה as distinct from מפלגה, fertility treatments as distinct from IVF, and the reserve-service limb covering a spouse or a child's other parent and its frequency and duration | חוק שוויון ההזדמנויות בעבודה, התשמ"ח-1988, ס' 2(א). The omit-list is derived from it, so an incomplete list produces an incomplete omit-list |
| 2 | The six heads the duty attaches to, including 2(א)(6) retirement-related benefits | Same, ס' 2(א)(1)-(6) |
| 3 | The mechanism stated correctly: the Law bans discrimination, not the question. ס' 9(ג) shifts the burden once a demand for the information is proved; ס' 15(ד) raises a rebuttable presumption in a criminal proceeding | Same, ס' 9(ג), 15(ד). Stating "it is illegal to ask" is the defect this checklist exists to prevent recurring |
| 3a | The applicability limit: ס' 21(ג) disapplies the whole Law, except ס' 7, to an employer of fewer than six employees, and ס' 21(ד) disapplies 9(ג) and 15(ד) where the information was demanded for equality or affirmative-action purposes | Same, ס' 21. Covered in SKILL.md/SKILL_HE.md Step 2 (21(ג), with the manpower-contractor counting rule) and in references/eeo-compliance-checklist.md (21(ג) and 21(ד)). Without it the mechanism in row 3 is stated more broadly than the statute supports, and many candidates apply to sub-six-person businesses |
| 4 | Section 2א: the employer may not demand the military profile, may not use it, and may not penalise a refusal. Shin Bet and Mossad carved out | Same, ס' 2א. The only flat prohibition on asking inside this statute, and it bears directly on the military section this skill writes |
| 5 | Section 2(ג) BFOQ carve-out, sourced to the Hebrew text | Same, ס' 2(ג) |
| 6 | Disability is governed by a different statute and is absent from the 2(א) list: חוק שוויון זכויות לאנשים עם מוגבלות, התשנ"ח-1998, ס' 8(א), and ס' 8(ה), which counts failure to accommodate (including in admission tests) as discrimination, with no employee-count threshold | Otherwise the skill presents the 1988 list as the whole protected-ground universe, which it is not |
| 7 | Criminal information: the route to an employer runs through the police with the candidate's prior written consent, never through the CV | חוק המידע הפלילי ותקנת השבים, התשע"ט-2019 |
| 8 | Photographs are market convention and bias avoidance, expressly NOT a statutory rule, and expressly not an ATS limitation | No Israeli statute regulates CV photographs. Both prior rationales were wrong |
| 9 | Military / national service section that does not treat non-service as an anomaly: Arab citizens, Haredi candidates, medical and other exemptions, olim, and שירות לאומי / שירות אזרחי as a listable credential | Framing the section as mandatory encodes an inference about לאום, דת and השקפה, all ס' 2(א) grounds |
| 10 | Confidentiality of unit and role governed by the discharge undertaking and the unit קצין ביטחון, with the corps name as the safe default | The role title itself can be the protected item for some units |
| 11 | Hebrew .docx output requires `-M dir=rtl`; `-V dir=rtl` is a silent no-op and markdown tables mirror wrongly regardless | The Hebrew output path runs entirely through one pandoc command |
| 12 | Enforcement: the Equal Employment Opportunities Commission (civil, ס' 18א, Ministry of Economy and Industry) and Labour Court remedies under ס' 10, with the NIS 120,000 ceiling confined to ס' 7 victimisation claims | The reference file states remedies, so it must state them correctly |

## Should cover (advanced)

| # | Item | Status |
|---|------|--------|
| 13 | Age 45+ practice: truncating experience to roughly the last 15 years, and the interaction with dropping the graduation year | Partially covered (graduation-year line only). Deferred to next cycle |
| 14 | Work authorisation for non-citizens: oleh rights, A/5 temporary residence, and the employer-tied היתר העסקה for foreign nationals | Not covered. Deferred |
| 15 | Foreign-degree evaluation (הערכת תואר) on the Education line for olim | Not covered. Deferred |
| 16 | Reserve-service protections that back the omit rule | Not covered. Deferred |
| 17 | A rule against volunteering protected information in the cover letter's gap explanation | Not covered. Deferred |

## Out of scope (explicit)

| Item | Rationale |
|------|-----------|
| The employer's duty to notify candidates of hiring-process progress and rejection (חוק הודעה לעובד ולמועמד לעבודה, התשס"ב-2002, ס' 3א) | Real and useful, but it governs what happens AFTER the CV is sent and changes nothing about the document this skill produces. Reviewed 2026-09-01: an ordinary user of a CV builder would not come here for it. Belongs in a job-search or candidate-rights skill |
| Salary history and equal-pay reporting | The skill's only salary rule is "no expected-salary line on the CV", which is a document rule. Negotiation is expressly routed to `israeli-tech-salary-negotiator` in the description. Reviewed 2026-09-01 |
| Interview preparation and how to answer a prohibited question live | Routed to `israeli-tech-interview-prep` in the description. Reviewed 2026-09-01 |
| Job-market research, salary benchmarks, LinkedIn strategy, employer-side screening, employment-contract review | Each routed to a named sibling skill in the description. Reviewed 2026-09-01 |
| Filing an actual discrimination complaint | Requires a lawyer. The legal notice says so and points to the Commission. Reviewed 2026-09-01 |

## Authoritative sources

- חוק שוויון ההזדמנויות בעבודה, התשמ"ח-1988 (Nevo): https://www.nevo.co.il/law_html/law01/p214m1_001.htm
- חוק שוויון זכויות לאנשים עם מוגבלות, התשנ"ח-1998: https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%A9%D7%95%D7%95%D7%99%D7%95%D7%9F_%D7%96%D7%9B%D7%95%D7%99%D7%95%D7%AA_%D7%9C%D7%90%D7%A0%D7%A9%D7%99%D7%9D_%D7%A2%D7%9D_%D7%9E%D7%95%D7%92%D7%91%D7%9C%D7%95%D7%AA
- חוק המידע הפלילי ותקנת השבים, התשע"ט-2019: https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%99%D7%93%D7%A2_%D7%94%D7%A4%D7%9C%D7%99%D7%9C%D7%99_%D7%95%D7%AA%D7%A7%D7%A0%D7%AA_%D7%94%D7%A9%D7%91%D7%99%D7%9D
- נציבות שוויון הזדמנויות בעבודה: https://www.gov.il/he/departments/units/equal-opportunities-at-work-unit
- שירות התעסוקה CV course: https://campus.gov.il/course/taasuka-gov-career-cvbuilding101-he/
