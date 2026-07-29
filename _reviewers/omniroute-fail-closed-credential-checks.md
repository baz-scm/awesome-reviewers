---
title: Fail-Closed Credential Checks
description: 'When validating security state (e.g., whether credentials are encrypted,
  authorized sessions exist, tokens exist, etc.), treat any inability to inspect sensitive
  data as a security failure—don’t silently default to a permissive/incorrect outcome.
  In practice:'
repository: diegosouzapw/OmniRoute
label: Security
language: JavaScript
comments_count: 2
repository_stars: 33162
---

When validating security state (e.g., whether credentials are encrypted, authorized sessions exist, tokens exist, etc.), treat any inability to inspect sensitive data as a security failure—don’t silently default to a permissive/incorrect outcome. In practice:
- Do not swallow exceptions in security checks (no empty `catch {}` that turns “unknown” into a benign value).
- Prefer “fail closed”: if the inspection DB/read/parsing step errors, return a conservative result (often “encrypted not confirmed” / “credentials not trusted”) and/or throw so the caller can block the unsafe path.
- Keep the change narrowly scoped: security PRs should avoid unrelated refactors that expand module/runtime surface.

Example pattern (fail closed on inspection errors):
```js
function hasEncryptedCredentials(dbPath) {
  if (!fs.existsSync(dbPath)) return false;

  try {
    const Database = require("better-sqlite3");
    const db = new Database(dbPath, { readonly: true, fileMustExist: true });
    try {
      const row = db
        .prepare(`
          SELECT 1
          FROM provider_connections
          WHERE access_token LIKE 'enc:v1:%'
             OR refresh_token LIKE 'enc:v1:%'
             OR api_key LIKE 'enc:v1:%'
             OR id_token LIKE 'enc:v1:%'
          LIMIT 1
        `)
        .get();
      return !!row; // only true when confirmed
    } finally {
      db.close();
    }
  } catch (e) {
    // Fail closed: do not treat inspection failure as a safe state.
    throw new Error(`Unable to inspect existing database at ${dbPath}`);
    // Alternatively: return false only if callers interpret false as “block/require re-encryption”.
  }
}
```

Apply this standard anytime code makes a security decision based on reading/parsing sensitive material (DBs, token stores, config files, key material). If you’re changing security-critical logic, avoid bundling unrelated refactors that could increase runtime/module-loading risk during the fix.