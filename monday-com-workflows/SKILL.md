---
name: monday-com-workflows
description: >-
  Optimize Monday.com workflows for Israeli teams with board management,
  automation recipes, and API integration. Use when user asks about Monday.com
  boards, Monday.com automations, "monday.com API", work management, sprint
  planning with Israeli calendar, or team workflow optimization on Monday.com.
  Enhances the official mondaycom/mcp server with Israeli team best practices
  including Sunday-Thursday work week, Hebrew boards, and holiday-aware
  scheduling. Do NOT use for other project management tools (Jira, Asana, etc.).
license: MIT
allowed-tools: "Bash(python:*) Bash(curl:*) WebFetch"
compatibility: "Best with mondaycom/mcp MCP server. Works standalone for guidance. Requires Monday.com API token."
metadata:
  author: skills-il
  version: 1.0.0
  category: communication
  tags: [monday, project-management, workflow, automation, teams, israel]
  mcp-server: mondaycom/mcp
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
- `references/graphql-patterns.md` — Monday.com GraphQL API query and mutation patterns covering authentication, board/item CRUD, column value updates, group management, pagination, and webhook setup. Consult when constructing API queries for board automation, bulk item operations, or custom integrations beyond what the MCP server provides.

## Troubleshooting

### Error: "Complexity budget exceeded"
Cause: GraphQL query too complex (over 10,000 points per minute)
Solution: Simplify queries, paginate with `limit` and `cursor`, avoid requesting all column values when not needed. Use `items_page` instead of `items` for large boards.

### Error: "MCP server not responding"
Cause: mondaycom/mcp server not configured or token invalid
Solution: Verify API token at monday.com then Admin then API. Restart MCP server. This skill works standalone without MCP using direct API calls.

### Error: "Column value format invalid"
Cause: Monday.com column values require specific JSON formats
Solution: Use `change_simple_column_value` mutation for text/number, or check Monday.com API docs for column-specific JSON formats (status labels, dates, etc.).
