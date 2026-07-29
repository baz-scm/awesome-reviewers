---
title: Fail-Closed Security Invariants
description: Default to secure behavior when you can’t verify. If a security-relevant
  check (e.g., whether encrypted credentials exist) or its dependencies (e.g., DB
  access) fails, treat the state as unsafe and stop or require explicit recovery—never
  assume “nothing to decrypt.” Also, preserve cross-component encryption/decryption
  invariants (prefix/salt/format) so that...
repository: diegosouzapw/OmniRoute
label: Security
language: Other
comments_count: 3
repository_stars: 33162
---

Default to secure behavior when you can’t verify. If a security-relevant check (e.g., whether encrypted credentials exist) or its dependencies (e.g., DB access) fails, treat the state as unsafe and stop or require explicit recovery—never assume “nothing to decrypt.” Also, preserve cross-component encryption/decryption invariants (prefix/salt/format) so that verification/encryption remains compatible.

Apply it:
- Encryption format compatibility: keep the same prefix/salt/parameters across CLI and server/app decrypt paths, or migrate both sides together.
- Fail closed on inspection errors: when you inspect for encrypted secrets and the inspection fails, don’t generate new keys based on a “no encrypted creds” assumption.
- Scope filesystem/path security checks to the proven threat to prevent both bypasses and excessive false positives.

Example (fail-closed encrypted credential inspection):
```js
function hasEncryptedCredentials(dataDir) {
  const dbPath = join(dataDir, 'storage.sqlite');
  if (!existsSync(dbPath)) return false;

  try {
    const Database = require('better-sqlite3');
    const db = new Database(dbPath, { readonly: true, fileMustExist: true });
    try {
      const row = db.prepare(`
        SELECT 1
        FROM provider_connections
        WHERE access_token LIKE 'enc:v1:%'
           OR refresh_token LIKE 'enc:v1:%'
           OR api_key LIKE 'enc:v1:%'
           OR id_token LIKE 'enc:v1:%'
        LIMIT 1
      `).get();
      return !!row;
    } finally {
      db.close();
    }
  } catch {
    // Fail closed: treat inspection failure as unsafe/unknown
    throw new Error('Failed to inspect encrypted credentials; aborting setup/bootstrap.');
  }
}
```