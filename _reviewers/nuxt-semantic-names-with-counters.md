---
title: semantic names with counters
description: When generating unique identifiers that may have multiple instances,
  combine semantic base names with counters or indices to ensure both readability
  and uniqueness. Use meaningful component names, scope IDs, or descriptive strings
  as the base, then append a counter to distinguish multiple instances.
repository: nuxt/nuxt
label: Naming Conventions
language: JavaScript
comments_count: 2
repository_stars: 57769
---

When generating unique identifiers that may have multiple instances, combine semantic base names with counters or indices to ensure both readability and uniqueness. Use meaningful component names, scope IDs, or descriptive strings as the base, then append a counter to distinguish multiple instances.

Use clear separators (like ':' or '-') between the semantic part and the counter to improve readability and parsing:

```js
// Good: semantic base + separator + counter
const defaultKey = this.$options._scopeId || this.$options.name || ''
this._fetchKey = key + ':' + getCounter(key)

// Results in readable keys like:
// 'MyComponent:0', 'MyComponent:1'
// 'UserProfile-0', 'UserProfile-1'
```

This pattern prevents identifier collisions while maintaining semantic meaning, making debugging and state inspection much easier than using purely numeric or random identifiers.