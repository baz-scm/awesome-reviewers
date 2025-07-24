---
title: Explicit role security management
description: Always be explicit about role privileges when configuring database security.
  Remember that both `authenticated` and `anon` roles typically have default privileges
  that need to be explicitly revoked. Use SQL migrations rather than GUI tools to
  manage role permissions for better version control and reproducibility.
repository: supabase/supabase
label: Database
language: Other
comments_count: 3
repository_stars: 86070
---

Always be explicit about role privileges when configuring database security. Remember that both `authenticated` and `anon` roles typically have default privileges that need to be explicitly revoked. Use SQL migrations rather than GUI tools to manage role permissions for better version control and reproducibility.

```sql
-- Example: Revoking update privileges from both authenticated and anon roles
revoke update on table public.posts from authenticated;
revoke update on table public.posts from anon;

-- Then grant specific column-level privileges as needed
grant update (title, content) on table public.posts to authenticated;
```

When implementing Row Level Security policies with JWT claims, ensure proper SQL syntax to extract JWT values. Use subqueries when referencing JWT values in comparisons:

```sql
-- Correct way to reference JWT values in RLS policies
create policy "Only organization admins can insert"
  on table_name
  to authenticated
  with check (
    (auth.jwt()->>'org_role' = 'org:admin')
      and
    (organization_id = (select auth.jwt()->>'org_id'))
  );
```

This approach ensures that your database access controls are precisely defined and consistently maintained through version-controlled code.