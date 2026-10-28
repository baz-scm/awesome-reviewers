---
title: Guard stale async updates
description: Hooks that kick off async work (network calls, timers, promises) must
  not blindly apply the result when it finally resolves — by then the component may
  have unmounted, remounted for a different entity, or the user may have taken a new
  action. Always validate that the async result is still relevant to the *current*
  binding/identity before dispatching it, and...
repository: cline/cline#|sleep 4
label: React
language: TypeScript
comments_count: 4
repository_stars: 70979
---

Hooks that kick off async work (network calls, timers, promises) must not blindly apply the result when it finally resolves — by then the component may have unmounted, remounted for a different entity, or the user may have taken a new action. Always validate that the async result is still relevant to the *current* binding/identity before dispatching it, and snapshot any input that the async call needs at the moment it starts rather than re-reading mutable refs/state when the result lands.

Two concrete patterns to apply:
1. **Generation/bound-id guards**: increment a generation counter (or capture the bound session/thread id) when starting an async operation, and check it again when the result arrives before applying state changes. This prevents a reply to an earlier bind/session from being applied after a newer bind has taken over.
2. **Snapshot-at-call-time**: capture the state the async action depends on (e.g., attached files, draft text, thread id) at the moment the action is dispatched, not at the moment its promise resolves. Reconcile the snapshot against the latest state when the verdict arrives (e.g., "send only the files still attached") instead of trusting either the stale snapshot or the live-but-possibly-unrelated current state.

```ts
const generationRef = useRef(0);

async function bindTo(sessionId: string) {
  generationRef.current += 1;
  const generation = generationRef.current;
  const result = await fetchStateFor(sessionId);
  if (generation !== generationRef.current) return; // stale reply, ignore
  dispatch({ type: "state", result });
}
```

This also applies to caches/maps keyed by a component-local id (e.g., per-thread draft storage): make sure the key uniquely and stably identifies the logical entity across remounts/aliases, and that a retired instance's ref/closure can never win a race against the currently-mounted instance for the same key. When reviewing hooks with `useEffect`/async callbacks, check for: missing generation/id checks before `dispatch`, reliance on refs that may belong to an unmounted instance, and lack of reconciliation when the async result and current state have diverged.