---
title: Guard async hook results against staleness
description: When a hook or callback performs an async operation (an API/sidecar invoke,
  a debounced fetch, a promise returned from a prop callback), component state can
  change before the result resolves — the user can navigate away, remount the component,
  change files/drafts, or start a newer request. Applying a stale result as if it
  were current causes subtle bugs:...
repository: cline/cline#"><b>zze3729958
label: React
language: TypeScript
comments_count: 4
repository_stars: 71067
---

When a hook or callback performs an async operation (an API/sidecar invoke, a debounced fetch, a promise returned from a prop callback), component state can change before the result resolves — the user can navigate away, remount the component, change files/drafts, or start a newer request. Applying a stale result as if it were current causes subtle bugs: overwriting a newer draft with an old one, sending files that were removed (or dropping files added) during the wait, treating an old fetch as "current" for a new turn, etc.

To avoid this, follow two complementary rules whenever a hook kicks off async work:

1. Snapshot the state you need at call time rather than re-reading mutable refs/state after the `await`. If the action depends on "what's attached/selected/typed right now", capture it before firing the request, and only use that snapshot (or a value derived from it, like `takeFiles(wanted)`) once the result lands.
2. Before applying an async result, validate that it is still relevant: bump a generation/request counter (or compare an id/key) when the owning state (session id, thread id, request params) changes, and discard replies whose generation no longer matches. Likewise, any cache/dependency key used to decide "is this result still current" must include every input that invalidates it (e.g. include message counts, not just tool-call counts, when that's the condition for "a new turn happened").

Example pattern:
```ts
const generationRef = useRef(0);

useEffect(() => {
  const generation = ++generationRef.current;
  void (async () => {
    const result = await invoke(action);
    if (generation !== generationRef.current) return; // stale, discard
    applyResult(result);
  })();
}, [deps]);
```

This pattern — snapshot-then-validate — should be applied consistently to any hook that fires an async request and later writes back into shared state (refs, context, external maps/caches). Without it, retired instances or superseded requests can silently clobber newer state after the user has already moved on.