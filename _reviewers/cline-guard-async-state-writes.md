---
title: Guard Async State Writes
description: When async work can overlap (awaits, polls, UI hide/show, user changes),
  never commit results blindly. Instead, make every async side-effect either (a) versioned
  (generation) or (b) in-flight locked—or remove the stale write path entirely.
repository: Cline/Cline
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70840
---

When async work can overlap (awaits, polls, UI hide/show, user changes), never commit results blindly. Instead, make every async side-effect either (a) versioned (generation) or (b) in-flight locked—or remove the stale write path entirely.

Apply these rules:
1) Generation-gate state updates
- For each logical request type (refresh, directory listing, overview fetch), increment a generation before starting.
- After every await, only apply results if the generation still matches.
- Also invalidate on user actions that “supersede” prior work (e.g., Sign Out, runtime switch).

2) In-flight lock for duplicate entry points
- If multiple UI events can trigger the same async operation (right/middle click + Ctrl+V), share one callback and guard with a ref/lock.
- Clear the lock when the async settles (and/or after a short delay if needed to debounce event bursts).

3) Prefer restructuring to avoid stale writes
- Store only user intent (what the user selected) and recompute derived state from current sources on each render/state change.
- This prevents late lookups from “flipping” the UI back.

4) Reset timers/flags on visibility/mode transitions
- If a component is hidden/restored without true unmount, ensure async timers/flags are correctly canceled or reset so resumed behavior restarts cleanly.

Example (generation-gated async update):
```ts
const genRef = useRef(0);

const refresh = useCallback(async () => {
  const gen = ++genRef.current;
  try {
    const result = await desktopClient.invoke("some_call", {/* ... */});

    // Drop stale responses
    if (gen !== genRef.current) return;

    // Safe to commit
    setState(result);
  } catch (e) {
    if (gen !== genRef.current) return;
    setError(String(e));
  }
}, []);
```

Example (in-flight guard):
```ts
const inFlightRef = useRef(false);

const doPaste = useCallback(async (source: () => Promise<string | null>) => {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await source();
    if (!text) return;
    setText((prev) => prev + text);
  } finally {
    inFlightRef.current = false;
  }
}, []);
```

Adopting these patterns will prevent out-of-order async responses from corrupting UI state, stop duplicate side effects, and make behavior robust under rapid user interactions and overlapping background work.