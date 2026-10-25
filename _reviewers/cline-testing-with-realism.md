---
title: Testing With Realism
description: 'When adding or updating tests, prefer realistic behavior checks over
  brittle mocks, keep them deterministic, and assert meaningful invariants.


  **Guidelines**'
repository: ClInE/cLiNe
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70838
---

When adding or updating tests, prefer realistic behavior checks over brittle mocks, keep them deterministic, and assert meaningful invariants.

**Guidelines**
- **Avoid fragile/platform-breaking plumbing:** If a mock would require shell wrappers or breaks on Windows, use the real underlying behavior (or an integration/smoke setup) instead.
- **Isolate the environment for “real” checks:** Run binaries with a temp HOME/data dir and explicitly set discovery/ports so parent-process config can’t affect results.
- **Reuse exported constants as source-of-truth:** Don’t hardcode values like package names/versions when the module already exports them; test should fail when the export changes.
- **Stub the right layer to prevent async leaks:** Ensure stubs don’t leave never-ending streams/listeners running past the test boundary.
- **Make helpers enforce real invariants:** Don’t write permissive utilities that let invalid data pass (e.g., stripping plural suffixes without validating required CLDR categories).
- **Assert behavior, not incidental internals:** Don’t write tests that tightly couple to log payload shape/field names unless you truly need that contract; rely on existing regression coverage for functional paths.

**Example pattern (isolated smoke test)**
```ts
const smokeHome = mkdtempSync(join(tmpdir(), "app-smoke-"));
const smokeEnv = {
  ...process.env,
  HOME: smokeHome,
  USERPROFILE: smokeHome,
  APP_DIR: join(smokeHome, ".app"),
  APP_DATA_DIR: join(smokeHome, "data"),
  APP_PORT: String(await findFreePort()),
};
// start the real binary and probe health using only smokeEnv
```