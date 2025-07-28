---
title: Explain non-obvious decisions
description: When code contains non-obvious parameter choices, conditional logic,
  or unexpected implementation changes, add comments explaining the reasoning behind
  these decisions. This helps other developers understand the context and prevents
  confusion during code reviews.
repository: denoland/deno
label: Documentation
language: Rust
comments_count: 3
repository_stars: 103714
---

When code contains non-obvious parameter choices, conditional logic, or unexpected implementation changes, add comments explaining the reasoning behind these decisions. This helps other developers understand the context and prevents confusion during code reviews.

Key scenarios requiring explanation:
- Hardcoded boolean values or magic numbers
- Conditional logic that skips validation or normal flow
- Unexpected library introductions or implementation changes
- Parameter choices that aren't self-evident

Example:
```rust
// Force dynamic loading to true because static analysis 
// cannot determine module type at compile time
.load_asset(&specifier, true, requested_module_type)

if !skip_graph_roots_validation {
  // Skip validation when called from dynamic imports where
  // root validation has already been performed upstream
  self.graph_roots_valid(graph, roots, allow_unknown_media_types)?;
}
```

The goal is to make the code self-documenting so that future maintainers can understand not just what the code does, but why specific decisions were made.