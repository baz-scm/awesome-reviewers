---
title: Independent Memoization
description: 'Cache (memoize) derived values independently whenever downstream usage
  is guaranteed not to mutate the inputs.


  Apply this rule:

  1) Determine whether a called function can mutate its arguments. If it cannot (known/pure
  signature), you may memoize the argument-producing expression on its own dependencies.'
repository: facebook/react#b16
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251891
---

Cache (memoize) derived values independently whenever downstream usage is guaranteed not to mutate the inputs.

Apply this rule:
1) Determine whether a called function can mutate its arguments. If it cannot (known/pure signature), you may memoize the argument-producing expression on its own dependencies.
2) For template/parameterized constructs, treat each parameter value (or parameter content) as a separate expression with its own cache key; reuse the memoized parameter value when building the parent structure.

Example pattern (memoize intermediate, then reuse it):
```js
function Component(props) {
  const $ = _c(6);
  const { name, data, icon } = props;

  // Memoize intermediate value independently
  let t2;
  if ($[4] !== name) {
    t2 = <Text type="h4">{name}</Text>;
    $[4] = name;
    $[5] = t2;
  } else {
    t2 = $[5];
  }

  // Reuse memoized intermediate inside higher-level param/container
  let t1;
  if ($[0] !== data || $[1] !== icon || $[2] !== name) {
    t1 = (
      <Text type="body4">
        {fbt._("{item author}{icon}{=m2}", [
          fbt._param("item author", t2),
          icon,
        ])}
      </Text>
    );
    $[0] = data; $[1] = icon; $[2] = name; $[3] = t1;
  } else {
    t1 = $[3];
  }

  return t1;
}
```

Outcome: fewer unnecessary cache invalidations and less coupling between unrelated dependencies, while remaining correct under function purity/non-mutation guarantees.