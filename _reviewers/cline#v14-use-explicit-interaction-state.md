---
title: Use explicit interaction state
description: 'When behavior depends on asynchronous events (timing, scrolling, resize/content
  growth), implement it as a small explicit state machine: define states, transitions,
  and invariants; use measurable signals (time gaps, distance-from-bottom, scroll
  offsets) rather than ambiguous event presence; and separate “internal/programmatic”
  actions from “external/user”...'
repository: cline/cline#v14
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70876
---

When behavior depends on asynchronous events (timing, scrolling, resize/content growth), implement it as a small explicit state machine: define states, transitions, and invariants; use measurable signals (time gaps, distance-from-bottom, scroll offsets) rather than ambiguous event presence; and separate “internal/programmatic” actions from “external/user” actions with an internal target/token so event streams aren’t misclassified.

How to apply:
- Model states explicitly (e.g., hold tracking: start/lastEvent/repeating; scroll tracking: pinned/unpinned; restore tracking: pending/ready).
- Drive transitions from deterministic metrics:
  - Time: stop when (idle > threshold) or when elapsed reaches holdMs.
  - Position: compute distance-from-bottom; pin if within PINNED_THRESHOLD_PX.
  - Resize/content growth: keep a pending restore anchor and apply only once the viewport can reach it.
- Classify causality:
  - For programmatic scrolls, set an internal “ourScrollTarget” and ignore/clear scroll events until arrival, unless the user un-pins mid-flight.
- Enforce invariants and document irreducible limitations (e.g., platform doesn’t deliver keyup under certain modifier conditions).

Example pattern (hold-style state + thresholds):
```ts
const REPEAT_GAP_MS = 350;
const FIRST_REPEAT_TIMEOUT_MS = 1500;

const holdRef = { start: 0, lastEvent: 0, repeating: false };
let interval: number | undefined;

function stop() { /* clear state + interval */ }

function tick(now = performance.now()) {
  const idle = now - holdRef.lastEvent;
  const timeout = holdRef.repeating ? REPEAT_GAP_MS : FIRST_REPEAT_TIMEOUT_MS;
  if (idle > timeout) return stop();

  const elapsed = now - holdRef.start;
  if (elapsed >= holdMs && holdRef.repeating) { stop(); quitApp(); }
}
```

This standard reduces accidental triggers and drift by making the logic algorithmic, testable, and resilient to event ordering and platform quirks.