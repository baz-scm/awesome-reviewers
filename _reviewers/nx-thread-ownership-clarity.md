---
title: Thread ownership clarity
description: When designing concurrent systems, ensure data ownership is explicit
  and clear at thread boundaries. Avoid passing references across threads or using
  indirect access patterns that obscure ownership responsibilities.
repository: nrwl/nx
label: Concurrency
language: Rust
comments_count: 2
repository_stars: 27518
---

When designing concurrent systems, ensure data ownership is explicit and clear at thread boundaries. Avoid passing references across threads or using indirect access patterns that obscure ownership responsibilities.

In multithreaded code, data must be owned by the thread that uses it, not borrowed from another thread. This prevents race conditions and makes the code's concurrency model explicit.

Example of problematic pattern:
```rust
// BAD: Trying to pass &mut self to a thread
fn start_collection(&mut self) -> Result<(), Error> {
    std::thread::spawn(|| {
        self.collection_loop(); // Error: can't pass references across threads
    });
}
```

Example of correct pattern:
```rust
// GOOD: Clone Arc references for thread ownership
fn start_collection(&mut self) -> Result<(), Error> {
    let should_collect = Arc::clone(&self.should_collect);
    let system = Arc::clone(&self.system);
    
    std::thread::spawn(move || {
        Self::collection_loop(should_collect, system); // Owned data
    });
}
```

Additionally, avoid indirect data access that obscures ownership. Instead of retrieving data through unrelated objects, pass required data directly to maintain clear responsibility chains and prevent confusion about data sources in concurrent contexts.