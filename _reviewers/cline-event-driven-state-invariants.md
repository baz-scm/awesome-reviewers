---
title: Event-Driven State Invariants
description: 'When implementing UI/device event behavior (key holds, scrolling, resize
  compensation), treat the logic as an explicit state machine with clear invariants:
  track the source of events, preserve correctness across async updates, and don’t
  infer “intent” from ambiguous signals.'
repository: CLINE/cline
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70839
---

When implementing UI/device event behavior (key holds, scrolling, resize compensation), treat the logic as an explicit state machine with clear invariants: track the source of events, preserve correctness across async updates, and don’t infer “intent” from ambiguous signals.

Apply this standard:
- Define invariants up front (e.g., “pinned means reader hasn’t un-pinned via user input”; “a quit requires an actual hold, not a tap”).
- Separate user-driven vs programmatic effects using explicit markers/targets (e.g., record the intended scrollTop or a “ourScrollTarget” and ignore intermediate scroll events until arrival).
- Use tolerance/thresholds to decide transitions (e.g., treat “arrived” as within 1px; treat hold success via measured repeat timing windows).
- Preserve position under async content changes by anchoring state (e.g., store/restore the content row/offset under the reader during resize) rather than using naive height assumptions.
- Document any platform limitations that force algorithmic tradeoffs, and state the safety behavior (e.g., what still distinguishes a tap vs hold, and what cannot be perfectly detected without native hooks).

Sketch of the pattern (scroll example):
```ts
const ourScrollTarget = useRef<number | null>(null);

const handleScroll = () => {
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived) ourScrollTarget.current = null;
    else if (pinnedRef.current) return; // ignore while pinned during our scroll
  }

  const distance = distanceFromBottom(viewport);
  setPinned(distance <= PINNED_THRESHOLD_PX);
};

const scrollToBottom = () => {
  ourScrollTarget.current = viewport.scrollHeight;
  setPinned(true);
  viewport.scrollTo({ top: viewport.scrollHeight, behavior: "smooth" });
};
```

This reduces subtle correctness bugs (accidental unpinning, scroll drift under streaming, misclassifying taps) by aligning the algorithm with the real event stream and preserving the same invariants throughout the lifecycle.