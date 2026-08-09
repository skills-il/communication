# תהליכי עבודה ב-Monday.com

## הנחיות

### שלב 1: אימות גישה ל-Monday.com

תבדקו את טוקן ה-API של Monday.com ושרת MCP אופציונלי. אל תשתמשו ב-`account { plan { max_users } }` כבדיקת חיים: השדה `account.plan` מתועד כמחזיר `null` בחשבונות שרצים על תשתית ריבוי-המוצרים של monday, וזה בדיוק מה שחשבונות חדשים מקבלים. תקראו במקום זאת `account { tier products { kind } }` ותתייחסו ל-`plan` כאופציונלי.

```python
import requests

API_URL = "https://api.monday.com/v2"

def verify_monday_access(api_token: str) -> dict:
    """Verify Monday.com API access and return normalized account info."""
    headers = {
        "Authorization": api_token,
        "API-Version": "2026-07",
        "Content-Type": "application/json",
    }
    query = '''
    {
      me { name email }
      account {
        name
        tier
        products { kind }
        plan { max_users tier period }
      }
    }
    '''
    data = requests.post(API_URL, headers=headers,
                         json={"query": query}, timeout=30).json()

    if data.get("errors"):
        raise RuntimeError(f"monday API error: {data['errors']}")

    account = data["data"]["account"]
    plan = account.get("plan")  # None on multi-product-infrastructure accounts
    return {
        "user": data["data"]["me"],
        "account_name": account["name"],
        # Prefer account.tier; fall back to plan.tier only when plan is present.
        "tier": account.get("tier") or (plan or {}).get("tier"),
        "products": [p["kind"] for p in (account.get("products") or [])],
        "max_users": (plan or {}).get("max_users"),  # None is normal, not an error
    }
```

אם `plan` חוזר `null` אבל `tier` מלא, הגישה תקינה. רק מערך `errors` מעיד שהטוקן שגוי.

אם שרת MCP זמין (`mondaycom/mcp`): תשתמשו בכלי MCP לפעולות CRUD בסיסיות.
אם יש רק API: תשתמשו בשאילתות GraphQL ישירות.

### שלב 2: בחירת תבנית תהליך עבודה

**תבניות תהליכי עבודה לצוותים ישראליים:**

| תהליך עבודה | מתאים ל | תכונה מרכזית |
|----------|----------|-------------|
| לוח ספרינט (א'-ה') | צוותי פיתוח | שבוע עבודה ישראלי, מודע לחגים |
| צינור מכירות | צוותי מכירות | תוויות שלבים בעברית, אוטומציות מעקב |
| קליטת לקוח | צוותי שירות | תהליכי אישור, מעקב SLA |
| קמפיין שיווקי | שיווק | לוח שנה לקמפיינים, אישור תכנים |
| גיוס משאבי אנוש | משאבי אנוש | מעקב מועמדים, תבניות בעברית |
| מעקב OKR | הנהלה | יעדים רבעוניים, התאמה לרבעונים ישראליים |

### שלב 3: יצירת לוח מותאם

**לוח ספרינט לצוות פיתוח ישראלי:**
```python
def create_israeli_sprint_board(api_token: str, workspace_id: int,
                                 sprint_name: str) -> dict:
    """Create a sprint board optimized for the Israeli work week."""
    headers = {
        "Authorization": api_token,
        "API-Version": "2026-07",
        "Content-Type": "application/json",
    }

    mutation = '''
    mutation {
      create_board(
        board_name: "%s"
        board_kind: public
        workspace_id: %d
      ) {
        id
      }
    }
    ''' % (sprint_name, workspace_id)

    response = requests.post(API_URL, headers=headers, json={"query": mutation})
    board_data = response.json()
    board_id = board_data["data"]["create_board"]["id"]

    groups = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Backlog",
        "Done",
    ]

    for group_name in groups:
        group_mutation = '''
        mutation {
          create_group(board_id: %s, group_name: "%s") {
            id
          }
        }
        ''' % (board_id, group_name)
        requests.post(API_URL, headers=headers, json={"query": group_mutation})

    return board_data
```

### שלב 4: הגדרת אוטומציות

לפני שמתכננים אוטומציה, תבדקו את מכסת הפעולות החודשית של החשבון (ראו תוכניות ומכסות). אוטומציה שרצה על כל פריט בלוח עמוס יכולה לשרוף את כל החודש של תוכנית Standard תוך ימים.

**מתכון 1: פתיחת ספרינט ביום ראשון**
```
טריגר: כל יום ראשון בשעה 09:00 (Asia/Jerusalem)
פעולה: העבר את כל הפריטים מ-"Backlog" לקבוצות יומיות
התראה: שלח לצוות עדכון "הספרינט התחיל"
```

**מתכון 2: סיכום יום חמישי**
```
טריגר: כל יום חמישי בשעה 16:00
פעולה: צור עדכון סיכום עם פריטים שלא הושלמו
פעולה: העבר פריטים שלא הושלמו חזרה ל-Backlog
התראה: שלח סיכום ספרינט לראש הצוות
```

**מתכון 3: הקפאת חגים**
```python
# Israeli holidays that affect sprint planning.
# Israel schedule (one-day Yom Tov). Verify a new year via hebcal.com/holidays/<year>?i=on
# NOT the Diaspora two-day-Yom-Tov dates, which would false-freeze a working day.
israeli_holidays_2026 = [
    ("2026-03-03", "2026-03-03", "Purim"),
    ("2026-04-02", "2026-04-08", "Pesach"),  # Israel: Yom Tov Apr 2 + Apr 8; chol hamoed Apr 3-7. Apr 9 is a workday.
    ("2026-04-14", "2026-04-14", "Yom HaShoah"),
    ("2026-04-21", "2026-04-21", "Yom HaZikaron"),
    ("2026-04-22", "2026-04-22", "Yom Ha'Atzmaut"),
    ("2026-05-22", "2026-05-22", "Shavuot"),
    ("2026-07-23", "2026-07-23", "Tisha B'Av"),
    ("2026-09-12", "2026-09-13", "Rosh Hashana"),
    ("2026-09-21", "2026-09-21", "Yom Kippur"),
    ("2026-09-26", "2026-10-03", "Sukkot"),
    ("2026-12-04", "2026-12-12", "Hanukkah"),
]

def is_israeli_holiday(date_str: str) -> tuple[bool, str]:
    """Check if a date falls on an Israeli holiday. Binary only: erev-chag
    half-days (Purim eve, seder day, Tisha B'Av) are not modelled here."""
    from datetime import datetime
    check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    for start, end, name in israeli_holidays_2026:
        start_d = datetime.strptime(start, "%Y-%m-%d").date()
        end_d = datetime.strptime(end, "%Y-%m-%d").date()
        if start_d <= check_date <= end_d:
            return True, name
    return False, ""
```

**מתכון 4: מעקב אוטומטי**
```
טריגר: כשתאריך "יצירת קשר אחרון" לפני 7+ ימים
תנאי: סטטוס אינו "הושלם" או "סגור"
פעולה: שנה סטטוס ל-"דרוש מעקב"
פעולה: התרה את האחראי
```

### שלב 5: שאילתות API מתקדמות

**שליפת לוחות, כולל לוחות רב-רמתיים:**

שאילתת `boards` לא מחזירה לוחות רב-רמתיים (עם תת-פריטים) כברירת מחדל. התיעוד מפורש: אם הארגומנט מושמט, יוחזרו רק לוחות מסוג `classic`, אלא אם ציינתם מזהי לוח מפורשים. השמטת `hierarchy_type` מסתירה בשקט כל לוח רב-רמתי, וסנכרון שנבנה עליה ייראה תקין בזמן שהוא מפספס נתונים.

```graphql
{
  boards(limit: 50, hierarchy_type: [classic, multi_level]) {
    id
    name
    board_kind
    columns { id title type }
  }
}
```

**חיפוש פריטים לפי ערך עמודה:**
```python
def search_items(api_token: str, board_id: int, column_id: str, value: str):
    """Search items by column value."""
    headers = {
        "Authorization": api_token,
        "API-Version": "2026-07",
        "Content-Type": "application/json",
    }
    # items_page_by_column_values מתחלק לעמודים בדיוק כמו items_page: הוא מחזיר `cursor`.
    # עם limit:50 מקבלים רק 50 התאמות ראשונות, אז כדי לקבל "את כל הפריטים שעברו את הזמן"
    # צריך ללולאה ולהעביר את ה-cursor חזרה דרך next_items_page עד ש-cursor הוא null.
    # בלוק `complexity` מראה איך לקרוא את תקציב הקצב שנותר באותה בקשה.
    query = '''
    {
      complexity { before after query }
      items_page_by_column_values(
        board_id: %d,
        columns: [{column_id: "%s", column_values: ["%s"]}],
        limit: 50
      ) {
        cursor
        items {
          id
          name
          column_values {
            id
            text
            value
          }
        }
      }
    }
    ''' % (board_id, column_id, value)
    response = requests.post(API_URL, headers=headers, json={"query": query})
    return response.json()
```

**עדכון פריטים בכמות:**
```python
def bulk_update_status(api_token: str, board_id: int,
                       item_ids: list, status: str):
    """Update status for multiple items."""
    headers = {
        "Authorization": api_token,
        "API-Version": "2026-07",
        "Content-Type": "application/json",
    }
    for item_id in item_ids:
        mutation = '''
        mutation {
          change_column_value(
            board_id: %d,
            item_id: %d,
            column_id: "status",
            value: "{\\"label\\": \\"%s\\"}"
          ) {
            id
          }
        }
        ''' % (board_id, item_id, status)
        requests.post(API_URL, headers=headers, json={"query": mutation})
```

**יצירת פריט עם תוכן בעברית:**
```python
def create_hebrew_item(api_token: str, board_id: int, group_id: str,
                       item_name: str, column_values: dict):
    """Create a board item with a Hebrew name and Hebrew column values."""
    import json
    headers = {
        "Authorization": api_token,
        "API-Version": "2026-07",
        "Content-Type": "application/json",
    }
    values_json = json.dumps(json.dumps(column_values))
    mutation = '''
    mutation {
      create_item(
        board_id: %d,
        group_id: "%s",
        item_name: "%s",
        column_values: %s
      ) {
        id
      }
    }
    ''' % (board_id, group_id, item_name, values_json)
    response = requests.post(API_URL, headers=headers, json={"query": mutation})
    return response.json()
```

### שלב 6: תיאום בין לוחות

```
צינור מכירות -> קליטת לקוח -> ביצוע פרויקט -> חיוב
     |                  |                    |              |
  Monday.com       Monday.com          Monday.com     הנהלת חשבונות / ERP
  (צוות מכירות)   (ניהול לקוחות)     (צוות פיתוח)   (צוות כספים)
```

**עמודות מראה ואוטומציות:**
- כשסטטוס עסקה = "נסגרה בהצלחה", תיצרו פריט בלוח קליטת לקוח
- כשקליטה הושלמה, תיצרו פריט בלוח פרויקט
- כשפרויקט נמסר, תפעילו חשבונית במערכת החיוב
- תשתמשו בעמודת "חיבור לוחות" של Monday.com להפניות צולבות

לרוב מערכות הנהלת החשבונות והחשבוניות הישראליות אין אפליקציה במרקטפלייס של monday.com. תחפשו ב-https://monday.com/marketplace לפני שאתם מבטיחים אינטגרציה בלחיצה אחת; כשאין רישום, התשובה הכנה היא אינטגרציה ייעודית מעל ה-API של monday יחד עם webhook, ולא התקנת אפליקציה.

## תוכניות, מכסות, ומה באמת חוסם תהליך עבודה

מערכת monday.com מחולקת לארבעה מוצרים נפרדים, לכל אחד סולם תוכניות משלו, והתוכניות בתשלום מתחילות במינימום של 3 מושבים:

| מוצר | דרגות | הערה |
|---------|-------|------|
| Work management | Free, Basic, Standard, Pro, Enterprise | דרגת Free קיימת רק כאן (עד 2 מושבים) |
| CRM | Basic, Standard, Pro, Ultimate | הדרגה העליונה היא Ultimate ולא Enterprise |
| Dev | Basic, Standard, Pro, Enterprise | |
| Service | Standard, Pro, Enterprise | אין דרגת Basic |

טעות כאן שולחת לקוח לדרגה שלא קיימת. אל תצטטו מחירים מהזיכרון; מחירים משתנים מהר יותר משמות הדרגות.

**מה הדרגה באמת חוסמת (work management):**

| יכולת | Standard | Pro | Enterprise |
|------------|----------|-----|------------|
| אוטומציות ואינטגרציות | הדרגה הראשונה שכוללת אותן, 250 פעולות בחודש | 25,000 פעולות בחודש | עד 250,000 פעולות בחודש |
| קריאות API | 1,000 ליום | 10,000 ליום | 25,000 ליום |
| עמודות מתקדמות (תלויות) | לא | כן | כן |

שתי תקרות חשובות יותר מתקציב המורכבות עבור צוות ישראלי קטן:

- **250 פעולות אוטומציה בחודש ב-Standard.** עסק קטן ב-Standard מקבל בערך שמונה פעולות אוטומציה ביום לכל החשבון. מתכון מסוג "התרעה על כל שינוי סטטוס" בלוח פעיל מסיים את המכסה תוך פחות משבוע. תתכננו טריגרים מקובצים או מתוזמנים במקום טריגרים לכל פריט, ותגידו את זה בקול לפני שאתם מציעים מתכון.
- **1,000 קריאות API ביום ב-Standard.** התקרה הזאת נתקעת הרבה לפני תקציב המורכבות של 10 מיליון נקודות. אינטגרציה שדוגמת את ה-API כל דקה צורכת 1,440 קריאות ביום ונכשלת ב-Standard מעצם הבנייה. תשתמשו ב-webhooks במקום.

אוטומציות ואינטגרציות נשענות על אותו מונה פעולות חודשי, ולכן תהליך שמשלב את שתיהן מחויב פעם אחת מול המונה הזה ולא פעמיים.

## וובהוקים מול פולינג

פולינג הוא טעות ברירת המחדל. ב-Standard מכסת הקריאות היומית הופכת דגימה כל דקה לבלתי אפשרית, ובכל דרגה פולינג שורף תקציב מורכבות רק כדי לגלות ששום דבר לא השתנה.

תשתמשו ב-webhook כשצריך להגיב לשינוי. תשתמשו בפולינג רק להתאמה תקופתית, בתדירות נמוכה.

```graphql
mutation {
  create_webhook(
    board_id: BOARD_ID
    url: "YOUR_WEBHOOK_URL"
    event: change_column_value
  ) {
    id
    board_id
  }
}
```

דברים ששוברים אינטגרציות אמיתיות:

- **לחיצת היד של ההרשמה.** בעת היצירה monday שולחת POST עם גוף JSON שמכיל טוקן אקראי בשדה `challenge`, והנקודה שלכם חייבת להחזיר את אותו טוקן בשדה `challenge` בגוף התשובה. נקודה שמחזירה 200 עם גוף ריק נכשלת ברישום.
- **ניסיונות חוזרים.** משלוחים שנכשלו חוזרים פעם בדקה במשך 30 דקות ואז נעצרים. אחרי זה האירוע אבוד, ולכן צרכן webhook עדיין צריך מעבר התאמה תקופתי כדי לרפא חלונות שהוחמצו.
- **תת-פריטים משדרים אירועים משלהם.** האירוע `change_column_value` בלוח האב לא מכסה תת-פריטים; תירשמו בנפרד ל-`change_subitem_column_value` ול-`create_subitem`, אחרת שינויים בתת-פריטים בלתי נראים.
- **אין הבטחת סדר.** תתייחסו לכל payload כאות לקרוא מחדש את הפריט, ולא כמצב החדש והסמכותי.

## מוזרויות של סוגי עמודות

רוב הבאגים באינטגרציות עם monday הם באגי עמודות ולא באגי שאילתות. ארבעה סוגים לא מתנהגים כמו שהתבנית הגנרית `column_values { text value }` מרמזת:

- **חיבור לוחות (connect boards).** גם `text` וגם `value` תמיד מחזירים `null` בעמודה הזאת. תקראו את `display_value` (שמות הפריטים המקושרים, מופרדים בפסיקים), את `linked_item_ids`, או את `linked_items` (שעליהם אפשר לשאול כל שדה של `Item`). הכתיבה משתמשת במבנה אחר לגמרי: `{"connect_boards": {"item_ids": [1122334455, 5544332211]}}`, וכדי לנקות שולחים `{"connect_boards": null}`. קוד שקורא `value` בעמודה הזאת מקבל `null` ומסיק בשקט שהקשר ריק.
- **מראה (mirror).** אותו זוג ריק: `text` ו-`value` מחזירים `null`, תשתמשו ב-`display_value` או ב-`mirrored_items`. עמודות מראה הן לקריאה ויצירה בלבד; אי אפשר לעדכן או לנקות אותן דרך ה-API כי הן משקפות את עמודת המקור בלוח המחובר. סינון לפי תוכן ממוראה לא נתמך, ולכן כל תוכנית של "מצא את כל הפריטים שהבעלים הממוראה שלהם הוא X" חייבת לשאול את לוח המקור במקום.
- **נוסחה (formula).** עמודה מחושבת לקריאה בלבד. אל תתכננו לכתוב אליה, ואל תניחו שה-API מחזיר את התוצאה המחושבת שמוצגת בממשק; תחשבו את הערך בעצמכם אם אוטומציה תלויה בו.
- **סטטוס (status).** כתיבה מקבלת אובייקט תווית, `{"label": "Done"}`, והתווית חייבת כבר להתקיים בלוח. תווית לא מוכרת זורקת `ColumnValueException`, ש-monday מחזירה עם קוד HTTP **200**, ולכן בדיקת `response.ok` תמימה מפרשת כתיבה שנכשלה כהצלחה. תבדקו תמיד את מערך ה-`errors`.

## דוגמאות

### דוגמה 1: הקמת לוח ספרינט
המשתמש אומר: "צור לוח ספרינט לצוות הפיתוח שלי שעובד ראשון עד חמישי"
פעולות:
1. תיצרו לוח עם קבוצות לשבוע עבודה ישראלי (א'-ה' + Backlog + הושלם)
2. תוסיפו עמודות: סטטוס, עדיפות, אחראי, נקודות סיפור, תאריך יעד
3. תבדקו את מכסת הפעולות החודשית של התוכנית, ואז תגדירו אוטומציות פתיחת ספרינט ביום ראשון וסיכום ביום חמישי
4. תגדירו תזמון מודע לחגים
תוצאה: לוח ספרינט מוכן לשימוש עם אינטגרציית לוח שנה ישראלי.

### דוגמה 2: צינור מכירות
המשתמש אומר: "הקם לוח CRM מכירות ב-Monday.com עם שלבים בעברית"
פעולות:
1. תיצרו לוח עם תוויות שלבים בעברית: ליד חדש, פגישה ראשונה, הצעת מחיר, משא ומתן, סגירה
2. תוסיפו עמודות: איש קשר, חברה, ערך עסקה (ש"ח), תאריך סגירה צפוי
3. תגדירו אוטומציות מעקב (התראה על 7 ימים בלי קשר)
4. תגידו למשתמש מראש שתוויות השלבים ושמות הפריטים יהיו בעברית אבל הממשק סביבם לא יהיה
תוצאה: צינור מכירות עם תוכן בעברית ואוטומציות עסקיות ישראליות.

### דוגמה 3: אינטגרציית API
המשתמש אומר: "שלוף את כל הפריטים שעברו את מועד היעד מלוח Monday.com שלי"
פעולות:
1. תשתמשו ב-GraphQL לשאילתת פריטי לוח עם עמודת תאריך יעד, ותעבירו `hierarchy_type` אם לוחות תת-פריטים רלוונטיים
2. תסננו פריטים שתאריך היעד שלהם לפני היום והסטטוס לא "הושלם"
3. תקבצו לפי אחראי ועדיפות
4. אופציונלית, תשלחו סיכום התראות
תוצאה: רשימה מסודרת של פריטים באיחור עם פילוח לפי אחראי.

## משאבים מצורפים

### קובצי עזר
- `references/graphql-patterns.md` -- תבניות שאילתות ומוטציות GraphQL ל-Monday.com API שכוללות אימות, CRUD של לוחות/פריטים, עדכוני ערכי עמודות, ניהול קבוצות, עימוד והגדרת webhooks. תסתכלו על הקובץ הזה כשאתם בונים שאילתות API לאוטומציית לוחות, פעולות פריטים בכמות, או אינטגרציות מותאמות מעבר למה ששרת ה-MCP מספק.

## שרתי MCP מומלצים

הסקיל הזה תוכנן להעצים את **שרת ה-MCP הרשמי `mondaycom/mcp`**. חברו את ה-MCP הזה תחילה, ואז השתמשו בסקיל לתבניות ישראליות מעליו.

| MCP | מה הוא מוסיף |
|-----|--------------|
| [`mondaycom/mcp`](https://github.com/mondaycom/mcp) (npm `@mondaydotcomorg/monday-api-mcp`, גרסה אחרונה 3.3.0) | כלים סטטיים ל-CRUD של לוחות/פריטים/קבוצות: `create_item`, `change_item_column_values`, `move_item_to_group`, `create_board`, `get_board_schema`, `create_column`, `delete_column`, `list_users_and_teams`, `create_form`/`get_form`, ובנוסף **Dynamic API Tools** (בטא) שיוצרים כל GraphQL בזמן ריצה. זמין כהתקנת npm מקומית או כ-MCP מארח. |

לכל מה שלא מכוסה בכלים סטטיים (validation rules, פעולות בפרויקטים/פורטפוליו, knowledge base CRUD, notetaker, שדות מטא-דאטה של לוח), תשתמשו ב-Dynamic API Tools beta ותקבעו `API-Version: 2026-07` (או חדש יותר) בבקשה.

## גרסאות API

מערכת Monday.com מנהלת גרסאות API לפי חודש ומשחררת גרסה חדשה כל רבעון. נכון לאוגוסט 2026 **גרסת ברירת המחדל היא `2026-07`**, כלומר הגרסה שנעשה בה שימוש כשלא נשלחת כותרת. גרסת `2026-10` היא ה-RC הנוכחי, שפורסם ב-1 ביולי 2026. גרסת `2026-04` נכנסה ל-**maintenance ב-1 ביולי 2026** וצפויה לצאת משימוש ביולי 2027, כך שסקיל או אינטגרציה שעדיין נעולים על `2026-04` נמצאים מעבר לחלון היציב וכדאי להזיז אותם. גרסאות `2024-10` ו-`2025-01` הוצאו משימוש ב-15 בפברואר 2026.

קבעו גרסה במפורש בכל בקשה:

```python
headers = {
    "Authorization": API_TOKEN,
    "API-Version": "2026-07",
    "Content-Type": "application/json",
}
```

**התנהגות קבועה, לא חדשות.** הדברים הבאים נכונים כבר כמה גרסאות ולא צריכים לתפוס תשומת לב של מיגרציה: משתנים בשאילתות חייבים להיות אובייקטי JSON ולא מחרוזות; אותיות ה-`column_type` השתנו (`StatusColumn` הפך ל-`status`); `ColumnValueException` נזרק במחמירות על JSON שגוי בעמודה; והשדה `value` בעמודות connect-boards, dependency ו-subtasks מחזיר `null` (תשתמשו ב-`linked_items` / `linked_item_ids`, ראו מוזרויות של סוגי עמודות).

**פעיל ב-`2026-07`:** שדרוג ישות המשתמש נכנס לתוקף. הארגומנטים `kind`, `newest_first` ו-`non_active` ב-`Query.users` יצאו משימוש לטובת `user_kind`, `sort` ו-`status`. שאילתת `users` בלי `limit` מחזירה עכשיו 200 משתמשים במקום כל ההתאמות, וה-`limit` המקסימלי נחסם ב-1000. שדות `User` חדשים כוללים `account_id`, שדה `status` מסוג enum, אובייקט מקונן `photo_url` ו-`became_active_at`; השדה `created_at` הוא כעת `ISO8601DateTime!`, `birthday` הוא `String` ו-`utc_hours_diff` הוא `Float`.

**מגיע ב-`2026-10`:** שדות `User` ישנים מוסרים, כולל שדות התמונה (`photo_original`, `photo_thumb`, `photo_thumb_small`, `photo_tiny`, `photo_small`) ודגלי הבוליאן של סוג וסטטוס (`is_guest`, `is_admin`, `is_pending`, `enabled`). תחליפו בדיקות דגלים בהשוואות `kind` לפני שאתם ננעלים על `2026-10`.

## מלכודות נפוצות

- **לממשק של monday.com אין עברית.** עברית ב-monday היא תוכן ולא לוקליזציה: שמות פריטים, שמות קבוצות, תוויות סטטוס ועדכונים יכולים להיות בעברית, אבל התפריטים, ההגדרות והודעות המערכת נשארים באחת משפות הממשק ש-monday מציעה, ועברית וערבית אינן ביניהן. אין גם הגדרת פריסה RTL ברמת הלוח או החשבון, ולכן טקסט עברי יושב בתוך ממשק שמאל-לימין. תוודאו את רשימת השפות העדכנית בהגדרות הפרופיל של החשבון לפני שאתם מבטיחים משהו. אל תגידו ללקוח ישראלי שהלוח "יהיה בעברית"; תגידו לו שהנתונים שלו יהיו, והממשק לא.
- לוחות רב-רמתיים (עם תת-פריטים) לא נכללים בשאילתת `boards` אלא אם מעבירים `hierarchy_type` או מזהי לוח מפורשים. הכשל הזה שקט: השאילתה מצליחה ופשוט מחזירה פחות לוחות.
- תכנון ספרינטים ב-Monday.com חייב להשתמש בשבוע העבודה הישראלי (ראשון עד חמישי). סוכנים עלולים ליצור מחזורי ספרינט על בסיס שני-שישי, מה שגורם לאי-התאמה בדדליינים וחישובי קיבולת.
- שמות עמודות בעברית מאוחסנים כטקסט RTL. שאילתות API שמשתמשות בשמות עמודות חייבות להתאים למחרוזת העברית המדויקת כולל רווחים וסימני פיסוק.
- אוטומציות Monday.com שמופעלות לפי עמודות תאריך לא מתחשבות בחגים ישראליים כברירת מחדל. סוכנים חייבים להוסיף חריגי חגים ידנית, אחרת האוטומציה תפעל בראש השנה, יום כיפור וכדומה.
- צוותים ישראליים ב-Monday.com בדרך כלל עושים סטנדאפ ביום ראשון. סוכנים עלולים להגדיר אוטומציות סטנדאפ ליום שני, מה שמחמיץ את היום הראשון בשבוע העבודה.
- הגדרת אזור הזמן ב-Monday.com חייבת להיות Asia/Jerusalem (UTC+2/+3) לצוותים ישראליים. סוכנים עלולים להגדיר UTC כברירת מחדל, מה שגורם לאוטומציות לפעול בזמנים שגויים.
- מכסת פעולות האוטומציה החודשית ומכסת קריאות ה-API היומית תלויות בדרגת התוכנית וקטנות ב-Standard. תבדקו אותן לפני שמתכננים תהליך עבודה, ולא אחרי שהלקוח נתקע בקיר.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|-----------|
| תיעוד אימות API של Monday.com | https://developer.monday.com/api-reference/docs/authentication | כתובת ה-endpoint, פורמט כותרת Authorization |
| מגבלות קצב ב-Monday.com | https://developer.monday.com/api-reference/docs/rate-limits | תקציבי מורכבות, `retry_in_seconds`, כותרות `RateLimit` |
| שגיאות ב-Monday.com | https://developer.monday.com/api-reference/docs/errors | קודי שגיאה וקודי ה-HTTP שלהם, כולל מקרי 200-עם-שגיאה |
| שאילתת Boards | https://developer.monday.com/api-reference/reference/boards | הארגומנט `hierarchy_type` וההתנהגות כשהוא מושמט |
| אובייקט Account | https://developer.monday.com/api-reference/reference/account | התנהגות `null` של `plan`, השדות `tier` ו-`products` |
| עמודת חיבור לוחות | https://developer.monday.com/api-reference/docs/connect | `display_value`, `linked_item_ids`, פורמט הכתיבה |
| עמודת מראה | https://developer.monday.com/api-reference/docs/mirror | התנהגות לקריאה בלבד, `mirrored_items` |
| וובהוקים ב-Monday.com | https://developer.monday.com/api-reference/docs/webhooks | רשימת אירועים, לחיצת יד `challenge`, חלון הניסיונות החוזרים |
| תיעוד Items API | https://developer.monday.com/api-reference/docs/items | `items_page`, עימוד עם cursor, ערכי עמודות |
| מסגרת האפליקציות של Monday.com | https://developer.monday.com/apps/docs/api-reference | טריגרים/פעולות אוטומציה מותאמים נבנים דרך מסגרת האפליקציות, אין ל-monday endpoint API ליבה לאוטומציות שאפשר לתשאל |
| גרסאות API של Monday.com | https://developer.monday.com/api-reference/docs/api-versioning | גרסה נוכחית / RC / maintenance / מיושנת |
| מחירון Monday.com | https://monday.com/pricing | מוצרים, שמות דרגות, מכסות פעולות וקריאות API |
| מרקטפלייס Monday.com | https://monday.com/marketplace | האם אפליקציית אינטגרציה באמת קיימת לפני שמבטיחים אותה |

## פתרון בעיות

### שגיאה: "חריגה מתקציב מורכבות"
סיבה: שאילתות GraphQL חרגו מהתקציב. טוקן API אישי מקבל תקציב משותף של 10 מיליון נקודות לדקה לקריאות ולכתיבות יחד (מיליון אחד לחשבונות ניסיון, מלכ"ר וחינם). טוקן אפליקציה שונה: קריאות וכתיבות מוגבלות ל-5 מיליון נקודות מורכבות לדקה **כל אחת**, ולכן אפליקציה שעוברת מטוקן אישי מקבלת תקרת קריאה קטנה יותר למרות שהמספר הכותרתי נראה דומה. שאילתה בודדת לא יכולה לעבור 5 מיליון נקודות בשני המקרים.
פתרון: תוסיפו את השדה `complexity { before after query }` כדי לראות את יתרת התקציב, תשתמשו ב-`items_page` עם `cursor` במקום `items`, תבקשו רק את העמודות שאתם צריכים, ותאטו. כל שגיאת הגבלת קצב מחזירה שדה `retry_in_seconds`, ותשובות 429 נושאות גם כותרת `Retry-After`. כותרות התשובה `RateLimit-Policy` ו-`RateLimit` מדווחות על המדיניות ועל היתרה הנוכחית בכל תשובה, כך שאפשר לווסת עוד לפני שנתקעים בקיר.

### שגיאה: 429 שאינה שגיאת מורכבות
סיבה: מערכת monday אוכפת כמה מצבי 429 נפרדים. הקוד `Rate Limit Exceeded` מציין יותר מ-5,000 בקשות בדקה, `maxConcurrencyExceeded` מציין יותר מדי שאילתות במקביל, `COMPLEXITY_BUDGET_EXHAUSTED` הוא מגבלת המורכבות, ו-`IP_RATE_LIMIT_EXCEEDED` הוא מגבלה לפי כתובת IP. בנפרד, מכסת קריאות ה-API היומית של התוכנית (1,000 ליום ב-Standard) יכולה להיגמר.
פתרון: תקראו את קוד השגיאה במקום להניח מורכבות. תקטינו מקביליות עבור `maxConcurrencyExceeded`, ואם המכסה היומית היא הבעיה, תעברו מפולינג ל-webhooks או תרכשו קריאות API נוספות.

### שגיאה: "שרת MCP לא מגיב"
סיבה: שרת mondaycom/mcp לא מוגדר או טוקן לא תקין.
פתרון: תוודאו את טוקן ה-API ב-monday.com תחת Developers -> My Access Tokens. תפעילו מחדש את שרת ה-MCP. הסקיל עובד גם בלי MCP באמצעות קריאות API ישירות.

### שגיאה: "פורמט ערך עמודה לא תקין"
סיבה: ערכי עמודות Monday.com דורשים פורמטי JSON ספציפיים, והשגיאה `ColumnValueException` מוחזרת עם קוד HTTP **200**, ולכן הבקשה נראית מוצלחת.
פתרון: תבדקו תמיד את מערך ה-`errors` ולא את קוד ה-HTTP. תשתמשו ב-`change_simple_column_value` לטקסט פשוט ולמספרים, תוודאו שתוויות הסטטוס כבר קיימות בלוח, ותבדקו בסעיף מוזרויות של סוגי עמודות את עמודות חיבור-לוחות, מראה ונוסחה.
