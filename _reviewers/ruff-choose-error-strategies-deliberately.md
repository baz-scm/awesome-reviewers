---
title: Choose error strategies deliberately
description: 'Make deliberate choices about error handling strategies based on the
  context. Decide between early returns with appropriate error reporting, panic mechanisms,
  or silent failures with diagnostics:'
repository: astral-sh/ruff
label: Error Handling
language: Rust
comments_count: 7
repository_stars: 40619
---

Make deliberate choices about error handling strategies based on the context. Decide between early returns with appropriate error reporting, panic mechanisms, or silent failures with diagnostics:

1. **Early returns** for expected error conditions:
   ```rust
   // Prefer this when the error is expected in normal operation
   if !output.status.success() {
       return Err(anyhow::anyhow!(
           "Git checkout failed: {}",
           String::from_utf8_lossy(&output.stderr)
       ));
   }
   ```

2. **Panic** only for true invariant violations:
   ```rust
   // Use panic! over unreachable! when an invariant is violated
   match definition.scope(db).node(db) {
       NodeWithScopeKind::Class(_) => {
           panic!("invalid definition kind for type variable")
       }
       // Valid cases...
   }
   ```

3. **Silent failures with diagnostics** when appropriate:
   ```rust
   // Return a sensible default and let type checking handle the error
   if !is_callable(test_expr) {
       return Truthiness::AlwaysFalse;
   }
   ```

Always document functions that can panic and under what conditions. When handling results, be explicit about error propagation choices - consider whether errors should be logged, propagated, or transformed into different error types based on the needs of the caller.