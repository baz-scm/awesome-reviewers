---
title: Simplify complex expressions
description: Break down complex code structures into simpler, more readable forms.
  This includes avoiding deep nesting, extracting complex logic into helper functions,
  simplifying boolean expressions, and reducing code duplication.
repository: tree-sitter/tree-sitter
label: Code Style
language: Rust
comments_count: 12
repository_stars: 21799
---

Break down complex code structures into simpler, more readable forms. This includes avoiding deep nesting, extracting complex logic into helper functions, simplifying boolean expressions, and reducing code duplication.

Key practices:
- Use `match` statements instead of multiple `if` conditions for the same variable
- Extract repeated logic into helper functions rather than duplicating code
- Hoist complex expressions out of tuple/struct construction into separate variables
- Simplify boolean expressions (e.g., use `!(a || b)` instead of separate conditions)
- Avoid deep nesting by using early returns or extracting functions
- Use functional patterns like `unwrap_or()` instead of imperative `if/else` blocks
- Wrap repetitive code patterns in helper functions

Example of improvement:
```rust
// Before: Complex nested conditions
if filename == "package.json" {
    // logic
}
if filename == "package.json" || filename == "pom.xml" {
    // more logic
}

// After: Clear match statement
match (generate_opts.author_url, filename) {
    (Some(url), "package.json" | "pom.xml") => replacement.replace(AUTHOR_URL_PLACEHOLDER, url),
    (None, "package.json") => replacement.replace(AUTHOR_URL_PLACEHOLDER_JS, ""),
    (None, "pom.xml") => replacement.replace(AUTHOR_URL_PLACEHOLDER_JAVA, ""),
    _ => {},
}
```

This approach improves code maintainability, reduces cognitive load, and makes the codebase more approachable for new contributors.