---
title: Use anchored state machines
description: 'For event-driven UI “algorithms” (scrolling, streaming, resizing), implement
  a deterministic state machine with explicit invariants, drift-free anchoring, and
  correct event attribution:'
repository: cline/cline#v3
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70863
---

For event-driven UI “algorithms” (scrolling, streaming, resizing), implement a deterministic state machine with explicit invariants, drift-free anchoring, and correct event attribution:

- Maintain an explicit state (e.g., pinned/unpinned) and only transition it on *classified* events:
  - Distinguish user input from programmatic changes (track programmatic targets; ignore their resulting scroll events as user intent).
- Use an *anchor* instead of heuristic compensation to avoid drift:
  - On user scroll, record a stable reference (e.g., the first row at/near the viewport top plus its offset).
  - On resize/content changes, recompute scrollTop to restore that same row/offset.
- Gate state transitions by event origin:
  - Keyboard/mouse/touch handlers should only un-pin when the event target is the controlled viewport (ignore nested focused controls).

Example pattern (self-contained):
```ts
const pinnedRef = useRef(true);
const ourScrollTarget = useRef<number | null>(null);
const anchorRef = useRef<{ topOffset: number; rowId: string } | null>(null);

function onScroll() {
  // 1) Ignore scroll events caused by our own programmatic scroll
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived) ourScrollTarget.current = null;
    else if (pinnedRef.current) return;
  }

  // 2) If user unpinned, update anchor
  if (!pinnedRef.current) {
    const row = firstRowIntersectingTop();
    anchorRef.current = { rowId: row.id, topOffset: row.offsetFromViewportTop };
  }
}

function onResizeOrContentGrowth() {
  // 3) Restore drift-free anchor while unpinned
  if (!pinnedRef.current && anchorRef.current) {
    const row = findRowById(anchorRef.current.rowId);
    writeScrollTop(viewport, row.computeScrollTopForOffset(anchorRef.current.topOffset));
  }
}

function onKeyDown(e: KeyboardEvent) {
  // 4) Only unpin for keys targeted at the viewport itself
  if (e.target !== viewport) return;
  if (["ArrowUp", "PageUp", "Home"].includes(e.key)) pinnedRef.current = false;
}
```

This standard prevents incorrect state transitions (wrong event attribution) and UI drift under dynamic content/layout changes by relying on explicit invariants and anchor-based restoration—core algorithmic principles: clear state, stable reference points, and deterministic recomputation.