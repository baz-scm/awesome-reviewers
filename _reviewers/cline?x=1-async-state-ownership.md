---
title: Async State Ownership
description: 'When multiple async operations can overlap, shared state must be protected
  by explicit ownership and ordering. Concretely:


  - **Claim before awaiting**: if a call will eventually resolve/commit shared state,
  assign an `attempt/generation` immediately (synchronously) and only apply results
  if the attempt is still current.'
repository: cline/cline?x=1
label: Concurrency
language: TypeScript
comments_count: 8
repository_stars: 70861
---

When multiple async operations can overlap, shared state must be protected by explicit ownership and ordering. Concretely:

- **Claim before awaiting**: if a call will eventually resolve/commit shared state, assign an `attempt/generation` immediately (synchronously) and only apply results if the attempt is still current.
- **Serialize per entity**: for mutations that must land in a specific order (e.g., teardown terminal status), chain/queue writes per key (sessionId/taskId) so “late” work can’t overwrite newer/terminal states.
- **Coalesce in-flight work**: polling/refresh should *join* the in-flight read and then apply results in order, rather than starting a superseding read that can return stale data.
- **Make persistence TOCTOU-safe**: delete/update based on earlier observations using **atomic rename + unlink-if-unchanged** (or CAS-like checks) so concurrent writers can’t be lost.
- **Validate “current” targets**: before acting (send/attach/route), confirm the target is still connected/attached/live; otherwise fail fast (and consider deadlines).

Example pattern (claim-before-await + generation gate):

```ts
let generation = 0;

async function resolveSharedState({ prompt }: { prompt: string }) {
  const myGen = ++generation; // claim synchronously
  const result = await prepareAttachmentsOrData(); // overlaps allowed

  // Only apply if still current for this logical entity
  if (myGen !== generation) return false;
  commitSharedState(result, { prompt });
  return true;
}

// Example usage: a second submission during prepare becomes a follow-up
// and cannot steal/resolve the same pending question.
```

Checklist for the codebase:
1) Any code that does `await ...; sharedState = ...` for the same logical entity must also do either (a) **generation/attempt gating**, or (b) **per-key serialization**, or (c) both.
2) Any “delete-if-old” or “update-if-then” persistence must use atomic compare semantics, not separate read/stat/unlink steps with awaits in between.
3) Any retry/poll loop must join/coalesce in-flight operations and be cancellation/timeout-aware so it doesn’t leak late effects.
