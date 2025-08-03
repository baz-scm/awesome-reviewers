---
title: Safe database operations
description: 'When modifying database structures or executing dynamic SQL queries,
  prioritize both performance and safety:


  1. **Use non-blocking operations** for schema changes in production databases. For
  example, when creating indexes on potentially busy tables, use `CREATE INDEX CONCURRENTLY`
  instead of standard `CREATE INDEX`:'
repository: supabase/supabase
label: Database
language: TypeScript
comments_count: 2
repository_stars: 86070
---

When modifying database structures or executing dynamic SQL queries, prioritize both performance and safety:

1. **Use non-blocking operations** for schema changes in production databases. For example, when creating indexes on potentially busy tables, use `CREATE INDEX CONCURRENTLY` instead of standard `CREATE INDEX`:

```typescript
// Avoid this - can lock tables during index creation
const sql = `CREATE INDEX ON "${schema}"."${entity}" USING ${type} (${columns})`;

// Prefer this - allows concurrent writes while building the index
const sql = `CREATE INDEX CONCURRENTLY ON "${schema}"."${entity}" USING ${type} (${columns})`;
```

2. **Properly handle SQL string escaping** when building dynamic queries, especially with date values and other complex types. Be careful about escaping clashes between JavaScript and SQL:

```typescript
// Problematic - potential escaping conflicts
const sql = `valid until ${literal(validUntil)}`;

// Better approach - use format specifiers for proper escaping
const sql = `valid until %L`;
const formattedSql = format(sql, validUntil);

// Or use parameterized queries when possible
const result = await client.query('UPDATE users SET valid_until = $1', [validUntil]);
```

These practices help prevent database locks that can impact application performance and avoid SQL injection vulnerabilities while ensuring query correctness.