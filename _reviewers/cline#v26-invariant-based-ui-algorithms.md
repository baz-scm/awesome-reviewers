---
title: Invariant-Based UI Algorithms
description: When implementing non-trivial UI behaviors (holds, streaming scroll,
  shortcut handling), design the logic as an explicit algorithm with clear invariants
  and measurements—don’t infer state from unreliable platform events or fragile assumptions.
repository: cline/cline#v26
label: Algorithms
language: TSX
comments_count: 4
repository_stars: 70893
---

When implementing non-trivial UI behaviors (holds, streaming scroll, shortcut handling), design the logic as an explicit algorithm with clear invariants and measurements—don’t infer state from unreliable platform events or fragile assumptions.

Apply this standard:
- Use measurable state: drive decisions from time/distance/geometry (e.g., performance.now() deltas, scroll distance-from-bottom, viewport-top anchor intersection).
- Track and separate inputs: ensure programmatic actions vs user actions are distinguishable (e.g., internal “our target” state vs reader scroll).
- Use stable anchors for dynamic content: when content changes height/structure, compute a stable reference (e.g., the element being read via viewport-top crossing) and restore it after resize/streaming.
- Coordinate competing handlers: add global suspension/guard state so multiple listeners can’t react simultaneously to the same gesture.
- If you must rely on imperfect signals, document the limitation and keep behavior bounded (e.g., timeouts) rather than producing inconsistent outcomes.

Sketch of the approach (anchor-based, measurement-driven):
```ts
type ReadingAnchor = { element: Element; offsetTop: number };

function findReadingAnchor(viewportEl: HTMLDivElement, contentEl: HTMLDivElement): ReadingAnchor | null {
  // Descend through the DOM to find the deepest child whose row crosses the viewport-top edge,
  // handling sibling wrappers/gaps so the anchor stays stable as layout changes.
  // Return { element, offsetTopRelativeToViewport } when found.
  return null;
}

// On resize/content updates:
// 1) recompute anchor
// 2) restore scrollTop so anchor.offset stays constant
```

This reduces accidental edge cases (missing keyup on macOS, streaming-induced scroll drift, mis-anchoring when banners/siblings exist, and shortcut conflicts) by making the behavior deterministic and testable.