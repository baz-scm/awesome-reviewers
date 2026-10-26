---
title: Avoid late async overwrites
description: When async operations overlap (polls vs actions, teardown vs lifecycle,
  retries vs cancellation), the default “last write wins” often breaks correctness.
  Enforce *ownership* and *ordering* so stale or late work cannot overwrite newer
  state.
repository: cline/cline#v14
label: Concurrency
language: TypeScript
comments_count: 10
repository_stars: 70876
---

When async operations overlap (polls vs actions, teardown vs lifecycle, retries vs cancellation), the default “last write wins” often breaks correctness. Enforce *ownership* and *ordering* so stale or late work cannot overwrite newer state.

Standards:
1) Serialize per entity when persisting shared state
- If multiple paths can update the same persisted field/status for the same entity, chain/queue writes per entity so teardown/dispose lands last.
- Example:
```ts
// per-entity write chain
const tail = new Map<string, Promise<void>>();
function enqueueStatusWrite(id: string, write: () => Promise<void>) {
  const prev = tail.get(id) ?? Promise.resolve();
  const next = prev.then(write).finally(() => {
    if (tail.get(id) === next) tail.delete(id);
  });
  tail.set(id, next);
  return next;
}
```

2) Use versioning/identity/claim-before-await for “single-shot” resolution
- If one request must be resolved exactly once (e.g., pending question, attachment delivery, offer serving), claim it *synchronously* before any `await`.
- Guard callbacks with a version/generation/revision token so late callbacks can’t re-become current.

3) Join in-flight work; don’t let later tasks silently supersede earlier reads
- Polling should join an in-flight read and/or queue exactly one fresh read behind it, so results don’t arrive out of order.

4) On timeout/cancellation, prevent late side effects and clean up resources
- If a timeout occurs, late completion must be discarded or reversed (e.g., disconnect after connect resolves after deadline).
- Ensure “settlement” (exit vs close, stream pumps) cancels/cleans listeners so background children/resources don’t keep the process alive or corrupt output.

5) Release/teardown must be conditional and idempotent
- When swapping/replacing resources (session runtime, host connections, sandboxes), only release the old resource if the slot still points to it; never assume the world stayed unchanged across awaits.

Practical checklist before approving a change:
- Can two async paths update the same entity/state concurrently?
- After an `await`, what guards prevent the resumed code from overwriting newer state?
- Are reads/writes joined/serialized, or can results arrive out of order?
- Do timeouts/cancels discard late outcomes and clean up listeners/resources?
- Does teardown/release use conditional/idempotent checks against the current owner/slot pointer?