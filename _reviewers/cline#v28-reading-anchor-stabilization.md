---
title: Reading anchor stabilization
description: When a UI viewport must stay stable while content is dynamically added/removed
  (e.g., streaming chat, virtualized lists), prefer an explicit **reading-anchor algorithm**
  over heuristic scroll/height-delta compensation.
repository: cline/cline#v28
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70893
---

When a UI viewport must stay stable while content is dynamically added/removed (e.g., streaming chat, virtualized lists), prefer an explicit **reading-anchor algorithm** over heuristic scroll/height-delta compensation.

**Standard**
1. **Define the anchor deterministically from geometry**: on each *user* scroll, compute a “reading anchor” as the deepest content element whose rectangle intersects the viewport’s top edge (or, if in a gap, the first element starting below that edge). Record both:
   - `element` (the anchored DOM element/row)
   - `offsetTop` (the element’s offset relative to the viewport top at the moment it was chosen)
2. **Restore the anchor after any layout/resize**: after resize/re-render, re-locate the same anchor element and adjust `scrollTop` so the element returns to the same `offsetTop`. This ensures “growth below the anchor produces zero drift.”
3. **Make anchor discovery DOM-robust**: do **not** assume fixed wrapper structure (like single-child wrappers). Traverse descendants by **rect intersection** with the viewport top, so sibling nodes (banners/notices) don’t change the selected anchor.

**Why (algorithmic rule)**
- Heuristics based on distance-to-bottom or height deltas can drift when content arrives above/below the reader or when layout includes variable siblings.
- A geometry-based anchor turns stabilization into a repeatable computational procedure.

**Illustrative sketch**
```ts
type ReadingAnchor = { element: Element; offsetTop: number };

type Rect = { top: number; bottom: number };

function rectOf(el: Element): Rect {
  const r = (el as HTMLElement).getBoundingClientRect();
  return { top: r.top, bottom: r.bottom };
}

// Descend from `content` through children whose rect crosses viewportTop.
// Avoid assumptions about wrapper depth/child counts.
function findReadingAnchor(viewport: HTMLElement, content: HTMLElement): ReadingAnchor | null {
  const viewportTop = 0; // relative to viewport: use elRect.top compared to viewport bounds

  let candidates: Element[] = Array.from(content.children);
  let anchored: Element | null = null;

  // Conceptually: keep descending into the best intersecting child until you reach the row.
  while (candidates.length > 0) {
    const intersecting = candidates.filter((c) => {
      const r = rectOf(c);
      return r.bottom > viewportTop && r.top <= viewportTop;
    });

    const next = intersecting.length
      ? intersecting
      : candidates.filter((c) => rectOf(c).top > viewportTop);

    if (next.length === 0) break;

    const chosen = next[0];
    anchored = chosen;

    const children = Array.from(chosen.children);
    candidates = children.length ? children : [];
  }

  if (!anchored) return null;

  const anchoredRect = rectOf(anchored);
  const offsetTop = anchoredRect.top - viewportTop; // record where it sat
  return { element: anchored, offsetTop };
}

function restoreAnchor(viewport: HTMLElement, anchor: ReadingAnchor) {
  // Compute scroll adjustment so anchored element returns to same offsetTop.
  // Implementation depends on how you measure element positions (e.g., using offsetTop + current scrollTop).
  // Pseudocode:
  // const elementOffsetWithinScroll = anchor.element.getBoundingClientRect().top + viewport.scrollTop;
  // viewport.scrollTop = elementOffsetWithinScroll - anchor.offsetTop;
}
```

**Adopt this whenever** your viewport can change height due to streaming, async content, images loading, or dynamic siblings that affect layout. This keeps the “what the user is reading” invariant, which is the core algorithmic requirement.