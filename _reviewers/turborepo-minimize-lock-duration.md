---
title: Minimize lock duration
description: When using locks in asynchronous code, minimize the scope and duration
  for which locks are held, especially across `.await` points. Holding locks during
  asynchronous operations can block progress in other tasks and lead to decreased
  concurrency or even deadlocks.
repository: vercel/turborepo
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 28115
---

When using locks in asynchronous code, minimize the scope and duration for which locks are held, especially across `.await` points. Holding locks during asynchronous operations can block progress in other tasks and lead to decreased concurrency or even deadlocks.

Always follow these practices:
1. Acquire locks in the smallest possible scope
2. Release locks as soon as the protected operation is complete
3. Never hold locks across I/O or other long-running async operations

```rust
// Bad: Lock held during potentially long-running operation
let changed_packages_guard = changed_packages.lock().await;
if !changed_packages_guard.borrow().is_empty() {
    let changed_packages = changed_packages_guard.take();
    self.execute_run(changed_packages).await?; // Lock still held during execution
}

// Good: Lock released after data extraction
let some_changed_packages = {
    let mut changed_packages_guard = changed_packages.lock().await;
    (!changed_packages_guard.is_empty())
        .then(|| std::mem::take(changed_packages_guard.deref_mut()))
};
if let Some(changed_packages) = some_changed_packages {
    self.execute_run(changed_packages).await?; // Lock already released
}
```

This pattern is particularly crucial when dealing with I/O operations, network requests, or UI updates, as these operations may take significant time to complete. Using scope blocks to manage lock lifetimes ensures other concurrent operations can make progress while long-running tasks execute.