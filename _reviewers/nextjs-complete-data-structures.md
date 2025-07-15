---
title: "Complete data structures"
description: "When implementing data structures such as tries, trees, or graphs, ensure all critical operations (insertion, deletion, traversal) are fully implemented with proper cleanup logic. Incomplete implementations can lead to memory leaks, stale data, and incorrect application behavior."
repository: "vercel/next.js"
label: "Algorithms"
language: "TypeScript"
comments_count: 2
repository_stars: 133000
---

When implementing data structures such as tries, trees, or graphs, ensure all critical operations (insertion, deletion, traversal) are fully implemented with proper cleanup logic. Incomplete implementations can lead to memory leaks, stale data, and incorrect application behavior.

For example, in a trie implementation, the `remove` operation should:
1. Traverse the structure to locate the target node
2. Clear the node's value
3. Clean up orphaned parent nodes when appropriate
4. Update any dependent systems

```typescript
function remove(value: Value) {
  const key = getKey(value)
  if (!key) return

  let current = root
  const parts = key.split('/')
  const path: Node[] = [current]

  // Traverse the trie to find the node
  for (const part of parts) {
    if (!current.children[part]) {
      return // Node doesn't exist
    }
    current = current.children[part]
    path.push(current)
  }

  // Clear the node's value
  current.value = undefined

  // Clean up empty parent nodes
  for (let i = path.length - 1; i > 0; i--) {
    const node = path[i]
    if (!node.value && Object.keys(node.children).length === 0) {
      const parent = path[i - 1]
      const nodeName = parts[i - 1]
      delete parent.children[nodeName]
    } else {
      break // Stop if we find a non-empty node
    }
  }

  // Notify listeners or update UI if needed
  markUpdated()
}
```

When designing data structures, also consider using generics to make them reusable across different value types, increasing their utility throughout your application.