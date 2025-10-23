---
title: Algorithm edge case validation
description: Ensure algorithmic implementations properly handle edge cases and boundary
  conditions before considering them complete. Many algorithm failures stem from insufficient
  consideration of special inputs, parameter combinations, or state transitions that
  occur at the boundaries of normal operation.
repository: servo/servo
label: Algorithms
language: Other
comments_count: 2
repository_stars: 32962
---

Ensure algorithmic implementations properly handle edge cases and boundary conditions before considering them complete. Many algorithm failures stem from insufficient consideration of special inputs, parameter combinations, or state transitions that occur at the boundaries of normal operation.

Key areas to validate:
- Invalid or malformed input data (like the `[0xFF]` byte in encoding scenarios)
- Boundary parameter values (such as `last=false` in streaming operations)
- Incomplete implementations of algorithmic steps (like missing subpixel snapping calculations)
- State management during partial processing or flushing operations

Example from encoding algorithms:
```rust
// Problem: encoding_rs::Decoder fails with single invalid byte when last=false
// The algorithm includes malformed bytes in bytes_read count, causing issues
// when transitioning to flushing state (last=true) with empty remaining slice
let result = decoder.decode_to_string_without_replacement(input, last=false);
// Edge case: single invalid byte [0xFF] doesn't return DecoderResult::Malformed
```

Before marking algorithmic work as complete, systematically test edge cases that could cause unexpected behavior in production. Document known limitations and file follow-up issues for incomplete algorithm implementations.