---
title: Use consistent temporal types
description: When implementing or modifying temporal operations, maintain consistent
  data types that align with existing temporal functions. Specifically, use Int8 for
  datetime components with small ranges (months, days, hours, minutes, seconds) and
  Int32/Int64 for larger values (years, microseconds). This approach reduces unnecessary
  type casting, improves code...
repository: pola-rs/polars
label: Temporal
language: Rust
comments_count: 2
repository_stars: 34296
---

When implementing or modifying temporal operations, maintain consistent data types that align with existing temporal functions. Specifically, use Int8 for datetime components with small ranges (months, days, hours, minutes, seconds) and Int32/Int64 for larger values (years, microseconds). This approach reduces unnecessary type casting, improves code readability, and ensures consistency with temporal functions like `.month()` that return specific types.

Example:
```rust
// Recommended approach - consistent types
let mut month = month.cast(&DataType::Int8)?;
let month = month.i8()?;

// Instead of
// let mut month = month.cast(&DataType::UInt32)?;
// let month = month.u32()?;
```