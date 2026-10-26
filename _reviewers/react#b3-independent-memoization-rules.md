---
title: Independent Memoization Rules
description: 'When applying caching/memoization, follow two constraints:


  1) Memoize independently only when inputs are safe

  - If a downstream value/function is known not to mutate its argument (or the argument
  is otherwise provably immutable for the cached lifetime), cache the derived value
  from its direct stable inputs, then reuse it.'
repository: facebook/react#b3
label: Caching
language: Markdown
comments_count: 4
repository_stars: 251883
---

When applying caching/memoization, follow two constraints:

1) Memoize independently only when inputs are safe
- If a downstream value/function is known not to mutate its argument (or the argument is otherwise provably immutable for the cached lifetime), cache the derived value from its direct stable inputs, then reuse it.

2) Memoize transitively across macro boundaries
- For any “custom macro” or compiler macro call, ensure *all* of its arguments are transitively memoized (not just a subset). Treat the macro call as a caching boundary.

3) Apply to FBT param payloads
- Treat `fbt.param` payload values (including JSX elements/fragments inside the param) as independently memoizable: cache the payload from its own stable dependencies, then pass the cached payload into `fbt._param`.

Example (safe independent memoization + fbt.param payload caching):
```js
function Component({ b, myVar }) {
  // Cached from stable input `b` because `fn` doesn't mutate its argument.
  let t1;
  if ($[0] !== b) {
    t1 = makeArray(b);
    $[0] = b;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const arr = t1;
  fn(arr);

  // Independently memoize fbt.param payload.
  let payload;
  if ($[2] !== myVar) {
    payload = <>{myVar}</>;
    $[2] = myVar;
    $[3] = payload;
  } else {
    payload = $[3];
  }

  return fbt._("{x}", [fbt._param("x", payload)]);
}
```
This prevents both correctness bugs (insufficient transitive memoization through macros) and missed performance opportunities (over-coupled caching when arguments are non-mutating/stable).