---
title: Appropriate error handling
description: Distinguish between implementation errors (invariant violations) and
  expected failure cases. For implementation errors that should never occur, use `unreachable!()`
  with explanatory comments rather than generic `panic!()` or `todo!()`. For expected
  failure modes, return proper error types with informative messages.
repository: pola-rs/polars
label: Error Handling
language: Rust
comments_count: 9
repository_stars: 34296
---

Distinguish between implementation errors (invariant violations) and expected failure cases. For implementation errors that should never occur, use `unreachable!()` with explanatory comments rather than generic `panic!()` or `todo!()`. For expected failure modes, return proper error types with informative messages.

Implementation invariant violations:
```rust
// Good: Clear explanation with unreachable!()
if parsed != incr {
    unreachable!("Parsing invariant violated: expected {} parsed digits, got {}", incr, parsed);
}

// Bad: Using todo() for cases that should never occur
match inner_fn {
    IRBitwiseFunction::And => (new_bitwise_and_reduction(get_dt(input)?), input),
    IRBitwiseFunction::Or => (new_bitwise_or_reduction(get_dt(input)?), input),
    IRBitwiseFunction::Xor => (new_bitwise_xor_reduction(get_dt(input)?), input),
    _ => todo!(), // Should be unreachable!() if this case can't happen
}
```

Expected failures:
```rust
// Good: Informative error with context
if ac.is_aggregated() {
    polars_bail!(InvalidOperation: "cannot slice() an aggregated value")
}

// Good: Using try_ methods with ? operator to propagate errors
offset_fn(&Duration::try_parse(offset)?, timestamp, time_zone).map(Some)
```

Document error conditions with appropriate doc comments:
```rust
/// # Panics
/// Panics if the parsing invariant is violated.

/// # Errors
/// Returns an error if the input cannot be parsed as a valid timestamp.
```

In debug builds, use `debug_assert!()` for checks that shouldn't affect release performance, but always check critical invariants in both debug and release builds.