---
title: Guard state across await boundaries
description: 'Any time execution resumes after an `await`, the world may have moved
  on: a newer request arrived, the resource was replaced or disposed, a flag like
  "shutting down" flipped, or another caller already claimed the same work. Code that
  applies a result, mutates shared state, or performs a destructive side effect must
  re-validate that it is still the operation...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Concurrency
language: TypeScript
comments_count: 22
repository_stars: 70986
---

Any time execution resumes after an `await`, the world may have moved on: a newer request arrived, the resource was replaced or disposed, a flag like "shutting down" flipped, or another caller already claimed the same work. Code that applies a result, mutates shared state, or performs a destructive side effect must re-validate that it is still the operation that should win — checking only once at entry is not enough, because any `await` in between is a window for a competing operation to interleave.

Apply these complementary techniques:

1. **Stamp and compare a generation/epoch before committing.** Capture a counter (or the exact object/instance reference) before starting async work, and compare it again immediately before applying the result. If it moved, discard the stale result silently instead of overwriting newer state.

```ts
async function bind(sessionId: string) {
  generation += 1;
  const myGeneration = generation;
  const states = await fetchStates(sessionId);
  if (myGeneration !== generation) return; // a newer bind/unbind superseded this
  applyStates(states);
}
```

2. **Claim shared mutable state synchronously, before the first `await`.** When an operation must have exclusive ownership of something (resolving a pending promise, answering a pending question, replacing a resident session), mark it claimed/consumed up front so a concurrent caller sees it unavailable and takes the fallback path, rather than both racing to complete the same thing.

```ts
const resolve = pendingResolve
if (!resolve) return false
pendingResolve = undefined // claimed before any await; a second caller now follows up instead
await deliverAttachments()
resolve(responseText)
```

3. **Re-check teardown/cancellation flags right before the mutation, not just at function entry.** A `shuttingDown`/`disposed`/`cancelled` check performed before a series of `await`s does not protect writes that happen after them; re-check immediately prior to any write that must not happen post-teardown.

4. **When replacing a live resource under the same identity, build the replacement fully before releasing the original, and only release the original once you can confirm it was actually displaced** (e.g., `registry.get(id) !== original`). This avoids both a window where the identity resolves to nothing, and releasing a resource that a failed rebuild never got to replace.

Cover these races in tests by holding one async step open (a blocked fetch/stat/connect) while triggering the competing operation, and asserting the stale path is a no-op.