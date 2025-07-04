---
title: Minimize critical path allocations
description: Avoid unnecessary memory allocations in performance-critical code paths.
  These allocations not only consume memory but also trigger expensive CPU operations
  that can significantly impact system performance.
repository: influxdata/influxdb
label: Performance Optimization
language: Rust
comments_count: 8
repository_stars: 30268
---

Avoid unnecessary memory allocations in performance-critical code paths. These allocations not only consume memory but also trigger expensive CPU operations that can significantly impact system performance.

Key optimization techniques:

1. **Use efficient data structures**: 
   - Box large enum variants to reduce memory footprint
   ```rust
   // Before
   enum Schedule {
       Cron(OwnedScheduleIterator<Utc>),  // 288 bytes
       Every(Duration),                   // 16 bytes
   }
   
   // After
   enum Schedule {
       Cron(Box<OwnedScheduleIterator<Utc>>),  // 16 bytes
       Every(Duration),                        // 16 bytes
   }
   ```
   - Prefer `HashMap` over `BTreeMap` for lookup-heavy operations
   - Consider `Arc<str>` or `&str` over `String` when appropriate

2. **Optimize container operations**:
   - Use `contains()` instead of `iter().any()` for membership checks
   ```rust
   // Less efficient
   if paths_without_authz.iter().any(|disabled_authz_path| *disabled_authz_path == path) {
       // ...
   }
   
   // More efficient
   if paths_without_authz.contains(&path) {
       // ...
   }
   ```
   - Consider how you handle capacity in vectors (clear vs. take)
   - Use iterators for lazy evaluation rather than materializing full collections

3. **Avoid string overhead**:
   - Use `to_string()` instead of `format!()` for simple conversions
   ```rust
   // Less efficient
   let partition_key = data_types::PartitionKey::from(format!("{}", parquet_file.chunk_time));
   
   // More efficient
   let partition_key = data_types::PartitionKey::from(parquet_file.chunk_time.to_string());
   ```
   - Avoid rebuilding schemas or data structures repeatedly in hot paths

Remember that even small allocations can have a significant impact when they occur frequently in critical code paths, particularly in high-throughput systems handling many requests or processing large datasets.