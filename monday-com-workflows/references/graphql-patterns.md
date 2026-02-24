# Monday.com GraphQL API Patterns

## Authentication

All requests use the Monday.com API token in the Authorization header:

```
POST https://api.monday.com/v2
Authorization: YOUR_API_TOKEN
Content-Type: application/json
```

---

## Common Query Patterns

### Get Current User Info
```graphql
{
  me {
    name
    email
    account {
      name
      plan {
        max_users
      }
    }
  }
}
```

### List All Boards
```graphql
{
  boards(limit: 50) {
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

---

## Common Mutation Patterns

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
{"url": "https://example.com", "text": "Example Site"}
```

### Long Text
```json
{"text": "This is a longer description with details."}
```

---

## Rate Limiting

- **Standard plan:** 10,000,000 complexity points per month
- **Per-minute limit:** 10,000 complexity points per 60 seconds
- **Rate limit header:** Check `X-Complexity-Points` in response

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
    url: "https://your-server.com/webhook/monday"
    event: change_column_value
  ) {
    id
    board_id
  }
}
```

### Available Webhook Events
- `change_column_value` -- Column value changed
- `create_item` -- New item created
- `create_update` -- New update/comment added
- `change_status_column_value` -- Status specifically changed
- `change_subitem_column_value` -- Sub-item column changed

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
    """Simple Monday.com API client."""

    def __init__(self, api_token: str):
        self.url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }

    def query(self, graphql_query: str, variables: dict = None) -> dict:
        """Execute a GraphQL query."""
        payload = {"query": graphql_query}
        if variables:
            payload["variables"] = variables
        response = requests.post(self.url, headers=self.headers,
                                 json=payload, timeout=30)
        return response.json()

    def get_board_items(self, board_id: int, limit: int = 100) -> list:
        """Get all items from a board with pagination."""
        items = []
        query = '''
        { boards(ids: [%d]) {
            items_page(limit: %d) {
              cursor
              items { id name group { title }
                column_values { id text } } } } }
        ''' % (board_id, limit)

        result = self.query(query)
        page = result["data"]["boards"][0]["items_page"]
        items.extend(page["items"])

        while page.get("cursor"):
            next_query = '''
            { next_items_page(cursor: "%s", limit: %d) {
                cursor
                items { id name group { title }
                  column_values { id text } } } }
            ''' % (page["cursor"], limit)
            result = self.query(next_query)
            page = result["data"]["next_items_page"]
            items.extend(page["items"])

        return items

    def create_item(self, board_id: int, group_id: str,
                    item_name: str, column_values: dict = None) -> dict:
        """Create a new item."""
        values = json.dumps(json.dumps(column_values)) if column_values else '"{}"'
        mutation = '''
        mutation {
          create_item(board_id: %d, group_id: "%s",
                      item_name: "%s", column_values: %s) { id }
        }
        ''' % (board_id, group_id, item_name, values)
        return self.query(mutation)

    def update_status(self, board_id: int, item_id: int,
                      column_id: str, label: str) -> dict:
        """Update a status column."""
        value = json.dumps(json.dumps({"label": label}))
        mutation = '''
        mutation {
          change_column_value(board_id: %d, item_id: %d,
                              column_id: "%s", value: %s) { id }
        }
        ''' % (board_id, item_id, column_id, value)
        return self.query(mutation)
```
