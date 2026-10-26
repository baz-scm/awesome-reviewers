---
title: Guard Against Stale Async
description: When async work can overlap (awaits, polling, event-triggered reads,
  or hidden/unhidden UI), ensure only the latest/current operation is allowed to commit
  side effects (React state, caches, localStorage, context writes, clipboard append,
  etc.).
repository: cline/cline#v29
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70893
---

When async work can overlap (awaits, polling, event-triggered reads, or hidden/unhidden UI), ensure only the latest/current operation is allowed to commit side effects (React state, caches, localStorage, context writes, clipboard append, etc.).

Practical rules:
1) Use a per-operation “generation” or “requestId”
- Capture the generation/requestId at start.
- After every await (or before every state write), verify that the operation is still the latest.
- On user actions that invalidate prior work (sign out, switching scope/root, new refresh, new directory path), increment/bump the generation.

2) Prefer “latest-wins” commits
- Don’t rely on closures alone—late responses must be explicitly checked.
- If polling is involved, don’t cancel or supersede slower operations in a way that prevents eventual completion.

3) Lock/dedupe duplicate async side effects
- If multiple UI paths can trigger the same async read (e.g., clipboard), add an in-flight guard so you don’t append twice.
- Release the guard shortly after the async settles (or when it’s provably safe) to prevent back-to-back duplicates.

4) Make hide/unmount cleanup concurrency-correct
- Clearing a timer/async scheduler must also reset any refs so future “show” paths re-arm correctly; otherwise pending flushes can stall.

5) Eliminate race-prone computed writes when possible
- Persist only user intent; resolve/compute derived values from authoritative state at render/commit time so late lookups can’t revert the user’s choice.

Example pattern (generation guard):
```ts
const genRef = useRef(0);

const refresh = useCallback(async () => {
  const myGen = ++genRef.current;
  setLoading(true);

  const result = await doAsync();
  if (myGen !== genRef.current) return; // drop stale result

  setLoading(false);
  setData(result);
}, []);

// Invalidation action
const signOut = useCallback(() => {
  genRef.current++; // bump to invalidate in-flight work
  setSignedOut(true);
}, []);
```

Example pattern (in-flight dedupe):
```ts
const pasteInFlightRef = useRef(false);

async function pasteFromClipboard() {
  if (pasteInFlightRef.current) return;
  pasteInFlightRef.current = true;

  try {
    const text = await readClipboardText();
    if (text) append(text);
  } finally {
    setTimeout(() => {
      pasteInFlightRef.current = false;
    }, 100);
  }
}
```