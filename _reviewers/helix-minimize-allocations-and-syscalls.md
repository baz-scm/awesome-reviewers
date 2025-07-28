---
title: Minimize allocations and syscalls
description: 'Optimize performance by minimizing unnecessary memory allocations and
  system calls. Key practices:


  1. Avoid unnecessary String allocations:

  ```rust

  // Instead of'
repository: helix-editor/helix
label: Performance Optimization
language: Rust
comments_count: 10
repository_stars: 39026
---

Optimize performance by minimizing unnecessary memory allocations and system calls. Key practices:

1. Avoid unnecessary String allocations:
```rust
// Instead of
let s = some_str.to_string();

// Use when possible
let s = some_str.into();
// Or
let s = Cow::Borrowed(some_str);
```

2. Pre-allocate collections when size is known:
```rust
// Instead of
let mut vec = Vec::new();
items.iter().for_each(|i| vec.push(i));

// Use
let mut vec = Vec::with_capacity(items.len());
items.iter().for_each(|i| vec.push(i));
```

3. Cache expensive system calls:
```rust
// Instead of
fn get_time() -> i64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs() as i64
}

// Use
static TIME_CACHE: LazyLock<EditorTime> = LazyLock::new(|| {
    EditorTime {
        start: SystemTime::now(),
        since: Instant::now(),
    }
});
```

4. Return iterators instead of collecting into vectors when possible:
```rust
// Instead of
pub fn items(&self) -> Vec<Item> {
    self.items.iter().map(|i| i.clone()).collect()
}

// Use
pub fn items(&self) -> impl Iterator<Item = Item> + '_ {
    self.items.iter().cloned()
}
```

5. Avoid filesystem operations in hot paths:
```rust
// Instead of checking is_dir() repeatedly
if path.is_dir() { ... }

// Cache the information once
let is_dir = entry.file_type()
    .is_ok_and(|ft| ft.is_dir());
```