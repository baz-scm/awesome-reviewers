---
title: Independent memoization boundaries
description: 'Cache/memoize derived values only when it’s safe to do so: treat downstream
  computations as not mutating (or otherwise observing changes to) the specific value
  you’re caching, and then memoize that value independently.'
repository: facebook/react#b2
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251882
---

Cache/memoize derived values only when it’s safe to do so: treat downstream computations as not mutating (or otherwise observing changes to) the specific value you’re caching, and then memoize that value independently.

Apply this in compiler/transformation code (and similar memoization logic):
- If a call site previously required conservative assumptions (e.g., “the function might mutate my argument”), tighten the assumption when you can prove/know the callee does not mutate its argument. Then you can cache the derived value separately.
- When computing structured content for helpers like `fbt._param`, memoize the param value payload independently, even if the surrounding expression changes.

Example pattern:
```js
// Unsafe-by-default approach: avoid caching if callee might mutate argument
// (omit independent memoization)

// Safe-by-design approach: if `fn` does not mutate `arr`, memoize `arr` independently
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

// Independent caching of fbt.param payload
let t2;
if ($[4] !== name) {
  t2 = <Text type="h4">{name}</Text>;
  $[4] = name;
  $[5] = t2;
} else {
  t2 = $[5];
}
// Pass cached payload into the param
fbt._param("item author", t2);
```