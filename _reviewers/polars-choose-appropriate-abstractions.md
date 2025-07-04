---
title: Choose appropriate abstractions
description: 'When designing APIs, select data types and patterns that match how they
  will be consumed while facilitating long-term maintainability:


  1. Use data types that naturally fit the intended usage pattern. For cloud paths,
  prefer `String`/`Box<str>` over `OsStr` when APIs you interact with expect string
  types:'
repository: pola-rs/polars
label: API
language: Rust
comments_count: 4
repository_stars: 34296
---

When designing APIs, select data types and patterns that match how they will be consumed while facilitating long-term maintainability:

1. Use data types that naturally fit the intended usage pattern. For cloud paths, prefer `String`/`Box<str>` over `OsStr` when APIs you interact with expect string types:
```rust
// Instead of:
path: Box<OsStr>, // requires conversions when used with string APIs

// Prefer:
path: Box<str>, // directly compatible with string-based APIs
```

2. Prefer serialization approaches that decouple interface from implementation. When handling complex structures that may change over time, consider JSON serialization rather than field-by-field matching:
```rust
// Instead of field-by-field matching:
IR::Sink { input, payload } => Sink {
    // Complex, brittle field extraction...
}

// Prefer:
IR::Sink { input, payload } => Sink {
    input: input.0,
    payload: serde_json::to_string(payload)?
}
```

3. Design for capability-based extensibility rather than type discrimination. Use flags to indicate capabilities instead of checking specific types, allowing for plugins and extensions:
```rust
// Instead of checking specific reader types
if let FileReaderType::CSV = reader_type {
    // CSV-specific handling
}

// Prefer capability flags
if reader.supports_projection() {
    // Handle projection for any reader supporting it
}
```

4. Structure APIs to avoid complex state management. Builder patterns with clear ownership transfer make code more predictable:
```rust
// Instead of:
let df = LazyCsvReader::new("reddit.csv") // Path stored as internal state

// Prefer:
let df = LazyCsvReader::new().load("reddit.csv") // No internal state tracking
```

These approaches lead to more maintainable APIs that are easier to extend and evolve over time.