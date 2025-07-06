---
title: Safe null handling
description: 'Always implement robust null handling patterns to prevent unexpected
  behavior and crashes. Consider all edge cases where null values might affect calculations,
  type conversions, or data operations:'
repository: pola-rs/polars
label: Null Handling
language: Rust
comments_count: 10
repository_stars: 34296
---

Always implement robust null handling patterns to prevent unexpected behavior and crashes. Consider all edge cases where null values might affect calculations, type conversions, or data operations:

1. Don't rely on potentially null values for sizing or allocation decisions:
```rust
// Bad: Zero allocation if first element is null
let capacity = from.get(0)
                  .map(|bytes| bytes.len() / element_size)
                  .unwrap_or(0);

// Good: Use a reasonable default or derive from non-null elements
let capacity = if from.is_empty() {
    DEFAULT_CAPACITY
} else {
    // Find first non-null element or use default
    from.iter()
        .filter_map(|opt| opt.map(|bytes| bytes.len() / element_size))
        .next()
        .unwrap_or(DEFAULT_CAPACITY)
};
```

2. Use `Option<T>` when a function might not be able to determine a result with certainty:
```rust
// Bad: Returns bool even when we're uncertain
pub fn can_cast_to(&self, to: &DataType) -> bool {
    // might return false when we're not sure
}

// Good: Explicitly communicates uncertainty
pub fn can_cast_to(&self, to: &DataType) -> Option<bool> {
    // None = not sure, Some(false) = definitely cannot cast
}
```

3. Avoid unsafe shortcuts when accessing potentially null values - prefer safe methods that properly handle nulls and bounds checking:
```rust
// Bad: Unsafe access for simple value retrieval
if let Some(value) = unsafe { array.get_unchecked(0) } {
    // ...
}

// Good: Safe access with proper null handling
if let Some(value) = array.get(0) {
    // ...
}
```