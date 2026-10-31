---
title: Safe, precise queries
description: 'Write queries that are explicit, secure, and correctly typed. Specifically:


  - Never use `SELECT *`; enumerate the columns you actually need. If you must add
  a column to an existing query (e.g. `COALESCE(byok_enabled, false)`), take the opportunity
  to list out all other selected columns explicitly instead of relying on `*`.'
repository: Helicone/helicone
label: Database
language: TypeScript
comments_count: 5
repository_stars: 6248
---

Write queries that are explicit, secure, and correctly typed. Specifically:

- Never use `SELECT *`; enumerate the columns you actually need. If you must add a column to an existing query (e.g. `COALESCE(byok_enabled, false)`), take the opportunity to list out all other selected columns explicitly instead of relying on `*`.
- Always scope multi-tenant queries by the authenticated organization/user id, even when selecting from a shared or denormalized store (e.g. `WHERE organization_id = {val_0} AND ...`). Don't rely on other filters (like a session id) alone to guarantee row ownership.
- Prefer database-level guarantees (unique constraints, foreign keys) over application-side existence checks for uniqueness/collision handling — let the DB enforce it and handle the resulting error rather than doing a redundant `SELECT` first.
- Choose the right data store/table for the access pattern: use indexed relational tables (e.g. Postgres with JSONB indexes) for point lookups/small reads, and reserve analytical stores (e.g. ClickHouse) for aggregate/OLAP-style queries, since point queries there tend to be slow.
- When aggregating numeric columns (e.g. `SUM(cost)`), confirm the column's integer type has enough headroom for realistic growth; if overflow is plausible, either widen the type (e.g. uint64 → uint128) or bound the aggregation with a time window/settlement period.
- When combining multiple boolean/status conditions in `WHERE`/`UPDATE` clauses, use `AND` instead of `OR` where it lets the query use indexes more efficiently and matches the intended semantics (e.g. `WHERE has_integrated = false` instead of `has_integrated = false OR has_onboarded = false`).

Example of enumerating columns instead of `SELECT *`:
```sql
SELECT id, name, provider, byok_enabled, created_at
FROM provider_keys
WHERE organization_id = $1
```