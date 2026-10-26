---
title: Async Ownership and Ordering
description: When multiple async operations can overlap (timeouts, retries, reconnects,
  replacements, or UI callbacks), enforce ownership and ordering so late completions
  can’t corrupt state.
repository: cline/cline#v23
label: Concurrency
language: TypeScript
comments_count: 9
repository_stars: 70889
---

When multiple async operations can overlap (timeouts, retries, reconnects, replacements, or UI callbacks), enforce ownership and ordering so late completions can’t corrupt state.

Standards:
1) Claim/advance synchronously before awaiting
- If a handler resolves a “pending” item (question, promise, request), take the state (clear/mark) before any await.
- Any second submission must fall through to a follow-up path instead of resolving the same pending item.

2) Use generation/version tokens for supersession
- Tag work with a monotonic token (e.g., per session, per request, per lifecycle generation).
- Before applying results, verify the token still matches the current owner; otherwise discard.

3) Serialize dependent side-effects / writes
- For logically ordered updates (status, teardown vs in-flight), chain writes through a per-resource queue or equivalent serialization.

4) Clean up late in-flight operations
- If you time out or “give up,” ensure that late completions are neutralized (disconnect after connect resolves, remove listeners/pipes, don’t let retries drain unattended, etc.).

5) Preserve data-availability contracts
- Don’t background work if callers (or later steps) rely on the result being present before proceeding; otherwise UI flags and invariants can break.

Example: claim-before-await + generation guard
```ts
let pendingResolve: ((text: string) => void) | undefined;
let currentGeneration = 0;

async function resolveAsk(input: {
  prompt?: string;
  images?: string[];
  files?: string[];
}) {
  const generation = currentGeneration;

  // 1) Claim synchronously
  const resolve = pendingResolve;
  if (!resolve) return false;
  pendingResolve = undefined;

  const hasAttachments = !!(input.images?.length || input.files?.length);

  // 2) Await delivery (late second call can’t resolve the same pending)
  if (hasAttachments) {
    await deliverAttachments({
      // 2a) optional stale check
      isCurrent: () => generation === currentGeneration,
      images: input.images,
      files: input.files,
    });
  }

  // 3) Apply only if still current
  if (generation !== currentGeneration) return true;
  options.setTurnPhase?.('streaming');
  resolve(input.prompt ?? '');
  return true;
}
```

Apply this checklist to:
- request/response handlers (ask questions, capability callbacks)
- reconnection/refresh flows (seed reads, upcoming schedules)
- teardown vs in-flight operations (session status, runtime release)
- timeout paths (disconnect/close/cleanup)
- background work that must satisfy an immediate downstream invariant (checkpoint hash, etc.)