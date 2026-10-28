---
title: Async staleness guards
description: Async operations (network calls, timers, polling, clipboard reads) can
  resolve out of order or be re-triggered while a previous call is still in flight.
  Across several bugs — a stale cloud-session creation reattaching after `/clear`,
  an account fetch overwriting state after sign-out, a directory listing overwriting
  a newer one, a reap running twice on...
repository: "cline/cline\t"
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70947
---

Async operations (network calls, timers, polling, clipboard reads) can resolve out of order or be re-triggered while a previous call is still in flight. Across several bugs — a stale cloud-session creation reattaching after `/clear`, an account fetch overwriting state after sign-out, a directory listing overwriting a newer one, a reap running twice on reconnect, and duplicate clipboard reads appending text twice — the root cause was always the same: an async result was applied to shared state without checking whether it was still valid or whether an equivalent operation was already running.

Apply two complementary guards whenever async work can outlive the context that started it or can be triggered concurrently:

1. **Generation/version tokens for staleness.** Capture a generation counter (or equivalent token) before starting the async call. Any action that invalidates the pending work (reset, cancel, sign-out, unmount) bumps the counter. After every `await`, check the token is unchanged *before* writing any state or side effect; if it changed, drop the result silently.

```ts
const generationRef = useRef(0);

function reset() {
  generationRef.current++; // invalidate anything in flight
  setState(initial);
}

async function load() {
  const generation = generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) return; // stale, discard
  setState(result);
}
```

2. **In-flight/memoized guards for deduplication.** When an operation could be started multiple times concurrently (rapid clicks, repeated effect runs, overlapping polls), store the pending promise (or a boolean ref) and have subsequent callers reuse it instead of starting a new one, releasing the guard only once the operation settles.

```ts
const pendingRef = useRef<Promise<T> | undefined>();

async function ensureLoaded() {
  pendingRef.current ??= doExpensiveWork();
  return pendingRef.current;
}
```

Use the staleness check for "did this already happen before applying this result" and the in-flight guard for "is this already happening." Add a regression test that creates the race explicitly (hold the old response, trigger the invalidating action, then resolve it) to assert the stale path is dropped and the duplicate path never re-runs.