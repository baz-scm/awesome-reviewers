---
title: Anchor-driven UI algorithms
description: 'When UI behavior depends on asynchronous input (user vs programmatic),
  platform event gaps, or layout changes, design the logic as an explicit algorithm
  with:'
repository: cline/cline#v16
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70882
---

When UI behavior depends on asynchronous input (user vs programmatic), platform event gaps, or layout changes, design the logic as an explicit algorithm with:

- **State invariants:** decide which actor “owns” the state (e.g., reader owns scroll position; programmatic scroll is tracked separately) and enforce it in your event handlers.
- **Origin classification:** never infer intent from raw events alone—track programmatic targets so smooth-scrolling emits events that won’t accidentally override user state.
- **Geometry-based anchors:** for correctness under resize/content growth, compute an **anchor** from viewport geometry (e.g., which row is being read, plus its offset), then restore to that anchor after DOM height changes. Avoid brittle assumptions like “single height-delta always applies.”
- **Explicit stop conditions + documented limitations:** if a platform omits key signals, encode the workaround in code with clear termination conditions and document the tradeoff.

Example pattern (reading-anchor + restore) 
```ts
type ReadingAnchor = { node: Element; offsetTop: number };

function findReadingAnchor(viewport: HTMLDivElement, content: HTMLDivElement): ReadingAnchor | null {
  // Descend through wrapper DOM to the deepest element intersecting the viewport-top edge.
  // Also handle gaps by anchoring the first child that starts below the edge.
  // (Implementation must not assume single-child wrappers.)
  let list: Element = content;
  while (list.children.length) {
    if (list.children.length !== 1) break;
    list = list.children[0];
  }
  // Select the element whose bottom edge is below viewport-top, then use its rect offset.
  // ...compute and return { node: deepestRow, offsetTop }
  return null;
}

function restoreAfterResize(viewport: HTMLDivElement, content: HTMLDivElement, anchor: ReadingAnchor) {
  // Recompute the node’s position after layout changes and set scrollTop to keep
  // the reader’s anchored row at the same viewport offset.
  const rect = anchor.node.getBoundingClientRect();
  const viewportTop = viewport.getBoundingClientRect().top;
  const targetScrollTop = viewport.scrollTop + (rect.top - viewportTop) + anchor.offsetTop;
  viewport.scrollTo({ top: Math.max(0, targetScrollTop), behavior: 'auto' });
}
```

Apply this standard when you see:
- “pinned/unpinned” or “follow bottom” logic
- smooth scrolling that triggers many intermediate events
- resize/content-streaming drift bugs
- keyboard/hold behaviors relying on missing OS signals

Also add tests that reproduce drift scenarios (content grows above/below, siblings/wrappers change anchor selection, smooth scroll mid-flight while the user unpins).