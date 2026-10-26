---
title: Deterministic UI State Machines
description: For event- and time-driven UI behavior, implement the logic as an explicit
  state machine with clear ownership/invariants, and ensure each event updates state
  only when it originates from the correct cause.
repository: cline/cline#v11
label: Algorithms
language: TSX
comments_count: 4
repository_stars: 70871
---

For event- and time-driven UI behavior, implement the logic as an explicit state machine with clear ownership/invariants, and ensure each event updates state only when it originates from the correct cause.

Apply this by:
- **Define states + invariants** (e.g., pinned/unpinned; hold-start/hold-timeout/quit-fired). State transitions should be predictable from inputs.
- **Separate sources of truth**: track *intent* for programmatic actions (e.g., a “scroll target” or “hold in progress”) so their resulting events don’t get misclassified as user actions.
- **Guard by event origin**: only treat keyboard/wheel/pointer events as user intent when they originate from the expected target (e.g., the viewport container), preventing accidental state changes from focused child controls.
- **Use deterministic thresholds and clamping**: when relying on time, auto-repeat gaps, or scroll distances, explicitly clamp progress and use named constants.
- **Preserve invariants under dynamic change**: when content resizes or streams, anchor to a stable reference (e.g., remembered offset/row) so the user’s view doesn’t “drift.”
- **Document unavoidable platform limitations** and keep the behavior safe (e.g., graceful fallback to platform-native shortcuts when the OS can’t provide required events).

Example (pattern):
```ts
// Ownership-tracked “intent” guard
const ourTarget = useRef<number | null>(null);
const [pinned, setPinned] = useState(true);

function scrollToBottom() {
  ourTarget.current = viewport.scrollHeight; // programmatic intent
  viewport.scrollTo({ top: viewport.scrollHeight, behavior: 'smooth' });
}

function onScroll() {
  if (ourTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourTarget.current) <= 1;
    if (arrived || pinned) { // don’t let our intent mispin/unpin
      if (arrived) ourTarget.current = null;
      return;
    }
    ourTarget.current = null;
  }
  // Now handle real user-driven pin/unpin
  setPinned(distanceFromBottom(viewport) <= PINNED_THRESHOLD_PX);
}

function onKeyDown(e: KeyboardEvent) {
  // Only unpin on keys that truly target the viewport container
  if (e.target !== viewport) return;
  if (['ArrowUp','PageUp','Home'].includes(e.key)) setPinned(false);
}
```
This approach reduces edge-case regressions by making state transitions provably tied to the correct causal inputs.