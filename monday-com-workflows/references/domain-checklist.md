# Domain coverage checklist, monday-com-workflows

Anchor for expert review. Scope: optimizing monday.com workflows (boards, groups, automations, GraphQL API) for Israeli teams, layered on top of the official mondaycom/mcp server.

## Must cover (core)
- monday.com GraphQL endpoint (https://api.monday.com/v2) + Authorization header auth.
- API versioning by month: pin API-Version explicitly. Default 2026-07 until 2026-10-01, then 2026-10 (2026-07 to maintenance, 2027-01 becomes RC). No deprecation date announced for 2026-04 or later. Deprecated 2024-10 / 2025-01 (2026-02-15).
- Core mutations/queries: create_board, create_group, create_item, change_column_value / change_simple_column_value, items_page + cursor pagination, items_page_by_column_values.
- boards query requires hierarchy_type to include multi-level boards; account.plan is null on multi-product-infrastructure accounts, read account.tier instead.
- Complexity/rate limits: personal token 10M points/min combined (1M trial/NGO/free), app token 5M each direction, 5M single-query cap; read remaining via complexity{} field and the RateLimit headers; retry_in_seconds on every rate limit error. Plan-tiered minute limit (5,000 / 2,500 / 1,000), concurrency (250 / 100 / 40), IP cap 5,000 per 10 s, daily calls reset midnight UTC and include hosted-MCP calls.
- Plan gating: several products with separate ladders (work management, CRM, Campaigns, Dev, Service; CRM tops out at Ultimate), work management Free up to 2 seats; automations/integrations start at Standard with 250 actions/month; API calls capped 1,000/day on Standard.
- Webhooks vs polling, including the challenge handshake and the 30-minute retry window.
- Column quirks: connect boards and mirror return null text/value; formula returns its result in display_value (text and value not populated); status writes fail with HTTP 200.
- monday has no Hebrew or Arabic interface language (15 interface languages per the support article); Hebrew is content only.
- Israeli work week: Sunday-Thursday sprint structure; Asia/Jerusalem timezone.
- Holiday-aware scheduling using the **Israel** holiday schedule (one-day Yom Tov), not Diaspora dates; verify per year via hebcal.com/holidays/<year>?i=on.
- Hebrew/RTL board + column handling; address columns by id, never by Hebrew title.
- User text passed through GraphQL variables (ASCII quotes in Hebrew acronyms break formatted queries); check the errors array on every call.
- Holiday table is year-bounded: must refuse an uncovered year rather than answer "working day"; three states (off / half / policy) per statute s.18A and the Independence Day Law.
- Overdue sweep (items_page with a TODAY lower_than rule, full cursor loop) and notifying Slack, native integration vs own job plus incoming webhook.
- Date filters resolve in the token owner's profile time zone and first day of week.
- Idempotency-Key on retried mutations.
- Workflows (Workflow Builder) distinct from automations; built via MCP against the preview schema.
- mondaycom/mcp pairing (static CRUD tools + Dynamic API Tools beta).

## Should cover (advanced)
- Current breaking changes for the pinned version, and what lands in the next version.
- Cross-board coordination (Connect Boards column, mirror, status-driven item creation).
- Automations are configured in the board's automation center, as custom monday apps, or through the Platform MCP create_automation tool.

## Out of scope (explicit)
- Other PM tools (Jira, Asana), excluded by the skill description.
- Billing/finance integration internals (handled by finance-system skills).
- (Re-opened 2026-09-19 and RESOLVED: half-day erev-chag modelling is now covered by the three-state table in references/israeli-holidays.md.)
- Aliased batch mutations for bulk updates: not written, because monday's docs did not show a documented batching pattern this cycle (2026-09-19). Revisit.

## Authoritative sources
- monday API versioning: https://developer.monday.com/api-reference/docs/api-versioning
- monday rate limits: https://developer.monday.com/api-reference/docs/rate-limits
- monday items API: https://developer.monday.com/api-reference/docs/items
- monday boards query: https://developer.monday.com/api-reference/reference/boards
- monday account object: https://developer.monday.com/api-reference/reference/account
- monday pricing and quotas: https://monday.com/pricing
- mondaycom/mcp: https://github.com/mondaycom/mcp
- Israel holiday dates: hebcal.com/holidays/<year>?i=on (Israel schedule)
- Statutory rest days: Law and Administration Ordinance s.18A; Independence Day Law s.1(c) (he.wikisource.org)
- monday idempotency: https://developer.monday.com/api-reference/docs/idempotency
- monday date column filters: https://developer.monday.com/api-reference/reference/date
