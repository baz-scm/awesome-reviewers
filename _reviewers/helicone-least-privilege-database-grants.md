---
title: Least-privilege database grants
description: Enabling Row Level Security (RLS) alone is not sufficient to secure a
  new table—Postgres/Supabase grants default privileges to roles like `anon` and `authenticated`
  that can allow unintended access even with RLS enabled unless explicit policies
  are also defined. When creating tables for sensitive or system-level data, always
  explicitly revoke default...
repository: Helicone/helicone
label: Security
language: Sql
comments_count: 1
repository_stars: 6248
---

Enabling Row Level Security (RLS) alone is not sufficient to secure a new table—Postgres/Supabase grants default privileges to roles like `anon` and `authenticated` that can allow unintended access even with RLS enabled unless explicit policies are also defined. When creating tables for sensitive or system-level data, always explicitly revoke default privileges from public-facing roles immediately after creation, then add only the specific policies needed for legitimate access. For example:

```sql
ALTER TABLE public.system_config ENABLE ROW LEVEL SECURITY;
REVOKE ALL PRIVILEGES ON TABLE public.system_config FROM anon;
REVOKE ALL PRIVILEGES ON TABLE public.system_config FROM authenticated;
```

Follow this pattern for any new table, especially configuration or internal-use tables, to enforce least-privilege access and avoid accidental data exposure through default role grants.</description>
</invoke>
