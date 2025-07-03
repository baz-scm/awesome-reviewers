---
title: Graph traversal optimization
description: 'When working with graph structures, avoid performing redundant depth-first
  search (DFS) traversals as each traversal incurs an O(V+E) complexity cost. Instead,
  consider:'
repository: apache/mxnet
label: Algorithms
language: Other
comments_count: 4
repository_stars: 20801
---

When working with graph structures, avoid performing redundant depth-first search (DFS) traversals as each traversal incurs an O(V+E) complexity cost. Instead, consider:

1. **Label nodes during initial traversal** to maintain state information for subsequent operations
2. **Cache traversal order** to avoid repeating the same path exploration
3. **Batch related operations** that can be performed in a single pass
4. **Create graph copies** when modifications might affect future traversals

For example, instead of:

```cpp
// Multiple independent DFS calls on the same graph structure
for (auto pattern : patterns) {
  DFSVisit(sym.outputs, [&](const nnvm::ObjectPtr &node) {
    if (node->is_variable()) return;
    // Find nodes matching pattern
  });
}
```

Consider:

```cpp
// Single traversal with collected state
std::vector<nnvm::ObjectPtr> traversal_order;
std::unordered_map<nnvm::ObjectPtr, int> node_labels;

DFSVisit(sym.outputs, [&](const nnvm::ObjectPtr &node) {
  if (node->is_variable()) return;
  traversal_order.push_back(node);
  // Label nodes as needed
});

// Now use cached traversal for pattern matching without repeating DFS
for (auto pattern : patterns) {
  for (const auto& node : traversal_order) {
    // Match against patterns
  }
}
```

This approach significantly reduces computational complexity when multiple operations or pattern matching need to be performed on the same graph structure.
