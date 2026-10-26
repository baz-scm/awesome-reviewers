---
title: Use State Invariants
description: 'When behavior depends on time, input, or changing layout, design it
  as an explicit algorithm with clear invariants and ownership rules.


  Apply this standard:'
repository: cline/cline#v13
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70874
---

When behavior depends on time, input, or changing layout, design it as an explicit algorithm with clear invariants and ownership rules.

Apply this standard:
- State & invariants: Define the states (e.g., pinned/unpinned, holding/tapping, anchored/unanchored) and the invariant that must always hold.
- Source ownership: Distinguish user-driven events from programmatic ones (track a target/intent marker so your own scrolls don’t look like reader intent).
- Measurement-based transitions: Use geometry/time measurements with thresholds/tolerances to drive transitions (e.g., distance-from-bottom, elapsed-time gaps, anchor element selection).
- Robustness to missing signals: If the OS/browser can’t provide a needed event, use a deterministic fallback and document the limitation (e.g., rely on auto-repeat timing instead of keyup).
- Layout-structure independence: Anchor/position-finding algorithms must not assume a fixed wrapper tree; traverse/compute based on actual rect crossings.
- Test the edge cases that break naive assumptions (focused child controls shouldn’t unpin; siblings/wrappers shouldn’t change the anchor result; OS-specific key behavior).

Example pattern (ownership marker + measurement-driven transition):
```ts
const ourScrollTarget = useRef<number | null>(null);

function scrollToBottom(viewport: HTMLDivElement) {
  ourScrollTarget.current = viewport.scrollHeight; // mark intent
  viewport.scrollTo({ top: viewport.scrollHeight, behavior: "smooth" });
}

function onScroll(viewport: HTMLDivElement) {
  // Ignore our own programmatic scroll until we arrive.
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (!arrived && /* still ours */ true) return;
    if (arrived) ourScrollTarget.current = null;
  }

  const distance = viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight;
  const pinned = distance <=  /* threshold */ 16;
  setPinned(pinned);
}
```
This approach keeps algorithms correct as content streams, layouts change, and event delivery is imperfect.