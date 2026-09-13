# Hebrew template rejection patterns

Patterns seen on Hebrew WhatsApp templates, with a corrected version of each. Read together with the Hebrew and RTL mechanics in SKILL.md Step 2.

| Rejected text | Why | Fixed version |
|---|---|---|
| "מבצע!! 20% הנחה רק היום, מהרו!" (in UTILITY) | Promotional copy + urgency markers in UTILITY category | Move to MARKETING, or rewrite as transactional: "ההנחה שלך {{1}}% פעילה עד {{2}}." |
| "תזכורת: יש לך תור ב-{{1}}" with example `["מחר"]` | Vague placeholder, not a realistic value | Use a real example like `["מרפאת השיניים ד\"ר כהן, 15.06.2026 בשעה 10:00"]` |
| Body with 6+ variables and 30 chars of literal text | Spam-like ratio of variables to text | Reduce to ≤3 variables, add more natural sentence connectives |
| Body starting with `{{1}}` and no language code | Variable-first RTL body, unclear language | Start with a Hebrew word, set `language: "he"`, add the Israeli disclosure footer from Step 4 |

## בעברית

| טקסט שנדחה | הסיבה | גרסה שעוברת |
|---|---|---|
| "מבצע!! 20% הנחה רק היום, מהרו!" (ב-UTILITY) | שפה שיווקית וסימני דחיפות בקטגוריית UTILITY | להעביר ל-MARKETING, או לנסח טרנזקציונית: "ההנחה שלך {{1}}% פעילה עד {{2}}." |
| "תזכורת: יש לך תור ב-{{1}}" עם דוגמה `["מחר"]` | פלייסהולדר עמום, לא ערך אמיתי | להשתמש בדוגמה אמיתית כמו `["מרפאת השיניים ד\"ר כהן, 15.06.2026 בשעה 10:00"]` |
| Body עם 6+ משתנים ו-30 תווי טקסט קבועים | יחס דמוי ספאם של משתנים לטקסט | להפחית ל-3 משתנים לכל היותר, להוסיף מילות קישור טבעיות |
| גוף שמתחיל ב-{{1}} ובלי קוד שפה | משתנה בתחילת גוף RTL, שפה לא ברורה | להתחיל במילה בעברית, להגדיר `language: "he"`, ולהוסיף את בלוק הגילוי הישראלי משלב 4 |
