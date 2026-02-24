# תהליכי עבודה ב-Monday.com

## הנחיות

### שלב 1: אימות גישה ל-Monday.com
בדקו את אסימון ה-API של Monday.com ושרת MCP אופציונלי:

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

אם שרת MCP זמין (`mondaycom/mcp`): השתמשו בכלי MCP לפעולות CRUD בסיסיות.
אם API בלבד: השתמשו בשאילתות GraphQL ישירות.

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
israeli_holidays_2025 = [
    ("2025-04-13", "2025-04-19", "Pesach"),
    ("2025-06-02", "2025-06-02", "Shavuot"),
    ("2025-09-23", "2025-09-24", "Rosh Hashana"),
    ("2025-10-02", "2025-10-02", "Yom Kippur"),
    ("2025-10-07", "2025-10-13", "Sukkot"),
]

def is_israeli_holiday(date_str: str) -> tuple[bool, str]:
    """Check if a date falls on an Israeli holiday."""
    from datetime import datetime
    check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    for start, end, name in israeli_holidays_2025:
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
- כשסטטוס עסקה = "נסגרה בהצלחה" -- צרו פריט בלוח קליטת לקוח
- כשקליטה הושלמה -- צרו פריט בלוח פרויקט
- כשפרויקט נמסר -- הפעילו חשבונית במערכת החיוב
- השתמשו בעמודת "חיבור לוחות" של Monday.com להפניות צולבות

## דוגמאות

### דוגמה 1: הקמת לוח ספרינט
המשתמש אומר: "צור לוח ספרינט לצוות הפיתוח שלי שעובד ראשון עד חמישי"
פעולות:
1. צרו לוח עם קבוצות לשבוע עבודה ישראלי (א'-ה' + Backlog + הושלם)
2. הוסיפו עמודות: סטטוס, עדיפות, אחראי, נקודות סיפור, תאריך יעד
3. הגדירו אוטומציות פתיחת ספרינט ביום ראשון וסיכום ביום חמישי
4. הגדירו תזמון מודע לחגים
תוצאה: לוח ספרינט מוכן לשימוש עם אינטגרציית לוח שנה ישראלי.

### דוגמה 2: צינור מכירות
המשתמש אומר: "הקם לוח CRM מכירות ב-Monday.com עם שלבים בעברית"
פעולות:
1. צרו לוח עם שלבי צינור בעברית: ליד חדש, פגישה ראשונה, הצעת מחיר, משא ומתן, סגירה
2. הוסיפו עמודות: איש קשר, חברה, ערך עסקה (ש"ח), תאריך סגירה צפוי
3. הגדירו אוטומציות מעקב (התראה על 7 ימים ללא קשר)
4. צרו דשבורד עם סיכום ערך הצינור
תוצאה: צינור מכירות בעברית עם אוטומציות עסקיות ישראליות.

### דוגמה 3: אינטגרציית API
המשתמש אומר: "שלוף את כל הפריטים שעברו את מועד היעד מלוח Monday.com שלי"
פעולות:
1. השתמשו ב-GraphQL לשאילתת פריטי לוח עם עמודת תאריך יעד
2. סננו פריטים שתאריך היעד שלהם לפני היום והסטטוס אינו "הושלם"
3. קבצו לפי אחראי ועדיפות
4. אופציונלית -- שלחו סיכום התראות
תוצאה: רשימה מסודרת של פריטים באיחור עם פילוח לפי אחראי.

## משאבים מצורפים

### קובצי עזר
- `references/graphql-patterns.md` — תבניות שאילתות ומוטציות GraphQL ל-Monday.com API הכוללות אימות, CRUD של לוחות/פריטים, עדכוני ערכי עמודות, ניהול קבוצות, עימוד והגדרת webhooks. היעזרו בקובץ בעת בניית שאילתות API לאוטומציית לוחות, פעולות פריטים בכמות, או אינטגרציות מותאמות מעבר למה ששרת ה-MCP מספק.

## פתרון בעיות

### שגיאה: "חריגה מתקציב מורכבות"
סיבה: שאילתת GraphQL מורכבת מדי (מעל 10,000 נקודות לדקה)
פתרון: פשטו שאילתות, השתמשו בעימוד עם `limit` ו-`cursor`, הימנעו מבקשת כל ערכי העמודות כשלא נדרש. השתמשו ב-`items_page` במקום `items` ללוחות גדולים.

### שגיאה: "שרת MCP לא מגיב"
סיבה: שרת mondaycom/mcp לא מוגדר או אסימון לא תקין
פתרון: ודאו את אסימון ה-API ב-monday.com ואז Admin ואז API. הפעילו מחדש את שרת ה-MCP. סקיל זה עובד גם ללא MCP באמצעות קריאות API ישירות.

### שגיאה: "פורמט ערך עמודה לא תקין"
סיבה: ערכי עמודות Monday.com דורשים פורמטי JSON ספציפיים
פתרון: השתמשו במוטציה `change_simple_column_value` לטקסט/מספר, או בדקו בתיעוד Monday.com API את פורמטי JSON הייעודיים לעמודות (תוויות סטטוס, תאריכים וכו').
