---
title: Prevent Stale Cache Writes
description: Async fetches/cached reads must not overwrite newer state. Correlate
  every async response to the cache epoch (generation/requestId) and apply it only
  if it still matches the latest epoch; bump the epoch whenever you invalidate/drop
  the cache entry.
repository: cline/cline#v23
label: Caching
language: TSX
comments_count: 3
repository_stars: 70889
---

Async fetches/cached reads must not overwrite newer state. Correlate every async response to the cache epoch (generation/requestId) and apply it only if it still matches the latest epoch; bump the epoch whenever you invalidate/drop the cache entry.

Also, don’t “refresh” stable configuration on unrelated lifecycle events—initialize once per app/component lifetime when the environment/account is fixed, and only retry initial lookups on reconnect failures.

Finally, separate user intent from derived/suggested state: treat late-arriving lookups as read-only suggestions and ensure they can’t revert an explicit user choice.

Example pattern:
```ts
const genRef = useRef(0);
const load = useCallback(async (key: string) => {
  const gen = ++genRef.current; // or gen per key/path
  setState(s => ({...s, [key]: {loading:true}}));
  try {
    const res = await fetchSomething(key);
    if (gen !== genRef.current) return; // discard stale
    setState(s => ({...s, [key]: {data: res, loading:false}}));
  } catch (e) {
    if (gen !== genRef.current) return;
    setState(s => ({...s, [key]: {error: String(e), loading:false}}));
  }
}, []);
```