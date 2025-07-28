---
title: optimize algorithmic complexity
description: When implementing or refactoring algorithms, prioritize efficient data
  structures and computational approaches over simpler but slower alternatives. This
  is especially critical in performance-sensitive code where operations may be called
  frequently.
repository: ggml-org/llama.cpp
label: Algorithms
language: C
comments_count: 3
repository_stars: 83559
---

When implementing or refactoring algorithms, prioritize efficient data structures and computational approaches over simpler but slower alternatives. This is especially critical in performance-sensitive code where operations may be called frequently.

Key considerations:
- Replace linear searches with hash table lookups when dealing with node/element lookups
- Use platform-specific optimizations (like ARM NEON vectorization) when available, with proper feature detection
- Preallocate resources and precompute operations when possible to avoid runtime overhead
- Consider the computational complexity of your approach and choose algorithms that scale well

Example from the codebase:
```c
// Instead of linear search through nodes:
int j = cgraph->n_nodes - 1;
for (; j >= 0; --j) {
    if (s == cgraph->nodes[j]) {
        break;
    }
}

// Use hash table lookup:
// Allocate use_counts array with hash_size and use ggml_hash_find
// to find the slot for the node, avoiding O(n) search complexity
```

This principle applies broadly - from choosing vectorized implementations over scalar ones, to using hash tables instead of linear searches, to preallocating command buffers rather than creating them on-demand. The goal is to minimize computational overhead, especially in hot code paths where these optimizations compound significantly.