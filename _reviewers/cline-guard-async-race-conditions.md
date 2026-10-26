---
title: Guard async race conditions
description: 'Async operations whose results feed into shared state (account data,
  caches, UI lists, polling) can resolve out of order, or after the context that started
  them is no longer valid (sign-out, switched account/runtime, cache invalidation,
  a newer request). Guard against this with a generation/version counter rather than
  relying on cancellation alone:'
repository: cline/cline
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70886
---

Async operations whose results feed into shared state (account data, caches, UI lists, polling) can resolve out of order, or after the context that started them is no longer valid (sign-out, switched account/runtime, cache invalidation, a newer request). Guard against this with a generation/version counter rather than relying on cancellation alone:

1. Keep a counter (or map of counters keyed by resource, e.g. per file path) that is bumped whenever the underlying context changes or is invalidated (sign-out, refresh, cache clear, user switches selection).
2. Before starting an async operation, capture the current generation.
3. After *every* `await` in the operation — not just the final one — re-check the captured generation against the current value before committing any state write. If it no longer matches, discard the result silently.

```ts
const generationRef = useRef(0);

async function loadOverview() {
  const generation = ++generationRef.current;
  const data = await fetchOverview();
  if (generation !== generationRef.current) return; // superseded, drop it
  setOverview(data);
}

function signOut() {
  generationRef.current++; // invalidate any in-flight loadOverview
  setSignedOut(true);
}
```

For polling/refresh loops over multiple independent resources (e.g. per-directory listings), key the generation by resource id so an in-flight request for one path isn't cancelled by an unrelated refresh, and so a slow request (e.g. over SSH) isn't permanently starved — skip re-issuing a request for a resource that's still loading rather than invalidating it.

Separately, when an action can be triggered from multiple entry points (mouse paste, keyboard paste, button + hotkey), use a single shared handler with an in-flight guard (a ref/flag set at the start and cleared after the operation settles) to prevent duplicate concurrent execution producing duplicated side effects. Only add this guard where the action performs an async read/side effect — synchronous paths that get data inline don't need it.

Add a regression test that holds an older async call open, lets a newer one resolve first, then resolves the stale one and asserts the fresh state wins.