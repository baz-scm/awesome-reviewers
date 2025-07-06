---
title: Optimize memory allocation
description: 'Be deliberate about memory allocation patterns to improve performance.
  Implement these practices:


  1. **Pre-allocate collections when the size is known**:'
repository: tokio-rs/tokio
label: Performance Optimization
language: Rust
comments_count: 6
repository_stars: 28981
---

Be deliberate about memory allocation patterns to improve performance. Implement these practices:

1. **Pre-allocate collections when the size is known**:
   ```rust
   // Less efficient - may require multiple reallocations
   let mut output = Vec::new();
   
   // More efficient - single allocation of correct size
   let mut output = Vec::with_capacity(self.len());
   ```

2. **Avoid unnecessary buffer clearing**:
   ```rust
   // Less efficient - discards existing content
   buffer.clear();
   buffer.extend(new_items);
   
   // More efficient - preserves existing content when appropriate
   buffer.extend(new_items);
   ```

3. **Use compact memory representations** when appropriate:
   ```rust
   // Less memory-efficient
   name: Option<Vec<u8>>,
   name_demangled: Option<String>,
   
   // More memory-efficient
   name: Option<Box<[u8]>>,
   name_demangled: Option<Box<str>>,
   ```

4. **Defer allocation until needed**:
   ```rust
   // Less efficient - always reserves space
   buffer.reserve(BLOCK_CAP);
   
   // More efficient - only reserves when necessary
   if buffer.len() == buffer.capacity() {
       buffer.reserve(BLOCK_CAP);
   }
   ```

5. **Be mindful of struct size and field initialization**:
   Only store fields directly in structs when they're always needed. Consider storing rarely used fields behind indirection (e.g., in an Option or Box) or restructuring to avoid initializing fields that aren't always required.

These practices reduce memory pressure, improve cache locality, and minimize the overhead of memory management operations.