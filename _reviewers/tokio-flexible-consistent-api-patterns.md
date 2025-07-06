---
title: Flexible consistent API patterns
description: Design APIs with flexibility and consistency by leveraging established
  patterns and avoiding unnecessary constraints. Accept generic type bounds instead
  of concrete types to provide more flexibility to users and simplify usage.
repository: tokio-rs/tokio
label: API
language: Rust
comments_count: 6
repository_stars: 28989
---

Design APIs with flexibility and consistency by leveraging established patterns and avoiding unnecessary constraints. Accept generic type bounds instead of concrete types to provide more flexibility to users and simplify usage.

**Be flexible with input types:**
```rust
// Less flexible - requires exact String type
pub fn name(&mut self, name: String) -> &mut Self {
    // ...
}

// More flexible - accepts any type that can be converted to String
pub fn name<S: Into<String>>(&mut self, name: S) -> &mut Self {
    // ...
}
```

**Follow established patterns** in your codebase to ensure consistency across similar APIs. When you need to design a new component, look for similar existing components as inspiration, avoiding unnecessary reinvention. For instance, if other stream types provide a specific set of methods, your new stream type should follow similar patterns.

**Avoid arbitrary restrictions** that don't align with similar methods. For example, if related methods allow zero values, a new method should also allow zero values unless there's a compelling reason not to:

```rust
// Inconsistent - restricts n to be > 0 when other methods don't
pub fn detach(&mut self, n: usize) -> Result<SemaphorePermit<'_>, Error> {
    if n == 0 || n >= self.permits {
        return Err(Error::InvalidValue);
    }
    // ...
}

// Consistent - follows the same patterns as similar methods
pub fn detach(&mut self, n: usize) -> Result<SemaphorePermit<'_>, Error> {
    if n > self.permits {
        return Err(Error::InvalidValue);
    }
    // ...
}
```

Choose names that clearly communicate behavior and purpose. Method names like `spawn_aborting` might suggest immediate abortion rather than creating something that aborts on drop. Consider alternatives like `spawn_with_abort_handle` or make it a constructor method on a type that better explains its purpose.