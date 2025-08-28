---
title: type-safe database operations
description: Implement proper type conversion and validation when working with different
  database systems to prevent runtime errors and data corruption. This is critical
  when handling data types that behave differently across database engines.
repository: rocicorp/mono
label: Database
language: TypeScript
comments_count: 10
repository_stars: 2091
---

Implement proper type conversion and validation when working with different database systems to prevent runtime errors and data corruption. This is critical when handling data types that behave differently across database engines.

Key practices:
1. **Explicit type casting**: When working with JSON data in PostgreSQL, use explicit casting to avoid driver confusion:
```typescript
// Instead of relying on automatic type inference
queryArgs: change.queryArgs === undefined ? null : JSON.stringify(change.queryArgs)

// Use explicit casting
queryArgs: ${change.queryArgs === undefined ? null : JSON.stringify(change.queryArgs)}::text::json
```

2. **Database-specific type mapping**: Create conversion functions for each database system:
```typescript
function toSQLiteType(v: unknown, type: ValueType): unknown {
  switch (type) {
    case 'boolean':
      return v === null ? null : v ? 1 : 0;
    case 'json':
      return JSON.stringify(v);
    default:
      return v;
  }
}
```

3. **Preserve data fidelity**: Choose data types that preserve original data structure. For example, use `JSON` instead of `JSONB` in PostgreSQL unless you specifically need JSONB features like indexing, since JSONB reorders fields and doesn't allow NULL bytes.

4. **Validate type assumptions**: Always validate boolean and enum conversions:
```typescript
// Correct boolean check
isEnum: row.enum.toLowerCase().startsWith('t')
// Not: row.enum.toLowerCase().startsWith('f')
```

5. **Handle timezone conversions carefully**: Use appropriate SQL functions for timestamp conversions:
```sql
-- For timestamp with timezone
EXTRACT(EPOCH FROM column_name) * 1000

-- For timestamp without timezone  
EXTRACT(EPOCH FROM column_name::timestamp AT TIME ZONE 'UTC') * 1000
```

This approach prevents subtle bugs that can occur when data types are handled inconsistently across different database systems and ensures reliable data persistence and retrieval.