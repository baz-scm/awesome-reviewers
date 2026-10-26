---
title: Stateful Interaction Algorithms
description: When implementing interactive UI behavior (keyboard holds, scroll anchoring,
  shortcut capture), model the logic as an explicit state machine with clear invariants,
  deterministic transitions, and robust cancellation/reset rules. Separate competing
  “sources of truth” (e.g., user vs programmatic scroll; shortcut mode active vs suspended)
  so events don’t get...
repository: cline/cline#v12
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70872
---

When implementing interactive UI behavior (keyboard holds, scroll anchoring, shortcut capture), model the logic as an explicit state machine with clear invariants, deterministic transitions, and robust cancellation/reset rules. Separate competing “sources of truth” (e.g., user vs programmatic scroll; shortcut mode active vs suspended) so events don’t get misclassified.

Practical rules:
- Define states and transitions (e.g., HoldTracking: idle → holding → repeating → quitting/timeout; ScrollPin: pinned → unpinned → re-pinned; Shortcuts: active → suspended → restored).
- Track the minimal required signals to disambiguate meaning (e.g., measure time gaps and repeat status for hold; track a read anchor so resize can restore the same content position).
- Cancel in-progress work when the mode changes or conflicts arise (e.g., suspending shortcuts must also stop any hold in progress).
- Document platform-specific signal limitations and ensure behavior is still safe (e.g., if an OS doesn’t provide keyup, rely on a measured timeout and explicitly state the limitation).

Example pattern (state + cancellation):
```ts
// Pseudocode structure
type Mode = "active" | "suspended";
let mode: Mode = "active";
let inProgress: { start: number; lastEvent: number; repeating: boolean } | null = null;

function onKeyDown(e: KeyboardEvent) {
  if (mode !== "active") return;
  if (!matchesAccelerator(e, "Cmd+Q")) return;
  e.preventDefault();
  if (!inProgress) startHoldTimer();
  else updateHoldTracking(e);
}

function suspendShortcuts() {
  mode = "suspended";
  inProgress = null; // cancel hold safely
  stopTimers();
}

function tick() {
  if (mode !== "active") return stopTimers();
  // deterministic timeout/transition logic based on measured signals
}
```
Adopting this approach prevents subtle correctness bugs caused by mixing event streams and ensures edge cases (repeat timing, resize, recording/suspension) behave predictably.