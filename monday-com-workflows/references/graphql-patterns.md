# Monday.com GraphQL API Patterns

## Authentication

All requests use the Monday.com API token in the Authorization header:

```
POST https://api.monday.com/v2
Authorization: YOUR_API_TOKEN
API-Version: 2026-07
Content-Type: application/json
```

Pin `API-Version` explicitly. `2026-07` is the default until 1 October 2026, when `2026-10` becomes the default and `2026-07` moves to maintenance; `2027-01` becomes the release candidate on the same day. See the schedule table in SKILL.md.

---

## Common Query Patterns

### Get Current User Info

`account.plan` returns `null` for accounts on the multi-product infrastructure, so do not branch on it. Read `account.tier` and `account.products` and treat `plan` as optional.

```graphql
{
  me {
    name
    email
  }
  account {
    name
    tier
    products { kind }
    plan {
      max_users
    }
  }
}
```

### List All Boards

`hierarchy_type` must be passed to see sub-item (multi-level) boards. Omit it and only `classic` boards come back, unless you supplied explicit board IDs.

```graphql
{
  boards(limit: 50, hierarchy_type: [classic, multi_level]) {
    id
    name
    state
    board_kind
    workspace {
      name
    }
    columns {
      id
      title
      type
    }
  }
}
```

### Get Board Items (Paginated)
```graphql
{
  boards(ids: [BOARD_ID]) {
    items_page(limit: 100) {
      cursor
      items {
        id
        name
        group {
          id
          title
        }
        column_values {
          id
          text
          value
        }
      }
    }
  }
}
```

### Get Next Page (Cursor-based Pagination)
```graphql
{
  next_items_page(cursor: "CURSOR_FROM_PREVIOUS", limit: 100) {
    cursor
    items {
      id
      name
      column_values {
        id
        text
      }
    }
  }
}
```

### Search Items by Column Value
```graphql
{
  items_page_by_column_values(
    board_id: BOARD_ID
    columns: [
      {column_id: "status", column_values: ["Working on it"]}
    ]
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
```
`items_page_by_column_values` returns a `cursor`, exactly like `items_page`. With `limit: 50` you only get the first page, so to fetch every match keep calling `next_items_page(cursor: ...)` until the returned `cursor` is `null`. Omitting the cursor loop silently truncates the result set at the limit.

---

## Common Mutation Patterns

The literal values below show the shape of each mutation. In code, pass every value (especially Hebrew names and labels) as a GraphQL variable, as the `MondayClient` helper at the end of this file does: an ASCII double quote inside a Hebrew acronym ends a literal string and breaks the query. When a mutation may be retried, send an `Idempotency-Key` header with the same value on each attempt; monday caches the first response for 30 minutes, and a concurrent duplicate gets `409 Conflict` with `Retry-After`.

### Create a Board
```graphql
mutation {
  create_board(
    board_name: "Sprint 2025-W10"
    board_kind: public
    workspace_id: WORKSPACE_ID
  ) {
    id
  }
}
```

### Create a Group
```graphql
mutation {
  create_group(
    board_id: BOARD_ID
    group_name: "Sunday Tasks"
  ) {
    id
  }
}
```

### Create an Item
```graphql
mutation {
  create_item(
    board_id: BOARD_ID
    group_id: "GROUP_ID"
    item_name: "New Task"
    column_values: "{\"status\": {\"label\": \"Working on it\"}, \"date\": {\"date\": \"2025-03-15\"}}"
  ) {
    id
  }
}
```

### Update Item Column Value
```graphql
mutation {
  change_column_value(
    board_id: BOARD_ID
    item_id: ITEM_ID
    column_id: "status"
    value: "{\"label\": \"Done\"}"
  ) {
    id
    name
  }
}
```

### Change Simple Column Value (Text/Number)
```graphql
mutation {
  change_simple_column_value(
    board_id: BOARD_ID
    item_id: ITEM_ID
    column_id: "text_column"
    value: "New text value"
  ) {
    id
  }
}
```

### Move Item to Group
```graphql
mutation {
  move_item_to_group(
    item_id: ITEM_ID
    group_id: "TARGET_GROUP_ID"
  ) {
    id
  }
}
```

### Archive an Item
```graphql
mutation {
  archive_item(item_id: ITEM_ID) {
    id
  }
}
```

### Add an Update (Comment)
```graphql
mutation {
  create_update(
    item_id: ITEM_ID
    body: "Sprint review: This task is 80% complete. Blocked by API integration."
  ) {
    id
  }
}
```

---

## Column Value Formats

Different column types require specific JSON formats:

### Status
```json
{"label": "Done"}
```

### Date
```json
{"date": "2025-03-15"}
```

### Date with Time
```json
{"date": "2025-03-15", "time": "14:00:00"}
```

### Person (Assignee)
```json
{"personsAndTeams": [{"id": USER_ID, "kind": "person"}]}
```

### Numbers
```json
"42"
```
(Use change_simple_column_value for numbers)

### Dropdown
```json
{"labels": ["Option 1", "Option 2"]}
```

### Email
```json
{"email": "user@example.com", "text": "user@example.com"}
```

### Phone
```json
{"phone": "+972541234567", "countryShortName": "IL"}
```

### Link
```json
{"url": "YOUR_LINK_URL", "text": "Example Site"}
```

### Long Text
```json
{"text": "This is a longer description with details."}
```

### Connect Boards (write)
```json
{"connect_boards": {"item_ids": [1122334455, 5544332211]}}
```
Pass `{"connect_boards": null}` to clear it. On read, both `text` and `value` return `null` on this column; use `display_value`, `linked_item_ids`, or `linked_items`.

### Mirror (read only)
Mirror columns cannot be updated or cleared through the API; they reflect the source column on the connected board. Both `text` and `value` return `null`; use `display_value` or `mirrored_items`. Filtering on mirrored content is not supported.

---

## Rate Limiting

- **Personal API token:** reads and writes share a combined budget of 10,000,000 complexity points per minute
- **App token:** reads and writes are limited to 5,000,000 complexity points per minute *each* (a separate ceiling per direction, not a shared pool)
- **Trial / NGO / free plan:** 1,000,000 complexity points per minute
- **Single-query cap:** 5,000,000 complexity points (one operation cannot exceed this)
- **Remaining budget:** add a `complexity { before after query }` field to your query to read how many points it cost and how many remain. Every response also carries `RateLimit-Policy` and `RateLimit` headers reporting the policy and the current remaining quota.
- **On an error:** every rate limit error returns a `retry_in_seconds` field. When the per-minute request limit is hit, the `Retry-After` header says when to retry.

### Plan-Level API Call Allowance

Separate from complexity, the account's plan caps daily API calls: 1,000/day on Standard, 10,000/day on Pro, 25,000/day on Enterprise (resets at midnight UTC). On Standard this binds long before complexity does; a once-a-minute poll needs 1,440 calls/day and cannot work. Calls made through the hosted monday MCP server count toward the same daily limit.

### Plan-Dependent Limits

| Limit | Enterprise | Pro | Other plans |
|-------|------------|-----|-------------|
| Requests per minute ("Minute limit rate exceeded") | 5,000 | 2,500 | 1,000 |
| Concurrent requests | 250 | 100 | 40 |
| Daily API calls (`DAILY_LIMIT_EXCEEDED`) | 25,000 | 10,000 | 1,000 |

`IP_RATE_LIMIT_EXCEEDED` is a separate cap of 5,000 requests per 10 seconds from one IP address.

`ColumnValueException` is different: it is returned with HTTP **200**, so check the `errors` array rather than the HTTP status.

### Complexity Estimation
- Simple query (1 board, few columns): ~100 points
- Items page (100 items): ~5,000-10,000 points
- Create/update mutation: ~10-50 points

### Best Practices to Stay Within Limits
1. Request only the columns you need (avoid `column_values` wildcard)
2. Use pagination with reasonable limits (50-100 items per page)
3. Batch related operations where possible
4. Cache board structure (columns, groups) -- these change infrequently
5. Use webhooks instead of polling for real-time updates

---

## Webhook Patterns

### Create a Webhook
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

### Subscription Handshake

On creation monday POSTs a JSON body containing a randomly generated token in a `challenge` field. Your endpoint must echo that token back as a `challenge` field in its own JSON response body, or registration fails.

### Retry Semantics

Failed deliveries retry once a minute for 30 minutes, then stop. The event is not replayable afterwards, so pair any webhook consumer with a low-frequency reconciliation pass. Delivery order is not guaranteed: treat each payload as a signal to re-read the item, not as authoritative state.

### Available Webhook Events
`change_column_value`, `change_status_column_value`, `change_subitem_column_value`, `change_specific_column_value`, `change_name`, `create_item`, `item_archived`, `item_deleted`, `item_moved_to_any_group`, `item_moved_to_specific_group`, `item_restored`, `create_subitem`, `change_subitem_name`, `move_subitem`, `subitem_archived`, `subitem_deleted`, `create_column`, `create_update`, `edit_update`, `delete_update`, `create_subitem_update`.

Subitem events are separate: a `change_column_value` subscription on the parent board does not deliver subitem changes.

### Webhook Payload Structure
```json
{
  "event": {
    "type": "change_column_value",
    "boardId": 123456,
    "pulseId": 789012,
    "pulseName": "Task Name",
    "columnId": "status",
    "columnTitle": "Status",
    "value": {"label": {"text": "Done"}},
    "previousValue": {"label": {"text": "Working on it"}},
    "userId": 54321,
    "triggerTime": "2025-03-15T10:30:00.000Z"
  }
}
```

---

## Python Helper: Monday.com API Client

```python
import requests
import json

class MondayClient:
    """Simple Monday.com API client. All user text goes through GraphQL
    variables: Hebrew text with an ASCII quote breaks a formatted query."""

    def __init__(self, api_token: str):
        self.url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": api_token,
            "API-Version": "2026-07",
            "Content-Type": "application/json"
        }

    def query(self, graphql_query: str, variables: dict = None) -> dict:
        """Execute a GraphQL operation and return `data`. Raises on an
        `errors` array, because monday returns many errors with HTTP 200."""
        response = requests.post(self.url, headers=self.headers, timeout=30,
                                 json={"query": graphql_query,
                                       "variables": variables or {}})
        result = response.json()
        if result.get("errors"):
            raise RuntimeError(f"monday API error: {result['errors']}")
        return result["data"]

    def get_board_items(self, board_id: int, limit: int = 100) -> list:
        """Get all items from a board with cursor pagination."""
        fields = "cursor items { id name group { title } column_values { id text } }"
        page = self.query(
            "query ($ids: [ID!], $limit: Int!) { boards(ids: $ids) { items_page(limit: $limit) { %s } } }" % fields,
            {"ids": [board_id], "limit": limit})["boards"][0]["items_page"]
        items = list(page["items"])
        while page.get("cursor"):
            page = self.query(
                "query ($c: String!, $limit: Int!) { next_items_page(cursor: $c, limit: $limit) { %s } }" % fields,
                {"c": page["cursor"], "limit": limit})["next_items_page"]
            items.extend(page["items"])
        return items

    def create_item(self, board_id: int, group_id: str,
                    item_name: str, column_values: dict = None) -> dict:
        """Create a new item."""
        return self.query("""
        mutation ($b: ID!, $g: String, $n: String!, $v: JSON) {
          create_item(board_id: $b, group_id: $g, item_name: $n, column_values: $v) { id }
        }""", {"b": board_id, "g": group_id, "n": item_name,
               "v": json.dumps(column_values or {}, ensure_ascii=False)})

    def update_status(self, board_id: int, item_id: int,
                      column_id: str, label: str) -> dict:
        """Update a status column. The label must already exist on the board."""
        return self.query("""
        mutation ($b: ID!, $i: ID!, $c: String!, $v: JSON!) {
          change_column_value(board_id: $b, item_id: $i, column_id: $c, value: $v) { id }
        }""", {"b": board_id, "i": item_id, "c": column_id,
               "v": json.dumps({"label": label}, ensure_ascii=False)})
```
