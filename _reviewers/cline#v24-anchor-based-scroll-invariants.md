---
title: Anchor-Based Scroll Invariants
description: 'When implementing scroll behavior that must remain stable during async
  updates (streaming, resize, virtualized content), treat it as an explicit algorithm
  with invariants:'
repository: cline/cline#v24
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70891
---

When implementing scroll behavior that must remain stable during async updates (streaming, resize, virtualized content), treat it as an explicit algorithm with invariants:

- Use a durable reading anchor: compute and store a reference position (e.g., the first visible item/row intersecting the viewport top plus its offset) on user-driven scroll.
- Restore the anchor after DOM/layout changes: on resize/content growth, re-position scroll so the anchored row remains at the same offset (avoids “drift” from naive scrollTop delta compensation).
- Model state transitions carefully: only the intended user actions should move the state (e.g., pinned/unpinned). Don’t let unrelated inputs (focused child controls, programmatic scroll events, async event ordering) trigger incorrect transitions.
- Gate event-driven transitions by validated targets/sources (e.g., only un-pin on arrow/page navigation when the event is targeted at the viewport, not a focused button inside it).
- Add invariant tests: e.g., “row under the reader stays in place when content below grows” and “absorbs height change above without moving the reader.”

Example pattern (self-contained):
```ts
// Pseudocode: anchor-based, drift-free restore
type Anchor = { rowId: string; offset: number };

function onReaderScroll(viewport, items): Anchor {
  const firstRow = items.find(r => r.elementTop <= viewport.top && r.nextTop > viewport.top);
  const offset = viewport.top - firstRow.elementTop;
  // record anchor only for user/reader scroll
  return { rowId: firstRow.id, offset };
}

function onContentResizeOrMutation(viewport, items, anchor: Anchor | null) {
  if (!anchor) return;
  const row = items.find(r => r.id === anchor.rowId);
  if (!row) return;
  // restore: keep the same row under the reader at the same offset
  viewport.scrollTo({ top: row.elementTop + anchor.offset, behavior: 'auto' });
}

function onKeyDown(e, viewport, setPinned) {
  // gate transition: only unpin if key targets the viewport, not a focused child control
  if (e.target !== viewport) return;
  if (['ArrowUp','PageUp','Home'].includes(e.key)) setPinned(false);
}
```
Applying this standard makes the “scroll ownership” algorithm robust, deterministic, and testable—even under continuous streaming and complex focus/event scenarios.