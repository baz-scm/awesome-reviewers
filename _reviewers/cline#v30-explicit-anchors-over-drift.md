---
title: Explicit Anchors Over Drift
description: 'When building UI logic that must remain correct under asynchronous events
  and changing content/layout (scrolling, streaming, key holds, resizes), implement
  the behavior as an explicit algorithm with:'
repository: cline/cline#v30
label: Algorithms
language: TSX
comments_count: 5
repository_stars: 70894
---

When building UI logic that must remain correct under asynchronous events and changing content/layout (scrolling, streaming, key holds, resizes), implement the behavior as an explicit algorithm with:

- **State invariants**: define states like pinned/unpinned (or holding/tapped) and only transition on the specific events that satisfy the state’s definition.
- **Source separation**: track whether events are **user-originated vs programmatic** (e.g., maintain an `ourScrollTarget` and ignore/match scroll events accordingly) so you never “learn” from the wrong signal.
- **Anchor-based position preservation**: instead of fragile height-delta compensation, store an **anchor** representing what the user is viewing (e.g., the row intersecting the viewport top plus its offset), and restore that anchor after layout/content changes.
- **Robust matching/guard conditions**: use guards to prevent false transitions (e.g., only unpin on specific key events aimed at the viewport; find anchors without assuming a particular DOM nesting like single-child wrappers).
- **Tolerance thresholds and timeouts**: for temporal behavior, use clear constants (gaps/timeouts) and document platform limitations; treat them as part of the algorithm’s correctness model.

Example pattern (anchor + restore, simplified):
```ts
type ReadingAnchor = { element: Element; offsetTop: number };

function computeAnchor(viewport: HTMLDivElement, content: HTMLDivElement): ReadingAnchor | null {
  // Descend through wrappers without assuming single-child structure,
  // find the deepest row whose rect crosses the viewport top edge,
  // and record its element + offset.
  // ...
  return null;
}

function restoreAnchor(viewport: HTMLDivElement, anchor: ReadingAnchor) {
  // After resize/stream growth, scroll so anchor.element keeps the same
  // offsetTop relative to viewport.
  // ...
}
```

Adopt this standard whenever the user’s perceived position matters: define the invariant, separate event sources, anchor the user’s reference point, and re-apply it after dynamic changes—rather than relying on deltas or incidental event timing.