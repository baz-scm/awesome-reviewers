---
title: Stateful UI Algorithms
description: 'When implementing UI behaviors driven by time, event streams, or asynchronous
  geometry (streaming content, resize, key repeat), treat them as explicit algorithms:'
repository: cline/cline#v22
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70886
---

When implementing UI behaviors driven by time, event streams, or asynchronous geometry (streaming content, resize, key repeat), treat them as explicit algorithms:

- Define clear states and invariants (e.g., “holding”, “repeating”, “pinned/unpinned”, “at anchor”).
- Use deterministic transition rules based on measurable quantities (performance.now(), scrollHeight/clientHeight distance, repeat gaps).
- Separate “user intent” from “programmatic effects” by tagging with a dedicated target/flag (e.g., a scroll target that the algorithm owns, so its resulting scroll events are not misclassified as user input).
- For asynchronous content/layout changes, persist a stable representation (target/anchor) and restore based on geometry becoming sufficient; retry on ResizeObserver/updates rather than assuming immediate layout.
- If the platform cannot provide a required signal, prefer documented limitations over fragile heuristics.

Example pattern (time-threshold state machine):

```ts
const FIRST_TIMEOUT_MS = 1500;
const REPEAT_GAP_MS = 350;

type HoldState = { start: number; lastEvent: number; repeating: boolean };

function shouldStop(hold: HoldState, now: number) {
  const idle = now - hold.lastEvent;
  const timeout = hold.repeating ? REPEAT_GAP_MS : FIRST_TIMEOUT_MS;
  return idle > timeout;
}

// Update hold.repeating from the event’s repeat signal; drive transitions from now-based thresholds.
```

Apply this approach to hold-confirmation actions and scroll/pinning/anchoring logic to make behavior predictable, testable, and resistant to misinterpreting event noise or async timing.