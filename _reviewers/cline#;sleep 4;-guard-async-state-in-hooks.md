---
title: Guard async state in hooks
description: Custom hooks that trigger async work (network invokes, debounced acknowledgements,
  session rebinds) must guard against the response arriving after the hook's relevant
  state has moved on. Before kicking off an async call, snapshot whatever values the
  eventual `.then`/resolution needs (e.g. attached files, session id, the item being
  acted on) instead of...
repository: cline/cline#;sleep 4;
label: React
language: TypeScript
comments_count: 6
repository_stars: 70976
---

Custom hooks that trigger async work (network invokes, debounced acknowledgements, session rebinds) must guard against the response arriving after the hook's relevant state has moved on. Before kicking off an async call, snapshot whatever values the eventual `.then`/resolution needs (e.g. attached files, session id, the item being acted on) instead of re-reading mutable refs when it resolves — state can change while the call is in flight. Track a generation counter or a "currently bound" ref that is bumped on every rebind/unmount, and check it immediately after the await before dispatching, writing to state, or firing side effects; discard the result if the generation/binding no longer matches.

When a boolean or derived condition is meant to suppress/gate behavior (e.g. "don't show the loader while provisioning"), apply that gate at the single point where conditions are combined for rendering, not only inside one sub-helper — otherwise other branches of the combined condition can override the intended suppression during async handoffs (e.g. between an optimistic update and its debounced acknowledgement).

When multiple async sources append to the same ordered list (e.g. optimistic user messages, streamed system notices, plugin warnings), don't assume a fixed relative order from a single code path; searches/dedupe logic that walk the list backward must explicitly skip or account for entries injected by other paths, or key off stable markers (`meta.messageKind`) instead of positional assumptions.

Finally, any state cached by an entity id inside a hook (e.g. a draft keyed by thread id) must use a key that is stable for the lifetime of that entity. If the same logical session can be represented by more than one id (e.g. a new session's temporary id vs. the id used when reopened from history), reconcile/alias those ids or migrate the cached value when the binding changes, otherwise state silently appears lost.

Example pattern for guarding async resolution in a hook:

```ts
const generationRef = useRef(0);

async function invoke(action) {
  const boundId = boundRef.current;
  const generation = generationRef.current;
  if (!boundId) return;
  const result = await callApi(boundId, action);
  if (generation !== generationRef.current) return; // stale, discard
  dispatch({ type: "reply", result });
}
```

Add tests that exercise the full hook (not just an isolated helper) across the timing window where optimistic/partial state and the authoritative async result can coexist, asserting the stale result is dropped and the gated condition stays correct.