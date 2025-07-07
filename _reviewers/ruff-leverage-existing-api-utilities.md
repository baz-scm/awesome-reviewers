---
title: Leverage existing API utilities
description: When implementing or consuming APIs, always prefer using existing utility
  methods and abstractions over manual implementations. This reduces code duplication,
  improves consistency, and helps avoid subtle bugs in conversion logic or interface
  handling.
repository: astral-sh/ruff
label: API
language: Rust
comments_count: 4
repository_stars: 40619
---

When implementing or consuming APIs, always prefer using existing utility methods and abstractions over manual implementations. This reduces code duplication, improves consistency, and helps avoid subtle bugs in conversion logic or interface handling.

For example, when working with text ranges in a language server:

```rust
// Instead of this manual conversion:
let start_offset = params.range.start.to_text_size(&source, &line_index, snapshot.encoding());
let end_offset = params.range.end.to_text_size(&source, &line_index, snapshot.encoding());
let requested_range = ruff_text_size::TextRange::new(start_offset, end_offset);

// Use the existing utility method:
let requested_range = params.range.to_text_range(...);
```

Similarly, when checking module types or other special cases:

```rust
// Instead of string comparison:
builtin: module_name.as_str() == "builtins"

// Use the domain-specific API:
builtin: module.is_known(KnownModule::Builtins)
```

And when performing pattern matching on expressions:

```rust
// Instead of nested match statements:
match expr {
    Expr::Call(expr_call) => match checker.semantic().resolve_qualified_name(&expr_call.func) {
        Some(name) => name.segments() == ["pathlib", "Path"],
        None => false,
    },
    _ => false,
}

// Use method chaining with is_some_and:
expr.as_call_expr().is_some_and(|expr_call| {
    checker
        .semantic()
        .resolve_qualified_name(&expr_call.func)
        .is_some_and(|name| matches!(name.segments(), ["pathlib", "Path"]))
})
```

Take time to familiarize yourself with the available utilities in the API you're working with, particularly for common operations like conversions, validations, and pattern matching.