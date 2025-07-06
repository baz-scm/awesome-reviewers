---
title: Declarative constraints over runtime
description: Design APIs that enforce constraints through type systems and declarative
  mechanisms rather than runtime checks. This makes invalid states unrepresentable
  by design and improves both API usability and reliability.
repository: astral-sh/uv
label: API
language: Rust
comments_count: 3
repository_stars: 60322
---

Design APIs that enforce constraints through type systems and declarative mechanisms rather than runtime checks. This makes invalid states unrepresentable by design and improves both API usability and reliability.

For example, when designing CLI arguments that shouldn't be used together, prefer declarative constraints:

```rust
// Preferred: Declarative constraint
#[arg(long, conflicts_with = "script")]
pub group: Option<String>

// Avoid: Runtime validation
if let (Some(_), Some(_)) = (group, script) {
    bail!("the argument '--group <GROUP>' cannot be used with '--script <SCRIPT>'")
}
```

Similarly, use appropriate types that enforce validity by construction rather than validation after parsing. This applies to enums for limited options, newtype patterns for validated values, and builder patterns with compile-time validation.