# Hebrew template submission and rejection patterns

A working Hebrew submission, then the patterns seen on rejected Hebrew WhatsApp templates, with a corrected version of each. Read together with the Hebrew and RTL mechanics in SKILL.md Step 2.

| Rejected text | Why | Fixed version |
|---|---|---|
| "מבצע!! הנחה ענקית רק היום, מהרו!" (in UTILITY) | Promotional copy + urgency markers in UTILITY category | Move to MARKETING, or rewrite as transactional: "ההנחה שלך {{1}}% פעילה עד {{2}}." |
| "תזכורת: יש לך תור ב-{{1}}" with example `["מחר"]` | Vague placeholder, not a realistic value | Use a real example like `["מרפאת השיניים ד\"ר כהן, 15.06.2026 בשעה 10:00"]` |
| Body with 6+ variables and 30 chars of literal text | Spam-like ratio of variables to text | Reduce to ≤3 variables, add more natural sentence connectives |
| Body starting with `{{1}}` and no language code | Variable-first RTL body, unclear language | Start with a Hebrew word, set `language: "he"`, and for MARKETING open with the word פרסומת and add the rest of the section 30א block from Step 4 |

## Submitting a Hebrew template

`POST /{waba_id}/message_templates`, where the ID is the Messaging account ID (existing WABA IDs carry over). Every variable needs a realistic value in `example`, and the body starts with a Hebrew word.

```python
def create_template(waba_id: str, access_token: str, template: dict):
    """Create a WhatsApp message template."""
    url = f"https://graph.facebook.com/v26.0/{waba_id}/message_templates"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=template)
    return response.json()

# Example: Hebrew appointment reminder template
appointment_template = {
    "name": "appointment_reminder_he",
    "language": "he",
    "category": "UTILITY",
    "components": [
        {
            "type": "BODY",
            "text": "שלום {{1}}, תזכורת על תור ב-{{2}} בתאריך {{3}} בשעה {{4}}. לאישור השיבו 1, לביטול השיבו 2.",
            "example": {
                "body_text": [["ישראל", "מרפאת השיניים ד״ר כהן", "15.03.2026", "10:00"]],
            },
        },
        {
            "type": "BUTTONS",
            "buttons": [
                {"type": "QUICK_REPLY", "text": "מאשר"},
                {"type": "QUICK_REPLY", "text": "צריך לשנות"},
            ],
        },
    ],
}
```

## בעברית

| טקסט שנדחה | הסיבה | גרסה שעוברת |
|---|---|---|
| "מבצע!! הנחה ענקית רק היום, מהרו!" (ב-UTILITY) | שפה שיווקית וסימני דחיפות בקטגוריית UTILITY | להעביר ל-MARKETING, או לנסח טרנזקציונית: "ההנחה שלך {{1}}% פעילה עד {{2}}." |
| "תזכורת: יש לך תור ב-{{1}}" עם דוגמה `["מחר"]` | פלייסהולדר עמום, לא ערך אמיתי | להשתמש בדוגמה אמיתית כמו `["מרפאת השיניים ד\"ר כהן, 15.06.2026 בשעה 10:00"]` |
| Body עם 6+ משתנים ו-30 תווי טקסט קבועים | יחס דמוי ספאם של משתנים לטקסט | להפחית ל-3 משתנים לכל היותר, להוסיף מילות קישור טבעיות |
| גוף שמתחיל ב-{{1}} ובלי קוד שפה | משתנה בתחילת גוף RTL, שפה לא ברורה | להתחיל במילה בעברית, להגדיר `language: "he"`, ובתבנית MARKETING לפתוח במילה פרסומת ולהוסיף את שאר הפרטים לפי סעיף 30א משלב 4 |
