---
title: Use Option methods idiomatically
description: When dealing with Optional values, prefer Rust's built-in Option methods
  over manual null checks. This makes code more concise, self-documenting, and less
  error-prone by leveraging Rust's type system to enforce null safety at compile time.
repository: tokio-rs/tokio
label: Null Handling
language: Rust
comments_count: 6
repository_stars: 28989
---

When dealing with Optional values, prefer Rust's built-in Option methods over manual null checks. This makes code more concise, self-documenting, and less error-prone by leveraging Rust's type system to enforce null safety at compile time.

For optional value checking:
```rust
// Instead of:
if self.processing_scheduled_tasks_started_at.is_some() {
    let busy_duration = self.processing_scheduled_tasks_started_at.unwrap().elapsed();
    // Use busy_duration...
}

// Use:
if let Some(processing_scheduled_tasks_started_at) = self.processing_scheduled_tasks_started_at {
    let busy_duration = processing_scheduled_tasks_started_at.elapsed();
    // Use busy_duration...
}
```

For lazy initialization:
```rust
// Instead of:
if me.entry.is_none() {
    let entry = TimerEntry::new(me.handle, deadline);
    me.entry.as_mut().set(Some(entry));
}

// Use:
let entry = me.entry.get_or_insert_with(|| TimerEntry::new(me.handle, deadline));
```

For error handling with Option:
```rust
// Instead of:
let n = match u32::try_from(n) {
    Ok(n) => n,
    Err(_) => return None,
};

// Use:
let n = u32::try_from(n).ok()?;
```