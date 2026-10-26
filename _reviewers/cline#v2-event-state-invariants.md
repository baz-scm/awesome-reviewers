---
title: Event State Invariants
description: 'When building event-driven UI logic that depends on time, async events,
  or streaming updates, implement it as a small deterministic algorithm: explicitly
  model state, use monotonic time, define thresholds/exit conditions, and preserve
  invariants across re-renders/resizes.'
repository: cline/cline#v2
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70861
---

When building event-driven UI logic that depends on time, async events, or streaming updates, implement it as a small deterministic algorithm: explicitly model state, use monotonic time, define thresholds/exit conditions, and preserve invariants across re-renders/resizes.

Practical rules:
- Use explicit state (e.g., refs/variables) to represent “in progress” vs “committed” phases.
- Use monotonic clocks for timing (e.g., `performance.now()`), and compute gaps/elapsed time with named constants.
- Define clear “stop/commit” conditions (e.g., when the hold expires, when the user unpins, when programmatic scroll is considered arrived).
- Separate user intent from programmatic/system actions; never infer intent from events that your code itself triggered.
- For streaming/resizes, prefer invariants/anchors (a stable reference row/position) over heuristic compensation (e.g., height delta guesses).
- Document platform limitations you cannot fully eliminate.

Example pattern (hold-to-commit with invariant exit conditions):
```ts
const TICK_MS = 40;
const REPEAT_GAP_MS = 350;
const FIRST_REPEAT_TIMEOUT_MS = 1_500;

type HoldState = { start: number; lastEvent: number; repeating: boolean };

const holdRef = { current: null as HoldState | null };

function tick(quit: () => void, holdMs: number) {
  const hold = holdRef.current;
  if (!hold) return;
  const now = performance.now();
  const idle = now - hold.lastEvent;
  const timeout = hold.repeating ? REPEAT_GAP_MS : FIRST_REPEAT_TIMEOUT_MS;
  if (idle > timeout) return (holdRef.current = null);

  const elapsed = now - hold.start;
  if (elapsed >= holdMs && hold.repeating) {
    holdRef.current = null;
    quit();
  }
}
```

Apply the same structure to scroll/streaming: keep ownership state (“pinned/unpinned”), track programmatic targets to avoid misattribution, and maintain a stable reading anchor across resize events so async content growth doesn’t drift the user.