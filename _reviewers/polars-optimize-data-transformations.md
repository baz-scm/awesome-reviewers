---
title: Optimize data transformations
description: 'When implementing data processing operations, avoid unnecessary data
  transformations, copies, and conversions that can impact query performance. Consider
  these practices:'
repository: pola-rs/polars
label: Database
language: Rust
comments_count: 4
repository_stars: 34296
---

When implementing data processing operations, avoid unnecessary data transformations, copies, and conversions that can impact query performance. Consider these practices:

1. Prefer direct pattern matching over string conversions:
```rust
// Avoid this:
matches!(function, FunctionExpr::Range(f) if f.to_string() == "int_range")

// Prefer this:
matches!(function, FunctionExpr::Range(RangeFunction::IntRange { .. }))
```

2. Avoid creating temporary data structures when existing ones can be reused:
```rust
// Avoid duplicate data with unnecessary temp dataframes:
let tmp_df = value_col.into_frame().hstack(pivot_df.get_columns()).unwrap();

// Instead, pass existing data directly:
// Use pivot_df directly in subsequent operations
```

3. Ensure schema is cleared after operations that modify DataFrame structure to prevent incorrect schema information from being cached:
```rust
// After modifying DataFrame columns
df.clear_schema();
```

4. Be precise about row handling in data processing operations, clearly distinguishing between rows scanned vs. rows read, especially important for operations like slicing, filtering, and maintaining correct row indices.