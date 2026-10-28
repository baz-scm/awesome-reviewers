---
title: Guard async hook state races
description: 'Hooks that kick off async work (invoking a backend verb, sending a prompt,
  waiting on an attachment list) must assume the component, binding, or external state
  can change before that work resolves: the user may navigate away and back, rebind
  to a new session, or mutate a ref the async call depends on. Applying a stale result
  or reading a mutable ref after...'
repository: cline/cline#&&sleep 4
label: React
language: TypeScript
comments_count: 5
repository_stars: 70980
---

Hooks that kick off async work (invoking a backend verb, sending a prompt, waiting on an attachment list) must assume the component, binding, or external state can change before that work resolves: the user may navigate away and back, rebind to a new session, or mutate a ref the async call depends on. Applying a stale result or reading a mutable ref after the fact silently corrupts state.

Apply two complementary techniques:

1. **Generation/identity guards.** Bump a monotonic counter (or capture the current bound ID) when starting the async call, and before dispatching its result, re-check that the counter/ID is unchanged. If it changed, drop the result instead of applying it.

```ts
const generationRef = useRef(0);

async function invoke(action: Action) {
  const generation = ++generationRef.current;
  const targetId = boundRef.current;
  const result = await callApi(targetId, action);
  if (generation !== generationRef.current) return; // stale, drop it
  dispatch({ type: "reply", result });
}
```

2. **Snapshot values at call time, not at resolution time.** If an async action depends on external, mutable state (attached files, a draft, a queued prompt), capture what you need before awaiting, and act on that snapshot — not on a ref re-read after the `await`, which may belong to a retired instance or reflect a newer, unrelated state.

Additionally, when state is lifted outside an unmounting component (e.g., a drafts cache keyed by thread ID), key it by a stable, canonical identity rather than a transient UI ID that can have multiple aliases for the same underlying entity — otherwise navigating away and back, or reopening via a different path, silently loses or overwrites that state.

Review any `useEffect`/callback that awaits a promise and then calls `dispatch`, mutates a ref, or writes to a shared Map: confirm it validates currency before applying the result and that it used a snapshot rather than a live, possibly-stale reference.