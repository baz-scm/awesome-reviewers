---
title: Optimize React performance patterns
description: 'Prioritize React performance by avoiding expensive operations and using
  proper React patterns. Key practices include:


  1. **Avoid unnecessary exception throwing**: Exception dispatch is a slow operation
  in React 18. Instead of throwing promises directly, create helper functions to minimize
  performance impact:'
repository: rocicorp/mono
label: React
language: TSX
comments_count: 3
repository_stars: 2091
---

Prioritize React performance by avoiding expensive operations and using proper React patterns. Key practices include:

1. **Avoid unnecessary exception throwing**: Exception dispatch is a slow operation in React 18. Instead of throwing promises directly, create helper functions to minimize performance impact:

```ts
// Good: Hoist React.use detection and create suspend helper
const reactUse = (React as unknown as {use?: (p: Promise<unknown>) => void}).use;
const suspend: (p: Promise<unknown>) => void = reactUse ? reactUse : p => { throw p; };

if (suspendUntil === 'complete' && !view.complete) {
  suspend(view.waitForComplete());
}
```

2. **Use modern JavaScript syntax**: Prefer optional chaining over verbose conditional checks:

```ts
// Good
init?.(z);

// Avoid
if (init) {
  init(z);
}
```

3. **Use appropriate React components**: Always use proper React components instead of generic HTML elements for interactive elements:

```ts
// Good
<Button onAction={() => setDisplayAllComments(true)}>Older</Button>

// Avoid
<div onClick={() => setDisplayAllComments(true)}>Older</div>
```

These practices improve both performance and code maintainability while following React best practices.