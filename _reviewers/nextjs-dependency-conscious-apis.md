---
title: "Dependency conscious APIs"
description: "Design APIs with dependency implications in mind. Carefully consider how your API design choices might force dependencies on consumers, which can lead to dependency bloat or tight coupling between components."
repository: "vercel/next.js"
label: "API"
language: "Rust"
comments_count: 2
repository_stars: 133000
---

Design APIs with dependency implications in mind. Carefully consider how your API design choices might force dependencies on consumers, which can lead to dependency bloat or tight coupling between components.

When designing APIs that bridge between different modules or layers:

1. Structure interfaces to minimize unnecessary dependencies across your codebase
2. Balance between using convenient abstractions and maintaining clean dependency isolation
3. Consider alternative designs that maintain functionality without adding dependencies

**Example:**
Instead of forcing all components to depend on a specific implementation:

```rust
// Avoid: Forces napi dependency on all consumers
#[napi(object)]
struct EventObject {
    type_name: String,
    severity: String,
    message: String
}

// Better: Uses generic interfaces without dependency leakage
pub fn emit_compilation_event<T: CompilationEvent>(event: T) {
    turbo_tasks().emit_compilation_event(Arc::new(event));
}
```

This approach allows functionality to be used without requiring direct dependencies on implementation details, keeping your architecture more flexible and maintainable.