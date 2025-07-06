---
title: Descriptive semantic naming
description: 'Create identifiers that clearly convey meaning through descriptive names
  and appropriate types. Two key practices improve code readability and prevent errors:'
repository: influxdata/influxdb
label: Naming Conventions
language: Rust
comments_count: 5
repository_stars: 30268
---

Create identifiers that clearly convey meaning through descriptive names and appropriate types. Two key practices improve code readability and prevent errors:

1. **Use semantic types instead of primitives** for domain concepts to provide type safety and clarity:

```rust
// Instead of raw primitives:
pub fn get_retention_period_cutoff_ts_nanos(&self, db_id: &DbId) -> Option<i64> { ... }

// Use semantic types:
pub struct UnixTimestampNanos(i64);
pub fn get_retention_period_cutoff(&self, db_id: &DbId) -> Option<UnixTimestampNanos> { ... }
```

2. **Choose clear, fully descriptive names** that convey complete context:

```rust
// Prefer:
let last_snapshotted_wal_sequence_number = get_sequence();  // Clear purpose

// Over:
let last_wal_sequence_number = get_sequence();  // Ambiguous
```

3. **Include units in variable names** when working with primitive numeric types:

```rust
let timestamp_ns: i64 = 1682939402000000000;  // Unit 'ns' clarifies meaning
```

4. **Follow established naming conventions** for your ecosystem. For metrics, follow standards like Prometheus conventions:

```rust
// Correct:
write_lines_total: Metric<U64Counter>  // Unit-less counters end with _total

// Avoid:
write_lines_count: Metric<U64Counter>  // Non-standard naming
```

These practices substantially improve code maintainability, preventing confusion and subtle bugs related to type misuse.