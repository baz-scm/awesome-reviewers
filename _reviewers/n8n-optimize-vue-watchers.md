---
title: Optimize Vue watchers
description: 'When implementing watchers in Vue applications, ensure they are configured
  appropriately for the data structures they observe. Two common pitfalls to avoid:'
repository: n8n-io/n8n
label: Vue
language: Other
comments_count: 2
repository_stars: 122978
---

When implementing watchers in Vue applications, ensure they are configured appropriately for the data structures they observe. Two common pitfalls to avoid:

1. **Use `deep: true` for complex data structures**: When watching arrays or objects that might be modified in-place (push, pop, property updates), enable deep watching to detect these changes:

```javascript
watch(
  () => props.messages,
  async (messages) => {
    // Handler logic
  },
  { immediate: true, deep: true } // Enable deep watching for arrays/objects
)
```

Without deep watching, the watcher will only trigger when the reference changes, not when items are added or properties modified.

2. **Watch specific properties instead of whole objects**: For better performance and stability, watch the specific primitive property you care about rather than the entire object:

```javascript
// Less optimal - watches entire object reference
watch(
  () => selected,
  // Handler logic
)

// More optimal - watches just the ID property
watch(
  () => selected?.id,
  // Handler logic
)
```

This prevents unnecessary watcher triggers when unrelated properties change and makes your reactivity system more predictable and efficient.