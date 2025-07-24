---
title: Benchmark before optimizing code
description: 'Always validate performance optimizations with benchmarks before implementation.
  Ensure measurements account for:

  1. Platform-specific characteristics (32-bit vs 64-bit)'
repository: rust-lang/rust
label: Performance Optimization
language: Rust
comments_count: 5
repository_stars: 105254
---

Always validate performance optimizations with benchmarks before implementation. Ensure measurements account for:
1. Platform-specific characteristics (32-bit vs 64-bit)
2. Realistic usage patterns
3. Appropriate metrics (wall time vs CPU time)

Example:
```rust
#[bench]
fn write_64bit_hex(bh: &mut Bencher) {
    // Test common cases first
    bh.iter(|| {
        write!(black_box(discard), "{:x}", black_box(0_u64)).unwrap();
        write!(black_box(discard), "{:x}", black_box(10000_i64)).unwrap();
        // Test edge cases
        write!(black_box(discard), "{:x}", black_box(-10000_i64)).unwrap();
    });
}
```

Avoid premature optimization based on theoretical gains. For instance, reusing buffers might seem beneficial but benchmarks often show stack allocation is equally efficient:
```rust
// Prefer simple, clear code unless benchmarks show meaningful gains
let mut buf = NumBuffer::new();  // Creates temporary buffer on stack
format!("{}", number)            // Let compiler optimize common case
```