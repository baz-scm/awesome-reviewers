---
title: reduce nesting complexity
description: Prefer code structures that minimize nesting levels and improve readability
  through early returns, pattern matching, and avoiding deeply nested assignments.
repository: helix-editor/helix
label: Code Style
language: Rust
comments_count: 5
repository_stars: 39026
---

Prefer code structures that minimize nesting levels and improve readability through early returns, pattern matching, and avoiding deeply nested assignments.

Use early returns and let-else patterns to reduce nesting:

```rust
// Instead of nested if-let
if let Some(doc) = doc {
    if let Some(version) = document_version {
        if version != doc.version() {
            log::info!("Version mismatch");
            return;
        }
    }
    // process doc
}

// Prefer early returns and let-else
let Some(doc) = self
    .documents
    .values_mut()
    .find(|doc| doc.uri().is_some_and(|u| u == uri))
else {
    return;
};
if let Some(version) = document_version {
    if version != doc.version() {
        log::info!("Version mismatch");
        return;
    }
}
// process doc
```

Use match statements instead of nested conditionals when appropriate, and avoid let blocks that increase indentation unnecessarily. Don't create deeply nested assignments as they are hard to read and don't fit with the codebase style. When possible, use mutable variables in the same scope rather than introducing additional nesting levels.