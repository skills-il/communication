---
name: monday-com-workflows
description: Optimize Monday.com workflows for Israeli teams with board management, automation recipes, and API integration. Use when user asks about Monday.com boards, Monday.com automations, "monday.com API", work management, sprint planning with Israeli calendar, or team workflow optimization on Monday.com. Enhances the official mondaycom/mcp server with Israeli team practice: Sunday-Thursday work week, Hebrew content on boards whose interface has no Hebrew option, plan and automation quota ceilings, and holiday-aware scheduling. Do NOT use for other project management tools (Jira, Asana, etc.).
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: Best with mondaycom/mcp MCP server. Works standalone for guidance. Requires Monday.com API token.
---

# Monday.com Workflows

## Instructions

### Step 1: Verify Monday.com Access

Check for a Monday.com API token and an optional MCP server. Do not read `account { plan { max_users } }` as a liveness check: `account.plan` is documented to return `null` for accounts on monday's multi-product infrastructure, which is exactly what newer accounts get. Read `account { tier products { kind } }` instead and treat `plan` as optional.

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

If `plan` comes back `null` and `tier` is populated, access is fine. Only an `errors` array means the token is bad.

If the MCP server is available (`mondaycom/mcp`): use MCP tools for basic CRUD.
If API-only: use GraphQL queries directly.

### Step 2: Choose Workflow Pattern

**Israeli team workflow templates:**

| Workflow | Best For | Key Feature |
|----------|----------|-------------|
| Sprint Board (Sun-Thu) | Dev teams | Israeli work week, holiday-aware |
| Sales Pipeline | Sales teams | Hebrew stage labels, follow-up automations |
| Client Onboarding | Service teams | Approval flows, SLA tracking |
| Marketing Campaign | Marketing | Campaign calendar, content approval |
| HR Recruitment | HR teams | Candidate tracking, Hebrew templates |
| OKR Tracking | Leadership | Quarterly goals, Israeli Q alignment |

### Step 3: Create Optimized Board

**Sprint board for an Israeli dev team:**
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

### Step 4: Set Up Automations

Before designing an automation, check the account's monthly action quota (see Plans and Quotas). A per-item automation on a busy board can burn a Standard plan's whole month in days.

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
# Israeli holidays that affect sprint planning.
israeli_holidays_2026 = [
    # Israel schedule (one-day Yom Tov). Verify a new year via hebcal.com/holidays/<year>?i=on
    # NOT the Diaspora two-day-Yom-Tov dates, which would false-freeze a working day.
    ("2026-03-03", "2026-03-03", "Purim"),
    ("2026-04-02", "2026-04-08", "Pesach"),  # Israel: Yom Tov Apr 2 + Apr 8; chol hamoed Apr 3-7. Apr 9 is a workday.
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

**Recipe 4: Automatic Follow-up**
```
Trigger: When "Last Contact" date is 7+ days ago
Condition: Status is not "Done" or "Closed"
Action: Change status to "Follow Up Needed"
Action: Notify assigned person
```

### Step 5: Advanced API Queries

**List boards, including multi-level boards:**

The `boards` query does NOT return sub-item (multi-level) boards by default. The docs are explicit: "If omitted, only `classic` boards will be returned unless specific board IDs are provided." Omitting `hierarchy_type` silently hides every multi-level board, and a sync built on it will look correct while missing data.

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

**Search items by column value:**
```python
def search_items(api_token: str, board_id: int, column_id: str, value: str):
    """Search items by column value."""
    headers = {
        "Authorization": api_token,
        "API-Version": "2026-07",
        "Content-Type": "application/json",
    }
    # items_page_by_column_values pages exactly like items_page: it returns a
    # `cursor`. With limit:50 you only get the first 50 matches, so for "all
    # overdue items" you must loop, passing the cursor back via next_items_page
    # until cursor is null. The `complexity` block shows how to read your
    # remaining rate-limit budget on the same call.
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

**Bulk update items:**
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

**Create item with Hebrew content:**
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

### Step 6: Cross-Board Coordination

```
Sales Pipeline -> Client Onboarding -> Project Delivery -> Billing
     |                  |                    |              |
  Monday.com       Monday.com          Monday.com     Accounting / ERP
  (Sales team)    (Account mgmt)      (Dev team)     (Finance team)
```

**Mirror columns and automations:**
- When deal status = "Won" then create item in Onboarding board
- When onboarding complete then create item in Project board
- When project delivered then trigger the invoice in the billing system
- Use Monday.com "Connect Boards" column for cross-references

Most Israeli accounting and invoicing systems have no monday.com marketplace app. Search https://monday.com/marketplace before promising a one-click integration; when there is no listing, the honest answer is a custom integration built on the monday API plus a webhook, not an app install.

## Plans, Quotas, and What Blocks a Workflow

monday.com is four separate products, each with its own plan ladder, and the paid plans start at a 3-seat minimum:

| Product | Tiers | Note |
|---------|-------|------|
| Work management | Free, Basic, Standard, Pro, Enterprise | Free exists only here (up to 2 seats) |
| CRM | Basic, Standard, Pro, Ultimate | Top tier is Ultimate, not Enterprise |
| Dev | Basic, Standard, Pro, Enterprise | |
| Service | Standard, Pro, Enterprise | No Basic tier |

Getting this wrong sends a client to a tier that does not exist. Do not quote prices from memory; prices drift faster than tier names.

**What the tier actually gates (work management):**

| Capability | Standard | Pro | Enterprise |
|------------|----------|-----|------------|
| Automations and integrations | first tier that has them, 250 actions / month | 25,000 actions / month | up to 250,000 actions / month |
| API calls | 1,000 / day | 10,000 / day | 25,000 / day |
| Advanced (dependency) columns | no | yes | yes |

Two ceilings matter more than the complexity budget for a small Israeli team:

- **250 automation actions per month on Standard.** An SMB on Standard gets roughly eight automation actions a day across the whole account. A "notify on every status change" recipe on an active board exhausts that in under a week. Design for batched or scheduled triggers, not per-item ones, and say so out loud before proposing a recipe.
- **1,000 API calls per day on Standard.** This binds long before the 10M complexity budget does. A polling integration that hits the API every minute uses 1,440 calls a day and fails on Standard by construction. Use webhooks instead.

Automations and integrations draw on the same monthly action counter, so a workflow that mixes them is billed once against that counter, not twice.

## Webhooks vs Polling

Polling is the default mistake. On Standard the daily API-call allowance makes a once-a-minute poll impossible, and on any tier polling burns complexity budget to discover that nothing changed.

Use a webhook when you need to react to a change. Use polling only for periodic reconciliation, at a low frequency.

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

Things that break real integrations:

- **The subscription handshake.** On creation monday POSTs a JSON body containing a randomly generated token in a `challenge` field, and your endpoint must echo that token back as a `challenge` field in its own JSON response. An endpoint that returns 200 with an empty body fails registration.
- **Retries.** Failed deliveries "retry once a minute for 30 minutes", then stop. After that the event is gone, so a webhook consumer still needs a periodic reconciliation pass to heal missed windows.
- **Subitems fire their own events.** `change_column_value` on a parent board does not cover subitems; subscribe to `change_subitem_column_value` and `create_subitem` separately or subitem changes are invisible.
- **Ordering is not guaranteed.** Treat each payload as a signal to re-read the item, not as the authoritative new state.

## Column Type Quirks

Most integration bugs on monday are column bugs, not query bugs. Four types do not behave the way the generic `column_values { text value }` pattern implies:

- **Connect boards.** Both `text` and `value` always return `null` on this column. Read `display_value` (the linked item names, comma separated), `linked_item_ids`, or `linked_items` (on which you can query any `Item` field). Writing uses a different shape again: `{"connect_boards": {"item_ids": [1122334455, 5544332211]}}`, and `{"connect_boards": null}` clears it. Code that reads `value` on this column gets `null` and silently concludes the relation is empty.
- **Mirror.** Same null pair: `text` and `value` return `null`, use `display_value` or `mirrored_items`. Mirror columns are read-and-create only; they cannot be updated or cleared through the API because they reflect the source column on the connected board. Filtering on mirrored content is not supported, so any "find all items whose mirrored owner is X" plan needs to query the source board instead.
- **Formula.** A read-only calculated column. Do not plan to write to it, and do not assume the API returns the evaluated result the UI shows; compute the value yourself if an automation depends on it.
- **Status.** Writes take a label object, `{"label": "Done"}`, and the label must already exist on the board. An unknown label raises `ColumnValueException`, which monday returns with HTTP **200**, so a naive `response.ok` check treats a failed write as a success. Always inspect the `errors` array.

## Examples

### Example 1: Sprint Board Setup
User says: "Create a sprint board for my dev team that works Sunday to Thursday"
Actions:
1. Create board with Israeli work week groups (Sun-Thu + Backlog + Done)
2. Add columns: Status, Priority, Assignee, Story Points, Due Date
3. Check the plan's monthly action quota, then set up Sunday kickoff and Thursday review automations
4. Configure holiday-aware scheduling
Result: Ready-to-use sprint board with Israeli calendar integration.

### Example 2: Sales Pipeline
User says: "Set up a sales CRM board in Monday.com with Hebrew stages"
Actions:
1. Create board with Hebrew pipeline stage labels: New Lead, First Meeting, Proposal, Negotiation, Closing
2. Add columns: Contact, Company, Deal Value (NIS), Expected Close Date
3. Set up follow-up automations (7-day no-contact alert)
4. Tell the user up front that stage labels and item names will be Hebrew but the surrounding interface will not
Result: Hebrew-content sales pipeline with Israeli business automations.

### Example 3: API Integration
User says: "Query all overdue items from my Monday.com board"
Actions:
1. Use GraphQL to query board items with the due-date column, passing `hierarchy_type` if subitem boards are in scope
2. Filter for items where the due date is before today and status is not "Done"
3. Group by assignee and priority
4. Optionally send a notification summary
Result: Structured list of overdue items with assignee breakdown.

## Bundled Resources

### References
- `references/graphql-patterns.md` -- Monday.com GraphQL API query and mutation patterns covering authentication, board/item CRUD, column value updates, group management, pagination, and webhook setup. Consult when constructing API queries for board automation, bulk item operations, or custom integrations beyond what the MCP server provides.

## Recommended MCP Servers

This skill is designed to enhance the **official `mondaycom/mcp` server**. Connect that MCP first, then use this skill for Israeli team patterns on top.

| MCP | What It Adds |
|-----|--------------|
| [`mondaycom/mcp`](https://github.com/mondaycom/mcp) (npm `@mondaydotcomorg/monday-api-mcp`, latest 3.3.0) | Static tools for board/item/group CRUD: `create_item`, `change_item_column_values`, `move_item_to_group`, `create_board`, `get_board_schema`, `create_column`, `delete_column`, `list_users_and_teams`, `create_form`/`get_form`, plus the **Dynamic API Tools** (beta) which generate any GraphQL query/mutation on demand. Available as a local npm install or hosted MCP. |

When building anything not covered by static tools (validation rules, projects/portfolio mutations, knowledge base CRUD, notetaker, board metadata fields), reach for the Dynamic API Tools beta and pin `API-Version: 2026-07` (or later) on the request.

## API Versioning

Monday.com versions its API by month and releases a new version every quarter. As of August 2026 the **default version is `2026-07`** ("Used as the default version when no header is passed"). `2026-10` is the current release candidate, published 1 July 2026. `2026-04` entered **maintenance on 1 July 2026** and is scheduled for deprecation in July 2027, so a skill or integration still pinned to `2026-04` is past its stable window and should move. Versions `2024-10` and `2025-01` were deprecated on 15 February 2026.

Pin your version explicitly on every request:

```python
headers = {
    "Authorization": API_TOKEN,
    "API-Version": "2026-07",
    "Content-Type": "application/json",
}
```

**Standing behaviour, not news.** These have been true for several versions and should not occupy migration attention: variables in queries must be JSON objects rather than strings; `column_type` casing changed (`StatusColumn` became `status`); `ColumnValueException` is thrown strictly on bad column JSON; and `value` on connect-boards, dependency and subtasks columns returns `null` (use `linked_items` / `linked_item_ids`, see Column Type Quirks).

**Active in `2026-07`:** the user entity overhaul landed. `Query.users` arguments `kind`, `newest_first` and `non_active` are deprecated in favour of `user_kind`, `sort` and `status`. A `users` query with no `limit` now returns 200 users instead of all matches, and the maximum `limit` is capped at 1000. New `User` fields include `account_id`, an enum `status`, a nested `photo_url` object and `became_active_at`; `created_at` is now `ISO8601DateTime!`, `birthday` is `String`, `utc_hours_diff` is `Float`.

**Lands in `2026-10`:** legacy `User` fields are removed, including the photo fields (`photo_original`, `photo_thumb`, `photo_thumb_small`, `photo_tiny`, `photo_small`) and the boolean kind/status flags (`is_guest`, `is_admin`, `is_pending`, `enabled`). Replace boolean flag checks with `kind` comparisons before pinning to `2026-10`.

## Gotchas

- **monday.com has no Hebrew interface.** Hebrew on monday is content, not localization: item names, group names, status labels and updates can be Hebrew, but menus, settings and system messages stay in one of the interface languages monday offers, and Hebrew and Arabic are not among them. There is also no board-level or account-level RTL layout setting, so Hebrew item text sits inside a left-to-right interface. Verify the current language list in the account's profile settings before promising anything. Never tell an Israeli client the board will "be in Hebrew"; tell them their data will be, and their interface will not.
- Multi-level (subitem) boards are excluded from the `boards` query unless you pass `hierarchy_type` or explicit board IDs. This fails silently: the query succeeds and simply returns fewer boards.
- Monday.com sprint planning must use the Israeli work week (Sunday-Thursday). Agents may generate sprint cycles based on Monday-Friday, causing misaligned deadlines and capacity calculations.
- Hebrew column names are stored as RTL text. API queries using column names must match the exact Hebrew string including any spaces or punctuation.
- Monday.com automations triggered by date columns do not account for Israeli holidays by default. Agents must add holiday exceptions manually or the automation will fire on Rosh Hashana, Yom Kippur, and so on.
- Israeli teams on Monday.com commonly use a Sunday standup pattern. Agents may set up Monday standup automations that miss the first day of the Israeli work week.
- Monday.com's timezone setting must be set to Asia/Jerusalem (UTC+2/+3) for Israeli teams. Agents may default to UTC, causing automations to trigger at wrong times.
- The account's monthly automation-action quota and daily API-call allowance are plan-gated and small on Standard. Check them before designing a workflow, not after the client hits the wall.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| Monday.com API Authentication | https://developer.monday.com/api-reference/docs/authentication | Endpoint URL, Authorization header format |
| Monday.com Rate Limits | https://developer.monday.com/api-reference/docs/rate-limits | Complexity budgets, `retry_in_seconds`, `RateLimit` headers |
| Monday.com Errors | https://developer.monday.com/api-reference/docs/errors | Error codes and their HTTP statuses, including the 200-with-error cases |
| Monday.com Boards Query | https://developer.monday.com/api-reference/reference/boards | `hierarchy_type` argument and its omission behaviour |
| Monday.com Account Object | https://developer.monday.com/api-reference/reference/account | `plan` null behaviour, `tier`, `products` |
| Monday.com Connect Boards Column | https://developer.monday.com/api-reference/docs/connect | `display_value`, `linked_item_ids`, write format |
| Monday.com Mirror Column | https://developer.monday.com/api-reference/docs/mirror | Read-only behaviour, `mirrored_items` |
| Monday.com Webhooks | https://developer.monday.com/api-reference/docs/webhooks | Event list, `challenge` handshake, retry window |
| Monday.com Items API | https://developer.monday.com/api-reference/docs/items | `items_page`, cursor pagination, column values |
| Monday.com Apps Framework | https://developer.monday.com/apps/docs/api-reference | Custom automation triggers/actions are built via the apps framework, monday has no queryable core-API "automations" endpoint |
| Monday.com API Versioning | https://developer.monday.com/api-reference/docs/api-versioning | Current / RC / maintenance / deprecated versions |
| Monday.com Pricing | https://monday.com/pricing | Products, tier names, action and API-call quotas |
| Monday.com Marketplace | https://monday.com/marketplace | Whether an integration app actually exists before promising it |

## Troubleshooting

### Error: "Complexity budget exceeded"
Cause: GraphQL queries consumed the budget. A personal API token has reads and writes sharing a combined budget of 10M points per minute (1M for trial, NGO and free accounts). An app token is different: reads and writes are limited to 5M complexity points per minute **each**, so an app that migrates from a personal token gets a smaller read ceiling even though the headline number looks similar. A single query cannot exceed 5M points on either.
Solution: Add the `complexity { before after query }` field to see the remaining budget, paginate with `items_page` plus `cursor` instead of `items`, request only the columns you need, and back off. Every rate limit error returns a `retry_in_seconds` field, and 429 responses also carry a `Retry-After` header. The `RateLimit-Policy` and `RateLimit` response headers report the policy and the current remaining quota on every response, so you can throttle before hitting the wall.

### Error: 429 that is not a complexity error
Cause: monday enforces several separate 429 conditions. `Rate Limit Exceeded` means more than 5,000 requests in one minute, `maxConcurrencyExceeded` means too many queries at once, `COMPLEXITY_BUDGET_EXHAUSTED` is the complexity limit, and `IP_RATE_LIMIT_EXCEEDED` is a per-IP cap. Separately, the plan's daily API-call allowance (1,000/day on Standard) can run out.
Solution: Read the error code rather than assuming complexity. Reduce concurrency for `maxConcurrencyExceeded`, and if the daily allowance is the problem, move from polling to webhooks or buy additional API calls.

### Error: "MCP server not responding"
Cause: mondaycom/mcp server not configured or token invalid.
Solution: Verify the API token in monday.com under Developers -> My Access Tokens. Restart the MCP server. This skill works standalone without MCP using direct API calls.

### Error: "Column value format invalid"
Cause: Monday.com column values require specific JSON formats, and `ColumnValueException` is returned with HTTP status **200**, so the request looks successful.
Solution: Always inspect the `errors` array rather than the HTTP status. Use `change_simple_column_value` for plain text and numbers, confirm status labels already exist on the board, and check the Column Type Quirks section for connect-boards, mirror and formula columns.
