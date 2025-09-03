---
title: Avoid unnecessary memoization
description: 'Memoization (useMemo, useCallback, React.memo) should only be used when
  the performance benefits outweigh the overhead costs. Avoid memoization in these
  scenarios:'
repository: ant-design/ant-design
label: Performance Optimization
language: TSX
comments_count: 3
repository_stars: 95882
---

Memoization (useMemo, useCallback, React.memo) should only be used when the performance benefits outweigh the overhead costs. Avoid memoization in these scenarios:

1. **Simple computations**: For basic logic like conditional assignments or simple object property access, the memoization overhead often exceeds the computation cost.

2. **Incomplete dependency arrays**: When you can't reliably maintain all dependencies, memoization becomes error-prone and can cause stale closures or missed updates.

3. **Object/array dependencies**: When dependencies are objects or arrays that frequently change reference (like props), memoization is often ineffective.

**Example of unnecessary memoization to avoid:**
```tsx
// ❌ Avoid - simple conditional logic doesn't need memoization
const closablePlacement = React.useMemo(() => {
  if (closable === false) return undefined;
  if (closable === undefined || closable === true) return 'start';
  return closable?.placement === 'end' ? 'end' : 'start';
}, [closable]);

// ✅ Better - direct computation is faster
const closablePlacement = closable === false ? undefined : 
  (closable === undefined || closable === true) ? 'start' :
  (closable?.placement === 'end' ? 'end' : 'start');
```

**When to use memoization:**
- Expensive computations (complex calculations, data transformations)
- Stable dependencies that rarely change
- Components that render frequently with the same props

Remember: "Sometimes memoization indeed causes negative optimization" - measure performance impact rather than assuming memoization always helps.