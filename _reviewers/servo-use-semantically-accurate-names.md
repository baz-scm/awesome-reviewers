---
title: Use semantically accurate names
description: Variable, method, and type names should accurately reflect their actual
  purpose, content, and behavior. Avoid generic or misleading names that don't match
  the underlying functionality.
repository: servo/servo
label: Naming Conventions
language: Rust
comments_count: 13
repository_stars: 32962
---

Variable, method, and type names should accurately reflect their actual purpose, content, and behavior. Avoid generic or misleading names that don't match the underlying functionality.

Key principles:
- Use plural names for collections: `visible_input_methods` not `visible_input_method` for a Vec
- Match names to actual functionality: `closed_any_websocket` not `canceled_any_fetch` when closing websockets
- Avoid generic terms: use specific descriptive names instead of "Generic", "this", "that"
- Reflect current state: `hit_test_result` not `cached_hit_test_result` when it's not always cached
- Use precise terminology: `area` not `size` when measuring area specifically

Example:
```rust
// Bad - misleading name
let cached_hit_test_result = match event.event { ... }

// Good - accurate name  
let hit_test_result = match event.event { ... }

// Bad - singular for collection
visible_input_method: Vec<EmbedderControlId>,

// Good - plural for collection
visible_input_methods: Vec<EmbedderControlId>,
```

Names should immediately communicate what the code actually does, not what it might do or what it was originally intended to do.