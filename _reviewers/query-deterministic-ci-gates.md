---
title: Deterministic CI Gates
description: 'Ensure CI/CD is deterministic and comprehensive: pin versions when dependencies/tooling
  have drifted, make the same checks run on PRs as on main, and test against the full
  supported toolchain/version range.'
repository: tanstack/query
label: CI/CD
language: Json
comments_count: 3
repository_stars: 49380
---

Ensure CI/CD is deterministic and comprehensive: pin versions when dependencies/tooling have drifted, make the same checks run on PRs as on main, and test against the full supported toolchain/version range.

Apply it like this:
- Pin fixed versions for dependencies that already jumped majors and can’t be realigned (this restores predictable builds).
- Don’t let critical checks run only on main—add/enable equivalent tasks in PR workflows so failures are caught before merge.
- If you support multiple TypeScript versions, run a CI matrix (e.g., TS 4.7 + newer) and avoid using language/library features in code paths that won’t compile on older versions.

Example (dependency pinning in a changeset-style config):
```json
{
  "fixed": [
    ["@some/package", "@some/other-package"],
    ["@some/devtools"],
    ["@some/svelte", "@some/svelte-devtools"]
  ]
}
```

Example (CI parity idea): if a quality check (e.g., `sherif`) isn’t running on PRs, add it to the PR workflow (or add equivalent tasks like formatting/lint scanning) so the same gates apply before merge.

Example (TypeScript compatibility): add a CI job per supported TS version (TS 4.7, TS 5.x) to prevent breaks when developers or tooling target different TypeScript releases.