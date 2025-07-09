---
title: Descriptive, unambiguous identifiers
description: Choose names that clearly express intent and behavior while avoiding
  ambiguity. Identifiers should communicate their purpose to other developers without
  requiring them to read implementation details.
repository: vercel/turborepo
label: Naming Conventions
language: Rust
comments_count: 8
repository_stars: 28115
---

Choose names that clearly express intent and behavior while avoiding ambiguity. Identifiers should communicate their purpose to other developers without requiring them to read implementation details.

When naming functions, prefer specific, action-oriented names over vague descriptions:
```rust
// Avoid: Not clear what "update" means in this context
fn update_task_selection_pinned_state(&mut self) -> Result<(), Error> {
    self.preferences.set_active_task(None)?;
    Ok(())
}

// Better: Clearly communicates the function's purpose
fn clear_pinned_task(&mut self) -> Result<(), Error> {
    self.preferences.set_active_task(None)?;
    Ok(())
}
```

Consider context when choosing names. If changing visibility (e.g., private to public), ensure the name makes sense in its new context:
```rust
// Private function with implementation-specific name
fn config_init(...) { ... }

// Better name when made public
pub fn create_config(...) { ... }
```

For enum variants and type names, choose terms that accurately reflect their purpose:
- Use `PackagePresenceReason` instead of `PackageChangeReason` when describing why a package is included
- Prefer `direct_dependencies()` over `immediate_dependencies()` to clearly relate to other dependency types
- Choose `LogicalProperty` over the generic `AdditionalProperty`
- Avoid potentially misleading terms like `GlobalFileChanged` when `NonPackageFileChanged` is more precise

When multiple related types exist, names should help clarify their relationships and distinctions.