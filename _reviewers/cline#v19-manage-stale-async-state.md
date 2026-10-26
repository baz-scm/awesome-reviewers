---
title: Manage Stale Async State
description: When multiple async operations can overlap (or UI can hide/unmount mid-flight),
  never let an older completion mutate current state. Use explicit “freshness” and
  lifecycle cleanup.
repository: cline/cline#v19
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70885
---

When multiple async operations can overlap (or UI can hide/unmount mid-flight), never let an older completion mutate current state. Use explicit “freshness” and lifecycle cleanup.

Standard:
1) Stale-response protection
- Assign each async request a generation/requestId (often per key) and, after every await, check that the response is still the latest before writing state.
- Prefer per-key generations for caches (e.g., directory listings keyed by path).
- Use current-state updaters (or refs) so async continuations don’t write using stale captured values.

2) Lifecycle reset for pending work
- If hiding/unmounting can cancel effects, ensure cleanup resets scheduling refs/timers and state flags so when the component becomes active again the needed async work is re-armed.

3) In-flight guards for event-triggered side effects
- For handlers that can be triggered repeatedly (click, Ctrl+V, context-menu), guard async reads/writes with an in-flight flag/ref so the same action can’t append/commit duplicates while a read is pending.

Example pattern (generation + post-await check + safe write):
```ts
const genRef = useRef(new Map<string, number>());
const bump = (key: string) => {
  genRef.current.set(key, (genRef.current.get(key) ?? 0) + 1);
};

async function load(key: string) {
  const myGen = (genRef.current.get(key) ?? 0) + 1;
  bump(key);

  const result = await fetchSomething(key);

  // Drop stale completion
  if ((genRef.current.get(key) ?? 0) !== myGen) return;

  setState((s) => ({ ...s, [key]: result }));
}
```

Applying this consistently prevents race conditions like “Sign Out still gets applied”, “older directory listing overwrites newer”, “stream text never flushes after restore”, and “duplicate clipboard appends” across the app.