---
title: Bounded, timeout-safe network calls
description: 'Every outbound network operation—fetches, downloads, remote commands—must
  be defensively bounded: enforce an explicit timeout/AbortSignal and a maximum size/data
  cap, and apply these to every code path, including fallback or secondary calls that
  are easy to overlook. Never trust server-declared metadata like `Content-Length`
  to bound memory use; instead...'
repository: cline/cline#`sleep 4`
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 70979
---

Every outbound network operation—fetches, downloads, remote commands—must be defensively bounded: enforce an explicit timeout/AbortSignal and a maximum size/data cap, and apply these to every code path, including fallback or secondary calls that are easy to overlook. Never trust server-declared metadata like `Content-Length` to bound memory use; instead check the running size incrementally while streaming and abort as soon as the limit is exceeded. Only fetch the minimum data needed for the current, confirmed action (e.g. don't pull full remote history just to preview unpublished commits) rather than eagerly pulling more than necessary. When a request times out or a connection looks unhealthy, don't assume failure and tear things down immediately—run a lightweight health probe (e.g. a cheap ping/list command) to confirm the connection is actually dead before resetting it or retrying, since blindly retrying a non-idempotent write risks duplicating work. For example, when downloading an archive:

```ts
// Don't trust Content-Length; check size as you stream.
const reader = response.body.getReader();
let total = 0;
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  total += value.length;
  if (total > maxArchiveBytes) {
    await reader.cancel();
    throw new Error("Archive exceeds size limit");
  }
}
```

and when issuing a fetch with a fallback path:

```ts
const response = await fetch(url, { signal: AbortSignal.timeout(5000) });
// Fallback must be bounded too, or a dropped-packet host hangs forever.
const fallback = await fetchModelIdsFromSource(url, { signal: AbortSignal.timeout(5000) });
```

Apply the same discipline to connection-level timeouts: before declaring a socket or SSH transport dead after a command timeout, probe it once rather than resetting on the first timeout, so in-flight writes aren't replayed against a connection that was actually still alive.</description>
