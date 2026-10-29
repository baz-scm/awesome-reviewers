---
title: Minimize complexity in data transforms
description: When writing algorithms that transform or traverse collections (e.g.,
  parsing form data into nested objects, walking a trie), explicitly consider computational
  complexity before merging. Avoid nested-loop patterns that degrade to O(n*m) when
  a restructured, single- or multi-pass approach can achieve O(n+m). For example,
  instead of re-scanning every key for...
repository: honojs/hono
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 32741
---

When writing algorithms that transform or traverse collections (e.g., parsing form data into nested objects, walking a trie), explicitly consider computational complexity before merging. Avoid nested-loop patterns that degrade to O(n*m) when a restructured, single- or multi-pass approach can achieve O(n+m). For example, instead of re-scanning every key for dotted/nested paths inside the main collection loop, do a first pass to group raw values, then a second pass to build the nested structure only for keys that need it:

```ts
// Avoid: nested processing inside the main loop (O(n*m))
formData.forEach((value, key) => {
  if (key.includes('.')) {
    handleNestedValues(form, key, value) // re-walks structure every time
  }
})

// Prefer: separate passes, each O(n)
formData.forEach((value, key) => {
  form[key] = value // simple assignment, single pass
})

if (options.dot) {
  Object.entries(form).forEach(([key, value]) => {
    if (key.includes('.')) {
      handleNestedValues(nestedForm, key, value) // only processes dotted keys
    }
  })
}
```

The same principle applies to traversal logic (e.g., trie/router node matching) and pattern-matching code (regexes): prefer the simplest expression/algorithm that correctly covers all required cases without redundant work or duplicate processing of the same node/value. When fixing a bug or adding a feature, check whether the chosen approach introduces redundant iterations, duplicate handler invocations, or unnecessarily complex patterns, and simplify to the most efficient correct solution before merging.