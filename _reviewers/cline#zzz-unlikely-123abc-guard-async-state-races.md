---
title: Guard async state races
description: Hooks that kick off async work (network calls, invokes, timers) and later
  apply the result to shared or cached state must verify the result is still relevant
  before applying it. Navigation, remounts, session switches, or newer user input
  can change the "current" context while a promise is in flight; applying a stale
  result corrupts state (a retired pane...
repository: cline/cline#zzz-unlikely-123abc
label: React
language: TypeScript
comments_count: 5
repository_stars: 71035
---

Hooks that kick off async work (network calls, invokes, timers) and later apply the result to shared or cached state must verify the result is still relevant before applying it. Navigation, remounts, session switches, or newer user input can change the "current" context while a promise is in flight; applying a stale result corrupts state (a retired pane overwriting a newer draft, a late reply reconciling against the wrong session, an optimistic flag racing an async acknowledgement, a stale `clear`/`use` applying to an item that was already refused or replaced).

To avoid this:
- Track an identity/generation for the active context (session id, thread id, bind generation, revision) in a ref, and bump it whenever the context changes.
- Before dispatching the result of an awaited call, re-check that the captured identity/generation still matches the current one; discard the result otherwise.
- When state is keyed by an id that can alias to the same underlying resource (e.g. two UI thread ids for one session), normalize or migrate the key instead of trusting the raw id, so a remount or alternate path can't strand or overwrite data.
- Prefer deriving combined UI conditions (e.g. "show loader") by gating on the authoritative async state rather than only on an optimistic flag, and cover the race with a test that interleaves the optimistic flag and the delayed acknowledgement.

Example pattern:
```ts
const generationRef = useRef(0);
const boundRef = useRef("");

useEffect(() => {
  generationRef.current += 1;
  const generation = generationRef.current;
  boundRef.current = sessionId;

  void (async () => {
    const result = await invoke(sessionId, action);
    if (generation !== generationRef.current) return; // stale: context changed, discard
    dispatch({ type: "reply", sessionId, result });
  })();
}, [sessionId]);
```

Apply this pattern any time a hook combines async results with mutable/cached state across component lifecycle changes, and add regression tests that simulate the out-of-order resolution (navigate away and back, delayed reply, remount) to lock in the fix.