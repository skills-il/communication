# Domain coverage checklist, monday-com-workflows

Anchor for expert review. Scope: optimizing monday.com workflows (boards, groups, automations, GraphQL API) for Israeli teams, layered on top of the official mondaycom/mcp server.

## Must cover (core)
- monday.com GraphQL endpoint (https://api.monday.com/v2) + Authorization header auth.
- API versioning by month: pin API-Version explicitly; current default 2026-04, 2026-07 RC becomes default 2026-07-01. Deprecated 2024-10 / 2025-01 (2026-02-15).
- Core mutations/queries: create_board, create_group, create_item, change_column_value / change_simple_column_value, items_page + cursor pagination, items_page_by_column_values.
- Complexity/rate limits: 10M points/min per user (1M trial/free), 5M single-query cap; read remaining via complexity{} field; Retry-After on 429.
- Israeli work week: Sunday-Thursday sprint structure; Asia/Jerusalem timezone.
- Holiday-aware scheduling using the **Israel** holiday schedule (one-day Yom Tov), not Diaspora dates; verify per year via hebcal.com/holidays/<year>?i=on.
- Hebrew/RTL board + column handling; exact-string column name matching.
- mondaycom/mcp pairing (static CRUD tools + Dynamic API Tools beta).

## Should cover (advanced)
- Current breaking changes for the pinned version, and what lands in the next version.
- Cross-board coordination (Connect Boards column, mirror, status-driven item creation).
- Automations are configured in-UI or via the apps framework, NOT a queryable core-API endpoint.

## Out of scope (explicit)
- Other PM tools (Jira, Asana), excluded by the skill description.
- Billing/finance integration internals (handled by finance-system skills).
- Half-day erev-chag modelling (binary holiday function only).

## Authoritative sources
- monday API versioning: https://developer.monday.com/api-reference/docs/api-versioning
- monday rate limits: https://developer.monday.com/api-reference/docs/rate-limits
- monday items API: https://developer.monday.com/api-reference/docs/items
- mondaycom/mcp: https://github.com/mondaycom/mcp
- Israel holiday dates: hebcal.com/holidays/<year>?i=on (Israel schedule)
