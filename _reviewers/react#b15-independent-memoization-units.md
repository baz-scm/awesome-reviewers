---
title: Independent Memoization Units
description: Memoize the smallest safe unit independently, and only when downstream
  code cannot mutate/observe the cached value. This improves cache reuse and reduces
  unnecessary coupling between unrelated dependencies.
repository: facebook/react#b15
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251891
---

Memoize the smallest safe unit independently, and only when downstream code cannot mutate/observe the cached value. This improves cache reuse and reduces unnecessary coupling between unrelated dependencies.

Apply this by:
- Verifying that functions used in the pipeline don’t mutate their arguments (or otherwise depend on the argument identity in a way that makes memoization unsafe).
- When constructing higher-level cached structures (e.g., template/parameter systems), memoize subexpressions/param values separately, then pass the memoized result into the wrapper.

Example pattern:
```js
function Component(props) {
  const $ = _c();

  // Memoize a param value independently
  let t1;
  if ($[0] !== props.text) {
    const memoText = identity(props.text);
    t1 = memoText;
    $[0] = props.text;
    $[1] = t1;
  } else {
    t1 = $[1];
  }

  const paramValue = <>{t1}</>;
  // Compose without forcing param internals to share outer cache dependencies
  return fbt._("{=m}", [fbt._param("label", paramValue)]);
}
```
If you find a step where the downstream function could mutate the value you plan to cache, split the cache boundary (or avoid caching that value) so correctness isn’t sacrificed for reuse.