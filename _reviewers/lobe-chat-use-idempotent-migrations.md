---
title: Use idempotent migrations
description: Always use defensive programming patterns in migration scripts to ensure
  they can be executed multiple times without errors. This prevents failures during
  re-execution scenarios and makes migrations more robust.
repository: lobehub/lobe-chat
label: Migrations
language: Sql
comments_count: 4
repository_stars: 65138
---

Always use defensive programming patterns in migration scripts to ensure they can be executed multiple times without errors. This prevents failures during re-execution scenarios and makes migrations more robust.

Key patterns to implement:
- Use `CREATE TABLE IF NOT EXISTS` instead of `CREATE TABLE`
- Use `ALTER TABLE ADD COLUMN IF NOT EXISTS` instead of `ALTER TABLE ADD COLUMN`
- Apply similar defensive patterns to other DDL statements

Example:
```sql
-- Good: Idempotent migration
CREATE TABLE IF NOT EXISTS "chat_groups" (
    "id" text PRIMARY KEY NOT NULL,
    "title" text
);

ALTER TABLE "messages" ADD COLUMN IF NOT EXISTS "group_id" text;

-- Bad: Non-idempotent migration
CREATE TABLE "chat_groups" (
    "id" text PRIMARY KEY NOT NULL,
    "title" text
);

ALTER TABLE "messages" ADD COLUMN "group_id" text;
```

This approach ensures migrations won't fail with "already exists" errors when run multiple times, which is common during development, testing, and deployment scenarios.