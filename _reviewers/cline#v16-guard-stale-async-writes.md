---
title: Guard Stale Async Writes
description: When async work can overlap, assume responses may arrive out of order.
  Only apply results that are still current, and ensure cleanup/reset so hidden/unmounted
  UI doesn’t leave stale timers/flags.
repository: cline/cline#v16
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70882
---

When async work can overlap, assume responses may arrive out of order. Only apply results that are still current, and ensure cleanup/reset so hidden/unmounted UI doesn’t leave stale timers/flags.

Standard:
1) Version every async request (generation/requestId). Increment before each start; capture the value; after every await, check it’s still the latest before any state write.
2) Invalidate on intent changes and lifecycle events: when the user signs out, changes selection, hides the app, or starts a new load, bump/invalidate generations so older responses are dropped.
3) Prefer “write user intent, derive everything else from current state.” Avoid persisting derived fields based on async lookups that may land after the user changed their mind.
4) For event handlers that may trigger multiple async reads (e.g., paste/clipboard), share a single guarded in-flight callback so repeated events can’t append duplicates.
5) On unmount/hide, cancel/clear timers and reset flags so when the component is shown again, new async flows start cleanly.

Example (generation guard):
```ts
const genRef = useRef(0);
const refresh = useCallback(async () => {
  const gen = ++genRef.current;
  setLoading(true);
  try {
    const next = await desktopClient.invoke("get_status");
    if (gen !== genRef.current) return; // stale
    setStatus(next);
  } finally {
    if (gen === genRef.current) setLoading(false);
  }
}, []);
```

Example (in-flight de-dupe):
```ts
const inFlight = useRef(false);
const pasteFromClipboard = useCallback(async () => {
  if (inFlight.current) return;
  inFlight.current = true;
  try {
    const text = await readClipboard();
    if (text) append(text);
  } finally {
    inFlight.current = false;
  }
}, []);
```