---
title: Independent And Transitive Memoization
description: When building/transforming cached values, split memoization boundaries
  whenever the consumer is safe to treat as non-mutating, but ensure that every expression
  passed through custom macros/components is memoized transitively so no dependent
  input becomes “uncached.”
repository: facebook/react#b8
label: Caching
language: Markdown
comments_count: 4
repository_stars: 251889
---

When building/transforming cached values, split memoization boundaries whenever the consumer is safe to treat as non-mutating, but ensure that every expression passed through custom macros/components is memoized transitively so no dependent input becomes “uncached.”

Apply this as:
- **Decouple caches by default when safe:** If a function/consumer is known (by signature/analysis) to not mutate its arguments, you can memoize derived values independently instead of treating any input as potentially tainted by mutation.
- **Preserve correctness through transitive memoization:** For **custom macros** (e.g., `idx`) and macro-like APIs (e.g., `fbt.param`), memoize all arguments they consume, including arguments that themselves contain further derived expressions (JSX/props/fields). Don’t rely on partial memoization coverage.

Example pattern (independent memoization):
```js
// If `fn` is known not to mutate its argument:
let t1;
if ($[0] !== b) {
  t1 = makeArray(b); // derived value memoized independently
  $[0] = b;
  $[1] = t1;
} else {
  t1 = $[1];
}
const arr = t1;
fn(arr);
```

Example pattern (macro argument memoization + independent JSX params):
```js
let t2;
if ($[4] !== name) {
  t2 = <Text type="h4">{name}</Text>; // memoize JSX content separately
  $[4] = name;
  $[5] = t2;
} else {
  t2 = $[5];
}

fbt._("...", [
  fbt._param("item author", t2), // the param value is stable
]);
```

Checklist:
- Can the consumer mutate its arguments? If **yes/unknown**, don’t decouple caches.
- For macro/consumer calls: are **all** consumed arguments memoized, including nested derived expressions?
- Prefer extracting memoized sub-expressions for specific dependencies rather than reusing broader cached slots unnecessarily.