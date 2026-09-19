---
name: monday-com-workflows
description: 'Optimize Monday.com workflows for Israeli teams with board management, automation recipes, and API integration. Use when user asks about Monday.com boards, Monday.com automations, "monday.com API", work management, sprint planning with Israeli calendar, or team workflow optimization on Monday.com. Enhances the official mondaycom/mcp server with Israeli team practice: Sunday-Thursday work week, Hebrew content on boards whose interface has no Hebrew option, plan and automation quota ceilings, and holiday-aware scheduling. Do NOT use for other project management tools (Jira, Asana, etc.).'
license: MIT
allowed-tools: Bash(python:*) Bash(curl:*) WebFetch
compatibility: Best with mondaycom/mcp MCP server. Works standalone for guidance. Requires Monday.com API token.
---

# Monday.com Workflows

## Instructions

### Step 1: Verify Monday.com Access

Check for a Monday.com API token and an optional MCP server. Do not read `account { plan { max_users } }` as a liveness check: `account.plan` is documented to return `null` for accounts on monday's multi-product infrastructure, which is exactly what newer accounts get. Read `account { tier products { kind } }` instead and treat `plan` as optional.

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

### Step 4: Set Up Automations

Before designing an automation, check the account's monthly action quota (see Plans and Quotas). A per-item automation on a busy board can burn a Standard plan's whole month in days.

The recipes below are set up in the board's automation center. Through the hosted monday MCP an agent can also create one from a natural-language description with the `create_automation` tool; when a detail is missing it returns `needs_clarification`, so ask the user rather than guessing.

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
A freeze needs three states, not a yes/no: `off` (the statutory rest days, plus Yom Ha'Atzmaut), `half` (erev chag, reduced capacity), and `policy` (chol hamoed, Hanukkah, Purim, Tisha B'Av, Yom HaShoah, Yom HaZikaron: legal working days that teams treat differently). Ask the team lead how they treat `policy` days before freezing anything; freezing all of Hanukkah deletes a working week.

`references/israeli-holidays.md` has the Israel-schedule table for 2026 through 2028, an `israel_today()` helper (a UTC server's `date.today()` is the wrong date for hours after Israeli midnight), a `holiday_state()` function that raises for a year it does not cover instead of silently answering "working day", and a `sprint_capacity()` helper that skips Friday and Saturday and accepts any start day. Always use the Israel dates (hebcal `i=on`), never the Diaspora two-day dates.

monday's own recurring automations cannot consult this table. When a recipe must skip holidays, run it from your own scheduled job that checks `holiday_state(israel_today())` and then calls the API.

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

**Overdue items (date before today), all pages:**
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
Filter out items whose status text is "Done" on your side before reporting them.

**Posting the overdue list to Slack.** Two routes. monday's native Slack integration runs inside monday and draws on the integration-action quota (250 actions a month on Standard, see Plans and Quotas), so a per-item notification can exhaust it. The alternative is your own daily job: call `overdue_items`, then POST `{"text": "..."}` as JSON to a Slack incoming-webhook URL. Check `holiday_state(israel_today())` first so the digest does not post on Yom Kippur, and remember each monday call counts toward the daily API-call allowance.

**Bulk update items:**
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

**Create item with Hebrew content:**
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

monday.com sells several products with separate plan ladders: work management, CRM, Campaigns, Dev and Service. Work management has Free, Basic, Standard, Pro and Enterprise (Free covers up to 2 seats); CRM's top tier is Ultimate, not Enterprise. Check the other products' ladders on their own pricing pages rather than assuming they mirror work management.

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

Calls made through the hosted monday MCP server count toward the same daily API-call limit, because each MCP tool call is executed as a GraphQL request. An agent working through the MCP on a Standard account shares the 1,000 calls a day with every other integration.

**Workflows are not automations.** The pricing page now lists a workflow count per tier (3 on Standard, 20 on Pro). monday's docs describe workflows as "cross-board, workspace-level objects", distinct from per-board automations. They are built through the MCP's workflow tools against the dev (preview) API schema, start as drafts, and must be published before they run. Do not promise a client a workflow built on the stable API.

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
- **Retries.** Failed deliveries "retry once a minute for 30 minutes". monday does not document any delivery after that window, so a webhook consumer still needs a periodic reconciliation pass to heal missed windows.
- **Your own retries duplicate things.** When a mutation times out and you retry it, send an `Idempotency-Key` header. monday caches the first response for 30 minutes and answers a retry with the cached result (`Idempotency-Replayed: true`) instead of creating a second item.
- **Subitems fire their own events.** `change_column_value` on a parent board does not cover subitems; subscribe to `change_subitem_column_value` and `create_subitem` separately or subitem changes are invisible.
- **Ordering is not guaranteed.** Treat each payload as a signal to re-read the item, not as the authoritative new state.

## Column Type Quirks

Most integration bugs on monday are column bugs, not query bugs. Four types do not behave the way the generic `column_values { text value }` pattern implies:

- **Connect boards.** Both `text` and `value` always return `null` on this column. Read `display_value` (the linked item names, comma separated), `linked_item_ids`, or `linked_items` (on which you can query any `Item` field). Writing uses a different shape again: `{"connect_boards": {"item_ids": [1122334455, 5544332211]}}`, and `{"connect_boards": null}` clears it. Code that reads `value` on this column gets `null` and silently concludes the relation is empty.
- **Mirror.** Same null pair: `text` and `value` return `null`, use `display_value` or `mirrored_items`. Mirror columns are read-and-create only; they cannot be updated or cleared through the API because they reflect the source column on the connected board. Filtering on mirrored content is not supported, so any "find all items whose mirrored owner is X" plan needs to query the source board instead.
- **Formula.** Read and create only; you cannot write a value into it. The computed result comes back in `display_value`; `text` and `value` are not populated, so code reading `text` concludes the formula is blank.
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
- `references/israeli-holidays.md` -- Israel-schedule holiday table for 2026 through 2028 with off / half / policy states, a `holiday_state()` function that refuses uncovered years, and a sprint-capacity helper. Consult for any sprint, freeze or scheduled-job logic.
- `references/graphql-patterns.md` -- Monday.com GraphQL API query and mutation patterns covering authentication, board/item CRUD, column value updates, group management, pagination, and webhook setup. Consult when constructing API queries for board automation, bulk item operations, or custom integrations beyond what the MCP server provides.

## Recommended MCP Servers

This skill is designed to enhance the **official `mondaycom/mcp` server**. Connect that MCP first, then use this skill for Israeli team patterns on top.

| MCP | What It Adds |
|-----|--------------|
| [`mondaycom/mcp`](https://github.com/mondaycom/mcp) (npm `@mondaydotcomorg/monday-api-mcp`, latest 3.3.0) | Static tools for board/item/group CRUD: `create_item`, `change_item_column_values`, `move_item_to_group`, `create_board`, `get_board_schema`, `create_column`, `delete_column`, `list_users_and_teams`, `create_form`/`get_form`, plus the **Dynamic API Tools** (beta) which generate any GraphQL query/mutation on demand. Available as a local npm install or hosted MCP. |

When building anything not covered by static tools (validation rules, projects/portfolio mutations, knowledge base CRUD, notetaker, board metadata fields), reach for the Dynamic API Tools beta and pin `API-Version: 2026-07` (or later) on the request.

## API Versioning

Monday.com versions its API by month and releases a new version every quarter. The official schedule:

| Version | Release candidate | Current (default) | Maintenance |
|---------|-------------------|-------------------|-------------|
| `2026-04` | 15 January 2026 | 1 April 2026 | 1 July 2026 |
| `2026-07` | 1 April 2026 | 1 July 2026 | 1 October 2026 |
| `2026-10` | 1 July 2026 | 1 October 2026 | 15 January 2027 |
| `2027-01` | 1 October 2026 | 15 January 2027 | 1 April 2027 |

So `2026-07` is the default ("Used as the default version when no header is passed") until **1 October 2026**, when `2026-10` becomes the default and `2026-07` moves to maintenance. Maintenance versions stay stable and usable; no deprecation date has been announced for `2026-04` or later (monday announces each one at least six months ahead). Versions `2024-10` and `2025-01` were deprecated on 15 February 2026. An unpinned integration changes behaviour on 1 October, which is why every sample here pins `API-Version` explicitly.

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

**Lands in `2026-10`:** the release notes list legacy `User` fields as removed, including the photo fields (`photo_original`, `photo_thumb`, `photo_thumb_small`, `photo_tiny`, `photo_small`) and the boolean kind/status flags (`is_guest`, `is_admin`, `is_pending`, `enabled`). Replace boolean flag checks with `kind` comparisons before pinning to `2026-10`.

## Gotchas

- **monday.com has no Hebrew interface.** Hebrew on monday is content, not localization: item names, group names, status labels and updates can be Hebrew, but menus, settings and system messages stay in one of the 15 interface languages monday's support article lists (last modified 31 August 2026), and Hebrew and Arabic are not among them. Hebrew item text therefore sits inside a left-to-right interface. Re-check that article, or the Language and Region tab in the profile, before promising anything. Never tell an Israeli client the board will "be in Hebrew"; tell them their data will be, and their interface will not.
- Multi-level (subitem) boards are excluded from the `boards` query unless you pass `hierarchy_type` or explicit board IDs. This fails silently: the query succeeds and simply returns fewer boards.
- Monday.com sprint planning must use the Israeli work week (Sunday-Thursday). Agents may generate sprint cycles based on Monday-Friday, causing misaligned deadlines and capacity calculations.
- Query and write columns by column **id** (`status`, `date4`), never by their Hebrew title. Resolve title to id once with `columns { id title type }` and store the id; titles get renamed and Hebrew punctuation makes exact matching fragile.
- Date filters such as `"TODAY"` are resolved in the time zone, date format and first day of the week set in the profile of the user who owns the token. A token owned by someone whose week starts on Monday, or whose profile is on UTC, shifts "this week" and "today" for an Israeli team.
- Monday.com automations triggered by date columns do not account for Israeli holidays. The holiday table in `references/israeli-holidays.md` covers 2026 through 2028 only; for later years fetch hebcal (`i=on`) rather than reusing an old table.
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
| Monday.com Apps Framework | https://developer.monday.com/apps/docs/api-reference | Custom automation triggers and actions built as monday apps |
| Monday.com Create Automation (MCP) | https://developer.monday.com/api-reference/docs/create-automation | Creating a board automation through the Platform MCP |
| Monday.com API Versioning | https://developer.monday.com/api-reference/docs/api-versioning | Current / RC / maintenance / deprecated versions |
| Monday.com Idempotency | https://developer.monday.com/api-reference/docs/idempotency | `Idempotency-Key` header, 30-minute replay window |
| Monday.com Date Column | https://developer.monday.com/api-reference/reference/date | `"TODAY"` compare values and the profile settings they depend on |
| Hebcal (Israel schedule) | https://www.hebcal.com/holidays/ | Holiday dates for a new year, with the Israel option |
| Monday.com Pricing | https://monday.com/pricing | Products, tier names, action and API-call quotas |
| Monday.com Marketplace | https://monday.com/marketplace | Whether an integration app actually exists before promising it |

## Troubleshooting

### Error: "Complexity budget exceeded"
Cause: GraphQL queries consumed the budget. A personal API token has reads and writes sharing a combined budget of 10M points per minute (1M for trial, NGO and free accounts). An app token is different: reads and writes are limited to 5M complexity points per minute **each**, so an app that migrates from a personal token gets a smaller read ceiling even though the headline number looks similar. A single query cannot exceed 5M points on either.
Solution: Add the `complexity { before after query }` field to see the remaining budget, paginate with `items_page` plus `cursor` instead of `items`, request only the columns you need, and back off. Every rate limit error returns a `retry_in_seconds` field, and when the per-minute request limit is hit, the `Retry-After` header says when to retry. The `RateLimit-Policy` and `RateLimit` response headers report the policy and the current remaining quota on every response, so you can throttle before hitting the wall.

### Error: 429 that is not a complexity error
Cause: monday enforces several separate limits besides complexity, and most of them depend on the plan:

| Limit | Enterprise | Pro | Other plans |
|-------|------------|-----|-------------|
| Requests per minute ("Minute limit rate exceeded") | 5,000 | 2,500 | 1,000 |
| Concurrent requests | 250 | 100 | 40 |
| Daily API calls (`DAILY_LIMIT_EXCEEDED`, resets at midnight UTC) | 25,000 | 10,000 | 1,000 |

There is also an `IP_RATE_LIMIT_EXCEEDED` cap of 5,000 requests per 10 seconds from one IP address. A Standard account therefore hits the minute limit at 1,000 requests, not 5,000.
Solution: Read the error code rather than assuming complexity. Lower parallelism for the concurrency limit, wait `retry_in_seconds` (or `Retry-After`) before retrying, and if the daily allowance is the problem, move from polling to webhooks or buy additional API calls.

### Error: "MCP server not responding"
Cause: mondaycom/mcp server not configured or token invalid.
Solution: Verify the API token in monday.com under Developers -> My Access Tokens. Restart the MCP server. This skill works standalone without MCP using direct API calls.

### Error: "Column value format invalid"
Cause: Monday.com column values require specific JSON formats, and `ColumnValueException` is returned with HTTP status **200**, so the request looks successful.
Solution: Always inspect the `errors` array rather than the HTTP status. Use `change_simple_column_value` for plain text and numbers, confirm status labels already exist on the board, and check the Column Type Quirks section for connect-boards, mirror and formula columns.
