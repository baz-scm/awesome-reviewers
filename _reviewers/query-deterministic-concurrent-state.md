---
title: Deterministic Concurrent State
description: When code runs with concurrent rendering and async workflows, ensure
  any async/derived value that can affect what gets rendered (or how consumers behave)
  is deterministic per concurrent “world”, and make promise behavior explicit.
repository: tanstack/query
label: Concurrency
language: TSX
comments_count: 4
repository_stars: 49380
---

When code runs with concurrent rendering and async workflows, ensure any async/derived value that can affect what gets rendered (or how consumers behave) is deterministic per concurrent “world”, and make promise behavior explicit.

Apply these rules:
1) Don’t use refs for render-visible concurrency state
- If a mutable value is read by render (directly or via context consumers) to decide which queries/results are active, store it in state (or another render-consistent mechanism), not a mutable ref.
- This avoids cross-tree leakage where concurrent renders expect different values.

2) Make enable/disable transitions deterministic
- Define what should happen to in-flight work when `enabled` toggles (e.g., reuse the same promise, or deterministically reject when disabled).
- Add tests that assert the exact expected promise/reuse behavior.

3) Be explicit about awaiting vs fire-and-forget
- In tests or code paths where you intentionally don’t wait for an async operation, explicitly discard the promise:

```ts
void queryClient.resumePausedMutations()
```
- If you need completion ordering, await it intentionally.

4) Treat CI-only failures as race-condition signals
- If tests intermittently fail, suspect async timing/races.
- Stabilize tests by awaiting the right signals (not arbitrary delays) and ensuring promise lifecycle/enablement semantics are exercised deterministically.

These practices prevent incorrect hydration/selection during concurrent rendering, clarify async semantics, and reduce flaky test outcomes caused by nondeterministic scheduling.