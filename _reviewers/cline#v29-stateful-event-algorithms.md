---
title: Stateful Event Algorithms
description: When behavior depends on asynchronous inputs (user scrolls, streaming
  content, auto-repeat keys, resize events), implement an explicit state model with
  clear invariants and event tagging—don’t infer intent from raw event order alone.
repository: cline/cline#v29
label: Algorithms
language: TSX
comments_count: 4
repository_stars: 70893
---

When behavior depends on asynchronous inputs (user scrolls, streaming content, auto-repeat keys, resize events), implement an explicit state model with clear invariants and event tagging—don’t infer intent from raw event order alone.

Apply this by:
- Define state and transitions (e.g., pinned/unpinned; holding progress; “ours” vs “reader”).
- Tag or anchor programmatic actions/events so their resulting emitted events can’t be misclassified (e.g., track a target scrollTop and ignore/handle scroll events until arrival).
- For continuous/streaming layout changes, prevent drift by using an anchor and restoring relative position after resize/height changes.
- Scope inputs to avoid false positives (e.g., only unpin on key events that originate from the intended target; ignore when a focused child control handles the key).
- Use thresholds/timeouts only as part of the state model, and document any platform limitations where the data is fundamentally unavailable.

Example pattern (scroll “tagging” + pinned invariant):
```ts
const pinnedRef = useRef(true);
const ourScrollTarget = useRef<number | null>(null);

function writeScrollTop(el: HTMLDivElement, top: number) {
  const maxTop = el.scrollHeight - el.clientHeight;
  const clamped = Math.min(Math.max(0, top), maxTop);
  ourScrollTarget.current = clamped !== el.scrollTop ? clamped : null;
  el.scrollTo({ top: clamped, behavior: 'smooth' });
}

function onScroll() {
  // If the scroll is the result of our tagged action, don’t treat it as user intent.
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (arrived || pinnedRef.current) {
      if (arrived) ourScrollTarget.current = null;
      return;
    }
    ourScrollTarget.current = null;
  }
  // Otherwise, classify user intent by distance-to-bottom and update state.
  const distance = viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight;
  pinnedRef.current = distance <= PINNED_THRESHOLD_PX;
}
```

Teams should treat this as an algorithms requirement: specify invariants (“pinned means reader hasn’t intentionally left bottom”; “anchors prevent drift”; “programmatic scroll events are never treated as user intent”) and encode them with state + tagging rather than ad-hoc heuristics.