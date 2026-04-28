---
name: monday-com-workflows
description: Optimize Monday.com workflows for Israeli teams with board management, automation recipes, and API integration. Use when user asks about Monday.com boards, Monday.com automations, "monday.com API", work management, sprint planning with Israeli calendar, or team workflow optimization on Monday.com. Enhances the official mondaycom/mcp server with Israeli team best practices including Sunday-Thursday work week, Hebrew boards, and holiday-aware scheduling. Do NOT use for other project management tools (Jira, Asana, etc.).
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: Best with mondaycom/mcp MCP server. Works standalone for guidance. Requires Monday.com API token.
version: 1.2.0
---

# Monday.com Workflows

## Instructions

### Step 1: Verify Monday.com Access
Check for Monday.com API token and optional MCP server:

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

If MCP server available (`mondaycom/mcp`): Use MCP tools for basic CRUD.
If API-only: Use GraphQL queries directly.

### Step 2: Choose Workflow Pattern

**Israeli team workflow templates:**

| Workflow | Best For | Key Feature |
|----------|----------|-------------|
| Sprint Board (Sun-Thu) | Dev teams | Israeli work week, holiday-aware |
| Sales Pipeline | Sales teams | Hebrew stages, follow-up automations |
| Client Onboarding | Service teams | Approval flows, SLA tracking |
| Marketing Campaign | Marketing | Campaign calendar, content approval |
| HR Recruitment | HR teams | Candidate tracking, Hebrew templates |
| OKR Tracking | Leadership | Quarterly goals, Israeli Q alignment |

### Step 3: Create Optimized Board

**Sprint board for Israeli dev team:**
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

### Step 4: Set Up Automations

**Israeli-aware automation recipes:**

**Recipe 1: Sunday Sprint Kickoff**
```
Trigger: Every Sunday at 09:00 (Asia/Jerusalem)
Action: Move all items from "Backlog" to day-specific groups
Notification: Send team "Sprint started" update
```

**Recipe 2: Thursday EOD Review**
```
Trigger: Every Thursday at 16:00
Action: Create summary update with incomplete items
Action: Move incomplete items back to Backlog
Notification: Send sprint summary to team lead
```

**Recipe 3: Holiday Freeze**
```python
# Israeli holidays that affect sprint planning
israeli_holidays_2026 = [
    # Yom Tov + chol hamoed; first/last days are observed as full holidays
    ("2026-03-03", "2026-03-03", "Purim"),
    ("2026-04-01", "2026-04-09", "Pesach"),  # Yom Tov Apr 2-3 + Apr 8-9; chol hamoed Apr 4-7
    ("2026-04-14", "2026-04-14", "Yom HaShoah"),
    ("2026-04-21", "2026-04-21", "Yom HaZikaron"),  # eve Apr 20
    ("2026-04-22", "2026-04-22", "Yom Ha'Atzmaut"),  # eve Apr 21
    ("2026-05-22", "2026-05-22", "Shavuot"),  # eve May 21
    ("2026-07-23", "2026-07-23", "Tisha B'Av"),
    ("2026-09-12", "2026-09-13", "Rosh Hashana"),
    ("2026-09-21", "2026-09-21", "Yom Kippur"),
    ("2026-09-26", "2026-10-03", "Sukkot"),  # Yom Tov Sep 26 + Oct 3; chol hamoed Sep 27-Oct 2
    ("2026-12-04", "2026-12-12", "Hanukkah"),  # workdays in most companies, schools off
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

**Recipe 4: Automatic Follow-up**
```
Trigger: When "Last Contact" date is 7+ days ago
Condition: Status is not "Done" or "Closed"
Action: Change status to "Follow Up Needed"
Action: Notify assigned person
```

### Step 5: Advanced API Queries

**Search items across boards:**
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

**Bulk update items:**
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

**Create item with Hebrew content:**
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

### Step 6: Cross-Board Coordination

**Connect boards for Israeli business workflows:**

```
Sales Pipeline -> Client Onboarding -> Project Delivery -> Billing
     |                  |                    |              |
  Monday.com       Monday.com          Monday.com     Priority/Rivhit
  (Sales team)    (Account mgmt)      (Dev team)    (Finance team)
```

**Mirror columns and automations:**
- When deal status = "Won" then create item in Onboarding board
- When onboarding complete then create item in Project board
- When project delivered then trigger invoice in billing system
- Use Monday.com "Connect Boards" column for cross-references

## Examples

### Example 1: Sprint Board Setup
User says: "Create a sprint board for my dev team that works Sunday to Thursday"
Actions:
1. Create board with Israeli work week groups (Sun-Thu + Backlog + Done)
2. Add columns: Status, Priority, Assignee, Story Points, Due Date
3. Set up Sunday kickoff and Thursday review automations
4. Configure holiday-aware scheduling
Result: Ready-to-use sprint board with Israeli calendar integration.

### Example 2: Sales Pipeline
User says: "Set up a sales CRM board in Monday.com with Hebrew stages"
Actions:
1. Create board with Hebrew pipeline stages: New Lead, First Meeting, Proposal, Negotiation, Closing
2. Add columns: Contact, Company, Deal Value (NIS), Expected Close Date
3. Set up follow-up automations (7-day no-contact alert)
4. Create dashboard with pipeline value summary
Result: Hebrew-language sales pipeline with Israeli business automations.

### Example 3: API Integration
User says: "Query all overdue items from my Monday.com board"
Actions:
1. Use GraphQL to query board items with due_date column
2. Filter for items where due_date is before today and status is not "Done"
3. Group by assignee and priority
4. Optionally send notification summary
Result: Structured list of overdue items with assignee breakdown.

## Bundled Resources

### References
- `references/graphql-patterns.md` -- Monday.com GraphQL API query and mutation patterns covering authentication, board/item CRUD, column value updates, group management, pagination, and webhook setup. Consult when constructing API queries for board automation, bulk item operations, or custom integrations beyond what the MCP server provides.

## Recommended MCP Servers

This skill is designed to enhance the **official `mondaycom/mcp` server**. Connect that MCP first, then use this skill for Israeli team patterns on top.

| MCP | What It Adds |
|-----|--------------|
| [`mondaycom/mcp`](https://github.com/mondaycom/mcp) (npm `@mondaydotcomorg/monday-api-mcp`) | Static tools for board/item/group CRUD: `create_item`, `change_item_column_values`, `move_item_to_group`, `create_board`, `get_board_schema`, `create_column`, `delete_column`, `list_users_and_teams`, `create_form`/`get_form`, plus the **Dynamic API Tools** (beta) which generate any GraphQL query/mutation on demand. Available as a local npm install or hosted MCP. |

When building anything not covered by static tools (validation rules, projects/portfolio mutations, knowledge base CRUD, notetaker, board metadata fields), reach for the Dynamic API Tools beta and pin `API-Version: 2026-04` (or later) on the request.

## API Versioning

Monday.com versions its API by month. As of 2026-04 the **default version is `2026-04`**, with `2026-07` in release-candidate and `2026-10` rolling out. Versions `2024-10` and `2025-01` were **deprecated 2026-02-15**.

Pin your version explicitly on every request:

```python
headers = {
    "Authorization": API_TOKEN,
    "API-Version": "2026-04",
    "Content-Type": "application/json",
}
```

**Breaking changes since 2025-04 to be aware of:**
- Variables in queries must be JSON objects, not strings
- `column_type` casing changed (e.g., `StatusColumn` → `status`)
- `ColumnValueException` is now strictly thrown on bad column JSON
- `value` for connect-boards / dependency / subtasks columns now returns `null`; query `linked_items` / `linked_item_ids` instead
- Queries on `users` without an explicit limit default to 200 (was unbounded)

## Gotchas

- Monday.com sprint planning must use the Israeli work week (Sunday-Thursday). Agents may generate sprint cycles based on Monday-Friday, causing misaligned deadlines and capacity calculations.
- Hebrew column names in Monday.com boards are stored as RTL text. API queries using column names must match the exact Hebrew string including any spaces or punctuation.
- Monday.com automations triggered by date columns do not account for Israeli holidays by default. Agents must add holiday exceptions manually or the automation will fire on Rosh Hashana, Yom Kippur, etc.
- Israeli teams on Monday.com commonly use a Sunday standup pattern. Agents may set up Monday standup automations that miss the first day of the Israeli work week.
- Monday.com's timezone setting must be set to Asia/Jerusalem (UTC+2/+3) for Israeli teams. Agents may default to UTC, causing automations to trigger at wrong times.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Monday.com API Authentication | https://developer.monday.com/api-reference/docs/authentication | Endpoint URL, Authorization header format |
| Monday.com Rate Limits | https://developer.monday.com/api-reference/docs/rate-limits | Complexity budget (10M points/min per user), reset interval |
| Monday.com GraphQL Overview | https://developer.monday.com/api-reference/docs/introduction-to-graphql | Query structure, default complexities, `complexity` field |
| Monday.com Items API | https://developer.monday.com/api-reference/docs/items | `items_page`, cursor pagination, column values |
| Monday.com Automations | https://developer.monday.com/api-reference/reference/automations | Trigger/action recipes, automation API surface |
| Monday.com API Versioning | https://developer.monday.com/api-reference/docs/api-versioning | Current / RC / deprecated versions, migration guides |

## Troubleshooting

### Error: "Complexity budget exceeded"
Cause: GraphQL queries consumed the per-user budget (10,000,000 complexity points per minute; 1,000,000 for trial and free accounts). A single query cannot exceed 5,000,000 points.
Solution: Add the `complexity` field to queries to see remaining budget, paginate with `items_page` + `cursor` instead of `items`, request only the columns you need, and back off until the next minute resets the budget.

### Error: "MCP server not responding"
Cause: mondaycom/mcp server not configured or token invalid
Solution: Verify the API token in monday.com under Developers -> My Access Tokens. Restart the MCP server. This skill works standalone without MCP using direct API calls.

### Error: "Column value format invalid"
Cause: Monday.com column values require specific JSON formats
Solution: Use `change_simple_column_value` mutation for text/number, or check Monday.com API docs for column-specific JSON formats (status labels, dates, etc.).