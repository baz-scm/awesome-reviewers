---
title: Stale Async State Writes
description: 'When async work can complete out-of-order (or be triggered repeatedly),
  never let its completion directly mutate shared state. Instead:


  1) Gate state writes by “latest intent”'
repository: cline/cline#v27
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70892
---

When async work can complete out-of-order (or be triggered repeatedly), never let its completion directly mutate shared state. Instead:

1) Gate state writes by “latest intent”
- Use a per-key generation/sequence number (or active token) and check it after every await, immediately before any state/localStorage write.
- Bump/invalidate the generation on any user action that supersedes prior work (e.g., Sign Out, changing the selected repo/directory).

2) Clean up schedulers and reset refs on hide/unmount
- If you pause/unmount UI (or suspend effects), ensure timers/queued work are cleared and the controlling ref is reset so the next mount/restore can re-arm correctly.

3) Prevent duplicate async triggers
- Use a single shared in-flight guard for async reads that could be invoked rapidly (multiple clicks, repeated paste triggers). Return early while pending; release after settling.

4) Prefer design that avoids stale writes
- If possible, avoid persisting derived/lookup-driven state from async responses. Persist only user choices, and resolve derived values from current state snapshots.

Example (React/TS) pattern with per-key generation:
```ts
const genRef = useRef(new Map<string, number>());
const invalidate = (key: string) => {
  genRef.current.set(key, (genRef.current.get(key) ?? 0) + 1);
};

async function load(key: string) {
  const myGen = (genRef.current.get(key) ?? 0) + 1;
  genRef.current.set(key, myGen);

  setLoading(true);
  const result = await fetchSomething(key);

  // Gate the write: only the latest completion may mutate state
  if ((genRef.current.get(key) ?? 0) !== myGen) return;
  setState(result);
  setLoading(false);
}

function onSupersedingAction() {
  invalidate("same-key-as-load"); // drops in-flight completions
}
```
Apply this standard to async effects, polling, and clipboard/IO handlers—especially when actions like sign-out, selection changes, panel hiding, or rapid user inputs can occur while requests are in-flight.