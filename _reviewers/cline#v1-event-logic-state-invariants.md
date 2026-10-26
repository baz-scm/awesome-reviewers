---
title: Event Logic State Invariants
description: When implementing interaction-driven behaviors (holds, scrolling, keyboard
  shortcuts, streaming/resize reactions), treat the logic as a small algorithm with
  explicit state, invariants, and deterministic thresholds/anchors.
repository: cline/cline#v1
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70862
---

When implementing interaction-driven behaviors (holds, scrolling, keyboard shortcuts, streaming/resize reactions), treat the logic as a small algorithm with explicit state, invariants, and deterministic thresholds/anchors.

**Standard**
1. **Define explicit state + invariants** (e.g., “pinned means scroll position is owned by the reader” or “hold progress only advances while the hold is still valid”).
2. **Classify event sources**: never let programmatic/system/OS-generated events be mistaken for user intent. Use a dedicated “target/anchor” (e.g., `ourScrollTarget`) or an “in-hold” state.
3. **Use deterministic timing rules** for temporal interactions. Prefer monotonic clocks (`performance.now()`), tick/timeout thresholds, and clear rules for edge cases (auto-repeat quirks, missing keyup, smooth scroll emitting many events).
4. **Prevent async drift**: when content changes (resize, streaming), restore position using an anchor/compensation strategy so the user’s perceived location doesn’t move.
5. **Update state only from the correct stimulus** (e.g., un-pin on user input, not on the resulting scroll event that may be delayed).
6. **Document unavoidable platform limitations** where correctness depends on OS behavior.

**Illustrative pattern (anchor/target + invariants)**
```ts
const pinnedRef = useRef(true);
const ourScrollTarget = useRef<number | null>(null);

function writeScrollTop(el: HTMLDivElement, top: number, behavior: ScrollBehavior) {
  const maxTop = Math.max(0, el.scrollHeight - el.clientHeight);
  const clamped = Math.min(Math.max(0, top), maxTop);
  ourScrollTarget.current = clamped !== el.scrollTop ? clamped : null;
  el.scrollTo({ top: clamped, behavior });
}

function handleScroll() {
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived || pinnedRef.current) {
      if (arrived) ourScrollTarget.current = null;
      return;
    }
    ourScrollTarget.current = null;
  }
  // Recompute pinned from distance-to-bottom thresholds.
  const distance = viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight;
  pinnedRef.current = distance <= PINNED_THRESHOLD_PX;
}
```

Apply this standard to avoid accidental triggers (e.g., confirmation holds) and to keep user experience stable under asynchronous UI changes (e.g., smooth scroll + streaming + resize).