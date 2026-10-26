---
title: Anchor-based scroll restoration
description: 'When implementing dynamic scrolling UIs (streaming chat, feeds), treat
  scroll-state as an algorithmic problem: use an explicit *reading anchor* (the element
  the user is “looking at” plus its offset) and restore that anchor across resizes/content
  growth. Avoid naive scrollTop/delta compensation, and make anchor detection resilient
  to real DOM nesting.'
repository: cline/cline#v27
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70892
---

When implementing dynamic scrolling UIs (streaming chat, feeds), treat scroll-state as an algorithmic problem: use an explicit *reading anchor* (the element the user is “looking at” plus its offset) and restore that anchor across resizes/content growth. Avoid naive scrollTop/delta compensation, and make anchor detection resilient to real DOM nesting.

Apply these rules:
1. **Use an anchor model, not height deltas**
   - On user scroll, compute a *ReadingAnchor* = (element, offsetTopWithinViewport).
   - On content resize/streaming updates, restore the same element to the remembered offset so growth *below* doesn’t drift the reader.

2. **Pin/unpin via thresholds, and unpin on input**
   - Maintain a `pinned` state based on distance-from-bottom (threshold).
   - Unpin on *user intent* (wheel up / ArrowUp / PageUp / Home), not on the asynchronous scroll event that that input generates.

3. **Ignore programmatic scroll events**
   - Track programmatic scrolling with a `ourScrollTarget` (expected `scrollTop`) and suppress interpreting intermediate scroll events as user movement until the target is reached.

4. **Anchor detection must handle real DOM**
   - Don’t assume single-child wrappers. Traverse descendants from the content root through whichever child rect crosses the viewport top edge, and anchor on the deepest matching row.
   - Support sibling layout changes (banners/notices/column+list shapes) without changing the anchored “row being read.”

5. **Test the algorithm with growth scenarios**
   - Add tests for “growth below reader keeps row under reader” and “growth above reader is absorbed without snapping/drift.” Include delayed restoration when container height changes haven’t reached the target yet.

Self-contained sketch:
```ts
type ReadingAnchor = { element: Element; offsetTop: number };

function distanceFromBottom(v: HTMLDivElement) {
  return v.scrollHeight - v.scrollTop - v.clientHeight;
}

function findReadingAnchor(viewport: HTMLDivElement, content: HTMLDivElement): ReadingAnchor | null {
  // Traverse descendants (don’t assume single-child wrappers) and find
  // the deepest element whose bottom is below viewportTop (or first that starts below in a gap).
  // Return { element, offsetTop: elementRect.top - viewportRect.top }.
  return null;
}

function restoreAnchor(viewport: HTMLDivElement, anchor: ReadingAnchor, behavior: ScrollBehavior) {
  const rect = anchor.element.getBoundingClientRect();
  const viewportRect = viewport.getBoundingClientRect();
  const desiredTop = viewport.scrollTop + (rect.top - viewportRect.top) - anchor.offsetTop;
  const maxTop = Math.max(0, viewport.scrollHeight - viewport.clientHeight);
  viewport.scrollTo({ top: Math.min(Math.max(0, desiredTop), maxTop), behavior });
}
```

Following this standard will produce drift-free reading during streaming and ensure correctness across diverse DOM structures and event timing.