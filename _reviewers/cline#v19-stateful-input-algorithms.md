---
title: Stateful Input Algorithms
description: 'When implementing interactive UI behaviors (keyboard shortcuts, scrolling/streaming
  readers), treat the behavior as an explicit algorithm/state machine: define invariants,
  distinguish intent sources, and guard side-effects so unrelated events can’t “pollute”
  the state.'
repository: cline/cline#v19
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70885
---

When implementing interactive UI behaviors (keyboard shortcuts, scrolling/streaming readers), treat the behavior as an explicit algorithm/state machine: define invariants, distinguish intent sources, and guard side-effects so unrelated events can’t “pollute” the state.

Apply these rules:
1) Explicitly separate user intent vs programmatic/other intent
- Track the origin of changes (e.g., “our pending scroll target” vs “reader input”).
- Only allow state transitions (pin/unpin, act on key) from the intended source.

2) Use gating/suspension flags for global handlers
- If a mode (e.g., recording) requires exclusive control, suspend other handlers while the mode is active.
- Ensure every competing handler consults the same flag.
- Prevent event leakage with stopImmediatePropagation() when needed.

3) Preserve stable anchors across async changes
- For streaming content/resizes, avoid approximate “delta” logic that drifts.
- Record a stable reading anchor (e.g., row intersecting viewport top + its offset) and restore to the same anchor position after updates.

4) Make termination/cleanup deterministic
- Cancel pending operations/timers when leaving the mode/state.
- Clear targets/anchors when the algorithm reaches its settled state.

Example pattern (conceptual):
```ts
// 1) Guard competing handlers with a shared flag
let shortcutsSuspended = false;

function setRecording(active: boolean) {
  shortcutsSuspended = active;
}

window.addEventListener('keydown', (e) => {
  if (shortcutsSuspended) return; // invariant: recording owns the key
  // handle normal shortcuts
});

// 2) Track intended target to disambiguate scroll events
const pendingScrollTarget = { current: null as number | null };
let pinned = true;

function scrollProgrammaticallyToBottom(viewport: HTMLDivElement) {
  pinned = true;
  pendingScrollTarget.current = viewport.scrollHeight;
  viewport.scrollTo({ top: viewport.scrollHeight, behavior: 'smooth' });
}

viewport.addEventListener('scroll', () => {
  // invariant: if this scroll is still due to our pending target, ignore it for pin/unpin
  if (pendingScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - pendingScrollTarget.current) <= 1;
    if (arrived || pinned) {
      if (arrived) pendingScrollTarget.current = null;
      return;
    }
    pendingScrollTarget.current = null;
  }
  // state transition only from user intent
  pinned = /* distance/anchor logic */ true;
});

// 3) On content resize/streaming: restore from an anchor instead of height deltas
// (store anchor row+offset while unpinned; after resize, find same row and offset)
```

Following this approach turns fragile event/async interactions into a predictable, testable algorithm with clear invariants—reducing “random” bugs like accidental shortcut triggering, mis-detected user intent, and scroll drift during streaming updates.