---
title: Intent from Event Streams
description: 'When implementing UI/OS-driven behaviors that depend on “user intent”
  (e.g., hold vs tap, pinned vs unpinned), treat the logic as an algorithm over an
  event stream: make the state explicit, derive transitions from trustworthy signals,
  and stop on clear termination conditions.'
repository: cline/cline#v21
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70886
---

When implementing UI/OS-driven behaviors that depend on “user intent” (e.g., hold vs tap, pinned vs unpinned), treat the logic as an algorithm over an event stream: make the state explicit, derive transitions from trustworthy signals, and stop on clear termination conditions.

Practical rules:
- Model as states + transitions: define what constitutes “active hold,” “arrived at target,” “user unpinned,” etc., rather than relying on incidental DOM/browser behavior.
- Separate user vs programmatic actions: maintain a distinct marker/target for programmatic scrolls so their events don’t get misclassified as user intent.
- Use robust measurement, not assumptions: when keyup is missing or scroll anchoring is unavailable, base decisions on available observables (auto-repeat keydown timing gaps; distance-from-bottom thresholds; resize deltas or restored anchors).
- Add explicit time/gap thresholds and “stop conditions”: e.g., require an auto-repeat phase before triggering a hold action; treat elapsed-time gaps as a release signal.
- Document non-verifiable platform limitations: if OS signals can’t distinguish tap vs hold, state the documented limitation and what behaviors remain correct.

Example pattern (hold detection with deterministic stop conditions):
```ts
const REPEAT_GAP_MS = 350;
const FIRST_REPEAT_TIMEOUT_MS = 1500;

function shouldQuit({ start, lastEvent, repeating, holdMs }: {
  start: number; lastEvent: number; repeating: boolean; holdMs: number;
}, now: number) {
  const idle = now - lastEvent;
  const limit = repeating ? REPEAT_GAP_MS : FIRST_REPEAT_TIMEOUT_MS;
  if (idle > limit) return { quit: false };

  const elapsed = now - start;
  if (elapsed >= holdMs && repeating) return { quit: true };
  return { quit: false };
}
```

Apply the same mindset to scroll/resize logic: keep a pinned/unpinned state, track anchors/targets, and compensate using measured deltas so streaming content doesn’t incorrectly move the reader’s view.