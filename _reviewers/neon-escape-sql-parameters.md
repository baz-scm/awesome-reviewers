---
title: Escape SQL parameters
description: Always escape parameters in database connection strings to prevent SQL
  injection attacks. Direct string concatenation with user-provided or database-sourced
  values creates security vulnerabilities that can be exploited.
repository: neondatabase/neon
label: Security
language: Sql
comments_count: 1
repository_stars: 19015
---

Always escape parameters in database connection strings to prevent SQL injection attacks. Direct string concatenation with user-provided or database-sourced values creates security vulnerabilities that can be exploited.

When using PostgreSQL's dblink function, apply proper escaping functions like quote_ident() for identifiers (e.g., database names) and quote_literal() for string values:

Instead of unsafe concatenation:
```sql
'dbname=' || d.datname || ' user=' || current_user || ' connect_timeout=5'
```

Use escaped parameters:
```sql
'dbname=' || quote_ident(d.datname) || ' user=' || quote_literal(current_user) || ' connect_timeout=5'
```

This practice should extend to all SQL query construction, ensuring that any dynamic values incorporated into queries are properly sanitized before execution.