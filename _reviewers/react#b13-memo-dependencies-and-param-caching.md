---
title: Memo dependencies and param caching
description: Only include a value as a memo/cache dependency when its *identity is
  stable* across renders; otherwise, your cache may incorrectly persist or thrash.
  In particular, don’t treat refs as safe dependency keys unless you can prove the
  ref identity won’t change—otherwise normalize to a stable value (e.g., the referenced
  value) or restructure so the cache...
repository: facebook/react#b13
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251893
---

Only include a value as a memo/cache dependency when its *identity is stable* across renders; otherwise, your cache may incorrectly persist or thrash. In particular, don’t treat refs as safe dependency keys unless you can prove the ref identity won’t change—otherwise normalize to a stable value (e.g., the referenced value) or restructure so the cache condition depends on value semantics, not ref identity.

When semantics allow (e.g., parameterized values like fbt.param), you may independently memoize sub-values used inside parameters/JSX content to avoid recomputation.

Example patterns:

- Avoid using potentially-unstable ref identity as the cache key:
```js
const customRef = useCustomRef(); // may not be stable
// ❌ Don’t key memo/caching purely on customRef identity unless guaranteed stable
if (memoCell[0] !== customRef) {
  // recompute...
}
```

- Memoize parameter sub-results independently when allowed:
```js
const $ = _c(4);
let t0;
if ($[0] !== props.text) {
  const t1 = identity(props.text);
  // cache parameter/JSX fragment result independently
  let t2;
  if ($[2] !== t1) {
    t2 = <>{t1}</>;
    $[2] = t1;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  t0 = fbt._param("item", t2);
}
```

Practical checklist:
- If the dependency is a ref/obj created by a function, assume identity may change unless proven stable.
- Prefer value-derived dependencies for cache invalidation.
- Use independent memoization for sub-values inside parameterized rendering when it doesn’t change semantics.