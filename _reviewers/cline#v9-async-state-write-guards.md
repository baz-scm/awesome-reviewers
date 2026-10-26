---
title: Async state write guards
description: When an async operation can resolve out-of-order (or be triggered repeatedly),
  never write its result to state without proving it’s still the latest relevant request
  and still valid for the current UI/session.
repository: cline/cline#v9
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70868
---

When an async operation can resolve out-of-order (or be triggered repeatedly), never write its result to state without proving it’s still the latest relevant request and still valid for the current UI/session.

Apply these rules:
1) Generation/request-id gating for out-of-order responses
- For each async “refresh/load” that updates state, increment a generation/requestId and capture it.
- After each await, compare the captured value to the current one; return/skip if superseded.
- Optionally mark entries as stale while keeping the old view until re-read is safe.

2) In-flight locks for duplicate async side-effects
- For user actions that may trigger the same async read/effect twice (e.g., clipboard/system clipboard reads), use a single in-flight ref/flag.
- If in-flight, return early; clear the flag when the operation finishes (and/or after a short settling delay if needed).

3) Avoid stale closures when persisting derived selections
- If you must write after an async check, read the latest selection at write-time (e.g., via updater functions) rather than relying on captured props/state.
- Prefer storing the minimal user choice and resolving derived fields from the latest source-of-truth when possible.

4) Lifecycle cleanup must fully reset schedulers/flags
- When hiding/unmounting UI that uses timers/recording flags, cleanup should reset the relevant refs/flags so re-show/mount re-arms correctly (not stuck in “pending” state).

Example pattern (generation guard)
```ts
const genRef = useRef(0);
const load = useCallback(async () => {
  const gen = ++genRef.current;
  const result = await fetchSomething();
  if (gen !== genRef.current) return; // superseded
  setState(result);
}, []);
```
Example pattern (in-flight clipboard read)
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
}, []);
```

Checklist
- Does this async function update React (or app) state? If yes, can it resolve out-of-order? Add a generation/request-id guard.
- Can the user trigger the same async read twice quickly? Add an in-flight guard.
- Does the write depend on selection/props/state captured before an await? Use a write-time updater or re-derive from current source-of-truth.
- Does hide/unmount use timers/flags? Ensure cleanup resets refs/flags for correct re-entry.