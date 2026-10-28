---
title: Guard async callbacks against stale state
description: When a hook or component kicks off an async operation (API call, invoke,
  timer), the component's state can change before that operation resolves — the user
  navigates away, remounts a different instance, a newer optimistic update lands,
  or a race between a fast optimistic state and a slower acknowledgement occurs. Applying
  the async result unconditionally...
repository: cline/cline;
label: React
language: TypeScript
comments_count: 4
repository_stars: 70964
---

When a hook or component kicks off an async operation (API call, invoke, timer), the component's state can change before that operation resolves — the user navigates away, remounts a different instance, a newer optimistic update lands, or a race between a fast optimistic state and a slower acknowledgement occurs. Applying the async result unconditionally can silently overwrite newer data or produce an inconsistent UI (e.g., a retired pane's failed-send handler overwriting a freshly typed draft, or a stale "exposed"/"used" revision double-applying).

Always validate liveness/currency before applying the outcome of an async operation:
- Use a generation/epoch counter (or similar token) captured at call time, and bail out if it no longer matches the current generation when the callback resolves.
- Prefer deriving "is this still relevant" from current shared state (e.g., a shared `Map` or latest ref) rather than trusting a local ref/closure captured by a component instance that may have since unmounted or been replaced.
- When combining an optimistic flag with a later authoritative state, gate the combined condition in one place (don't duplicate the check across call sites) so the optimistic value cannot override an already-arrived authoritative value.
- Make repeat actions idempotent/no-op while one is in flight (e.g., ignore a second "undo" press while the first is still pending).

Example pattern:
```ts
const generationRef = useRef(0);

async function run(action) {
  const generation = ++generationRef.current;
  const result = await doAsyncWork(action);
  if (generation !== generationRef.current) return; // stale, discard
  applyResult(result);
}
```

When testing this behavior, exercise the full hook/component (not just an isolated pure helper) with the actual async timing — e.g., a stale optimistic value overlapping a delayed authoritative update — so the race is actually reproduced and caught.