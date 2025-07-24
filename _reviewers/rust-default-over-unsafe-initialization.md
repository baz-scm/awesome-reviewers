---
title: Default over unsafe initialization
description: Prefer using safe initialization methods like `Default::default()` over
  unsafe alternatives like `MaybeUninit::uninit()` or null values when initializing
  variables. This reduces the risk of undefined behavior and eliminates unnecessary
  unsafe blocks.
repository: rust-lang/rust
label: Null Handling
language: Rust
comments_count: 3
repository_stars: 105254
---

Prefer using safe initialization methods like `Default::default()` over unsafe alternatives like `MaybeUninit::uninit()` or null values when initializing variables. This reduces the risk of undefined behavior and eliminates unnecessary unsafe blocks.

Example - Instead of:
```rust
let mut config_data: MaybeUninit<ConfigData> = MaybeUninit::zeroed();
// ... later ...
unsafe { config_data.assume_init() }
```

Prefer:
```rust
let config_data = ConfigData::default();
```

This approach:
- Reduces unsafe code blocks
- Provides better guarantees about initialization state
- Makes code more maintainable and robust against future type changes
- Prevents potential undefined behavior from uninitialized memory

Only use `MaybeUninit` or manual null handling when there are specific performance requirements or when dealing with FFI boundaries where default initialization is not possible.