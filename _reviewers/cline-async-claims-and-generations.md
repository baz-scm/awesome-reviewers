---
title: Async Claims And Generations
description: 'When an async flow “resolves” shared state (answers a question, updates
  UI/model state, applies attach/detach replies, forwards terminal input, writes checkpoint
  hashes, etc.), treat concurrency as a first-class contract:'
repository: Cline/Cline
label: Concurrency
language: TypeScript
comments_count: 10
repository_stars: 70840
---

When an async flow “resolves” shared state (answers a question, updates UI/model state, applies attach/detach replies, forwards terminal input, writes checkpoint hashes, etc.), treat concurrency as a first-class contract:

1) **Claim synchronously before awaiting**
- The moment you decide “this async operation owns the outcome,” update the owning state/flag immediately—*before* any `await`—so a second submission can’t also “win” the same race.

2) **Validate staleness with generation/version tokens after awaits**
- Attach a `generation`/`attemptId`/`boundId`/`reasonVersion` to the operation.
- After every `await` (or in `finally` boundaries where appropriate), check that the operation is still the current owner before applying results.

3) **Avoid stacking handlers across retries**
- Register event listeners exactly once per resource, and route through tab/session state that is updated on spawn/start/exit. Retries should not add duplicate handlers.

Example pattern (claim + generation):
```ts
let pendingResolve: ((text: string) => void) | undefined;
let claimToken = 0;

async function resolvePending(prompt: string | undefined, deliver?: () => Promise<void>) {
  const resolve = pendingResolve;
  if (!resolve) return false;

  // Claim synchronously.
  const token = ++claimToken;
  pendingResolve = undefined;

  const text = prompt ?? "";
  if (deliver) {
    await deliver();
    if (token !== claimToken) return true; // still safe to return/route, but don’t apply/echo.
  }

  resolve(text);
  return true;
}
```

Apply these rules in your codebase for: pending-question resolution, bind/unbind of UI plugin slots, polling + forced refresh, terminal/session spawn/retry forwarding, checkpoint/hash writes that downstream UI depends on immediately, and cancellation-aware retries. The goal is: **no stale callback can apply to current state, and no two concurrent operations can both claim the same ownership.**