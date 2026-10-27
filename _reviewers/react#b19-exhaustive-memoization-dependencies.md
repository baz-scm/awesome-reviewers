---
title: Exhaustive memoization dependencies
description: When specifying dependency arrays for useMemo/useCallback (or any memoization
  macro), the dependencies must exactly match the values actually read inside the
  callback—no more, no less. Under-specifying dependencies (e.g. depending on `x.y.z.a`
  when the callback reads `x?.y.z?.a`) causes stale values because the memo won't
  recompute when the real inputs...
repository: facebook/react#b19
label: React
language: Markdown
comments_count: 2
repository_stars: 251893
---

When specifying dependency arrays for useMemo/useCallback (or any memoization macro), the dependencies must exactly match the values actually read inside the callback—no more, no less. Under-specifying dependencies (e.g. depending on `x.y.z.a` when the callback reads `x?.y.z?.a`) causes stale values because the memo won't recompute when the real inputs change. Over-specifying dependencies (e.g. including `x`, `y.z`, and `z?.y?.a` when the callback body never reads them) causes unnecessary recomputation and can trigger extra renders or effect runs.

Pay special attention to optional chaining and nested property access: the dependency should reflect the precise access path used in the body, including any `?.` operators, rather than a broader or narrower path. For example:

```js
// Bad: missing dependency, reads x?.y.z?.a but depends on a narrower/different path
const a = useMemo(() => {
  return x?.y.z?.a;
}, [x?.y.z?.a.b]); // wrong: should depend on `x?.y.z?.a`

// Bad: unnecessary dependencies not read in the body
const f = useMemo(() => {
  return [];
}, [x, y.z, z?.y?.a]); // wrong: none of these are read

// Good: dependency matches exactly what's read
const a = useMemo(() => {
  return x?.y.z?.a;
}, [x?.y.z?.a]);
```

This same precision applies to custom macros or utilities (e.g. `idx`) that access nested properties on their arguments—treat their inputs as needing the same transitive, exact dependency tracking as native React hooks. When in doubt, derive the dependency list directly from the property paths actually accessed in the callback, and avoid adding extra paths "just in case."</description>
</invoke>
