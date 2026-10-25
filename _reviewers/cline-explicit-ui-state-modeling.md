---
title: Explicit UI State Modeling
description: When UI behavior depends on time, repeated events, streaming content,
  or resize, implement it with explicit state modeling (state machine + invariants),
  not ad-hoc event heuristics.
repository: CLINE/CLINE
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70837
---

When UI behavior depends on time, repeated events, streaming content, or resize, implement it with explicit state modeling (state machine + invariants), not ad-hoc event heuristics.

Apply these rules:
- Separate “user intent” from “programmatic effects” using explicit tracking (e.g., a target/anchor ref). Treat events originating from programmatic actions as non-authoritative for user state.
- Gate state transitions with well-defined thresholds/constants. Define timing/epsilon values (tick rate, repeat gaps, arrival tolerances, pinned/unpinned thresholds) as named constants.
- Preserve user reference points on content changes (resize/streaming): use an anchor/target and restore the same relative position after DOM size changes.
- Use deterministic stop conditions for async loops/intervals: clear timers on completion, on losing the expected signal, or after a timeout gap.

Example pattern (sketch):

```ts
const FIRST_TIMEOUT_MS = 1500;
const REPEAT_GAP_MS = 350;

type HoldState = { start: number; lastEvent: number; repeating: boolean } | null;

function createHoldController({ holdMs }: { holdMs: number }) {
  let state: HoldState = null;

  function onKeyDown(now: number, isRepeat: boolean) {
    if (!state) state = { start: now, lastEvent: now, repeating: false };
    else {
      state.lastEvent = now;
      if (isRepeat) state.repeating = true;
    }
  }

  function tick(now: number) {
    if (!state) return { done: true };

    const idle = now - state.lastEvent;
    const limit = state.repeating ? REPEAT_GAP_MS : FIRST_TIMEOUT_MS;
    if (idle > limit) return { done: true };

    const elapsed = now - state.start;
    if (elapsed >= holdMs && state.repeating) return { done: true, quit: true };

    return { done: false };
  }

  return { onKeyDown, tick, reset: () => (state = null) };
}
```

Use the same approach for scrolling/streaming: track an explicit “ourScrollTarget” (programmatic) and a “pinned/anchor” state (user), then update them only when invariants are satisfied (arrival tolerance, user input events, resize anchor restoration).