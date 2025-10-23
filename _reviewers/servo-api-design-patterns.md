---
title: API design patterns
description: Design APIs with appropriate parameter types, place conversion functions
  as trait implementations in the correct modules, and reuse existing patterns instead
  of creating new abstractions.
repository: servo/servo
label: API
language: Rust
comments_count: 9
repository_stars: 32962
---

Design APIs with appropriate parameter types, place conversion functions as trait implementations in the correct modules, and reuse existing patterns instead of creating new abstractions.

Key principles:
1. **Use appropriate parameter types**: Prefer `&[T]` over `&Vec<T>` for function parameters to accept more input types and improve API flexibility.

2. **Place conversions as trait implementations**: When creating conversion functions, implement them as traits (like `From<&str>`) in the module where the target type is defined, rather than standalone functions elsewhere.

3. **Reuse existing patterns**: Before creating new IPC messages, traits, or abstractions, check if existing patterns can be extended or reused. Avoid adding dependencies just for cleaner conversions when simple functions suffice.

4. **Prefer functional patterns**: Use `map()`, `unwrap_or_else()`, and similar combinators instead of imperative if-let chains when it improves readability.

Example of good API design:
```rust
// Good: slice parameter, functional style
fn process_link_headers(link_headers: &[LinkHeader]) -> Vec<ProcessedLink> {
    link_headers.iter()
        .map(|header| process_header(header))
        .collect()
}

// Good: trait implementation in type's module
impl From<&str> for CorsSettings {
    fn from(token: &str) -> Self {
        match_ignore_ascii_case! { token,
            "anonymous" => CorsSettings::Anonymous,
            "use-credentials" => CorsSettings::UseCredentials,
            _ => CorsSettings::Anonymous,
        }
    }
}
```

This approach creates more flexible, discoverable, and maintainable APIs while avoiding unnecessary complexity.