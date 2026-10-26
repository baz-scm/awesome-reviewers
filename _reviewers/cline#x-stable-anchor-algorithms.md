---
title: Stable Anchor Algorithms
description: 'When UI content changes dynamically (streaming, async inserts, resizes),
  treat scroll anchoring as an algorithmic “stable reference” problem.


  **Standard**'
repository: cline/cline#x
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70861
---

When UI content changes dynamically (streaming, async inserts, resizes), treat scroll anchoring as an algorithmic “stable reference” problem.

**Standard**
1. **Model a stable anchor**: capture an anchor as `{ element, offsetTop }` (or equivalent) derived from the reader’s current view.
2. **Update anchor on reader intent** (e.g., their own scroll), not on every programmatic scroll.
3. **Restore using the anchor, not scrollTop deltas**: after resize/content updates, recompute/restore scroll position so the anchor element stays at the same offset.
4. **Compute the anchor robustly**: select the element using **geometry** (e.g., “the first child whose rect crosses the viewport top edge”) and **don’t assume uniform DOM wrappers**—handle siblings, banners/notices, and gaps.
5. **Test the algorithm with structure and direction changes**:
   - Growth **below** the anchor should not drift the reader.
   - Growth **above** the anchor should be absorbed so the same row remains in view.
   - DOM variations: list inside containers with siblings.

**Example (anchor selection via geometric descent)**
```ts
type ReadingAnchor = { element: Element; offsetTop: number };

function findReadingAnchor(viewportEl: HTMLDivElement, contentEl: HTMLDivElement): ReadingAnchor | null {
  // Start from the content root and descend until the deepest relevant element.
  let node: Element = contentEl;

  while (node.children.length > 0) {
    const children = Array.from(node.children) as Element[];

    // Choose the first child whose bottom edge is below the viewport top.
    const viewportTop = viewportEl.getBoundingClientRect().top;
    const crossed = children
      .map((c) => {
        const r = c.getBoundingClientRect();
        return { c, bottom: r.bottom };
      })
      .find(({ bottom }) => bottom >= viewportTop);

    // If nothing crosses (gap/end), pick the first child (or stop).
    const next = crossed?.c ?? children[0];
    if (!next) break;

    node = next;

    // Stop when we’re at the row/list item granularity expected by the caller.
    // (In practice: stop at known row containers or when single-element wrappers end.)
    if (node.childElementCount === 0) break;
  }

  const anchorRect = node.getBoundingClientRect();
  const vpRect = viewportEl.getBoundingClientRect();
  const offsetTop = anchorRect.top - vpRect.top;
  return { element: node, offsetTop };
}
```

Apply this standard any time you need deterministic “what the user is reading” stability under changing layout: it prevents drift and reduces sensitivity to DOM structure assumptions by turning the problem into a robust reference-selection + restore algorithm.