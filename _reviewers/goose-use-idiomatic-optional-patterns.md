---
title: Use idiomatic optional patterns
description: Prefer Rust's built-in optional handling methods over manual checks and
  intermediate variables. Use `if let Some(value) = option` for pattern matching,
  `option.map(|x| x.field).unwrap_or(default)` for transformations with fallbacks,
  and `option.is_some_and(|x| condition)` for conditional checks.
repository: block/goose
label: Null Handling
language: Rust
comments_count: 3
repository_stars: 19037
---

Prefer Rust's built-in optional handling methods over manual checks and intermediate variables. Use `if let Some(value) = option` for pattern matching, `option.map(|x| x.field).unwrap_or(default)` for transformations with fallbacks, and `option.is_some_and(|x| condition)` for conditional checks.

Instead of creating intermediate variables:
```rust
let is_recipe_execution = recipe.is_some();
let recipe_name_for_telemetry = recipe.clone().unwrap_or_default();
```

Use direct pattern matching:
```rust
if let Some(recipe_name) = recipe {
    // use recipe_name directly
}
```

Instead of verbose match statements:
```rust
let recipe_version = match load_recipe(&name, params) {
    Ok(recipe) => recipe.version,
    Err(_) => "unknown".to_string(),
};
```

Use method chaining:
```rust
let recipe_version = load_recipe(&name, params)
    .map(|r| r.version)
    .unwrap_or_else(|| "unknown".to_string());
```

These patterns reduce boilerplate, improve readability, and leverage Rust's type system for safer null handling.