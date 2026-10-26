---
title: Stateful UI Invariants
description: When implementing interactive UI logic (especially under unreliable event
  delivery or constantly changing content), write it as an explicit algorithm with
  clear invariants.
repository: cline/cline#v5
label: Algorithms
language: TSX
comments_count: 2
repository_stars: 70864
---

When implementing interactive UI logic (especially under unreliable event delivery or constantly changing content), write it as an explicit algorithm with clear invariants.

Core rules:
1) Define the invariant up front (e.g., “the reader’s anchor row stays under the reader during streaming”, or “a quit hold must be distinguished from a tap”).
2) Separate user intent from programmatic effects using explicit sentinels/targets (e.g., store a “ourScrollTarget” and ignore scroll events until the target is reached; track “hold repeating” from auto-repeat).
3) Use robust termination/timeout conditions rather than assuming event symmetry (e.g., stop tracking after a repeat gap; stop pinning/unpinning based on measured distance/arrival).
4) Compensate for changing underlying reality (DOM resize/streaming) with an anchoring strategy so observers don’t introduce drift (e.g., restore scrollTop by height delta or anchored row+offset).
5) If a platform limitation makes a fully correct solution unsafe, keep the safe behavior and document the limitation (e.g., relying on repeat to distinguish hold vs tap on macOS).

Example pattern (scroll “owned position” with a sentinel):
```ts
const ourScrollTarget = useRef<number | null>(null);

function scrollToBottom(behavior: ScrollBehavior) {
  if (!viewport) return;
  // Pin intent immediately; mark programmatic target.
  ourScrollTarget.current = viewport.scrollHeight;
  setPinned(true);
  viewport.scrollTo({ top: viewport.scrollHeight, behavior });
}

function onScroll() {
  // Ignore intermediate events while the user hasn’t unpinned.
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (!arrived && pinnedRef.current) return;
    if (arrived) ourScrollTarget.current = null;
  }
  // Now compute state based on measured distance/invariant.
  const distance = viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight;
  setPinned(distance <= PINNED_THRESHOLD_PX);
}
```

Adopt this standard for algorithmic UI features (keyboard-hold, scroll anchoring, streaming updates) to prevent misclassification, drift, and accidental actions.