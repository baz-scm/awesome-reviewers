---
title: Avoid post-paint sync
description: When you need two pieces of UI state to stay consistent (selection/results/filtering/etc.),
  don’t “repair” it in a `useEffect` after the browser has painted—this can create
  a stale frame and UI thrashing. Instead, keep the relationship in render/memo, and
  update state synchronously from already-derived inputs.
repository: facebook/react#b11
label: React
language: JavaScript
comments_count: 4
repository_stars: 251894
---

When you need two pieces of UI state to stay consistent (selection/results/filtering/etc.), don’t “repair” it in a `useEffect` after the browser has painted—this can create a stale frame and UI thrashing. Instead, keep the relationship in render/memo, and update state synchronously from already-derived inputs.

Also: don’t write to refs as a stand-in for state during render; if you need to track prop changes, use `useState` (or derive directly) so React’s rules and consistency guarantees hold.

Example pattern (sync in render, not effect):
```js
function Controller({commitData, selectCommitIndex}) {
  const [prevCommitData, setPrevCommitData] = useState(commitData);

  if (prevCommitData !== commitData) {
    setPrevCommitData(commitData);
    selectCommitIndex(commitData.length > 0 ? 0 : null);
  }

  // derive the rest from commitData here (useMemo if expensive)
  // return UI that matches the derived state in the same render
}
```

Use effects only for external side effects that can’t be expressed in render (e.g., calling an imperative DOM API like `scrollToItem` in response to a derived selection), and keep dependencies/guards so you don’t act on “fallback” indices after deselection.