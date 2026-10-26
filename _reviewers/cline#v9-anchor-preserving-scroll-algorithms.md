---
title: Anchor-Preserving Scroll Algorithms
description: When UI state depends on dynamic content and layout changes (e.g., streaming
  chat, virtualized lists), implement scroll/viewport behavior with an explicit algorithm
  that preserves a clear invariant (an anchor), and only transitions state on intended
  inputs.
repository: cline/cline#v9
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70868
---

When UI state depends on dynamic content and layout changes (e.g., streaming chat, virtualized lists), implement scroll/viewport behavior with an explicit algorithm that preserves a clear invariant (an anchor), and only transitions state on intended inputs.

**Standard**
1. **Preserve an invariant via an anchor**: Track a stable reference point in the content (e.g., the first row intersecting the viewport top + its offset). After any resize/content growth, restore the viewport so that the anchored row remains at the same offset. Avoid relying on fragile heuristics like “height delta compensation” when you can instead directly re-establish the invariant.
2. **Clamp and deterministically compute targets**: When writing scrollTop, clamp to valid ranges and treat the computed scroll target as the source of truth.
3. **Model as pinned/unpinned state with guarded transitions**: Use an internal state model (pinned vs unpinned) and change it only on the correct user intents. For keyboard/mouse/touch handlers, gate transitions by event target/context so focused child controls don’t accidentally trigger state changes.

**Sketch (anchor + guarded transition)**
```ts
// Anchor invariant: keep the anchored row at the same offset after resizes.
let anchorEl: HTMLElement | null = null;
let anchorOffsetPx = 0;

function captureAnchor(viewportTop: number, container: HTMLElement) {
  const firstRow = [...container.children]
    .find(el => el instanceof HTMLElement && el.offsetTop <= viewportTop);
  if (!firstRow) return;
  anchorEl = firstRow as HTMLElement;
  anchorOffsetPx = viewportTop - anchorEl.offsetTop;
}

function restoreAnchor(container: HTMLElement, scrollContainer: HTMLDivElement) {
  if (!anchorEl) return;
  const desiredTop = anchorEl.offsetTop + anchorOffsetPx;
  const maxTop = Math.max(0, scrollContainer.scrollHeight - scrollContainer.clientHeight);
  const clampedTop = Math.min(Math.max(0, desiredTop), maxTop);
  scrollContainer.scrollTop = clampedTop;
}

function onKeyDown(e: KeyboardEvent, viewport: HTMLDivElement, setPinned: (v:boolean)=>void) {
  // Guard: only unpin when the key event is intended for the viewport.
  if (e.target !== viewport) return;
  if (['ArrowUp','PageUp','Home'].includes(e.key)) setPinned(false);
}
```

Applying this standard reduces “scroll drift” bugs and prevents accidental state transitions caused by asynchronous rendering or events targeted at child controls.