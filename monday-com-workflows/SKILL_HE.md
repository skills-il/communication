# תהליכי עבודה ב-Monday.com

## הנחיות

### שלב 1: אימות גישה ל-Monday.com

תבדקו את טוקן ה-API של Monday.com ושרת MCP אופציונלי. אל תשתמשו ב-`account { plan { max_users } }` כבדיקת חיים: השדה `account.plan` מתועד כמחזיר `null` בחשבונות שרצים על תשתית ריבוי-המוצרים של monday, וזה בדיוק מה שחשבונות חדשים מקבלים. תקראו במקום זאת `account { tier products { kind } }` ותתייחסו ל-`plan` כאופציונלי.

```python
import json, re, time, uuid
import requests

API_URL = "https://api.monday.com/v2"
API_VERSION = "2026-07"  # see API Versioning before changing

def gql(api_token: str, query: str, variables: dict | None = None,
        idempotency_key: str | None = None, retries: int = 3) -> dict:
    """Run one GraphQL operation and return its `data`.

    Pass every user-supplied string through `variables`, never by string
    formatting: a Hebrew acronym typed with an ASCII quote (for example
    the Hebrew abbreviation for VAT) ends a GraphQL string literal and the
    query fails to parse. monday also returns many errors with HTTP 200,
    so the `errors` array is checked, not the status code.

    For a mutation, pass one idempotency_key (e.g. str(uuid.uuid4())) per
    logical change; it is reused on every retry so a retry cannot create
    a duplicate: a timed-out request is re-sent here with the same key.
    Rate-limit errors and 409/429 responses wait for the time monday gives."""
    headers = {"Authorization": api_token, "API-Version": API_VERSION,
               "Content-Type": "application/json"}
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    for attempt in range(retries + 1):
        try:
            resp = requests.post(API_URL, headers=headers, timeout=30,
                                 json={"query": query, "variables": variables or {}})
        except (requests.Timeout, requests.ConnectionError):
            is_mutation = query.lstrip().startswith("mutation")
            if attempt == retries or (is_mutation and not idempotency_key):
                raise  # without a key, re-sending a mutation could duplicate it
            time.sleep(2 ** attempt)  # same headers, same Idempotency-Key
            continue
        retry_after = resp.headers.get("Retry-After", "")
        if resp.status_code in (409, 429) and retry_after.isdigit() and attempt < retries:
            time.sleep(int(retry_after))
            continue
        try:
            data = resp.json()
        except ValueError:
            raise RuntimeError(f"monday API HTTP {resp.status_code}: {resp.text[:200]}")
        wait = re.search(r'"retry_in_seconds":\s*(\d+)', json.dumps(data))
        if wait and attempt < retries:
            time.sleep(int(wait.group(1)))
            continue
        if data.get("errors"):
            raise RuntimeError(f"monday API error: {data['errors']}")
        return data["data"]

def verify_monday_access(api_token: str) -> dict:
    """Verify Monday.com API access and return normalized account info."""
    data = gql(api_token, """
    {
      me { name email }
      account { name tier products { kind } plan { max_users tier period } }
    }""")
    account = data["account"]
    plan = account.get("plan")  # None on multi-product-infrastructure accounts
    return {
        "user": data["me"],
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
    board = gql(api_token, """
    mutation ($name: String!, $ws: ID) {
      create_board(board_name: $name, board_kind: public, workspace_id: $ws) { id }
    }""", {"name": sprint_name, "ws": workspace_id},
        idempotency_key=str(uuid.uuid4()))["create_board"]

    for group_name in ["Sunday", "Monday", "Tuesday", "Wednesday",
                       "Thursday", "Backlog", "Done"]:
        gql(api_token, """
        mutation ($board: ID!, $name: String!) {
          create_group(board_id: $board, group_name: $name) { id }
        }""", {"board": board["id"], "name": group_name},
            idempotency_key=str(uuid.uuid4()))
    return board
```

### שלב 4: הגדרת אוטומציות

לפני שמתכננים אוטומציה, תבדקו את מכסת הפעולות החודשית של החשבון (ראו תוכניות ומכסות). אוטומציה שרצה על כל פריט בלוח עמוס יכולה לשרוף את כל החודש של תוכנית Standard תוך ימים.

את המתכונים שלמטה מגדירים במרכז האוטומציות של הלוח. דרך שרת ה-MCP המאוחסן של monday, סוכן יכול גם ליצור אוטומציה מתיאור בשפה טבעית עם הכלי `create_automation`; כשחסר פרט הוא מחזיר `needs_clarification`, ואז צריך לשאול את המשתמש ולא לנחש.

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
הקפאה צריכה שלושה מצבים ולא כן/לא: `off` (ימי המנוחה הקבועים בחוק, ובנוסף יום העצמאות), `half` (ערב חג, קיבולת מופחתת), ו-`policy` (חול המועד, חנוכה, פורים, תשעה באב, יום השואה ויום הזיכרון: ימי עבודה על פי חוק שצוותים מתייחסים אליהם אחרת). תשאלו את ראש הצוות איך הם מתייחסים לימי `policy` לפני שמקפיאים משהו; הקפאה של כל חנוכה מוחקת שבוע עבודה שלם.

בקובץ `references/israeli-holidays.md` יש טבלה לפי לוח החגים בישראל ל-2026 עד 2028, עוזר `israel_today()` (בשרת שעובד ב-UTC, `date.today()` מחזיר תאריך שגוי במשך כמה שעות אחרי חצות בישראל), פונקציה `holiday_state()` שזורקת שגיאה על שנה שאינה בטבלה במקום לענות בשקט "יום עבודה", ועוזר `sprint_capacity()` שמדלג על שישי ושבת ומקבל כל יום התחלה. תמיד תשתמשו בתאריכים של ישראל (hebcal עם `i=on`), ולעולם לא בתאריכי חוץ לארץ עם יום טוב שני.

האוטומציות החוזרות של monday עצמה לא יכולות לבדוק את הטבלה הזו. כשמתכון צריך לדלג על חגים, תריצו אותו מג'וב מתוזמן משלכם שבודק `holiday_state(israel_today())` ורק אז קורא ל-API.

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
    """Search items by column value. Returns the first page plus a cursor:
    with limit:50 you only get 50 matches, so loop with next_items_page
    until the cursor is null. `complexity` shows the remaining budget."""
    return gql(api_token, """
    query ($board: ID!, $columns: [ItemsPageByColumnValuesQuery!]) {
      complexity { before after query }
      items_page_by_column_values(board_id: $board, columns: $columns, limit: 50) {
        cursor
        items { id name column_values { id text value } }
      }
    }""", {"board": board_id,
           "columns": [{"column_id": column_id, "column_values": [value]}]})
```

**פריטים באיחור (תאריך לפני היום), כל העמודים:**
```python
def overdue_items(api_token: str, board_id: int, due_column_id: str) -> list:
    """Every item whose due date is before today. "TODAY" is resolved in the
    time zone of the user who owns the token (see Gotchas)."""
    page = gql(api_token, """
    query ($board: [ID!], $params: ItemsQuery) {
      boards(ids: $board) {
        items_page(limit: 100, query_params: $params) {
          cursor
          items { id name column_values { id text } }
        }
      }
    }""", {"board": [board_id], "params": {"rules": [{
        "column_id": due_column_id, "compare_value": ["TODAY"],
        "operator": "lower_than"}]}})["boards"][0]["items_page"]
    items = page["items"]
    while page["cursor"]:
        page = gql(api_token, """
        query ($cursor: String!) {
          next_items_page(limit: 100, cursor: $cursor) {
            cursor
            items { id name column_values { id text } }
          }
        }""", {"cursor": page["cursor"]})["next_items_page"]
        items += page["items"]
    return items
```
תסננו בצד שלכם פריטים שטקסט הסטטוס שלהם הוא "Done" לפני שמדווחים עליהם.

**שליחת רשימת האיחורים ל-Slack.** יש שתי דרכים. האינטגרציה המובנית של monday ל-Slack רצה בתוך monday וצורכת ממכסת פעולות האינטגרציה (250 פעולות בחודש ב-Standard, ראו תוכניות ומכסות), ולכן התראה על כל פריט יכולה לגמור אותה. החלופה היא ג'וב יומי משלכם: לקרוא ל-`overdue_items`, ואז לשלוח POST עם JSON בצורה `{"text": "..."}` לכתובת incoming webhook של Slack. תבדקו קודם את `holiday_state(israel_today())` כדי שהסיכום לא יישלח ביום כיפור, ותזכרו שכל קריאה ל-monday נספרת במכסת קריאות ה-API היומית.

**עדכון פריטים בכמות:**
```python
def bulk_update_status(api_token: str, board_id: int, item_ids: list,
                       status: str, status_column_id: str):
    """Set a status label on many items. Pass the status column's id (it is
    often not literally "status" on copied or template boards). Each item is
    one API call, so on Standard (1,000 calls/day) keep batches small."""
    value = json.dumps({status_column_id: {"label": status}}, ensure_ascii=False)
    for item_id in item_ids:
        gql(api_token, """
        mutation ($board: ID!, $item: ID!, $value: JSON!) {
          change_multiple_column_values(board_id: $board, item_id: $item,
                                        column_values: $value) { id }
        }""", {"board": board_id, "item": item_id, "value": value},
            idempotency_key=str(uuid.uuid4()))
```

**יצירת פריט עם תוכן בעברית:**
```python
def create_hebrew_item(api_token: str, board_id: int, group_id: str,
                       item_name: str, column_values: dict):
    """Create an item with a Hebrew name and Hebrew column values. Variables
    keep quotes inside Hebrew text from breaking the query."""
    return gql(api_token, """
    mutation ($board: ID!, $group: String, $name: String!, $values: JSON) {
      create_item(board_id: $board, group_id: $group, item_name: $name,
                  column_values: $values) { id }
    }""", {"board": board_id, "group": group_id, "name": item_name,
           "values": json.dumps(column_values, ensure_ascii=False)},
        idempotency_key=str(uuid.uuid4()))
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

מערכת monday.com מוכרת כמה מוצרים, לכל אחד סולם תוכניות משלו: work management, CRM, Campaigns, Dev ו-Service. ל-work management יש Free, Basic, Standard, Pro ו-Enterprise (דרגת Free מכסה עד 2 מושבים); הדרגה העליונה של CRM היא Ultimate ולא Enterprise. את הסולמות של שאר המוצרים תבדקו בדפי התמחור שלהם, ואל תניחו שהם זהים ל-work management.

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

קריאות דרך שרת ה-MCP המאוחסן של monday נספרות באותה מכסת קריאות API יומית, כי כל קריאה לכלי MCP מבוצעת כבקשת GraphQL. סוכן שעובד דרך ה-MCP בחשבון Standard חולק את 1,000 הקריאות ביום עם כל שאר האינטגרציות.

**תהליכי Workflows אינם אוטומציות.** דף התמחור מציג היום מספר workflows לכל דרגה (3 ב-Standard, 20 ב-Pro). התיעוד של monday מתאר אותם כאובייקטים חוצי-לוחות ברמת סביבת העבודה, נפרדים מאוטומציות שמוגדרות לכל לוח בנפרד. בונים אותם דרך כלי ה-workflow של ה-MCP מול סכמת ה-API בגרסת dev (preview), הם נוצרים כטיוטה, וצריך לפרסם אותם לפני שהם רצים. אל תבטיחו ללקוח workflow שנבנה על ה-API היציב.

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
- **ניסיונות חוזרים.** משלוחים שנכשלו חוזרים פעם בדקה במשך 30 דקות. monday לא מתעדת שום משלוח אחרי החלון הזה, ולכן צרכן webhook עדיין צריך מעבר התאמה תקופתי כדי לרפא חלונות שהוחמצו.
- **ניסיון חוזר שלכם משכפל דברים.** כשמוטציה נתקעת ואתם שולחים אותה שוב, תצרפו כותרת `Idempotency-Key`. המערכת שומרת את התשובה הראשונה ל-30 דקות ועונה לניסיון החוזר עם התוצאה השמורה (`Idempotency-Replayed: true`) במקום ליצור פריט שני.
- **תת-פריטים משדרים אירועים משלהם.** האירוע `change_column_value` בלוח האב לא מכסה תת-פריטים; תירשמו בנפרד ל-`change_subitem_column_value` ול-`create_subitem`, אחרת שינויים בתת-פריטים בלתי נראים.
- **אין הבטחת סדר.** תתייחסו לכל payload כאות לקרוא מחדש את הפריט, ולא כמצב החדש והסמכותי.

## מוזרויות של סוגי עמודות

רוב הבאגים באינטגרציות עם monday הם באגי עמודות ולא באגי שאילתות. ארבעה סוגים לא מתנהגים כמו שהתבנית הגנרית `column_values { text value }` מרמזת:

- **חיבור לוחות (connect boards).** גם `text` וגם `value` תמיד מחזירים `null` בעמודה הזאת. תקראו את `display_value` (שמות הפריטים המקושרים, מופרדים בפסיקים), את `linked_item_ids`, או את `linked_items` (שעליהם אפשר לשאול כל שדה של `Item`). הכתיבה משתמשת במבנה אחר לגמרי: `{"connect_boards": {"item_ids": [1122334455, 5544332211]}}`, וכדי לנקות שולחים `{"connect_boards": null}`. קוד שקורא `value` בעמודה הזאת מקבל `null` ומסיק בשקט שהקשר ריק.
- **מראה (mirror).** אותו זוג ריק: `text` ו-`value` מחזירים `null`, תשתמשו ב-`display_value` או ב-`mirrored_items`. עמודות מראה הן לקריאה ויצירה בלבד; אי אפשר לעדכן או לנקות אותן דרך ה-API כי הן משקפות את עמודת המקור בלוח המחובר. סינון לפי תוכן ממוראה לא נתמך, ולכן כל תוכנית של "מצא את כל הפריטים שהבעלים הממוראה שלהם הוא X" חייבת לשאול את לוח המקור במקום.
- **נוסחה (formula).** קריאה ויצירה בלבד; אי אפשר לכתוב אליה ערך. התוצאה המחושבת חוזרת בשדה `display_value`; השדות `text` ו-`value` לא מאוכלסים, כך שקוד שקורא את `text` יסיק שהנוסחה ריקה.
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
- `references/israeli-holidays.md` -- טבלת חגים לפי לוח ישראל ל-2026 עד 2028 עם מצבי off / half / policy, פונקציה `holiday_state()` שמסרבת לענות על שנים שאינן מכוסות, ועוזר לחישוב קיבולת ספרינט. תסתכלו עליו בכל לוגיקה של ספרינט, הקפאה או ג'וב מתוזמן.
- `references/graphql-patterns.md` -- תבניות שאילתות ומוטציות GraphQL ל-Monday.com API שכוללות אימות, CRUD של לוחות/פריטים, עדכוני ערכי עמודות, ניהול קבוצות, עימוד והגדרת webhooks. תסתכלו על הקובץ הזה כשאתם בונים שאילתות API לאוטומציית לוחות, פעולות פריטים בכמות, או אינטגרציות מותאמות מעבר למה ששרת ה-MCP מספק.

## שרתי MCP מומלצים

הסקיל הזה תוכנן להעצים את **שרת ה-MCP הרשמי `mondaycom/mcp`**. חברו את ה-MCP הזה תחילה, ואז השתמשו בסקיל לתבניות ישראליות מעליו.

| MCP | מה הוא מוסיף |
|-----|--------------|
| [`mondaycom/mcp`](https://github.com/mondaycom/mcp) (npm `@mondaydotcomorg/monday-api-mcp`, גרסה אחרונה 3.3.0) | כלים סטטיים ל-CRUD של לוחות/פריטים/קבוצות: `create_item`, `change_item_column_values`, `move_item_to_group`, `create_board`, `get_board_schema`, `create_column`, `delete_column`, `list_users_and_teams`, `create_form`/`get_form`, ובנוסף **Dynamic API Tools** (בטא) שיוצרים כל GraphQL בזמן ריצה. זמין כהתקנת npm מקומית או כ-MCP מארח. |

לכל מה שלא מכוסה בכלים סטטיים (validation rules, פעולות בפרויקטים/פורטפוליו, knowledge base CRUD, notetaker, שדות מטא-דאטה של לוח), תשתמשו ב-Dynamic API Tools beta ותקבעו `API-Version: 2026-07` (או חדש יותר) בבקשה.

## גרסאות API

מערכת Monday.com מנהלת גרסאות API לפי חודש ומשחררת גרסה חדשה כל רבעון. זה לוח הזמנים הרשמי:

| גרסה | Release candidate | נוכחית (ברירת מחדל) | Maintenance |
|------|-------------------|---------------------|-------------|
| `2026-04` | 15 בינואר 2026 | 1 באפריל 2026 | 1 ביולי 2026 |
| `2026-07` | 1 באפריל 2026 | 1 ביולי 2026 | 1 באוקטובר 2026 |
| `2026-10` | 1 ביולי 2026 | 1 באוקטובר 2026 | 15 בינואר 2027 |
| `2027-01` | 1 באוקטובר 2026 | 15 בינואר 2027 | 1 באפריל 2027 |

כלומר `2026-07` היא ברירת המחדל (הגרסה שנעשה בה שימוש כשלא נשלחת כותרת) עד **1 באוקטובר 2026**, ואז `2026-10` הופכת לברירת המחדל ו-`2026-07` עוברת ל-maintenance. גרסאות maintenance נשארות יציבות ושמישות; לא פורסם תאריך יציאה משימוש ל-`2026-04` או לגרסאות מאוחרות יותר (monday מודיעה על כל אחד לפחות שישה חודשים מראש). גרסאות `2024-10` ו-`2025-01` הוצאו משימוש ב-15 בפברואר 2026. אינטגרציה שלא נועלת גרסה משנה התנהגות ב-1 באוקטובר, ולכן כל הדוגמאות כאן נועלות את `API-Version` במפורש.

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

**מגיע ב-`2026-10`:** לפי ה-release notes, שדות `User` ישנים מוסרים, כולל שדות התמונה (`photo_original`, `photo_thumb`, `photo_thumb_small`, `photo_tiny`, `photo_small`) ודגלי הבוליאן של סוג וסטטוס (`is_guest`, `is_admin`, `is_pending`, `enabled`). תחליפו בדיקות דגלים בהשוואות `kind` לפני שאתם ננעלים על `2026-10`.

## מלכודות נפוצות

- **לממשק של monday.com אין עברית.** עברית ב-monday היא תוכן ולא לוקליזציה: שמות פריטים, שמות קבוצות, תוויות סטטוס ועדכונים יכולים להיות בעברית, אבל התפריטים, ההגדרות והודעות המערכת נשארים באחת מ-15 שפות הממשק שמופיעות במאמר התמיכה של monday (עודכן לאחרונה ב-31 באוגוסט 2026), ועברית וערבית אינן ביניהן. לכן טקסט עברי יושב בתוך ממשק שמאל-לימין. תבדקו שוב את המאמר, או את הלשונית Language and Region בפרופיל, לפני שאתם מבטיחים משהו. אל תגידו ללקוח ישראלי שהלוח "יהיה בעברית"; תגידו לו שהנתונים שלו יהיו, והממשק לא.
- לוחות רב-רמתיים (עם תת-פריטים) לא נכללים בשאילתת `boards` אלא אם מעבירים `hierarchy_type` או מזהי לוח מפורשים. הכשל הזה שקט: השאילתה מצליחה ופשוט מחזירה פחות לוחות.
- תכנון ספרינטים ב-Monday.com חייב להשתמש בשבוע העבודה הישראלי (ראשון עד חמישי). סוכנים עלולים ליצור מחזורי ספרינט על בסיס שני-שישי, מה שגורם לאי-התאמה בדדליינים וחישובי קיבולת.
- תפנו לעמודות לפי ה-**id** שלהן (`status`, `date4`), ולעולם לא לפי הכותרת העברית. תמפו כותרת ל-id פעם אחת עם `columns { id title type }` ותשמרו את ה-id; כותרות משתנות, וסימני פיסוק בעברית הופכים התאמה מדויקת לשבירה.
- מסנני תאריך כמו `"TODAY"` מחושבים לפי אזור הזמן, פורמט התאריך והיום הראשון בשבוע שמוגדרים בפרופיל של המשתמש שהטוקן שייך לו. טוקן של מי שהשבוע שלו מתחיל ביום שני, או שהפרופיל שלו על UTC, מזיז את "השבוע" ואת "היום" עבור צוות ישראלי.
- אוטומציות Monday.com שמופעלות לפי עמודות תאריך לא מתחשבות בחגים ישראליים. טבלת החגים ב-`references/israeli-holidays.md` מכסה רק את 2026 עד 2028; לשנים הבאות תשלפו מ-hebcal (`i=on`) במקום לעשות שימוש חוזר בטבלה ישנה.
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
| מסגרת האפליקציות של Monday.com | https://developer.monday.com/apps/docs/api-reference | טריגרים ופעולות אוטומציה מותאמים שנבנים כאפליקציות monday |
| יצירת אוטומציה (MCP) ב-Monday.com | https://developer.monday.com/api-reference/docs/create-automation | יצירת אוטומציה בלוח דרך ה-Platform MCP |
| גרסאות API של Monday.com | https://developer.monday.com/api-reference/docs/api-versioning | גרסה נוכחית / RC / maintenance / מיושנת |
| Idempotency ב-Monday.com | https://developer.monday.com/api-reference/docs/idempotency | כותרת `Idempotency-Key`, חלון שחזור של 30 דקות |
| עמודת תאריך ב-Monday.com | https://developer.monday.com/api-reference/reference/date | ערכי השוואה כמו `"TODAY"` והגדרות הפרופיל שהם תלויים בהן |
| Hebcal (לוח ישראל) | https://www.hebcal.com/holidays/ | תאריכי חגים לשנה חדשה, עם האפשרות של ישראל |
| מחירון Monday.com | https://monday.com/pricing | מוצרים, שמות דרגות, מכסות פעולות וקריאות API |
| מרקטפלייס Monday.com | https://monday.com/marketplace | האם אפליקציית אינטגרציה באמת קיימת לפני שמבטיחים אותה |

## פתרון בעיות

### שגיאה: "חריגה מתקציב מורכבות"
סיבה: שאילתות GraphQL חרגו מהתקציב. טוקן API אישי מקבל תקציב משותף של 10 מיליון נקודות לדקה לקריאות ולכתיבות יחד (מיליון אחד לחשבונות ניסיון, מלכ"ר וחינם). טוקן אפליקציה שונה: קריאות וכתיבות מוגבלות ל-5 מיליון נקודות מורכבות לדקה **כל אחת**, ולכן אפליקציה שעוברת מטוקן אישי מקבלת תקרת קריאה קטנה יותר למרות שהמספר הכותרתי נראה דומה. שאילתה בודדת לא יכולה לעבור 5 מיליון נקודות בשני המקרים.
פתרון: תוסיפו את השדה `complexity { before after query }` כדי לראות את יתרת התקציב, תשתמשו ב-`items_page` עם `cursor` במקום `items`, תבקשו רק את העמודות שאתם צריכים, ותאטו. כל שגיאת הגבלת קצב מחזירה שדה `retry_in_seconds`, וכשנתקלים במגבלת הבקשות לדקה, הכותרת `Retry-After` אומרת מתי לנסות שוב. כותרות התשובה `RateLimit-Policy` ו-`RateLimit` מדווחות על המדיניות ועל היתרה הנוכחית בכל תשובה, כך שאפשר לווסת עוד לפני שנתקעים בקיר.

### שגיאה: 429 שאינה שגיאת מורכבות
סיבה: מערכת monday אוכפת כמה מגבלות נפרדות מלבד מורכבות, ורובן תלויות בתוכנית:

| מגבלה | Enterprise | Pro | שאר התוכניות |
|-------|------------|-----|--------------|
| בקשות לדקה ("Minute limit rate exceeded") | 5,000 | 2,500 | 1,000 |
| בקשות במקביל | 250 | 100 | 40 |
| קריאות API ביום (`DAILY_LIMIT_EXCEEDED`, מתאפס בחצות UTC) | 25,000 | 10,000 | 1,000 |

יש גם מגבלת `IP_RATE_LIMIT_EXCEEDED` של 5,000 בקשות ב-10 שניות מכתובת IP אחת. כלומר חשבון Standard נתקע במגבלה לדקה ב-1,000 בקשות, ולא ב-5,000.
פתרון: תקראו את קוד השגיאה במקום להניח מורכבות. תורידו מקביליות מול מגבלת הבקשות במקביל, תחכו `retry_in_seconds` (או `Retry-After`) לפני ניסיון חוזר, ואם המכסה היומית היא הבעיה, תעברו מפולינג ל-webhooks או תרכשו קריאות API נוספות.

### שגיאה: "שרת MCP לא מגיב"
סיבה: שרת mondaycom/mcp לא מוגדר או טוקן לא תקין.
פתרון: תוודאו את טוקן ה-API ב-monday.com תחת Developers -> My Access Tokens. תפעילו מחדש את שרת ה-MCP. הסקיל עובד גם בלי MCP באמצעות קריאות API ישירות.

### שגיאה: "פורמט ערך עמודה לא תקין"
סיבה: ערכי עמודות Monday.com דורשים פורמטי JSON ספציפיים, והשגיאה `ColumnValueException` מוחזרת עם קוד HTTP **200**, ולכן הבקשה נראית מוצלחת.
פתרון: תבדקו תמיד את מערך ה-`errors` ולא את קוד ה-HTTP. תשתמשו ב-`change_simple_column_value` לטקסט פשוט ולמספרים, תוודאו שתוויות הסטטוס כבר קיימות בלוח, ותבדקו בסעיף מוזרויות של סוגי עמודות את עמודות חיבור-לוחות, מראה ונוסחה.
