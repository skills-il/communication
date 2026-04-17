---
name: gws-hebrew-email-automation
description: >-
  אוטומציית ג'ימייל לפרילנסרים ישראלים באמצעות Google Workspace CLI (gws).
  מתאים כשהמשתמש מבקש "לשלוח מייל ללקוח", "תזכורת תשלום בשקלים",
  "למיין את תיבת הדואר עם תוויות בעברית", "להגדיר פילטרים לג'ימייל",
  או "לשמור טיוטה לשליחה מאוחרת" שמכבדת שעות עבודה ישראליות.
  יכולות מרכזיות: ניסוח מיילים דו-לשוניים דרך gws gmail +send,
  רצפי תזכורות תשלום בשקלים, תיוג תיבת דואר בעברית דרך Discovery API,
  ותהליך draft-then-send מותאם שבת.
  Do NOT use for ספקי מייל שאינם Gmail, אוטומציית Outlook,
  או ניהול CRM.
license: MIT
---

# אוטומציית מייל בעברית עם GWS

## הוראות

### שלב 1: התקנה ואימות gws

לפני כל פקודת Gmail, תוודאו ש-`gws` מותקן ומאומת. `gws` זה בינארי Rust שנכתב על ידי הקהילה ומופץ ב-npm בשם `@googleworkspace/cli`. זה לא מוצר רשמי של גוגל, אז אתם צריכים לספק פרויקט Google Cloud ו-OAuth client משלכם.

```bash
# בדיקת גרסה (האחרונה היא 0.22.x)
gws --version

# התקנה גלובלית אם חסר
npm install -g @googleworkspace/cli

# הגדרה ראשונית: פרויקט GCP, הפעלת Gmail API,
# יצירת OAuth client מסוג Desktop. דורש gcloud CLI.
gws auth setup

# התחברות ואישור הרשאות Gmail (פותח דפדפן)
gws auth login --scopes gmail

# בדיקת הסטטוס
gws auth status
```

אם `gws auth setup` לא מוצא את `gcloud`, תפתחו את ה-Google Cloud Console, תיצרו פרויקט, תפעילו את Gmail API, תיצרו OAuth client מסוג Desktop ותשמרו את קובץ ה-JSON שהורד ב-`~/.config/gws/client_secret.json`. אז תריצו `gws auth login --scopes gmail`.

הטוקנים מוצפנים במנוחה (AES-256-GCM) ומתרעננים אוטומטית, אז אין פקודת `refresh` נפרדת.

### שלב 2: ניסוח ושליחת מיילים דו-לשוניים עברית/אנגלית

כשאתם צריכים לשלוח מייל מקצועי ללקוח ישראלי, תנסחו את המייל בעברית כשפה ראשית עם חלק אנגלי אופציונלי מתחת.

**מבנה מייל לתקשורת עסקית ישראלית:**

| חלק | שפה | הנחיות |
|-----|-----|--------|
| שורת נושא | עברית | עד 50 תווים, כולל פריט פעולה מרכזי |
| ברכה | עברית | רשמי: `שלום [שם],` או לא רשמי: `היי [שם],` |
| גוף | עברית (ראשי) | ימין-לשמאל, שימוש במונחים עסקיים מקומיים |
| חלק אנגלי | אנגלית (אופציונלי) | להוסיף מתחת למפריד אם הנמען צריך |
| חתימה | דו-לשוני | שם בעברית קודם, אנגלית מתחת |

**שליחת מייל עם ה-helper ‎`+send`:**

הקידומת `+` מסמנת פקודות helper כתובות ביד ב-`gws`, הן קיימות במקביל למשטח Discovery האוטומטי ולא מתנגשות בשמות מתודות. הדגלים האמיתיים של `gws gmail +send`: `--to`, `--subject`, `--body`, `--cc`, `--bcc`, `--from`, `--attach`/`-a`, `--html`, `--draft`, `--dry-run`.

```bash
gws gmail +send \
  --to "client@example.com" \
  --subject "הצעת מחיר - פרויקט פיתוח אתר" \
  --body "שלום רב,

מצורפת הצעת המחיר עבור פרויקט פיתוח האתר כפי שדובר.

סה\"כ: 15,000 ש\"ח (לא כולל מע\"מ)
תנאי תשלום: שוטף + 30

אשמח לתשובתך.

בברכה,
[שם]" \
  --dry-run
```

**חשוב:** תמיד תריצו קודם עם `--dry-run` כדי לראות את הבקשה המלאה. תסירו את הדגל רק אחרי אישור המשתמש. לסקירה לפני שליחה אמיתית, תשתמשו ב-`--draft` ששומר את המייל כטיוטה ב-Gmail במקום לשלוח.

**עיצוב סכומים בשקלים (ILS):**
- קיצור השקל: `ש"ח` (שקל חדש)
- פורמט: `15,000 ש"ח` (הפרדת אלפים בפסיק, הקיצור אחרי המספר)
- עבור מע"מ: לציין `לא כולל מע"מ` או `כולל מע"מ`
- שיעור מע"מ ישראלי נוכחי: **18%** (עלה מ-17% ב-1 בינואר 2025 לפי חוק ההסדרים). אפשר להשתמש ב-`scripts/shekel-formatter.py --vat` לחישוב הפירוט.

### שלב 3: רצפי תזכורות תשלום

לתזכורות תשלום לפרילנסרים, תעקבו אחרי רצף הסלמה:

| שלב | ימי איחור | טון | קידומת נושא |
|-----|-----------|-----|------------|
| תזכורת ידידותית | 1-7 | מנומס, לא רשמי | תזכורת - |
| הודעה שנייה | 8-21 | מקצועי, נחרץ | תזכורת שנייה - |
| הודעה אחרונה | 22-30 | רשמי, דחוף | תזכורת אחרונה - |
| אזהרת איחור | 30+ | טון משפטי | חשבונית באיחור - |

**דוגמה: תזכורת תשלום ידידותית שנשמרת כטיוטה לסקירת המשתמש**

```bash
gws gmail +send \
  --to "client@example.com" \
  --subject "תזכורת - חשבונית מס' 1042 לתשלום" \
  --body "שלום [שם הלקוח],

רציתי להזכיר שחשבונית מס' 1042 על סך 8,500 ש\"ח (כולל מע\"מ) עדיין לא שולמה.

פרטי החשבונית:
- מספר חשבונית: 1042
- תאריך הפקה: 15.01.2026
- סכום: 8,500 ש\"ח
- תנאי תשלום: שוטף + 30
- תאריך פירעון: 15.02.2026

אשמח אם תוכל/י לטפל בכך.

תודה רבה,
[שם]" \
  --draft
```

תשמרו כ-`--draft`, ואז תבקשו מהמשתמש לפתוח את Gmail, לסקור וללחוץ שלח (או לתזמן דרך ממשק Gmail).

**עיצוב תאריכים לחשבוניות ישראליות:**
- פורמט DD.MM.YYYY (תקן ישראלי)
- תנאי תשלום: שוטף + 30 (נטו 30 מסוף החודש הנוכחי), שוטף + 45, שוטף + 60

### שלב 4: מיון תיבת הדואר ותיוג בעברית

ה-helper ‎`+triage` זה סיכום לקריאה בלבד, הוא מציג הודעות לא נקראות אבל לא מתייג כלום. כדי באמת להחיל תוויות עבריות על מיילים תואמים, תשלבו שלוש פקודות Discovery: רשימת תוויות, רשימת הודעות לפי שאילתה, ואז modify לכל הודעה להוספת התווית.

**4א. סיכום הודעות לא נקראות (קריאה בלבד):**

```bash
# ברירת מחדל: 20 ההודעות הלא נקראות האחרונות בטבלה
gws gmail +triage

# צמצום לפי שאילתת חיפוש של Gmail
gws gmail +triage --max 10 --query "from:(leumi.co.il OR bankhapoalim.co.il)"

# כולל שמות תוויות לכל הודעה
gws gmail +triage --labels
```

דגלים ש-`+triage` מקבל: `--max`, `--query`, `--labels`. אין דגלי `--from` או `--label`.

**4ב. יצירת תווית בעברית (פעם אחת בלבד):**

```bash
gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "בנקאות", "labelListVisibility": "labelShow", "messageListVisibility": "show"}' \
  --dry-run
```

תיקחו את ה-`id` שחוזר (לדוגמה `Label_1234567890`) לשלב הבא.

**4ג. רשימת הודעות לפי שאילתת Gmail והחלת התווית:**

```bash
# מציאת מיילים של בנקים (שימוש בתחביר חיפוש Gmail ב-`q`)
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:(leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il OR mizrahi-tefahot.co.il)", "maxResults": 50}' \
  | jq -r '.messages[].id' > /tmp/bank-msg-ids.txt

# החלת התווית על כל הודעה תואמת
while read -r msg_id; do
  gws gmail users messages modify \
    --params "{\"userId\": \"me\", \"id\": \"$msg_id\"}" \
    --json '{"addLabelIds": ["Label_1234567890"]}' \
    --dry-run
done < /tmp/bank-msg-ids.txt
```

**מבנה תוויות לפרילנסרים ישראלים:**

| תווית (עברית) | תווית (אנגלית) | שאילתת `q:` מוצעת |
|--------------|----------------|-------------------|
| בנקאות | Banking | `from:(leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il OR mizrahi-tefahot.co.il OR mercantile.co.il)` |
| חשבוניות | Invoices | `from:(greeninvoice.co.il OR icount.co.il OR ezcount.co.il OR hashavshevet.co.il)` |
| ממשלתי | Government | `from:(gov.il OR taxes.gov.il OR btl.gov.il)` |
| לקוחות/פעיל | Clients/Active | דומיינים של לקוחות (מוגדר ע"י המשתמש) |
| קבלות | Receipts | `from:(paybox.co.il OR bitpay.co.il OR paypal.com)` |

### שלב 5: יצירת פילטרים קבועים לג'ימייל

פילטרים של Gmail מתייגים אוטומטית דואר נכנס. אין helper ‎`gws gmail +filter`, תשתמשו במתודת Discovery ‎`users settings filters create` עם סכמת הפילטרים האמיתית של Gmail.

```bash
# פילטר: תיוג התראות בנקאיות ישראליות
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il"},
    "action": {"addLabelIds": ["Label_1234567890"]}
  }' \
  --dry-run

# פילטר: ארכוב קבלות אוטומטית (דילוג על INBOX, החלת תווית)
gws gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "greeninvoice.co.il OR icount.co.il"},
    "action": {"addLabelIds": ["Label_2345678901"], "removeLabelIds": ["INBOX"]}
  }' \
  --dry-run
```

אפשר להשתמש ב-`gws gmail users settings filters list --params '{"userId": "me"}'` לבדיקת פילטרים קיימים וב-`gws gmail users settings filters delete --params '{"userId": "me", "id": "FILTER_ID"}'` למחיקה.

### שלב 6: שמירה על שעות עבודה ישראליות ושבת

ל-`gws gmail +send` **אין** דגל תזמון שליחה. תזמון שליחה של Gmail זמין רק בממשק הווב והמובייל של Gmail. כדי לכבד את המנהגים העסקיים הישראליים מה-CLI, תשמרו טיוטות עם `--draft` ותנו למשתמש לסקור ולשלוח (או לתזמן) אותן מ-Gmail.

| כלל | פרטים |
|-----|-------|
| ימי עבודה | ראשון עד חמישי |
| שעות עבודה | 09:00-18:00 שעון ישראל (חורף UTC+2, קיץ UTC+3) |
| יום שישי | העבודה מסתיימת מוקדם, בדרך כלל עד 13:00-14:00 |
| ערב שבת | לא לשלוח אחרי 14:00 ביום שישי |
| שבת | לא לשלוח משקיעת החמה ביום שישי עד מוצאי שבת |
| חגים יהודיים | להימנע משליחה בחגים |

**זרימת עבודה מומלצת:**

```bash
# 1. בדיקת השעה הנוכחית בישראל
TZ=Asia/Jerusalem date

# 2. אם זה מחוץ לשעות עבודה, לשמור כטיוטה לסקירה
gws gmail +send \
  --to "client@example.com" \
  --subject "עדכון פרויקט" \
  --body "שלום,

מצורף עדכון שבועי לגבי התקדמות הפרויקט..." \
  --draft

# 3. להודיע למשתמש: הטיוטה נשמרה. לפתוח Gmail, Drafts,
#    ללחוץ Schedule send ולבחור ראשון 09:00 שעון ישראל.
```

**לפני ניסוח כל מייל יוצא, תבדקו:**
1. האם זה יום שישי אחרי 14:00 שעון ישראל? תשמרו כ-`--draft` ותגידו למשתמש לתזמן ליום ראשון 09:00.
2. האם זה שבת (משקיעת החמה בשישי עד מוצאי שבת)? תשמרו כ-`--draft`.
3. האם זה אחרי 18:00 ביום חול? תשמרו כ-`--draft` והציעו שליחה לבוקר למחרת.
4. האם זה חג יהודי (תאמתו עם המשתמש)? תשמרו כ-`--draft`.

### שלב 7: מעקב אחר מיילים נכנסים (מתקדם, אופציונלי)

ה-helper ‎`+watch` מזרים מיילים חדשים כ-NDJSON דרך Gmail push notifications מעל Google Pub/Sub. הוא דורש פרויקט GCP עם Pub/Sub מופעל ומסנן רק לפי **label IDs**, לא לפי דומיינים של שולחים. כדאי להשתמש בזה כשצריך תגובה בזמן אמת (חשבונית חדשה ואז ping ל-Slack), לא לארגון פסיבי של תיבת הדואר.

```bash
# משיכה חד-פעמית: מביא הודעות חדשות ב-INBOX פעם אחת ויוצא
gws gmail +watch \
  --project my-gcp-project \
  --label-ids INBOX \
  --once

# watch ארוך טווח עם ניקוי Pub/Sub אוטומטי
gws gmail +watch \
  --project my-gcp-project \
  --label-ids INBOX,UNREAD \
  --cleanup \
  --output-dir ./incoming
```

דגלים אמיתיים: `--project`, `--subscription`, `--topic`, `--label-ids`, `--max-messages`, `--poll-interval`, `--msg-format`, `--once`, `--cleanup`, `--output-dir`. רישומי Gmail watch פגים אחרי 7 ימים וצריך לחדש אותם. אם למשתמש אין כבר Pub/Sub מוגדר, כדאי לדלג על השלב הזה, זרימת התיוג הבסיסית בשלב 4 מספיקה לרוב הפרילנסרים.

## דוגמאות

### דוגמה 1: פרילנסר ישראלי שולח תזכורת תשלום

המשתמש אומר: "שלח תזכורת תשלום ל-david@techstartup.co.il על חשבונית 2045, 12,000 שקל, פג תוקף לפני 10 ימים"

פעולות:
1. חישוב תאריך הפירעון המקורי (לפני 10 ימים מהיום)
2. קביעת שלב ההסלמה: 8-21 ימים = "הודעה שנייה"
3. ניסוח מייל בעברית בטון מקצועי ונחרץ
4. עיצוב סכום כ-`12,000 ש"ח`
5. הכללת פרטי חשבונית
6. שמירה כ-`--draft` לסקירת המשתמש לפני שליחה

```bash
gws gmail +send \
  --to "david@techstartup.co.il" \
  --subject "תזכורת שנייה - חשבונית 2045 לתשלום" \
  --body "שלום דוד,

זו תזכורת שנייה לגבי חשבונית מס' 2045.

פרטי החשבונית:
- סכום: 12,000 ש\"ח
- תנאי תשלום: שוטף + 30
- סטטוס: באיחור של 10 ימים

אודה לטיפולך בהקדם.

בברכה,
[שם]" \
  --draft
```

תוצאה: המייל נשמר כטיוטה ב-Gmail בעברית מקצועית עם עיצוב שקלים נכון. המשתמש פותח Gmail, Drafts, Send.

### דוגמה 2: תיוג מיילים מבנקים עם תווית בעברית

המשתמש אומר: "תארגן לי את תיבת הדואר, תתייג את כל המיילים מהבנקים עם בנקאות"

פעולות:
1. יצירת התווית בעברית אם לא קיימת, לקיחת ה-`id`
2. רשימת הודעות לא נקראות מבנקים ישראליים עם `users messages list`
3. לכל הודעה תואמת, החלת התווית עם `users messages modify`
4. דיווח על המספר

```bash
# יצירת תווית (פעם אחת)
LABEL_ID=$(gws gmail users labels create \
  --params '{"userId": "me"}' \
  --json '{"name": "בנקאות"}' | jq -r '.id')

# רשימת מיילים של בנקים
gws gmail users messages list \
  --params '{"userId": "me", "q": "from:(leumi.co.il OR bankhapoalim.co.il OR discountbank.co.il OR mizrahi-tefahot.co.il)", "maxResults": 50}' \
  | jq -r '.messages[].id' > /tmp/bank-msgs.txt

# החלת התווית
while read -r id; do
  gws gmail users messages modify \
    --params "{\"userId\": \"me\", \"id\": \"$id\"}" \
    --json "{\"addLabelIds\": [\"$LABEL_ID\"]}"
done < /tmp/bank-msgs.txt

echo "תויגו $(wc -l < /tmp/bank-msgs.txt) הודעות בנקים תחת בנקאות"
```

תוצאה: כל המיילים התואמים של בנקים נושאים את התווית בנקאות ב-Gmail.

### דוגמה 3: שמירת טיוטה במקום שליחה ביום שישי אחה"צ

המשתמש אומר: "שלח עדכון פרויקט ללקוח, אבל עכשיו יום שישי אחר הצהריים"

פעולות:
1. בדיקת שעון ישראל הנוכחי: `TZ=Asia/Jerusalem date` מראה יום שישי 15:30 IDT
2. קביעה שזה אחרי סף 14:00 של יום שישי (ערב שבת)
3. שמירת המייל כטיוטה ב-Gmail במקום לשלוח
4. הנחיית המשתמש לפתוח Gmail Drafts וללחוץ Schedule send ליום ראשון 09:00

```bash
TZ=Asia/Jerusalem date
# Fri Apr 17 15:30:12 IDT 2026, אחרי 14:00, לא לשלוח

gws gmail +send \
  --to "client@example.com" \
  --subject "עדכון שבועי - פרויקט אתר" \
  --body "שלום,

מצורף עדכון שבועי לגבי התקדמות הפרויקט..." \
  --draft
```

תוצאה: הטיוטה נשמרה. המשתמש עודכן ששליחות בשישי אחה"צ נדחות, לפתוח Gmail Drafts לסקירה ולתזמן שליחה ליום ראשון 09:00 שעון ישראל.

## משאבים מצורפים

### סקריפטים
- `scripts/shekel-formatter.py` — עיצוב סכומי מטבע לתקן השקל הישראלי (ILS) עם סימון נכון ופירוט מע"מ 18% אופציונלי. הרצה: `python scripts/shekel-formatter.py --help`

### מסמכי עזר
- `references/israeli-business-email-templates.md` — אוסף תבניות מייל בעברית לתרחישים נפוצים של פרילנסרים: הצעות מחיר, חשבוניות, מעקב, עדכוני פרויקט. תעיינו בזה כשאתם מנסחים מיילים מקצועיים בעברית ללקוחות ישראליים.
- `references/gws-gmail-commands.md` — מדריך מהיר לפקודות האמיתיות של `gws gmail` שבשימוש בסקיל הזה (`+send`, `+triage`, `+watch`, ובנוסף משטח Discovery של ‎`users.labels`, `users.messages.list/modify`, `users.settings.filters`). תעיינו בזה כשאתם בונים פקודות `gws` או מתקשים בפתרון תקלות.

## שרתי MCP מומלצים

אין כרגע שרתי MCP של Gmail או Google Workspace ברשימת skills-il. אם משתמש מעדיף גישה מבוססת כלים על פני פקודות CLI, תפנו אותו ל-`gws auth setup` ולהוראות בשלב 1, ה-CLI זה הנתיב הנתמך.

## מלכודות נפוצות

- פקודות helper של `gws` משתמשות בקידומת `+` (`gws gmail +send`, `gws gmail +triage`, `gws gmail +watch`). סוכנים שאומנו על מוסכמות CLI אחרות הרבה פעמים משמיטים את ה-`+` ומייצרים פקודות שיחזירו "unknown subcommand". תכללו תמיד את סימן הפלוס ב-helpers.
- ל-`gws gmail +send` **אין** דגל `--schedule`. תזמון השליחה של Gmail קיים רק בממשק הווב והמובייל של Gmail. סוכנים שמניחים שיש דגל `--schedule` יפיקו פקודות שיחזירו שגיאה. תשתמשו ב-`--draft` ותנחו את המשתמש לתזמן מ-Gmail אם צריך שליחה דחויה.
- `gws gmail +triage` הוא **קריאה בלבד**, הוא מציג טבלה של הודעות לא נקראות אבל לא משנה את תיבת הדואר. כדי באמת להחיל תוויות, תשתמשו ברצף ‎`users messages list` ו-‎`users messages modify` משלב 4. סוכנים מבלבלים ביניהם הרבה פעמים.
- ימי העבודה בישראל הם ראשון עד חמישי, לא שני עד שישי. סוכנים עלולים לתזמן מיילים לשבת או להניח ששישי הוא יום עבודה מלא.
- סכומים בשקלים נכתבים `15,000 ש"ח` (הקיצור אחרי המספר), לא `₪15,000`. סוכנים עלולים להשתמש במוסכמות הצבת סימן מטבע של דולר/יורו.
- תאריכי חשבוניות ישראליות בפורמט DD.MM.YYYY (מופרד בנקודות), לא DD/MM/YYYY או MM/DD/YYYY.
- תנאי התשלום הישראלי הסטנדרטי `שוטף + 30` פירושו נטו 30 מ**סוף החודש הנוכחי**, לא 30 יום מתאריך החשבונית. חשבונית מ-01.01 ב-שוטף + 30 פירעונה 28.02, לא 31.01.

## קישורי עזר

| מקור | URL | מה לבדוק |
|------|-----|---------|
| README של Google Workspace CLI | https://github.com/googleworkspace/cli/blob/main/README.md | התקנה, זרימת auth, רשימת פקודות helper |
| סקיל קנוני ‎`gws gmail +send` | https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-send/SKILL.md | הדגלים המדויקים ש-`+send` מקבל |
| סקיל קנוני ‎`gws gmail +triage` | https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-triage/SKILL.md | `+triage` הוא סיכום קריאה בלבד, דגלים `--max`, `--query`, `--labels` |
| סקיל קנוני ‎`gws gmail +watch` | https://github.com/googleworkspace/cli/blob/main/skills/gws-gmail-watch/SKILL.md | דרישות Pub/Sub, `--label-ids` (לא `--from`) |
| Gmail API ‎`users.settings.filters` | https://developers.google.com/gmail/api/reference/rest/v1/users.settings.filters | סכמת criteria/action לשלב 5 |
| שיעור מע"מ ישראלי (18% מ-1 בינואר 2025) | https://www.gov.il/BlobFolder/dynamiccollectorresultitem/represent-info-051224-2/he/vat_represent-info-051224-2.pdf | הוראת פרשנות 1/2025 של רשות המסים: העלאת מע"מ מ-17% ל-18% |

## פתרון בעיות

### שגיאה: "gws: command not found"
סיבה: `@googleworkspace/cli` לא מותקן או לא נמצא ב-`PATH`.
פתרון: תתקינו עם `npm install -g @googleworkspace/cli`. תאמתו עם `gws --version`. אפשר גם להוריד בינארי מוכן מעמוד [GitHub Releases](https://github.com/googleworkspace/cli/releases) ולשים אותו ב-`PATH`.

### שגיאה: "Access blocked" או 403 במהלך `gws auth login`
סיבה: אפליקציית ה-OAuth נמצאת במצב בדיקה וחשבון הגוגל שלכם לא רשום כ-test user, או שביקשתם יותר מדי scopes בבת אחת (אפליקציות לא מאומתות מוגבלות ל-~25).
פתרון: תפתחו את [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent) בפרויקט ה-GCP שלכם, תוסיפו את המייל שלכם תחת Test users, ותריצו שוב עם רשימת scopes מצומצמת: `gws auth login --scopes gmail`.

### שגיאה: `accessNotConfigured`, "Gmail API has not been used in project ..."
סיבה: ה-Gmail API לא מופעל בפרויקט ה-GCP הקשור ל-OAuth client שלכם.
פתרון: תעקבו אחרי ה-`enable_url` שמודפס בשגיאה ל-Cloud Console API library, תלחצו Enable, תחכו כ-10 שניות, ותנסו שוב. `gws auth setup` יכול להפעיל גם APIs נדרשים אוטומטית.

### שגיאה: "unknown subcommand: send"
סיבה: כתבתם `gws gmail send` במקום `gws gmail +send`. פקודות helper ב-`gws` משתמשות בקידומת `+` כדי להבדיל בינן לבין מתודות Discovery האוטומטיות.
פתרון: תוסיפו את סימן הפלוס: `gws gmail +send --to ... --subject ... --body ...`.

### שגיאה: "Label not found" בהחלת תווית
סיבה: התווית בעברית עדיין לא קיימת, או השתמשתם בשם התווית במקום ב-`id` של התווית.
פתרון: תיצרו קודם את התווית עם `gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "בנקאות"}'`, תיקחו את ה-`id` שחוזר, ותעבירו את ה-`id` הזה ל-`addLabelIds` ב-`users messages modify`.

### שגיאה: "Rate limit exceeded" בתיוג הודעות רבות
סיבה: Gmail API אוכף מכסת quota units לשנייה לכל משתמש, קריאות `messages modify` בלולאה צפופה יכולות להיתקל במכסה.
פתרון: תוסיפו `sleep 0.1` קטן בין קריאות `modify` או תעבדו הודעות בבאצ'ים. לגבי מגבלות שליחה יומיות, Gmail צרכני מוגבל ל-100 נמענים ביום ו-Google Workspace ל-2,000 נמענים ביום.
