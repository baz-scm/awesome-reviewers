---
title: Release locks before waking
description: In concurrent systems, it's critical to release locks before performing
  operations that might trigger reentrancy or block the current thread, such as waking
  waiters. Holding locks while waking tasks can lead to deadlocks if the awakened
  code attempts to acquire the same lock.
repository: tokio-rs/tokio
label: Concurrency
language: Rust
comments_count: 9
repository_stars: 28989
---

In concurrent systems, it's critical to release locks before performing operations that might trigger reentrancy or block the current thread, such as waking waiters. Holding locks while waking tasks can lead to deadlocks if the awakened code attempts to acquire the same lock.

This pattern applies to any concurrency primitive that maintains a list of waiters, such as semaphores, notification systems, or task schedulers.

```rust
// PROBLEMATIC: Holding lock while waking waiters
let mut lock = self.waiters.lock();
while let Some(waker) = lock.waiters.pop() {
    waker.wake(); // Deadlock risk if woken task tries to acquire the same lock
}
```

Instead, collect the wakers to wake while holding the lock, then drop the lock before waking them:

```rust
let wakers_to_wake = {
    let mut lock = self.waiters.lock();
    std::mem::take(&mut lock.waiters) // Take ownership of waiters
    // Lock is released at the end of this block
};

// Wake waiters after releasing the lock
for waker in wakers_to_wake {
    waker.wake();
}
```

For batch operations, you can use a helper structure like `WakeList` to avoid waking too many waiters at once:

```rust
let mut waker_list = WakeList::new();
let mut lock = self.mutex.lock();

while let Some(waker) = process_next_waiter(&mut lock) {
    waker_list.push(waker);
    
    if !waker_list.can_push() {
        // Wake a batch of waiters with the lock temporarily dropped
        drop(lock);
        waker_list.wake_all();
        
        // Reacquire the lock to continue processing
        lock = self.mutex.lock();
    }
}

// Don't forget to wake remaining waiters
drop(lock);
waker_list.wake_all();
```

By following this pattern, you maintain system liveness and avoid deadlocks in concurrent code.