---
title: Guard stale async state
description: Effects and callbacks that run after an `await` or a timer can fire after
  the component's state has moved on (a newer prop, a different selection, a reconnect).
  Relying on a closed-over value, or inferring "is this still relevant" from an indirect
  comparison (counts, diff sizes), lets a stale result overwrite a fresher one or
  trigger the wrong action. Guard...
repository: cline/cline#;sleep 4;
label: React
language: TSX
comments_count: 9
repository_stars: 70976
---

Effects and callbacks that run after an `await` or a timer can fire after the component's state has moved on (a newer prop, a different selection, a reconnect). Relying on a closed-over value, or inferring "is this still relevant" from an indirect comparison (counts, diff sizes), lets a stale result overwrite a fresher one or trigger the wrong action. Guard every async write with an explicit freshness check:

- Track freshness directly, not by proxy. Prefer an explicit flag/epoch that changes exactly when the meaningful event happens (a turn starting, a selection changing) over inferring it from side-effects like message counts or diff totals, which can coincide for unrelated reasons.
- When multiple async operations can race for the same key (a file read, a directory listing, a branch lookup), bump a per-key generation counter before issuing the request and check it still matches when the response lands; drop the response if it doesn't.
```ts
const generation = (readGenerationRef.current.get(key) ?? 0) + 1;
readGenerationRef.current.set(key, generation);
const isCurrent = () => readGenerationRef.current.get(key) === generation;
...
fetchData(key).then((result) => {
  if (!isCurrent()) return;
  setState(result);
});
```
- Read current values through a ref instead of a closed-over variable when a callback can run after an await and the user may have changed something in the meantime (which folders are expanded, which repo/branch is selected). Update the ref on every render or state change, and dereference it at the point of use, not at the point the async call was started.
- When persisting a derived value asynchronously, write with a functional updater that reads the current state at commit time (`persist((current) => ...)`), so a write that resolves after the user already changed their choice doesn't clobber it. Prefer resolving derived values from the single source of truth instead of computing and storing them in multiple places that can drift out of sync.
- Prefer a single "is this data current" flag over comparing counters that can match by coincidence (e.g. compare a monotonically increasing epoch rather than a run count that can repeat across turns).

Add a regression test that reproduces the race (start the async operation, change the relevant state, let the operation resolve, assert the stale result was discarded) whenever you fix this class of bug.