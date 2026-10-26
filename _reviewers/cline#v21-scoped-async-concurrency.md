---
title: Scoped Async Concurrency
description: All async work that can outlive its caller (UI binds, sessions, hooks,
  background commits, refreshes, IPC/subprocess) must be (1) scoped to a validity
  token, (2) target-stable (capture the exact entity you intend to update before the
  first await), (3) serialized/merged when calls overlap, and (4) cleaned up on settle/unmount/abort
  so stragglers can’t apply...
repository: cline/cline#v21
label: Concurrency
language: TypeScript
comments_count: 9
repository_stars: 70886
---

All async work that can outlive its caller (UI binds, sessions, hooks, background commits, refreshes, IPC/subprocess) must be (1) scoped to a validity token, (2) target-stable (capture the exact entity you intend to update before the first await), (3) serialized/merged when calls overlap, and (4) cleaned up on settle/unmount/abort so stragglers can’t apply effects or keep resources alive.

Practical rules:
- **Reject stale results with a generation/token**: increment a token on each bind/unbind (or each scheduler replacement). Only apply async replies if the token still matches.
- **Claim shared resolution synchronously**: for “pending question/ask” or any one-shot resolution, set/clear the shared state before awaiting deliveries.
- **Capture the exact target before awaiting**: if you must run work in the background, capture the message id/index (or version) up-front; never “find the latest” later.
- **Serialize competing operations**: for refresh/tick/reads, use a single in-flight gate and merge additional requests into one rerun after the current read finishes.
- **Order-sensitive teardown**: if later code disposes/closes state, await the critical path that must run first.
- **Clean up resources on settle**: when an operation resolves, detach listeners and close/detach inherited resources (timers/stdio pipes) so background children can’t keep the host alive.

Example (generation token to avoid stale UI applying):
```ts
const generationRef = useRef(0);
const [state, setState] = useState(initial);

function bind(sessionId: string) {
  generationRef.current += 1;
  const gen = generationRef.current;

  void (async () => {
    const reply = await fetchState(sessionId);
    if (gen !== generationRef.current) return; // stale
    setState(reply);
  })();

  return () => {
    generationRef.current += 1; // invalidate inflight work
  };
}
```

Example (capture exact target before await):
```ts
await say("checkpoint_created");
const idx = findLastCheckpointCreatedIndex(); // capture synchronously
const commitHash = await checkpointTracker.commit();
if (commitHash) {
  await updateClineMessage(idx, { lastCheckpointHash: commitHash });
}
```

Following these rules prevents: out-of-order writes, late callbacks overwriting current state, overlapping resolutions that drop data, and “settled but still running” async/resource leaks.