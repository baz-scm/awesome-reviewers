---
title: Guard async hook state races
description: 'Hooks that kick off async work (invokes, fetches, debounced acknowledgements)
  and later apply the result to local state are prone to race conditions: a stale
  reply can land after newer state has already superseded it, an optimistic update
  can be overwritten by a late confirmation, or a cache/refresh key can fail to capture
  every state change that should...'
repository: cline/cline#`sleep 4`
label: React
language: TypeScript
comments_count: 6
repository_stars: 70979
---

Hooks that kick off async work (invokes, fetches, debounced acknowledgements) and later apply the result to local state are prone to race conditions: a stale reply can land after newer state has already superseded it, an optimistic update can be overwritten by a late confirmation, or a cache/refresh key can fail to capture every state change that should invalidate it. Guard against this class of bug explicitly:

1. Tag every async action with a generation/epoch token (or a snapshot of the relevant state at dispatch time) and verify that token still matches before applying the result. Discard replies from a stale generation, a session that's no longer bound, or a revision that's since changed.
2. When an async action depends on mutable external state (e.g. attached files, a composer draft), snapshot what's needed at the moment the action fires, and reconcile explicitly against current state when the result arrives, rather than assuming nothing changed during the await.
3. When deriving "is this data current" from a key (refresh key, cache key, thread/session id), make sure the key changes for every transition that should be considered a new state — don't let two different events collapse to the same key just because one path (e.g. no tool calls) didn't bump a sub-field.
4. When combining multiple async-derived flags into one UI condition (e.g. optimistic flag + debounced confirmed state), compute the combined condition in one place and cover the handoff window with a test — don't duplicate partial logic across helpers where one path misses the gate.

Example pattern for discarding stale async replies:

```ts
const generationRef = useRef(0);

useEffect(() => {
  generationRef.current += 1;
  const generation = generationRef.current;
  void (async () => {
    const result = await invoke(action);
    if (generation !== generationRef.current) return; // stale reply, ignore
    dispatch({ type: "reply", result });
  })();
}, [action]);
```

Applying this consistently avoids duplicated/stranded optimistic rows, dropped or wrongly-applied async verdicts, and UI that flickers or shows outdated data during the gap between an optimistic update and its async confirmation.