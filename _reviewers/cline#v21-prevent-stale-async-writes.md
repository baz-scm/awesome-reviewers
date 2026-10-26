---
title: Prevent Stale Async Writes
description: 'When async work can complete out of order (or after UI/account state
  changes), never let it blindly update state. Instead:


  - Use a per-operation “generation” or requestId, and check it immediately before
  *every* state write after an await.'
repository: cline/cline#v21
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70886
---

When async work can complete out of order (or after UI/account state changes), never let it blindly update state. Instead:

- Use a per-operation “generation” or requestId, and check it immediately before *every* state write after an await.
- Bump/invalidate the generation on relevant transitions (e.g., sign out, switching targets, hiding/unmounting) so late results are dropped.
- Ensure cleanup fully resets timers/refs so a later remount can re-arm work.
- For user-triggered async side effects (clipboard/network reads), add an in-flight guard so repeated events can’t duplicate effects.
- If possible, avoid writing derived selection state from async lookups; make lookups read-only and resolve current choices from authoritative state.

Example pattern (generation-based stale-drop):

```ts
const genRef = useRef(0);

useEffect(() => {
  // Invalidate prior in-flight work on transition
  genRef.current += 1;
}, [criticalState]);

async function load() {
  const myGen = genRef.current;
  const result = await fetchSomething();
  if (myGen !== genRef.current) return; // drop stale response
  setState(result); // safe: only the latest generation writes
}
```

Example pattern (in-flight guard for repeated triggers):

```ts
const inFlightRef = useRef(false);

const doOncePerBurst = useCallback(async () => {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const data = await readClipboard();
    append(data);
  } finally {
    // Release after settling to absorb rapid repeated events
    setTimeout(() => { inFlightRef.current = false; }, 100);
  }
}, []);
```

Adopting these rules prevents race conditions like “late async overwrites current state”, “stale results rehydrate signed-out data”, “timers never re-arm after hide”, and “duplicate side effects from multiple rapid inputs.”