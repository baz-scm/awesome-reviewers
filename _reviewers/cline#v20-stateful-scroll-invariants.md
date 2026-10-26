---
title: Stateful scroll invariants
description: 'When implementing scroll/viewport behavior under incremental updates
  (streaming content, resize, async events), treat it like a small stateful algorithm:'
repository: cline/cline#v20
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70886
---

When implementing scroll/viewport behavior under incremental updates (streaming content, resize, async events), treat it like a small stateful algorithm:
- Define and preserve an explicit invariant (e.g., “the reader’s anchored row stays at the same offset; no drift when content grows below”).
- Use anchor-based restoration instead of ad-hoc delta compensation when the invariant is “no movement under certain growth.”
- Make restoration conditional and readiness-aware: if you must restore a remembered position/offset, defer applying it until the scrollable range can actually reach it; retry on resize and clear the pending restore after success.
- Guard state transitions: only unpin/pin in response to the correct input source (e.g., keyboard events aimed at the viewport itself, not focused child controls).
- Clamp all computed scrollTop values to the valid range and centralize “write scroll” logic.

Example pattern (self-contained):
```ts
const pinnedRef = useRef(true);
const pendingRestoreRef = useRef<{top:number}|null>(null);
const viewportRef = useRef<HTMLDivElement|null>(null);

function clampTop(v: HTMLDivElement, top: number) {
  const maxTop = Math.max(0, v.scrollHeight - v.clientHeight);
  return Math.min(Math.max(0, top), maxTop);
}

function writeTop(v: HTMLDivElement, top: number, behavior: ScrollBehavior) {
  v.scrollTo({ top: clampTop(v, top), behavior });
}

// Guarded transition: only viewport-scoped key handling triggers unpin
function onKeyDown(e: KeyboardEvent) {
  const v = viewportRef.current;
  if (!v) return;
  if (e.target !== v) return;
  if (['ArrowUp','PageUp','Home'].includes(e.key)) pinnedRef.current = false;
}

// Conditional restoration: apply only when range is sufficient; retry on resize
function tryRestore() {
  const v = viewportRef.current;
  const pending = pendingRestoreRef.current;
  if (!v || !pending) return;
  const maxTop = v.scrollHeight - v.clientHeight;
  if (maxTop < pending.top) return; // not ready yet
  writeTop(v, pending.top, 'auto');
  pendingRestoreRef.current = null;
}
```
Adopt this approach to avoid subtle correctness bugs caused by asynchronous UI evolution (streaming + resize + mixed input targets) and to make the behavior testable with cases like “growth below anchor does not move the reader” and “restore waits until the transcript is tall enough.”