---
title: Deterministic Interaction State
description: 'When implementing UI behaviors that depend on continuous input (key
  holds, scrolling, streaming updates, resize), treat the logic as a deterministic
  state machine: define explicit state, maintain invariants, and only transition state
  based on semantically correct event sources.'
repository: cline/cline#v23
label: Algorithms
language: TSX
comments_count: 3
repository_stars: 70889
---

When implementing UI behaviors that depend on continuous input (key holds, scrolling, streaming updates, resize), treat the logic as a deterministic state machine: define explicit state, maintain invariants, and only transition state based on semantically correct event sources.

Apply these rules:
- Separate intent from side effects: track whether an event came from the user (intent) or your own code (effect). Don’t infer user intent from the resulting state changes if those changes can also be caused programmatically or asynchronously.
- Use ownership/targets: when driving scroll (or similar), store an “expected target/anchor” and ignore intermediate events unless they match your invariants; clear the target only when you know you’ve arrived.
- Unpin/stop on the right signals: if downstream async work will produce events, update state on input events (wheel/key/tap/keydown targeting the right element) rather than on the later “settled” event that can be polluted by streaming/resizes.
- Prevent drift with anchors: for content growth/resizes, rely on a stable reference (e.g., the item under the viewport top plus offset) and restore that reference after resize; avoid fragile delta-only compensation.
- Handle platform constraints explicitly: if the platform can’t provide a required signal (e.g., missing keyup vs key-repeat differences), document the limitation and define safe fallbacks/stop conditions rather than attempting unreliable detection.

Example pattern (scroll ownership):
```ts
// Invariant: ourScrollTarget represents the active programmatic scroll.
const ourScrollTarget = useRef<number | null>(null);

function writeScrollTop(el: HTMLDivElement, top: number, behavior: ScrollBehavior) {
  const clamped = Math.min(Math.max(0, top), el.scrollHeight - el.clientHeight);
  ourScrollTarget.current = clamped !== el.scrollTop ? clamped : null;
  el.scrollTo({ top: clamped, behavior });
}

function onScroll() {
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(el.scrollTop - ourScrollTarget.current) <= 1;
    // Until arrived, treat scroll as programmatic unless the user unpins.
    if (arrived || pinnedRef.current) {
      if (arrived) ourScrollTarget.current = null;
      return;
    }
    ourScrollTarget.current = null; // user interrupted
  }
  // Update pinned/unpinned based on distance-to-bottom, then emit state.
}
```

Use the same approach for key-hold/quit logic: explicitly maintain hold state (start time, last event, repeating/tick), define stop conditions (e.g., repeat gap/timeout), and document any OS-level ambiguity you can’t resolve.
