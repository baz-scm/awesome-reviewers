---
title: Real Regression Tests
description: 'When you fix behavior (especially edge/boundary cases), add regression
  tests that are:

  - **Reachable** (not unexported/inaccessible without refactors that make them testable).'
repository: diegosouzapw/OmniRoute
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 33162
---

When you fix behavior (especially edge/boundary cases), add regression tests that are:
- **Reachable** (not unexported/inaccessible without refactors that make them testable).
- **Meaningful** (tests should fail when the buggy logic is restored, not merely “exercise” code).
- **Aligned with the repo’s runner** (use the framework actually used by the unit test script).
- **Supported by testable design** (prefer dependency injection over `as any` to control external effects).

Apply like this:
- If you add/adjust internal logic, make it testable (e.g., extract helpers or inject dependencies) so unit tests can target the exact behavior.
- For boundary bugs, include exact-limit cases and verify tests catch regressions.

Example (boundary regression + meaningful failure):
```ts
// Arrange
const LIMIT = 10;
// Restoring a buggy form should make this test fail.
function fixedAppend(current: string, next: string) {
  if (!next) return current;
  if (current.length >= LIMIT) {
    const keep = LIMIT > next.length ? LIMIT - next.length : 0;
    if (keep <= 0) return next.slice(-LIMIT);
    return current.slice(-keep) + next;
  }
  return current + next;
}

// Assert (exact boundary)
import test from "node:test";
import assert from "node:assert/strict";

test("appendBoundedText clamps at limit", () => {
  const cur = "x".repeat(LIMIT);
  const next = "y".repeat(LIMIT);
  assert.equal(fixedAppend(cur, next), next); // should be clamped
});
```

Also add guard assertions when you have rule systems/transform pipelines so that “no-op” rules (e.g., patterns that never change anything) can’t be introduced unnoticed.