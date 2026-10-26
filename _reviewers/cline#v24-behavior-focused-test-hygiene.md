---
title: Behavior-Focused Test Hygiene
description: 'When adding or adjusting tests, aim for:

  - **Behavior over implementation**: Assert observable correctness (e.g., git behavior
  for literal filenames, correct parsing rules). Avoid brittle harness plumbing that
  depends on OS/process internals.'
repository: cline/cline#v24
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 70891
---

When adding or adjusting tests, aim for:
- **Behavior over implementation**: Assert observable correctness (e.g., git behavior for literal filenames, correct parsing rules). Avoid brittle harness plumbing that depends on OS/process internals.
- **Targeted edge cases**: Add or strengthen tests only when they prevent real correctness gaps (e.g., filenames that resemble globs; required CLDR plural cardinal categories).
- **Strict isolation & cleanup**: Stubs/mocks must not leak listeners, timers, never-ending streams, or global env changes across tests.
- **Avoid incidental detail assertions**: Don’t lock tests to log payload field names/formatting unless the payload shape is a contractual API; prefer existing coverage that already exercises the behavioral path.

Practical patterns:
- Use real-world outcomes instead of mocking deep internals when that would be platform-fragile.
- Stub environment variables using the framework’s scoped helpers and restore generically.

Example (scoped env stubbing + cleanup):
```ts
// Vitest
vi.stubEnv({ CL...: 'value' });
try {
  await runCommand();
} finally {
  vi.unstubAllEnvs(); // safe even if the var didn’t previously exist
}
```

Example (edge-case correctness test idea):
- When invoking git with user-provided paths, include a test for a literal filename that would otherwise be treated like a glob (e.g., `draft*.txt`) and verify the sibling file remains.

Checklist for any PR touching tests:
- Does the test validate user-visible behavior?
- Are new mocks/stubs scoped and cleaned up?
- Would this test require OS/process internals to pass?
- Is the test protecting against a real correctness regression (not just internal/log formatting)?