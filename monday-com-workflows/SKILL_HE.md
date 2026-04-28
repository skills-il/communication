# תהליכי עבודה ב-Monday.com

## הנחיות

### שלב 1: אימות גישה ל-Monday.com
תבדקו את טוקן ה-API של Monday.com ושרת MCP אופציונלי:

```python
import requests

def verify_monday_access(api_token: str) -> dict:
    """Verify Monday.com API access and get account info."""
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    query = '{ me { name email account { name plan { max_users } } } }'
    response = requests.post(url, headers=headers, json={"query": query})
    return response.json()
```

אם שרת MCP זמין (`mondaycom/mcp`): תשתמשו בכלי MCP לפעולות CRUD בסיסיות.
אם API בלבד: תשתמשו בשאילתות GraphQL ישירות.

### שלב 2: בחירת תבנית תהליך עבודה

**תבניות תהליכי עבודה לצוותים ישראליים:**

| תהליך עבודה | מתאים ל | תכונה מרכזית |
|----------|----------|-------------|
| לוח ספרינט (א'-ה') | צוותי פיתוח | שבוע עבודה ישראלי, מודע לחגים |
| צינור מכירות | צוותי מכירות | שלבים בעברית, אוטומציות מעקב |
| קליטת לקוח | צוותי שירות | תהליכי אישור, מעקב SLA |
| קמפיין שיווקי | שיווק | לוח שנה לקמפיינים, אישור תכנים |
| גיוס משאבי אנוש | משאבי אנוש | מעקב מועמדים, תבניות בעברית |
| מעקב OKR | הנהלה | יעדים רבעוניים, התאמה לרבעונים ישראליים |

### שלב 3: יצירת לוח מותאם

**לוח ספרינט לצוות פיתוח ישראלי:**
```python
def create_israeli_sprint_board(api_token: str, workspace_id: int,
                                 sprint_name: str) -> dict:
    """Create a sprint board optimized for Israeli work week."""
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }

    # Create board with Israeli sprint structure
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

    response = requests.post(url, headers=headers, json={"query": mutation})
    board_data = response.json()
    board_id = board_data["data"]["create_board"]["id"]

    # Create groups for Israeli work week
    groups = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Backlog",
        "Done"
    ]

    for group_name in groups:
        group_mutation = '''
        mutation {
          create_group(board_id: %s, group_name: "%s") {
            id
          }
        }
        ''' % (board_id, group_name)
        requests.post(url, headers=headers, json={"query": group_mutation})

    return board_data
```

### שלב 4: הגדרת אוטומציות

**מתכוני אוטומציה מותאמים לישראל:**

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
# Israeli holidays that affect sprint planning
israeli_holidays_2026 = [
    ("2026-03-03", "2026-03-03", "Purim"),
    ("2026-04-01", "2026-04-09", "Pesach"),
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
    """Check if a date falls on an Israeli holiday."""
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

**חיפוש פריטים בין לוחות:**
```python
def search_items(api_token: str, board_id: int, column_id: str, value: str):
    """Search items by column value."""
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
    }
    query = '''
    {
      items_page_by_column_values(
        board_id: %d,
        columns: [{column_id: "%s", column_values: ["%s"]}],
        limit: 50
      ) {
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
    response = requests.post(url, headers=headers, json={"query": query})
    return response.json()
```

**עדכון פריטים בכמות:**
```python
def bulk_update_status(api_token: str, board_id: int,
                       item_ids: list, status: str):
    """Update status for multiple items."""
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
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
        requests.post(url, headers=headers, json={"query": mutation})
```

**יצירת פריט עם תוכן בעברית:**
```python
def create_hebrew_item(api_token: str, board_id: int, group_id: str,
                       item_name: str, column_values: dict):
    """Create a board item with Hebrew name and values."""
    import json
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": api_token,
        "Content-Type": "application/json"
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
    response = requests.post(url, headers=headers, json={"query": mutation})
    return response.json()
```

### שלב 6: תיאום בין לוחות

**חיבור לוחות לתהליכי עבודה עסקיים ישראליים:**

```
צינור מכירות -> קליטת לקוח -> ביצוע פרויקט -> חיוב
     |                  |                    |              |
  Monday.com       Monday.com          Monday.com     Priority/רווחית
  (צוות מכירות)   (ניהול לקוחות)     (צוות פיתוח)   (צוות כספים)
```

**עמודות מראה ואוטומציות:**
- כשסטטוס עסקה = "נסגרה בהצלחה", תיצרו פריט בלוח קליטת לקוח
- כשקליטה הושלמה, תיצרו פריט בלוח פרויקט
- כשפרויקט נמסר, תפעילו חשבונית במערכת החיוב
- תשתמשו בעמודת "חיבור לוחות" של Monday.com להפניות צולבות

## דוגמאות

### דוגמה 1: הקמת לוח ספרינט
המשתמש אומר: "צור לוח ספרינט לצוות הפיתוח שלי שעובד ראשון עד חמישי"
פעולות:
1. תיצרו לוח עם קבוצות לשבוע עבודה ישראלי (א'-ה' + Backlog + הושלם)
2. תוסיפו עמודות: סטטוס, עדיפות, אחראי, נקודות סיפור, תאריך יעד
3. תגדירו אוטומציות פתיחת ספרינט ביום ראשון וסיכום ביום חמישי
4. תגדירו תזמון מודע לחגים
תוצאה: לוח ספרינט מוכן לשימוש עם אינטגרציית לוח שנה ישראלי.

### דוגמה 2: צינור מכירות
המשתמש אומר: "הקם לוח CRM מכירות ב-Monday.com עם שלבים בעברית"
פעולות:
1. תיצרו לוח עם שלבי צינור בעברית: ליד חדש, פגישה ראשונה, הצעת מחיר, משא ומתן, סגירה
2. תוסיפו עמודות: איש קשר, חברה, ערך עסקה (ש"ח), תאריך סגירה צפוי
3. תגדירו אוטומציות מעקב (התראה על 7 ימים בלי קשר)
4. תיצרו דשבורד עם סיכום ערך הצינור
תוצאה: צינור מכירות בעברית עם אוטומציות עסקיות ישראליות.

### דוגמה 3: אינטגרציית API
המשתמש אומר: "שלוף את כל הפריטים שעברו את מועד היעד מלוח Monday.com שלי"
פעולות:
1. תשתמשו ב-GraphQL לשאילתת פריטי לוח עם עמודת תאריך יעד
2. תסננו פריטים שתאריך היעד שלהם לפני היום והסטטוס לא "הושלם"
3. תקבצו לפי אחראי ועדיפות
4. אופציונלית, תשלחו סיכום התראות
תוצאה: רשימה מסודרת של פריטים באיחור עם פילוח לפי אחראי.

## משאבים מצורפים

### שרתי MCP מומלצים

הסקיל הזה תוכנן להעצים את **שרת ה-MCP הרשמי `mondaycom/mcp`**. חברו את ה-MCP הזה תחילה, ואז השתמשו בסקיל לתבניות ישראליות מעליו.

| MCP | מה הוא מוסיף |
|-----|--------------|
| [`mondaycom/mcp`](https://github.com/mondaycom/mcp) (npm `@mondaydotcomorg/monday-api-mcp`) | כלים סטטיים ל-CRUD של לוחות/פריטים/קבוצות: `create_item`, `change_item_column_values`, `move_item_to_group`, `create_board`, `get_board_schema`, `create_column`, `delete_column`, `list_users_and_teams`, `create_form`/`get_form`, ובנוסף **Dynamic API Tools** (בטא) שיוצרים כל GraphQL בזמן ריצה. זמין כהתקנת npm מקומית או כ-MCP מארח. |

לכל מה שלא מכוסה בכלים סטטיים (validation rules, פעולות בפרויקטים/פורטפוליו, knowledge base CRUD, notetaker, שדות מטא-דאטה של לוח), השתמשו ב-Dynamic API Tools beta והקפידו על `API-Version: 2026-04` (או חדש יותר) בבקשה.

### גרסאות API

Monday.com מנהלת גרסאות API לפי חודש. נכון ל-2026-04 **גרסת ברירת המחדל היא `2026-04`**, עם `2026-07` כ-RC ו-`2026-10` בהפצה. גרסאות `2024-10` ו-`2025-01` **הוצאו משימוש ב-2026-02-15**.

קבעו גרסה במפורש בכל בקשה:

```python
headers = {
    "Authorization": API_TOKEN,
    "API-Version": "2026-04",
    "Content-Type": "application/json",
}
```

**שינויים שוברים מאז 2025-04:**
- משתנים בשאילתות חייבים להיות JSON, לא string
- `column_type` באותיות שונות (למשל `StatusColumn` → `status`)
- `ColumnValueException` נזרק במחמירות על JSON שגוי בעמודה
- `value` בעמודות connect-boards / dependency / subtasks מחזיר עכשיו `null`; השתמשו ב-`linked_items` / `linked_item_ids`
- שאילתות על `users` בלי הגבלה מפורשת מקבלות 200 כברירת מחדל (היה ללא הגבלה)

### קובצי עזר
- `references/graphql-patterns.md` -- תבניות שאילתות ומוטציות GraphQL ל-Monday.com API שכוללות אימות, CRUD של לוחות/פריטים, עדכוני ערכי עמודות, ניהול קבוצות, עימוד והגדרת webhooks. תסתכלו על הקובץ הזה כשאתם בונים שאילתות API לאוטומציית לוחות, פעולות פריטים בכמות, או אינטגרציות מותאמות מעבר למה ששרת ה-MCP מספק.

## מלכודות נפוצות

- תכנון ספרינטים ב-Monday.com חייב להשתמש בשבוע העבודה הישראלי (ראשון עד חמישי). סוכנים עלולים ליצור מחזורי ספרינט על בסיס שני-שישי, מה שגורם לאי-התאמה בדדליינים וחישובי קיבולת.
- שמות עמודות בעברית ב-Monday.com מאוחסנים כטקסט RTL. שאילתות API שמשתמשות בשמות עמודות חייבות להתאים למחרוזת העברית המדויקת כולל רווחים וסימני פיסוק.
- אוטומציות Monday.com שמופעלות לפי עמודות תאריך לא מתחשבות בחגים ישראליים כברירת מחדל. סוכנים חייבים להוסיף חריגי חגים ידנית, אחרת האוטומציה תפעל בראש השנה, יום כיפור וכו'.
- צוותים ישראליים ב-Monday.com בדרך כלל עושים סטנדאפ ביום ראשון. סוכנים עלולים להגדיר אוטומציות סטנדאפ ליום שני, מה שמחמיץ את היום הראשון בשבוע העבודה.
- הגדרת אזור הזמן ב-Monday.com חייבת להיות Asia/Jerusalem (UTC+2/+3) לצוותים ישראליים. סוכנים עלולים להגדיר UTC כברירת מחדל, מה שגורם לאוטומציות לפעול בזמנים שגויים.

## קישורי עזר

| מקור | כתובת | מה לבדוק |
|------|-------|-----------|
| תיעוד אימות API של Monday.com | https://developer.monday.com/api-reference/docs/authentication | כתובת ה-endpoint, פורמט כותרת Authorization |
| מגבלות קצב ב-Monday.com | https://developer.monday.com/api-reference/docs/rate-limits | תקציב מורכבות (10 מיליון נקודות לדקה למשתמש), איפוס |
| סקירת GraphQL של Monday.com | https://developer.monday.com/api-reference/docs/introduction-to-graphql | מבנה שאילתות, מורכבויות ברירת מחדל, שדה `complexity` |
| תיעוד Items API | https://developer.monday.com/api-reference/docs/items | `items_page`, עימוד עם cursor, ערכי עמודות |
| אוטומציות ב-Monday.com | https://developer.monday.com/api-reference/reference/automations | מתכוני טריגר/פעולה, ממשק API לאוטומציות |
| גרסאות API של Monday.com | https://developer.monday.com/api-reference/docs/api-versioning | גרסה נוכחית / RC / מיושנת, מדריכי מיגרציה |

## פתרון בעיות

### שגיאה: "חריגה מתקציב מורכבות"
סיבה: שאילתות GraphQL חרגו מתקציב המשתמש (10,000,000 נקודות מורכבות לדקה; 1,000,000 לחשבונות ניסיון וחינמיים). שאילתה בודדת לא יכולה לעבור 5,000,000 נקודות.
פתרון: תוסיפו את שדה `complexity` לשאילתות כדי לראות את יתרת התקציב, תשתמשו ב-`items_page` עם `cursor` במקום `items`, תבקשו רק את העמודות שאתם צריכים ותחכו לאיפוס התקציב בתחילת הדקה הבאה.

### שגיאה: "שרת MCP לא מגיב"
סיבה: שרת mondaycom/mcp לא מוגדר או טוקן לא תקין
פתרון: תוודאו את טוקן ה-API ב-monday.com תחת Developers -> My Access Tokens. תפעילו מחדש את שרת ה-MCP. הסקיל עובד גם בלי MCP באמצעות קריאות API ישירות.

### שגיאה: "פורמט ערך עמודה לא תקין"
סיבה: ערכי עמודות Monday.com דורשים פורמטי JSON ספציפיים
פתרון: תשתמשו במוטציה `change_simple_column_value` לטקסט/מספר, או תבדקו בתיעוד Monday.com API את פורמטי JSON הייעודיים לעמודות (תוויות סטטוס, תאריכים וכו').
