---
title: Data model guardrails
description: 'Default schemas should be designed for (a) correct capacity/performance
  assumptions and (b) efficient, queryable storage.


  1) Use correct cardinality math for sizing'
repository: awslabs/mcp
label: Database
language: Markdown
comments_count: 3
repository_stars: 9545
---

Default schemas should be designed for (a) correct capacity/performance assumptions and (b) efficient, queryable storage.

1) Use correct cardinality math for sizing
- When you estimate InfluxDB series/cardinality for capacity planning, series cardinality must be computed as:
  - **measurement + tag set + field key**
- If you ignore **field keys**, you will systematically underestimate cardinality (and likely undersize the instance).

2) Prefer JSONB for “array-like” / structured columns you will query
- If the DB doesn’t have native array column types, store arrays/collections in a **JSONB** column so you can use native JSONB operators and avoid casting in every query.
- TEXT is only for truly opaque data (app-side parsing only, no DB-side querying).

Example (JSONB-backed tags):
```sql
CREATE TABLE orders (
  order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id VARCHAR(255) NOT NULL,
  status VARCHAR(50) NOT NULL,
  tags JSONB,
  metadata JSONB
);

-- Query JSONB array contents
-- (works directly on JSONB)
SELECT jsonb_array_elements_text(tags);

-- Filter by array containment
SELECT *
FROM orders
WHERE tags @> '["urgent"]';

-- Key-existence checks
SELECT *
FROM orders
WHERE tags ? 'shipped';
```

Practical checks
- Before locking a schema, confirm: “How will we query/filter this?” If queries will happen in the DB, JSONB should be the default choice.
- For performance sizing, validate your cardinality model against the definition your system uses (include field keys where applicable).