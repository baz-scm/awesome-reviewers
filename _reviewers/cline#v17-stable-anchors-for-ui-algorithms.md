---
title: Stable Anchors For UI Algorithms
description: 'When implementing event-driven UI behaviors that depend on asynchronous
  updates (streaming content, resize observers, smooth scrolling), treat the logic
  like an algorithmic state machine: define a stable invariant and ensure state transitions
  are triggered only by intended user inputs.'
repository: cline/cline#v17
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70883
---

When implementing event-driven UI behaviors that depend on asynchronous updates (streaming content, resize observers, smooth scrolling), treat the logic like an algorithmic state machine: define a stable invariant and ensure state transitions are triggered only by intended user inputs.

Apply this standard:
1. **Anchor the invariant**: If content growth can occur above/below the user, compute and store a stable reference (e.g., an anchor row intersecting the viewport top + its offset). On every resize/content change, restore the user’s view so growth *below* doesn’t drift them and growth *above* is compensated.
2. **Use explicit state transitions**: Model “pinned/unpinned” (or equivalent) as state, and update it using clear rules (e.g., reaching bottom re-pins; specific user actions un-pin).
3. **Validate event provenance**: Guard transitions so only the correct event source triggers state changes. For keyboard-driven unpinning, check that the event originated from the intended element (e.g., `event.target === viewport`) to avoid stealing focus-based interactions from child controls.
4. **Test invariant scenarios**: Include cases for (a) content growing below while unpinned, (b) content height changes above while the reader is positioned, and (c) keyboard input aimed at focused descendants.

Example pattern (self-contained):
```ts
const [pinned, setPinned] = useState(true);
const pinnedRef = useRef(pinned);
pinnedRef.current = pinned;

// Example anchor: store a stable reference + offset when unpinned.
const anchorRef = useRef<{topRowId: string; offsetPx: number} | null>(null);

function handleReaderScroll() {
  const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
  const nextPinned = distanceFromBottom <= PINNED_THRESHOLD_PX;
  setPinned(nextPinned);

  if (!nextPinned) {
    // Compute anchor from current viewport position.
    anchorRef.current = {
      topRowId: findRowAtViewportTop(el),
      offsetPx: computeOffsetFromViewportTop(el),
    };
  }
}

function handleResizeOrStream() {
  if (!anchorRef.current) return;
  if (pinnedRef.current) {
    scrollToBottom('auto');
    return;
  }

  // Restore the anchored row to the same offset.
  const { topRowId, offsetPx } = anchorRef.current;
  const restoredTop = computeScrollTopForRowOffset(topRowId, offsetPx);
  writeScrollTop(el, restoredTop, 'auto');
}

function handleKeyDown(e: KeyboardEvent) {
  // Only unpin for keys targeted at the scroll container.
  if (e.target !== el) return;
  if (['ArrowUp', 'PageUp', 'Home'].includes(e.key)) setPinned(false);
}
```
This approach prevents drift caused by asynchronous layout changes and avoids incorrect state transitions caused by events originating from focused child elements—turning UI behavior into a predictable, testable algorithm.