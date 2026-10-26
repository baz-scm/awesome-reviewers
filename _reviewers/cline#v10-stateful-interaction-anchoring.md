---
title: Stateful Interaction Anchoring
description: 'When implementing UI behaviors that must remain stable under dynamic
  changes (streaming content, re-renders, OS/event quirks), treat the feature as an
  explicit algorithm: define invariants, separate intent events from observations,
  and (when needed) anchor the user’s “perceived position” using robust geometry.'
repository: cline/cline#v10
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70869
---

When implementing UI behaviors that must remain stable under dynamic changes (streaming content, re-renders, OS/event quirks), treat the feature as an explicit algorithm: define invariants, separate intent events from observations, and (when needed) anchor the user’s “perceived position” using robust geometry.

Apply this standard:
- Define ownership and invariants
  - Example invariant: “Programmatic scrolls do not affect pinned/unpinned state.”
  - Update derived state from a measurable quantity (e.g., distance from bottom, elapsed hold time), not from incidental events.
- Separate intent from observation
  - Unpin/pause state should change on user intent events (wheel/key/drag), while scroll events are treated as observations that can be filtered/ignored when they originated programmatically.
- Use a geometric anchor to prevent drift
  - Compute a stable “reading anchor” from the DOM (which row/element is being read) and restore that anchor’s relative offset after content resize/updates.
  - Anchor discovery must tolerate wrapper/DOM-shape variance (e.g., single-child wrappers, siblings like banners).
- When perfect signals aren’t available on a platform
  - Prefer the best available invariant (e.g., elapsed-time model) but document the limitation and the expected failure mode; don’t silently pretend correctness.

Sketch (anchor + restore idea):
```ts
type ReadingAnchor = { element: Element; offsetTop: number };

function findReadingAnchor(viewport: HTMLDivElement, content: HTMLDivElement): ReadingAnchor | null {
  // Descend through wrappers, pick the deepest element whose rect crosses the viewport’s top,
  // and handle DOM siblings by choosing the first appropriate child when the reader is between rows.
  // (Implementation details depend on your DOM structure.)
  return null;
}

function restoreAnchor(viewport: HTMLDivElement, anchor: ReadingAnchor) {
  const rect = anchor.element.getBoundingClientRect();
  const currentOffsetTop = rect.top - viewport.getBoundingClientRect().top;
  const delta = currentOffsetTop - anchor.offsetTop;
  viewport.scrollTop += delta;
}
```

Result: fewer edge-case “snapping,” no drift while streaming, and clearer correctness because your code is grounded in explicit computational invariants rather than event timing accidents.