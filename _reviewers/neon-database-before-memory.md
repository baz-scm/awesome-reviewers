---
title: Database before memory
description: When working with database systems that also maintain in-memory state,
  always update the persistent database state before updating the in-memory representation.
  This ensures that if a crash occurs between operations, the system can correctly
  rebuild its state from the database without inconsistencies or "time traveling"
  issues.
repository: neondatabase/neon
label: Database
language: Rust
comments_count: 3
repository_stars: 19015
---

When working with database systems that also maintain in-memory state, always update the persistent database state before updating the in-memory representation. This ensures that if a crash occurs between operations, the system can correctly rebuild its state from the database without inconsistencies or "time traveling" issues.

For example:
```rust
// Good practice
self.persistence
    .set_tombstone(node_id)
    .await?;

// Now update in-memory state
let mut locked = self.inner.write().unwrap();
let (nodes, _, scheduler) = locked.parts_mut();
scheduler.node_remove(node_id);
// ...rest of in-memory updates

// Bad practice - DON'T DO THIS
let mut locked = self.inner.write().unwrap();
let (nodes, _, scheduler) = locked.parts_mut();
scheduler.node_remove(node_id);

// If we crash here, database is out of sync with what was in memory
self.persistence
    .set_tombstone(node_id)
    .await?;
```

Additionally, be careful not to schedule redundant database operations. When deleting database objects, ensure you're not accidentally scheduling the same deletion twice through different mechanisms. Always handle edge cases where automatic cleanup might not occur, such as empty collections that won't be iterated over by reconciliation processes.