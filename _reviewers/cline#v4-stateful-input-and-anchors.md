---
title: Stateful Input And Anchors
description: 'When implementing interactive behaviors (holds, scrolling, streaming
  updates), treat the feature as a small deterministic algorithm: define explicit
  invariants, separate input sources, and anchor/compensate whenever the underlying
  state changes.'
repository: cline/cline#v4
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70864
---

When implementing interactive behaviors (holds, scrolling, streaming updates), treat the feature as a small deterministic algorithm: define explicit invariants, separate input sources, and anchor/compensate whenever the underlying state changes.

Apply this as a coding standard:
- Use explicit state + invariants
  - Define who “owns” the state (e.g., reader vs programmatic scroll; hold detection vs native shortcut).
  - Maintain termination/timeout conditions using a monotonic clock (e.g., performance.now) and clear reset paths.
- Separate event sources
  - Track whether a change was triggered programmatically (e.g., store a target position) so you don’t misclassify it as user intent.
- Anchor to prevent drift
  - For dynamic geometry (streaming content, resize), store an anchor associated with the reader’s current context and restore it after updates so growth doesn’t move the user.
- Clamp and tolerate precision
  - Clamp computed positions/distances to valid ranges and use small tolerances for “arrival” checks.
- Document unavoidable platform constraints
  - If platform event semantics make a perfect solution impossible, document the limitation and keep behavior safe.

Example pattern (anchor + ownership, analogous to scroll pinning):
```ts
const anchorRef = useRef<{ rowId: string; offset: number } | null>(null);

function onReaderScroll(viewport: HTMLDivElement) {
  // Update anchor only on reader-driven intent
  const row = findTopRowIntersecting(viewport);
  anchorRef.current = { rowId: row.id, offset: row.offsetFromTop };
}

function onContentResizeOrStreamUpdate() {
  // Restore reader’s anchored row after layout changes
  const a = anchorRef.current;
  if (!a) return;
  const rowEl = document.querySelector(`[data-row-id="${a.rowId}"]`);
  if (!rowEl || !viewportRef.current) return;
  const top = computeScrollTopForRowOffset(rowEl, a.offset);
  viewportRef.current.scrollTo({ top: clamp(top), behavior: "auto" });
}
```
This standard prevents common correctness bugs: accidental exits from time-based holds, and scroll drift when content changes asynchronously.