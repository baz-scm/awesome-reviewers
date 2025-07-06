---
title: Prefer idiomatic Option handling
description: When handling null values in Rust, use idiomatic Option patterns instead
  of verbose nested conditionals. This improves code readability, safety, and reduces
  the chance of runtime errors.
repository: zed-industries/zed
label: Null Handling
language: Rust
comments_count: 9
repository_stars: 62119
---

When handling null values in Rust, use idiomatic Option patterns instead of verbose nested conditionals. This improves code readability, safety, and reduces the chance of runtime errors.

Always prefer:
1. `is_some_and()` over `map_or(false, |x| ...)` when checking conditions on Option values:
```rust
// Instead of:
self.popover
    .as_ref()
    .map_or(false, |popover| popover.signature.len() > 1)

// Use:
self.popover
    .as_ref()
    .is_some_and(|popover| popover.signature.len() > 1)
```

2. The `?` operator for early returns instead of verbose `if let Some()` patterns:
```rust
// Instead of:
if let Some(editor) = Self::resolve_active_item_as_svg_editor(workspace, cx) {
    if Self::is_svg_file(&editor, cx) {
        // ... implementation ...
    }
}

// Use:
let editor = Self::resolve_active_item_as_svg_editor(workspace, cx)?;
if Self::is_svg_file(&editor, cx) {
    // ... implementation ...
}
```

3. `.ok()` to convert a Result to an Option when appropriate:
```rust
// Instead of:
let system_id = ids::get_or_create_id(&ids::eval_system_id_path())
    .unwrap_or_else(|_| String::new());

// Use:
let system_id = ids::get_or_create_id(&ids::eval_system_id_path()).ok();
```

4. Safe alternatives to `.unwrap()` which can cause runtime panics:
```rust
// Instead of:
workspace.subscribe(&workspace.weak_handle().upgrade().unwrap(), |editor, ...

// Use:
if let Some(workspace) = workspace.weak_handle().upgrade() {
    cx.subscribe(&workspace, |editor, ...
}
```

These patterns make your code more robust against null reference errors while keeping it concise and readable.