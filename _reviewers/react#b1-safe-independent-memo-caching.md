---
title: Safe Independent Memo Caching
description: 'When applying caching/memoization, keep it both *safe* and *fine-grained*:
  memoize independently only if you can guarantee the consumer won’t mutate inputs
  and you use correct cache keys for values whose identity/stability you can’t prove.'
repository: facebook/react#b1
label: Caching
language: Markdown
comments_count: 4
repository_stars: 251878
---

When applying caching/memoization, keep it both *safe* and *fine-grained*: memoize independently only if you can guarantee the consumer won’t mutate inputs and you use correct cache keys for values whose identity/stability you can’t prove.

Apply these rules:
- **Prove non-mutation before independent memoization:** If a cached value could be mutated by a downstream function, don’t memoize it independently; keep it coupled to the call’s broader invalidation.
- **Never assume ref/hook stability:** If a value comes from a hook and its identity stability isn’t guaranteed, don’t treat it as dependency-irrelevant. Use it in the cache guard (or re-create cache when it changes).
- **Use fine-grained cache slots:** For derived values used inside params/JSX (e.g., `fbt.param` inputs), memoize the sub-value separately so unrelated changes don’t invalidate the whole block.

Example (fine-grained + correct invalidation):
```js
function Component({ text }) {
  const $ = _c(4);

  // Cache a derived param/JSX value independently.
  let t0;
  if ($[0] !== text) {
    const t1 = identity(text);
    let t2;
    if ($[2] !== t1) {
      t2 = <>{t1}</>;
      $[2] = t1;
      $[3] = t2;
    } else {
      t2 = $[3];
    }
    t0 = fbt._("{x}", [fbt._param("x", t2)]);
    $[0] = text;
  } else {
    // reuse previously cached block outputs as appropriate
    t0 = $[1];
  }

  return t0;
}
```
Key takeaway: **cache smaller sub-values, but only when you can justify both “no mutation” and “correct identity invalidation.”**