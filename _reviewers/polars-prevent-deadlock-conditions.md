---
title: Prevent deadlock conditions
description: 'Carefully manage resource acquisition and release to prevent deadlocks
  in concurrent code. Deadlocks typically occur when multiple threads hold resources
  while waiting for resources held by each other. To avoid deadlocks:'
repository: pola-rs/polars
label: Concurrency
language: Rust
comments_count: 4
repository_stars: 34296
---

Carefully manage resource acquisition and release to prevent deadlocks in concurrent code. Deadlocks typically occur when multiple threads hold resources while waiting for resources held by each other. To avoid deadlocks:

1. **Release resources before blocking operations**: Always drop locks, tokens, or other exclusive resources before operations that might block or wait on results from other threads.

2. **Be careful with resource ordering**: When a component needs to interact with multiple synchronization primitives, establish and maintain a consistent acquisition order.

3. **Properly propagate blocking states**: When implementing custom synchronization mechanisms, ensure blocking states are correctly propagated between components to prevent hidden deadlocks.

4. **Ensure proper cancellation**: When using async tasks, wrap each task handle in cancellation mechanisms (like `AbortOnDropHandle`) immediately after creation to prevent resource leaks during cancellation.

Example of fixing a deadlock-prone pattern:

```rust
// Problematic code - potential deadlock
fn process_data(mut morsel: Morsel, sender: &mut Sender<Morsel>, linearizer: &mut Linearizer) {
    // Holding consume_token while inserting into linearizer can create circular wait
    let consume_token = morsel.take_consume_token();
    linearizer.insert(morsel);
    // If linearizer is waiting for another thread, and that thread needs consume_token
    // to be dropped to proceed, we have a deadlock
}

// Fixed version
fn process_data(mut morsel: Morsel, sender: &mut Sender<Morsel>, linearizer: &mut Linearizer) {
    // Drop the token before potentially blocking operations
    let consume_token = morsel.take_consume_token();
    drop(consume_token); // Explicitly drop before linearizer operation
    linearizer.insert(morsel);
}
```