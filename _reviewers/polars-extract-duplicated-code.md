---
title: Extract duplicated code
description: Identify and extract duplicated code into reusable functions or move
  common fields to parent structures. This makes the codebase more maintainable and
  reduces the risk of inconsistencies when code needs to be updated.
repository: pola-rs/polars
label: Code Style
language: Rust
comments_count: 10
repository_stars: 34296
---

Identify and extract duplicated code into reusable functions or move common fields to parent structures. This makes the codebase more maintainable and reduces the risk of inconsistencies when code needs to be updated.

Consider these refactoring approaches:

1. **Move common fields to parent structures** when multiple states or variants contain the same fields:
```rust
// Instead of this:
struct ShiftNode {
    state: State,
}
enum State {
    StateA { buffer: Vec<T>, seq: MorselSeq },
    StateB { buffer: Vec<T>, seq: MorselSeq },
}

// Do this:
struct ShiftNode {
    state: State,
    buffer: Vec<T>,
    seq: MorselSeq,
}
enum State {
    StateA,
    StateB,
}
```

2. **Extract repeated patterns into functions** when similar code appears in multiple locations:
```rust
// Instead of repeating this pattern:
match self.dtype() {
    #[cfg(feature = "timezones")]
    Datetime(_, Some(tz)) => { /* complex logic */ },
    _ => { /* similar complex logic */ }
}

// Create a helper function:
fn process_with_timezone(&self, has_timezone: bool) -> Result {
    // Implementation that handles both cases
}
```

3. **Use named constants** instead of magic numbers:
```rust
// Instead of:
Scalar::new(Time, AnyValue::Time(86_399_999_999_999))

// Use a descriptive constant:
Scalar::new(Time, AnyValue::Time(NS_IN_DAY - 1))
```

4. **Parameterize functions** to handle variation rather than duplicating similar functions:
```rust
// Instead of two nearly identical functions:
fn prepare_expression_for_context() { /* ... */ }
fn prepare_expression_for_context_with_schema() { /* ... */ }

// Create one function with an optional parameter:
fn prepare_expression_for_context(schema: Option<Schema>) { /* ... */ }
```

These refactorings improve readability, maintainability, and reduce the risk of bugs when one instance of duplicated code is updated but others are missed.