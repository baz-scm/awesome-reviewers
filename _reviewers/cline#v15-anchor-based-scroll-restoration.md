---
title: Anchor-Based Scroll Restoration
description: 'When implementing scroll behavior for dynamically growing content (e.g.,
  streaming chat), treat scroll preservation as an explicit algorithm:


  - **Anchor, don’t guess:** Remember a stable reference (e.g., the content row intersecting
  the viewport top + its offset) at the moment the user changes intent. Restore using
  that anchor after layout/resize so growth...'
repository: cline/cline#v15
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70877
---

When implementing scroll behavior for dynamically growing content (e.g., streaming chat), treat scroll preservation as an explicit algorithm:

- **Anchor, don’t guess:** Remember a stable reference (e.g., the content row intersecting the viewport top + its offset) at the moment the user changes intent. Restore using that anchor after layout/resize so growth below the anchor produces **zero drift**.
- **Restore only when feasible:** If the stored target depends on container size, defer restoration until `scrollHeight - clientHeight` can actually reach the desired position (otherwise retry on subsequent resize/updates).
- **Gate state transitions by verified user intent:** Only unpin/pin based on the user’s actual input source (e.g., ignore key events coming from focused child controls). Also separate programmatic scrolls from user scrolls so you don’t misclassify event streams.

Example shape (self-contained):
```ts
type Anchor = { rowId: string; offsetPx: number };

function restoreIfFeasible(viewport: HTMLDivElement, anchor: Anchor, getRowTopPx: (id: string) => number) {
  const maxTop = Math.max(0, viewport.scrollHeight - viewport.clientHeight);
  const targetTop = getRowTopPx(anchor.rowId) + anchor.offsetPx;
  if (targetTop > maxTop) return false; // not ready; retry later on next resize

  viewport.scrollTo({ top: Math.min(targetTop, maxTop), behavior: 'auto' });
  return true;
}

function shouldUnpinFromKey(event: KeyboardEvent, viewport: HTMLDivElement) {
  // Unpin only when the event truly comes from the scroll container.
  return event.target === viewport && ['ArrowUp','PageUp','Home'].includes(event.key);
}
```
Applying this standard prevents drift, avoids premature restores during intermediate layout states, and makes the pinned/unpinned state machine robust to real-world focus and event targeting.