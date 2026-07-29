---
title: Database-safe atomic updates
description: 'When writing/reading sensitive or destructive data, make the database
  do the work safely and atomically:


  - Prefer SQL-side filtering to avoid broad in-memory fetch/processing (e.g., add
  `authType` filtering in the query rather than filtering afterward).'
repository: diegosouzapw/OmniRoute
label: Database
language: TypeScript
comments_count: 3
repository_stars: 33162
---

When writing/reading sensitive or destructive data, make the database do the work safely and atomically:

- Prefer SQL-side filtering to avoid broad in-memory fetch/processing (e.g., add `authType` filtering in the query rather than filtering afterward).
- For read-modify-write flows that require audit/comparison (e.g., capture previous scopes), wrap the previous-row SELECT and the UPDATE in a single atomic SQL block using explicit `BEGIN … COMMIT` (and `ROLLBACK` on error) rather than assuming a higher-level `db.transaction()` exists.
- For identifier-driven destructive queries, avoid `LIKE` with unescaped/untrusted identifiers (because `%`/`_` change semantics). Use deterministic predicates like exact match or parameterized prefix matching (e.g., `substr(col,1,?) = ?`).

Example pattern (atomic read + update + safe predicates):

```ts
// Atomic read-modify-write even without db.transaction()
const nextScopes = Array.isArray(scopesUpdate)
  ? scopesUpdate.filter((s): s is string => typeof s === "string")
  : [];

const result = db.exec(`
  BEGIN IMMEDIATE;
`);

try {
  const prevRow = db
    .prepare<{ scopes: string | null }>(
      "SELECT scopes FROM api_keys WHERE id = ?"
    )
    .get(id);
  const previousScopes = parseStringList(prevRow?.scopes ?? null);

  db.prepare("UPDATE api_keys SET scopes = ? WHERE id = ?")
    .run(JSON.stringify(nextScopes), id);

  db.exec("COMMIT;");

  // emit audit using previousScopes -> nextScopes
} catch (e) {
  db.exec("ROLLBACK;");
  throw e;
}
```

```sql
-- Safe destructive delete by identifier prefix (no LIKE)
DELETE FROM key_value
WHERE namespace = 'syncedAvailableModels'
  AND substr(key, 1, ?) = ?;
```

Applying this consistently reduces correctness bugs, prevents expensive over-fetching, and keeps audit trails reliable across different SQLite/driver backends.