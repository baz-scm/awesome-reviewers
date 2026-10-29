---
title: Guard stale async updates
description: When kicking off async work (network calls, subprocess polling, clipboard
  reads) whose result will later mutate shared state, protect against races caused
  by out-of-order completion or duplicate concurrent invocations before applying that
  result.
repository: cline/cline#1
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 71024
---

When kicking off async work (network calls, subprocess polling, clipboard reads) whose result will later mutate shared state, protect against races caused by out-of-order completion or duplicate concurrent invocations before applying that result.

For "stale response" races (a newer request should win over an older one that resolves later), capture a generation/version token before starting the async call, and re-check it immediately before every state write after each await. Bump the token whenever the context changes in a way that invalidates in-flight requests (e.g. user clears state, signs out, switches selection). If the token no longer matches, drop the result silently instead of applying it.

```ts
const generationRef = useRef(0);

async function refresh() {
  const generation = ++generationRef.current;
  const result = await fetchStatus();
  if (generation !== generationRef.current) return; // superseded, drop it
  setStatus(result);
}

function invalidate() {
  generationRef.current++; // any in-flight refresh is now stale
}
```

For per-key caches (e.g. file/directory listings keyed by path), keep a generation map per key instead of a single ref, and only invalidate the entries that actually changed—avoid cancelling unrelated in-flight work.

For "duplicate invocation" races (the same async action fired twice before the first completes, e.g. rapid paste clicks), use a simple in-flight guard/mutex: return early if a call is already pending, and release the guard only after the call settles (with a short delay if the side effect, like a clipboard read, can lag the UI event).

Add a regression test that simulates the race directly: start a second async call, resolve the first one late with stale data, and assert the stale result was dropped and the final state matches the latest request.