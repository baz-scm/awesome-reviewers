---
title: Async state guards
description: 'Treat every async operation as potentially out-of-order: never let stale
  results overwrite newer state or cause duplicate side effects.


  Apply these rules:'
repository: cline/cline#v12
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70872
---

Treat every async operation as potentially out-of-order: never let stale results overwrite newer state or cause duplicate side effects.

Apply these rules:
1) Guard async->state writes with a monotonically increasing generation (or cancellation token)
- Increment a ref before starting the async work.
- After every await (or before each state write), verify the token/gen still matches; otherwise drop the result.
- Bump the same token on user transitions like “Sign Out”, switching accounts/orgs, changing selected runtime, or hiding/unmounting relevant UI.

2) Use in-flight locks for side-effectful async handlers
- If multiple UI paths can trigger the same async read/side effect (e.g., clipboard read + mouse + Ctrl+V), consolidate into one callback and add a single in-flight guard that returns early while the read is pending.
- Release the lock after a short settling window if needed to absorb rapid repeated triggers.

3) Make lifecycle boundaries concurrency-safe
- If UI “hide/show” keeps components mounted but pauses behavior, ensure cleanup correctly resets timers/flags so that returning to visible state re-arms scheduling.
- Don’t allow pending async work (promises/timers) to land into a hidden or logically “disposed” state—pair with generation checks.

Example (generation guard pattern):
```ts
const genRef = useRef(0);

const refresh = useCallback(async () => {
  const gen = ++genRef.current;
  setLoading(true);
  try {
    const data = await apiFetch();
    if (gen !== genRef.current) return; // stale
    setData(data);
  } finally {
    if (gen === genRef.current) setLoading(false);
  }
}, []);

// On transition that invalidates prior work
const onSignOut = useCallback(() => {
  genRef.current++; // bump so pending responses are dropped
  setSignedOut(true);
}, []);
```

Example (in-flight lock consolidation):
```ts
const inFlightRef = useRef(false);
const pasteFromClipboard = useCallback(async () => {
  if (inFlightRef.current) return;
  inFlightRef.current = true;
  try {
    const text = await readClipboard();
    if (!text) return;
    append(text);
  } finally {
    setTimeout(() => (inFlightRef.current = false), 100);
  }
}, []);

usePaste((e) => append(normalizePasteEventText(e)));
```