---
title: Event-State Intent Algorithms
description: 'When implementing interactive, time- or event-driven UI behavior (holds,
  scrolling, pinning, debounced actions), model it as an explicit state machine/algorithm:
  (1) track intent explicitly (e.g., user vs programmatic, hold vs tap), (2) use clear
  temporal/positional thresholds, (3) gate transitions by the correct event source/target,
  and (4) document any...'
repository: cline/cline#v25
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70891
---

When implementing interactive, time- or event-driven UI behavior (holds, scrolling, pinning, debounced actions), model it as an explicit state machine/algorithm: (1) track intent explicitly (e.g., user vs programmatic, hold vs tap), (2) use clear temporal/positional thresholds, (3) gate transitions by the correct event source/target, and (4) document any platform/event guarantees you must rely on.

How to apply:
- Separate “who caused the change” with an explicit state/target variable.
  - Example: store `ourScrollTarget` when calling `scrollToBottom()` and treat scroll events as “ours” until the viewport reaches that target; only un-pin on genuine reader input.
- Use time/threshold logic for correctness.
  - Example: for hold-to-quit, compute elapsed time with `performance.now()` and stop/quits only when repeat/idle conditions indicate an intentional hold.
- Gate on event target/source to avoid accidental transitions.
  - Example: only un-pin on arrow-key actions when the event is intended for the viewport (not when a child control is focused).
- If the platform cannot provide the needed signal (e.g., missing key-up), either encode the workaround in the algorithm and document the limitation.

Minimal patterns:
```ts
// Separate intent: programmatic vs user
const ourScrollTarget = useRef<number | null>(null);
const handleScroll = () => {
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived) ourScrollTarget.current = null;
    return; // ignore until reached, unless user un-pins
  }
  // only now interpret reader intent (distance/threshold)
};

// Gate transitions by event target
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.target !== viewport) return;
  if (['ArrowUp','PageUp','Home'].includes(e.key)) setPinned(false);
};

// Temporal logic: hold/tap distinction
const tick = () => {
  const hold = holdRef.current;
  if (!hold) return;
  const elapsed = performance.now() - hold.start;
  if (elapsed >= holdMs && hold.repeating) { quitApp(); }
};
```

This standard prevents accidental actions (e.g., misclassifying a programmatic scroll as user intent, or unpinning from unrelated focused controls) and makes event-driven behavior reliably testable like an algorithm.