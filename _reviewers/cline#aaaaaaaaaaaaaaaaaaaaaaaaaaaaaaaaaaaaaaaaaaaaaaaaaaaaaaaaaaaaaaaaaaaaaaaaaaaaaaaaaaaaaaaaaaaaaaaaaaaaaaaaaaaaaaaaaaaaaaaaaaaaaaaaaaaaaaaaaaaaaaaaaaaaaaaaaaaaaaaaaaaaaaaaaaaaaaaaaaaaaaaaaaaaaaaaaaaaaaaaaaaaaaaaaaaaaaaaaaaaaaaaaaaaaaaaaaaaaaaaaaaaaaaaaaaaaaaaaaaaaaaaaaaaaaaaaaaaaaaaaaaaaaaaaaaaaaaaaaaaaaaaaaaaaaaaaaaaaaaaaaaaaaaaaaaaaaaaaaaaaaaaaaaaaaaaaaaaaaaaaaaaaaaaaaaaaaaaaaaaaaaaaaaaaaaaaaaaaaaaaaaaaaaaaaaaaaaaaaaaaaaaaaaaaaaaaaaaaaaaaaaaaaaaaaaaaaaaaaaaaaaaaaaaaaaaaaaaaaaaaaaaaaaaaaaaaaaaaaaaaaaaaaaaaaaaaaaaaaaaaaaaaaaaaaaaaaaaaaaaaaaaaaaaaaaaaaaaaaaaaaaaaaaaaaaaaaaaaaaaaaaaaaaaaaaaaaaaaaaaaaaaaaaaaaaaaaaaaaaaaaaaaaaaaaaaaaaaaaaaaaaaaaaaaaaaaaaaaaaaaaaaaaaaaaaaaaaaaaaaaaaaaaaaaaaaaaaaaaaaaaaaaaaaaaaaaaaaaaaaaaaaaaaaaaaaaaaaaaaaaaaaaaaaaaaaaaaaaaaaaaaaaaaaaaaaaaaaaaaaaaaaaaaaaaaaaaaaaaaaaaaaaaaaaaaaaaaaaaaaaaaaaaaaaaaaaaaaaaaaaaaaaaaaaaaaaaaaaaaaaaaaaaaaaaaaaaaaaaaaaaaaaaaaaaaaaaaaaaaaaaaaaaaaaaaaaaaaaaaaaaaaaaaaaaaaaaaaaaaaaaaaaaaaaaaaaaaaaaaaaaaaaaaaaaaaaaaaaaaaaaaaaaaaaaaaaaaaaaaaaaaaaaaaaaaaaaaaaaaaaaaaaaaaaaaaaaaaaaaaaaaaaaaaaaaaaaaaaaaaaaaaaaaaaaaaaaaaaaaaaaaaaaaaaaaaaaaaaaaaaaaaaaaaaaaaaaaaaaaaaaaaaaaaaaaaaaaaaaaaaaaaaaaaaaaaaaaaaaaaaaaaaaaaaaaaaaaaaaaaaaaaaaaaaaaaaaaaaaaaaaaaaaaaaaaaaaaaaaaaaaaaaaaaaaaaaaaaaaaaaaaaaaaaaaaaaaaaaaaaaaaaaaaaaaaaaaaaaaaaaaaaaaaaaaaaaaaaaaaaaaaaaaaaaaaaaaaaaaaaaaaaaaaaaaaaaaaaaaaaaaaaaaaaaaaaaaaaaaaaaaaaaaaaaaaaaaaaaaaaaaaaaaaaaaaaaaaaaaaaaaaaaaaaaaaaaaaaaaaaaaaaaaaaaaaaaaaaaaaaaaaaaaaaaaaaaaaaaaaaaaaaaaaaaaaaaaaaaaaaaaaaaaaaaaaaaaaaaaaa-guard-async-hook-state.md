---
title: Guard async hook state
description: Hooks that kick off async work (invoke calls, promises, subscriptions,
  timers) must validate that the originating context is still current before applying
  the result or mutating shared state. Components can unmount, remount, navigate away
  and back, or rebind to a different session/thread while an async operation is in
  flight; without a staleness check, a...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: React
language: TypeScript
comments_count: 5
repository_stars: 70965
---

Hooks that kick off async work (invoke calls, promises, subscriptions, timers) must validate that the originating context is still current before applying the result or mutating shared state. Components can unmount, remount, navigate away and back, or rebind to a different session/thread while an async operation is in flight; without a staleness check, a late callback can silently overwrite newer state, duplicate an action, or re-apply an outdated condition.

Use a generation/version token (or an equivalent "still bound" check) captured at the start of the async call, and compare it before dispatching or writing shared state:

```ts
const generationRef = useRef(0);

useEffect(() => {
  generationRef.current += 1;
  const generation = generationRef.current;
  const boundId = sessionId;

  void (async () => {
    const result = await invokeSomething(boundId);
    if (generation !== generationRef.current) return; // stale reply, drop it
    dispatch({ type: "reply", result });
  })();
}, [sessionId]);
```

Apply the same discipline when:
- Restoring/undoing optimistic state after a failed async action (verify what was actually removed/sent rather than assuming success, and guard against a second concurrent invocation doing nothing or double-applying).
- Writing to state shared across remounted instances (e.g., a `Map` keyed by thread/session id) — validate against the current id/version rather than a retired instance's local ref before writing back.
- Composing derived booleans (e.g., loader/visibility conditions) that depend on both an async-acknowledged state and an optimistic/partial one — gate the combined condition explicitly at the point of composition instead of relying on one branch to always win, and add a test that exercises the actual race window (stale state + optimistic flag both present).

Add regression tests that reproduce the race (navigate away and back before the async call resolves, or trigger the partial-vs-full update ordering) to prove the guard actually prevents the stale write.