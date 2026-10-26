---
title: Discard stale async results
description: When multiple async operations can overlap (polls, refreshes, reads,
  clipboard/system fetches), ensure that only the latest (or still-relevant) operation
  is allowed to update state.
repository: cline/cline#v4
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70864
---

When multiple async operations can overlap (polls, refreshes, reads, clipboard/system fetches), ensure that only the latest (or still-relevant) operation is allowed to update state.

Practical rules:
1) Use generations/IDs for overlapping async calls
- Capture a monotonically increasing “generation” (global) or a per-key/per-path generation before each request.
- After every await, check that the generation/id still matches; otherwise, drop the response.
- Consider per-resource generations (e.g., per file path) so independent reads don’t block each other.

2) Single-flight guard for duplicate side effects
- If an action must be applied once (e.g., read clipboard and append text), use a ref/flag to return early while the async read is in-flight; release the guard after completion.

3) Cleanup must reset pending work
- When unmounting/hiding/remounting, clear timers/listeners and null out timer refs/flags so future mounts re-arm correctly.

4) Avoid late async writes that can contradict current user intent
- Prefer constraining writes to user-driven events.
- If background lookups must happen, treat them as reads and only write when the user’s current selection still allows it.

Example pattern (generation + per-key):
```ts
const genRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const k of keys) {
    genRef.current.set(k, (genRef.current.get(k) ?? 0) + 1);
  }
}

async function loadKey(key: string) {
  const gen = (genRef.current.get(key) ?? 0) + 1;
  genRef.current.set(key, gen);

  const result = await fetchSomething(key);

  // Drop stale response
  if ((genRef.current.get(key) ?? 0) !== gen) return;

  setState(prev => ({ ...prev, [key]: result }));
}
```

Adopting this approach prevents “late arrivals” from overwriting newer UI state, stops duplicate async side effects, and keeps behavior consistent under polling, StrictMode, and rapid user interaction.