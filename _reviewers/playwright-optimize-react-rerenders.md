---
title: optimize React rerenders
description: Ensure React components avoid unnecessary rerenders by maintaining object
  identity in dependencies and eliminating unused state variables. When objects are
  recreated on every render, they cause effects and child components to re-execute
  unnecessarily, leading to performance issues.
repository: microsoft/playwright
label: React
language: TSX
comments_count: 3
repository_stars: 76113
---

Ensure React components avoid unnecessary rerenders by maintaining object identity in dependencies and eliminating unused state variables. When objects are recreated on every render, they cause effects and child components to re-execute unnecessarily, leading to performance issues.

Key practices:
- Use `useMemo` to maintain object identity for effect dependencies when the underlying data hasn't changed
- Remove state variables that don't contribute to rendering decisions, as they trigger rerenders without benefit
- Consider state stability when designing data structures - avoid creating new objects every render cycle

Example of the problem:
```js
// Bad: Creates new object every render, causing effect to run unnecessarily
const snapshotUrls = {
  snapshotInfoUrl: snapshot?.url
};

React.useEffect(() => {
  // This runs on every render due to new snapshotUrls object
}, [snapshotUrls]);

// Good: Memoize to maintain object identity
const snapshotUrls = React.useMemo(() => ({
  snapshotInfoUrl: snapshot?.url
}), [snapshot?.url]);
```

Also avoid state variables used only for calculations:
```js
// Bad: Unnecessary state that causes rerenders
const [containerWidth, setContainerWidth] = React.useState(0);

// Good: Use ref or calculate directly if not needed for rendering
const containerRef = React.useRef();
```