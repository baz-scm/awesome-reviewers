---
title: UI Algorithms With Invariants
description: When implementing event-driven UI behaviors that must remain correct
  under timing issues and dynamic DOM updates, design the logic as an algorithm with
  explicit invariants and ownership of state transitions.
repository: Cline/Cline
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70840
---

When implementing event-driven UI behaviors that must remain correct under timing issues and dynamic DOM updates, design the logic as an algorithm with explicit invariants and ownership of state transitions.

Apply this pattern:
1) Define an invariant (what must remain true) and enforce it from reliable signals.
   - Example invariant: “The row the reader is currently viewing must not move when content changes elsewhere.”
2) Attribute events to the correct actor (user vs programmatic / reliable vs missing).
   - Track “our” scroll target or intent so programmatic scroll events don’t unpin/alter state.
   - If the platform can’t provide a needed event (e.g., key-up), document the limitation and use an alternative reliable signal (e.g., repeat-gap + timeout thresholds).
3) For drift under content growth, use measurement-based anchoring rather than global height deltas.
   - Identify a stable “reading anchor” element (robustly, even with varying wrappers/siblings), store its offset, and after resize restore scrollTop so that anchor stays at the same viewport offset.
4) Add tests that reproduce the problematic shapes/timing:
   - streaming under reader, content added above/below, and DOM structures with siblings/wrappers.

Minimal example (anchor-based stabilization sketch):
```ts
type Anchor = { element: Element; offsetTop: number };

function findAnchor(viewport: HTMLDivElement, content: HTMLDivElement): Anchor | null {
  // Descend through wrappers regardless of structure; pick the deepest child
  // whose bottom edge crosses the viewport top (or the first child below if in a gap).
  // Return element + its offsetTop relative to viewport.
  return null;
}

function restoreAnchorScroll(viewport: HTMLDivElement, content: HTMLDivElement, anchor: Anchor) {
  const elRect = anchor.element.getBoundingClientRect();
  const viewportRect = viewport.getBoundingClientRect();
  const currentOffset = elRect.top - viewportRect.top;
  const delta = currentOffset - anchor.offsetTop;
  viewport.scrollTop += delta; // clamp as needed
}

// On resize/content mutation:
// - recompute anchor only when appropriate
// - restore scrollTop to keep invariant
```

Coding standard takeaway: UI “correctness” should be expressed as invariants + ownership + measurement-based anchoring, not as ad-hoc event handling and one-off deltas.