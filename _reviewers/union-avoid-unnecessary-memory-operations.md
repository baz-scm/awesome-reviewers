---
title: avoid unnecessary memory operations
description: Be mindful of memory usage when working with large data structures. Avoid
  unnecessary clones of large objects, remove unused large fields from data structures,
  and prefer references when possible. Large data structures can significantly impact
  both memory usage and execution speed.
repository: unionlabs/union
label: Performance Optimization
language: Rust
comments_count: 2
repository_stars: 74800
---

Be mindful of memory usage when working with large data structures. Avoid unnecessary clones of large objects, remove unused large fields from data structures, and prefer references when possible. Large data structures can significantly impact both memory usage and execution speed.

For example, when dealing with large arrays or collections, avoid cloning:
```rust
// Avoid - unnecessary clone of large data
let block_tx_event_count = block
    .txs_results
    .clone()  // txs_results is quite big

// Prefer - use reference instead
let block_tx_event_count = &block.txs_results
```

Similarly, remove large unused fields from stored state:
```rust
// Remove large fields that aren't needed after initialization
// e.g., initial_sync_committee: 1024 * 384 bytes of BLS pubkeys
pub client_state: Option<T::ClientState>, // Set to None to remove large unused data
```

Always consider the memory footprint of your data structures and operations, especially in resource-constrained environments.