---
title: Guard async state writes
description: 'When multiple async/event paths can overlap, ensure only the latest/allowed
  path can produce side effects.


  Apply these rules:

  1) Version your async work (generation/requestId)'
repository: cline/cline#v17
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70883
---

When multiple async/event paths can overlap, ensure only the latest/allowed path can produce side effects.

Apply these rules:
1) Version your async work (generation/requestId)
- Increment a counter before each async start.
- After every await, before any state write, verify the counter still matches.
- Ignore stale responses.

2) Use in-flight guards to prevent duplicate side effects
- When an action can trigger multiple async reads (clipboard, network), use a ref/flag to return early while a read is pending, and release after completion/settling.

3) Suspend competing handlers during critical flows
- If a user flow must be exclusive (e.g., recording keystrokes), temporarily suspend other listeners/handlers and ensure all relevant handlers check the suspension state.

4) Reset scheduling state on lifecycle/visibility changes
- In unmount/hide cleanup, clear timers and reset flags/refs so reshowing re-arms correctly.

5) Prefer storing intent over writing derived state after awaits
- Store minimal user choices; resolve derived fields from current state on render or from a fresh read, avoiding “write-back after await” races.

Example pattern (generation guard):
```ts
const genRef = useRef(0);

const refresh = useCallback(async () => {
  const gen = ++genRef.current;
  setLoading(true);
  const next = await fetchStatus();
  if (gen !== genRef.current) return; // stale
  setStatus(next);
  setLoading(false);
}, []);
```

Example pattern (in-flight dedupe):
```ts
const inFlightRef = useRef(false);
const pasteFromClipboard = useCallback(async () => {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await readClipboard();
    if (text) append(text);
  } finally {
    inFlightRef.current = false;
  }
}, [append]);
```