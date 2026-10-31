---
title: Deliberate schema constraints
description: 'When writing migrations, define schemas deliberately and avoid redundant
  or speculative elements. Specifically:


  - Don''t duplicate mechanisms: if a unique constraint already enforces uniqueness,
  don''t also create a separate unique index for the same columns.'
repository: Helicone/helicone
label: Migrations
language: Sql
comments_count: 5
repository_stars: 6248
---

When writing migrations, define schemas deliberately and avoid redundant or speculative elements. Specifically:

- Don't duplicate mechanisms: if a unique constraint already enforces uniqueness, don't also create a separate unique index for the same columns.
- Bound your columns: avoid unconstrained `character varying`/`text` where a reasonable limit is known (e.g., use `varchar(255) not null` instead of bare `character varying`).
- Add audit columns where relevant, such as `added_by uuid not null` to track who granted/created a relationship (e.g., linking an API key to a router).
- For data that changes over time (configs, settings), model it with a base table plus a `_versions` table (`config_id`, `version`, `config jsonb`, `created_at`) so you can track history and prevent stale/overwritten state, e.g.:

```sql
CREATE TABLE gateway_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    organization_id UUID NOT NULL,
    gateway_key_id BIGINT,
    name VARCHAR(255)
);

CREATE TABLE gateway_config_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_id UUID NOT NULL REFERENCES gateway_configs(id),
    version VARCHAR(255) NOT NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

- Don't add columns, indexes, or primary keys speculatively "just in case." Only include them when there's a concrete, current use case; add them later via a new migration if the need arises. For ClickHouse tables especially, keep primary keys to the highest-order granularity actually needed for filtering, or omit them if every column is already part of the filter criteria.

Applying these rules keeps migrations lean, self-documenting, and free of unnecessary maintenance burden while still supporting correctness and future auditability.