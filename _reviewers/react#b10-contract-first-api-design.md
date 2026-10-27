---
title: Contract-first API Design
description: Design and evolve public or cross-environment APIs so that (1) misuse
  is detected early, (2) call shapes match the intended external contract/schema,
  and (3) semantics/constants/types are correct and unambiguous.
repository: facebook/react#b10
label: API
language: JavaScript
comments_count: 4
repository_stars: 251894
---

Design and evolve public or cross-environment APIs so that (1) misuse is detected early, (2) call shapes match the intended external contract/schema, and (3) semantics/constants/types are correct and unambiguous.

Apply this standard:
- Fail fast for environment boundaries: If an API is server-only, don’t export client-tolerant no-ops. Prefer making client imports error (build/runtime) so incorrect usage is obvious.
- Schema-aligned interfaces: For public tools/APIs, prefer an options bag / object parameter whose keys match the schema (avoid positional arguments that encourage drift).
- Verify semantic/protocol details: Ensure constants/values map exactly to the platform spec (e.g., correct `rel` values for preload: use `style`, not `stylesheet`).
- Encode intent in types: Use correct generic variance annotations so type relationships match how the API is actually meant to be used.

Example patterns:
- Schema-aligned call shape:
  ```js
  // Prefer:
  getComponentByUid({uid, includeHooks}); // keys match schema

  // Over:
  getComponentByUid(uid, includeHooks); // harder to keep stable
  ```
- Fail-fast boundary (conceptual):
  ```js
  // If imported in a client context, throw or make the import invalid
  if (isClient()) {
    throw new Error('create*Ledger is server-only');
  }
  ```