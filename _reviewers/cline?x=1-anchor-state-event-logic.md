---
title: Anchor State Event Logic
description: 'When implementing event-driven behaviors (keyboard holds/shortcuts,
  scroll pinning, streaming UI), treat the logic as an explicit algorithm with:


  - **State + invariants:** Model the behavior with clear states (e.g., idle → tracking
  hold → repeating → done; pinned vs unpinned; ours vs reader’s intent). Drive transitions
  from measurable signals (timestamps,...'
repository: cline/cline?x=1
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70861
---

When implementing event-driven behaviors (keyboard holds/shortcuts, scroll pinning, streaming UI), treat the logic as an explicit algorithm with:

- **State + invariants:** Model the behavior with clear states (e.g., idle → tracking hold → repeating → done; pinned vs unpinned; ours vs reader’s intent). Drive transitions from measurable signals (timestamps, repeat flags, scroll deltas), not from incidental timing.
- **Single gating mechanism:** If the app can enter a mode where handlers must not run (e.g., shortcut recording), use a shared **suspension/lock** that every relevant listener consults, and cancel any in-progress state when gating flips.
- **Anchors over heuristics:** For positioning under asynchronous change (content growth, resize, smooth/programmatic scroll), store an **anchor/target** and restore to it after changes. Distinguish programmatic scrolls from user intent so your own updates don’t re-trigger your heuristics.

Example pattern (scroll anchoring + programmatic separation):
```ts
const pinnedRef = useRef(true);
const ourScrollTarget = useRef<number | null>(null);

function onScroll() {
  // If we initiated the scroll, ignore intermediate events.
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived) ourScrollTarget.current = null;
    if (arrived || pinnedRef.current) return;
    ourScrollTarget.current = null;
  }
  const distance = viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight;
  pinnedRef.current = distance <= PINNED_THRESHOLD_PX;
}

function writeScrollTop(top: number) {
  const clampedTop = clamp(top);
  ourScrollTarget.current = clampedTop !== viewport.scrollTop ? clampedTop : null;
  viewport.scrollTo({ top: clampedTop, behavior: 'auto' });
}
```

Apply this standard to keyboard/shortcut logic (derive hold/stop from timestamps + repeat signals; globally suspend during recording) and to UI positioning logic (use an anchor/target and cancel/restore across async change).