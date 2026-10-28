---
title: Guard stale async results
description: Async operations (fetches, creates, refreshes, clipboard reads) can resolve
  after the state they depend on has moved on — a sign-out, a reset, a newer request,
  or a second concurrent trigger. Applying their result blindly causes stale writes,
  duplicate side effects, or wrong reattachment (e.g. a cloud session created before
  `/clear` reattaching after the...
repository: cline/cline?x
label: Concurrency
language: TSX
comments_count: 8
repository_stars: 70983
---

Async operations (fetches, creates, refreshes, clipboard reads) can resolve after the state they depend on has moved on — a sign-out, a reset, a newer request, or a second concurrent trigger. Applying their result blindly causes stale writes, duplicate side effects, or wrong reattachment (e.g. a cloud session created before `/clear` reattaching after the clear, or a sign-out being overwritten by a late profile fetch).

Protect every async write to shared/component state with one of these patterns:

1. **Generation token**: before starting the async call, capture a monotonically increasing counter/ref. Bump the counter on any event that invalidates in-flight work (reset, sign-out, new request for the same resource). After the `await`, compare the captured value to the current counter before writing state or acting on the result; if it no longer matches, drop the result silently.

```ts
const generationRef = useRef(0);

function reset() {
  generationRef.current++;
}

async function load() {
  const generation = generationRef.current;
  const result = await fetchSomething();
  if (generation !== generationRef.current) return; // stale, discard
  applyResult(result);
}
```

2. **In-flight guard** for duplicate concurrent triggers of the same action (e.g. two input paths both reading the clipboard): use a single shared ref/promise so a second call while one is pending is a no-op or awaits the same result, rather than re-running and double-applying the effect.

3. **Serialize dependent async calls**: when multiple callers could kick off the same expensive operation (e.g. creating a session), have them share one in-flight promise instead of issuing multiple creates, and queue dependent actions to run only after the shared operation settles.

4. Prefer resolving derived values from current source-of-truth on every read (not caching a value that an async callback writes later) wherever feasible — this removes the race entirely instead of just mitigating it.

When fixing a race, add a regression test that artificially delays the async call, triggers the invalidating action, then resolves the delayed call — asserting the stale result was dropped and only the fresh state/effect remains.