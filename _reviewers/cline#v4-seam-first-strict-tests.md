---
title: Seam-First, Strict Tests
description: When writing tests, validate behavior/contracts through the correct seam
  instead of brittle internals, while keeping unit tests deterministic and assertions
  strict enough to catch missing correctness.
repository: cline/cline#v4
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 70864
---

When writing tests, validate behavior/contracts through the correct seam instead of brittle internals, while keeping unit tests deterministic and assertions strict enough to catch missing correctness.

Guidelines:
- Integration/wiring: Prefer “real adapter/real command output” tests that exercise the actual wiring/shape. Stub only external dependencies (e.g., network) at the boundary, not internal platform/process details.
  - Example pattern:
    - Drive `transcribeAudio` through the real adapter.
    - Stub `fetch` so the test still fails if the request path/body wiring is wrong.
- Unit tests: Stub the correct seam to avoid hanging/leaked listeners.
  - Don’t use never-ending streams or mocks that require extra teardown; stub the method whose behavior triggers the code path.
- Avoid masking: Don’t normalize away missing correctness in assertions (e.g., stripping plural suffixes) if that can let incorrect data pass.
  - Prefer assertions that require the full set of expected categories/groups.
- Avoid hardcoded “tag/range” expectations: If code exports a contract (versions/constants), test it against the source-of-truth metadata and require exact matches (e.g., `x.y.z`, not `latest`).

Result: tests become less brittle across OS/tooling, more reliable (no leaks/hangs), and better at detecting real regressions in wiring and correctness contracts.