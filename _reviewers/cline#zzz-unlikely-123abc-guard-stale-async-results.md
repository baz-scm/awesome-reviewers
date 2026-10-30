---
title: Guard stale async results
description: Async operations (fetches, creates, polls, clipboard reads) can resolve
  out of order or after the state they were started for has moved on (a sign-out,
  a reset, a newer request, a user override). Applying such a stale result overwrites
  fresher state and reintroduces data the user already dismissed. Every async flow
  that writes to shared/mutable state must...
repository: cline/cline#zzz-unlikely-123abc
label: Concurrency
language: TSX
comments_count: 8
repository_stars: 71035
---

Async operations (fetches, creates, polls, clipboard reads) can resolve out of order or after the state they were started for has moved on (a sign-out, a reset, a newer request, a user override). Applying such a stale result overwrites fresher state and reintroduces data the user already dismissed. Every async flow that writes to shared/mutable state must protect against this:

1. Prefer eliminating the race class entirely: if a value can be derived/resolved synchronously from authoritative state instead of being written asynchronously, do that — a cached read is safe, a stale write is not.
2. Where an async write is unavoidable, tag each attempt with a generation/request id captured before the async work starts, and bump that counter whenever the relevant state is reset, cleared, or superseded. Check the captured id against the current counter immediately before every state mutation (not just once at the start) — a request can become stale partway through, after any `await`.
3. When multiple concurrent triggers can start the same operation (e.g. duplicate submits, duplicate clipboard reads, duplicate repository creates), use a single in-flight guard/shared promise so only one attempt runs and late or duplicate triggers no-op or reuse the pending result, rather than racing independent calls.
4. Write a regression test that reproduces the race (start operation A, trigger the invalidating action, resolve A late) and asserts the stale result was dropped.

Example pattern:
```ts
const generationRef = useRef(0);

function reset() {
  generationRef.current++;
  // clear state here
}

async function load() {
  const generation = generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) return; // stale, drop it
  applyResult(result);
}
```

This generation-token pattern (or an equivalent in-flight guard) should be the default whenever an async result is written back into shared state that can change before the async call settles.</description>
