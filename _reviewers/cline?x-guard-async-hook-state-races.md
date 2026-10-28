---
title: Guard async hook state races
description: 'Custom hooks that mix optimistic local state with async confirmations
  (network calls, event streams, debounced acknowledgements) must be written defensively
  against races and staleness:'
repository: cline/cline?x
label: React
language: TypeScript
comments_count: 4
repository_stars: 70983
---

Custom hooks that mix optimistic local state with async confirmations (network calls, event streams, debounced acknowledgements) must be written defensively against races and staleness:

- Tag each async operation with a generation/request counter (or similar token) and drop any reply whose token no longer matches the current one, so a response from a superseded bind/session/request can never mutate state that has since moved on (e.g. `generationRef`, `requestRef`).
- Guard against duplicate concurrent invocations of the same user action with an in-flight flag/ref (e.g. `sendInFlightRef`), so a second press/call while one is pending is a no-op instead of firing twice.
- Any cache key, refresh key, or "is this data current" comparison must be derived from *all* the inputs that affect correctness, not just the ones that happen to change in common cases — e.g. a refresh key based only on tool-call count missed new turns that had no tool calls; include every state dimension (status, message counts, etc.) that could legitimately produce different data.
- When optimistic markers and async stream events can interleave (e.g. an optimistic "sending" state vs. a partial-message event arriving before the debounced full-state update), the condition that decides what's rendered must account for the latest known tail/state, not just the optimistic flag, to avoid showing contradictory UI (two loaders, duplicated messages, stale "current" data).
- Test these hooks end-to-end (not just a pure helper function) with the exact interleaving that caused the bug — e.g. render the full hook with a stale state, a pending optimistic flag, and the real async event — to prove the race is actually closed, since a helper-only test can pass while the composed hook still reproduces the race.

Example pattern for dropping stale replies:
```ts
const generationRef = useRef(0);

async function bind(sessionId: string) {
  generationRef.current += 1;
  const generation = generationRef.current;
  const result = await invoke(sessionId);
  if (generation !== generationRef.current) return; // stale, ignore
  dispatch({ type: "state", result });
}
```