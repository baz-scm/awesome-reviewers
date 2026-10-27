---
title: Defer Derived Work Safely
description: 'When introducing concurrency/async behavior, make the boundary explicit:

  - Keep user-facing controlled state updates synchronous so UI stays responsive.'
repository: facebook/react#b11
label: Concurrency
language: JavaScript
comments_count: 6
repository_stars: 251894
---

When introducing concurrency/async behavior, make the boundary explicit:
- Keep user-facing controlled state updates synchronous so UI stays responsive.
- Defer expensive derived computation to transition/low priority (or a deferred derived value) so it can’t block the update that changes the input.
- Use scheduling primitives that reflect the intended semantics (microtask vs task). Avoid “always sync” scheduleWork/scheduleMicrotask except for narrow requirements, and avoid constructing never-resolving promises.

Example pattern (sync input, deferred derived work):

```js
function useSearch(searchText, rootID, selectedCommitIndex, didRecordCommits) {
  // Controlled input update stays sync
  const setSearchTextState = useStateSetter();

  const deferredText = useDeferredValue(searchText); // transition priority

  const searchResults = useMemo(() => {
    if (deferredText === '' || rootID == null || selectedCommitIndex == null || !didRecordCommits) {
      return [];
    }

    // expensive tree walk here
    return computeMatches(deferredText, rootID, selectedCommitIndex);
  }, [deferredText, rootID, selectedCommitIndex, didRecordCommits]);

  return { setSearchTextState, searchResults };
}
```

Scheduling guidelines:
- Prefer `queueMicrotask` for microtasks when available; otherwise fall back to `Promise.resolve().then(callback)` with error forwarding.
- Never return “never resolved” promises as placeholders; use `Promise.resolve()` when you need an already-completed async value.
- Ensure side-effects don’t accidentally depend on whether `.then()`/wake passes run; initialize/move debug/state transfer consistently across all completion paths.