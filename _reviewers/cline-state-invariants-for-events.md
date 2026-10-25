---
title: State Invariants for Events
description: When behavior depends on indirect event signals (timing, scroll events,
  key events, async streaming), implement it as an explicit state machine with clear
  invariants—and always separate *what caused the change* from *the side effect you
  observe*.
repository: cline/CLINE
label: Algorithms
language: TSX
comments_count: 4
repository_stars: 70839
---

When behavior depends on indirect event signals (timing, scroll events, key events, async streaming), implement it as an explicit state machine with clear invariants—and always separate *what caused the change* from *the side effect you observe*.

Practical checklist:
- **Define states** (e.g., `pinned`/`un-pinned`, `hold`/`tap`, `awaiting-restore`/`restored`).
- **State the invariant in code comments**: “Only X transitions the state; side effect Y must not.”
- **Track event provenance**: maintain dedicated variables for “our programmatic action target” vs “user input”. Don’t infer user intent from the resulting scroll events.
- **Use deterministic algorithms for classification**: derive decisions from thresholds/elapsed time/distance-to-bottom/anchors instead of ad-hoc checks.
- **Handle async/resize deterministically**: when layout/content changes, restore to a remembered anchor (or a clamped target) and retry until it becomes achievable.
- **Document platform/observation gaps** (when the OS/browser can’t provide the signal you want) and constrain behavior accordingly.

Example pattern (adapted):
```ts
// Invariant: only user input unpins; programmatic scrolls are excluded.
const pinnedRef = useRef(true);
const ourScrollTarget = useRef<number | null>(null);

const writeScrollTop = (el: HTMLDivElement, top: number) => {
  const clamped = Math.max(0, Math.min(top, el.scrollHeight - el.clientHeight));
  ourScrollTarget.current = clamped !== el.scrollTop ? clamped : null;
  el.scrollTo({ top: clamped, behavior: 'smooth' });
};

const onScroll = () => {
  // Ignore scroll events that belong to our own programmatic target.
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(el.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived || pinnedRef.current) {
      if (arrived) ourScrollTarget.current = null;
      return;
    }
    ourScrollTarget.current = null;
  }

  const distance = el.scrollHeight - el.scrollTop - el.clientHeight;
  const nextPinned = distance <= PINNED_THRESHOLD_PX;
  pinnedRef.current = nextPinned;
};

// Unpin only on direct user input, not on resulting async scroll events.
el.addEventListener('wheel', e => { if (e.deltaY < 0) pinnedRef.current = false; });
```
This approach prevents misclassification and drift by making the logic’s “reasoning model” explicit—improving correctness across complex, asynchronous UI behavior (the same rigor also applies to time-based key/hold detection).