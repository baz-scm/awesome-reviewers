---
title: Database type consistency
description: Ensure database-specific types, imports, and serialization are used consistently
  throughout the codebase. This prevents runtime errors, improves type safety, and
  maintains proper data handling across different database systems.
repository: drizzle-team/drizzle-orm
label: Database
language: TypeScript
comments_count: 15
repository_stars: 29461
---

Ensure database-specific types, imports, and serialization are used consistently throughout the codebase. This prevents runtime errors, improves type safety, and maintains proper data handling across different database systems.

Key areas to verify:

1. **Use correct database-specific imports**: Import types and utilities from the appropriate database core module (e.g., `mysql-core`, `pg-core`, `sqlite-core`) rather than mixing imports from different databases.

2. **Handle data type serialization properly**: Convert problematic types like BigInt to appropriate formats before serialization to avoid "Do not know how to serialize a BigInt" errors.

3. **Manage timezone and date handling consistently**: Override default database driver parsers when needed to ensure consistent date/timestamp behavior across environments.

Example of incorrect usage:
```typescript
// Wrong - using PostgreSQL types for MySQL
import { AnyPgColumn, AnyPgTable } from 'drizzle-orm/mysql-core';

// Wrong - BigInt serialization issue
declare global {
    interface BigInt {
        toJSON(): Number;
    }
}
```

Example of correct usage:
```typescript
// Correct - use appropriate database types
import { AnyMySqlColumn, AnyMySqlTable } from 'drizzle-orm/mysql-core';

// Correct - handle BigInt conversion in serializer
if (typeof defaultValue === 'bigint') {
    defaultValue = defaultValue.toString();
}

// Correct - override timestamp parsing for consistency
const transparentParser = (val: any) => val;
for (const type of ['1184', '1082', '1083', '1114']) {
    client.types.setTypeParser(type, transparentParser);
}
```

This ensures type safety, prevents serialization errors, and maintains consistent behavior across different database systems and environments.