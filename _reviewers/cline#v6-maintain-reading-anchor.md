---
title: Maintain reading anchor
description: 'When UI content dynamically changes (e.g., streaming chat), treat scroll
  anchoring as an algorithmic invariant problem: preserve the reader’s perceived position
  by anchoring to a specific content element plus its viewport-relative offset, then
  restoring that same anchor after every resize/layout change.'
repository: cline/cline#v6
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70864
---

When UI content dynamically changes (e.g., streaming chat), treat scroll anchoring as an algorithmic invariant problem: preserve the reader’s perceived position by anchoring to a specific content element plus its viewport-relative offset, then restoring that same anchor after every resize/layout change.

How to apply:
1. Define the invariant
   - A “reading anchor” = (stable DOM element reference, offsetTop of that element relative to the viewport).
   - Update the anchor when the reader scrolls (user-driven).
2. Find the anchor robustly
   - Do not assume a fixed DOM wrapper shape (single child only).
   - Instead, select the element that should be “being read” using geometry: descend from the content root to find the deepest element whose geometry crosses the viewport’s top edge.
   - If there is a gap, anchor to the first child starting below the top edge.
3. Restore after layout changes
   - After ResizeObserver/layout updates, re-resolve the anchored element (or re-find the equivalent) and set scrollTop so that the anchored element returns to the same viewport-relative offset.
   - The goal is “zero drift” for content growth below/above the anchor (preventing the user from being pushed).

Self-contained sketch:
```ts
type ReadingAnchor = { element: Element; offsetTop: number };

function findReadingAnchor(viewport: HTMLDivElement, content: HTMLDivElement): ReadingAnchor | null {
  // Descend through the real geometry, not structural assumptions.
  let node: Element = content;
  while (true) {
    const children = Array.from(node.children);
    if (children.length === 0) break;

    // Pick the child whose rect crosses the viewport top edge.
    const topY = viewport.getBoundingClientRect().top;
    let crossed = children
      .map(c => ({ c, r: c.getBoundingClientRect() }))
      .filter(x => x.r.bottom > topY)
      .sort((a,b) => a.r.top - b.r.top)[0];

    // If none crosses (gap), anchor the first child starting below the edge.
    if (!crossed) {
      const firstBelow = children
        .map(c => ({ c, r: c.getBoundingClientRect() }))
        .sort((a,b) => a.r.top - b.r.top)[0];
      if (!firstBelow) break;
      node = firstBelow.c;
      break;
    }

    node = crossed.c;
  }

  const offsetTop = (node.getBoundingClientRect().top - viewport.getBoundingClientRect().top) + viewport.scrollTop;
  return { element: node, offsetTop };
}

function restoreAnchor(viewport: HTMLDivElement, anchor: ReadingAnchor | null) {
  if (!anchor) return;
  // Recompute desired scrollTop so the anchor element’s offsetTop matches.
  // (Implementation detail: re-measure anchor element’s current offsetTop, then adjust scrollTop by the delta.)
}
```

Testing guidance (based on the same failure modes):
- Add regression tests for “growth below anchor keeps the same row under the reader.”
- Add regression tests for layouts with siblings/extra banners/notices to ensure the anchor-finder is not coupled to a single-child wrapper structure.