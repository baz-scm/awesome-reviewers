---
title: track migration state immediately
description: Ensure migration state is recorded in the database immediately after
  each migration file is successfully applied, rather than batching all state updates
  at the end. This prevents inconsistent states where migrations are partially applied
  but not tracked, leaving users unable to determine which migrations have been executed.
repository: drizzle-team/drizzle-orm
label: Migrations
language: TypeScript
comments_count: 2
repository_stars: 29461
---

Ensure migration state is recorded in the database immediately after each migration file is successfully applied, rather than batching all state updates at the end. This prevents inconsistent states where migrations are partially applied but not tracked, leaving users unable to determine which migrations have been executed.

When a migration process fails partway through, users should be able to resume from the last successfully applied migration. If state tracking is deferred until all migrations complete, a failure will leave the database in an unknown state.

Example of problematic pattern:
```typescript
// BAD: State tracking deferred until end
for await (const migration of migrations) {
  if (!lastDbMigration || Number(lastDbMigration.created_at) < migration.folderMillis) {
    for (const stmt of migration.sql) {
      await db.session.execute(sql.raw(stmt));
    }
    rowsToInsert.push(sql`insert into ${migrationsTable}...`); // Deferred
  }
}
// Execute all inserts at end - if this fails, no state is tracked
```

Better approach:
```typescript
// GOOD: State tracked immediately after each migration
for await (const migration of migrations) {
  if (!lastDbMigration || Number(lastDbMigration.created_at) < migration.folderMillis) {
    for (const stmt of migration.sql) {
      await db.session.execute(sql.raw(stmt));
    }
    // Track state immediately after successful application
    await db.session.execute(sql`insert into ${migrationsTable} ("hash", "created_at") values(${migration.hash}, ${migration.folderMillis})`);
  }
}
```

This principle also applies when making changes to migration tooling - always consider the impact on existing migration state and provide clear guidance for users to handle state inconsistencies.