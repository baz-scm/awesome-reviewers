---
title: Thorough, resilient test coverage
description: Write tests that cover edge cases and realistic variations, not just
  the simplest happy path. For example, when testing a SQL validation rule for forbidden
  columns, also test wildcard selects (`SELECT * FROM request_response_rmt`) and nested/sub-queries,
  since these are common ways the restriction could be bypassed. Likewise, avoid encoding
  test assertions...
repository: Helicone/helicone
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 6248
---

Write tests that cover edge cases and realistic variations, not just the simplest happy path. For example, when testing a SQL validation rule for forbidden columns, also test wildcard selects (`SELECT * FROM request_response_rmt`) and nested/sub-queries, since these are common ways the restriction could be bypassed. Likewise, avoid encoding test assertions around behavior that is explicitly expected to change soon (e.g., asserting a specific "default provider" when more providers are about to be added) — such tests become misleading or flaky almost immediately; either remove them, mark them clearly as temporary, or assert on the stable invariant instead of the volatile implementation detail. Finally, keep test code itself maintainable: use explicit, stricter types for test helper parameters and return values (avoid `any`) so test utilities stay reliable and easy to refactor as the suite grows.