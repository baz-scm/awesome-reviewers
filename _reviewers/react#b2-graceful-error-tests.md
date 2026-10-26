---
title: Graceful error tests
description: Adopt error-handling behavior that (1) avoids throwing when the decision
  depends on unknown runtime side effects, and (2) uses runtime-executable fixtures
  so tests validate the real failure mode.
repository: facebook/react#b2
label: Error Handling
language: Markdown
comments_count: 2
repository_stars: 251882
---

Adopt error-handling behavior that (1) avoids throwing when the decision depends on unknown runtime side effects, and (2) uses runtime-executable fixtures so tests validate the real failure mode.

How to apply:
- When encountering uncertain conditions (e.g., a global function call inside an effect where you can’t know whether it triggers state updates), choose a graceful fallback instead of throwing. Treat this as a “best-effort”/degrade-without-exception policy.
- For tests that cover error paths or special-case behavior, ensure any referenced symbols are real runtime implementations (not type-only declarations). Otherwise, failures like `X is not defined` will mask the behavior you intended to test.

Example (runtime-verifiable fixture):
```ts
declare function id<T>(x: T): T; // ❌ type-only; runtime may fail

function id<T>(x: T): T {      // ✅ runtime implementation
  return x;
}

export function test<T = string>(value = id<string>("hi")) {
  return value;
}
```

Outcome: fewer spurious exceptions in uncertain scenarios and error-handling tests that reliably reflect what will happen in production.