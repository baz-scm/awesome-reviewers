---
title: Design interfaces, not implementations
description: Create intuitive API interfaces that abstract away implementation details
  while providing a consistent experience for consumers. Use appropriate parameter
  types that express intent and maintain established patterns across your codebase.
repository: zed-industries/zed
label: API
language: Rust
comments_count: 12
repository_stars: 62119
---

Create intuitive API interfaces that abstract away implementation details while providing a consistent experience for consumers. Use appropriate parameter types that express intent and maintain established patterns across your codebase.

When designing function parameters:
- Use enums instead of primitive types for options with discrete values
- Consider builder patterns for complex configurations
- Hide implementation complexity behind clean interfaces
- Extract common patterns into reusable abstractions

```rust
// Before: Implementation-focused API
pub fn fetch(&self, remote_name: String, cx: &mut ModelContext<Self>) { /* ... */ }

// After: Intent-focused API with better parameter types
pub enum FetchTarget {
    AllRemotes,
    SpecificRemote(String)
}

pub fn fetch(&self, target: FetchTarget, cx: &mut ModelContext<Self>) { /* ... */ }

// Before: Platform-specific APIs with inconsistent signatures
fn set_dock_menu(&self, menu: Vec<MenuItem>, keymap: &Keymap) {}
fn update_jump_list(&self, entries: &[&Vec<String>]) -> Option<Vec<Vec<String>>> {}

// After: Unified interface hiding platform differences
fn update_recent_projects(&self, projects: Vec<PathBuf>) -> Result<()> {
    // Platform-specific implementations inside
}

// Maintain consistent builder patterns where established
let branch_button = Button::new("project_branch_trigger", branch_name)
    .color(Color::Muted)
    .style(ButtonStyle::Subtle)
    .when(settings.show_branch_icon, |button| {
        button.with_icon(Icon::GitBranch)
    });
```

Good interfaces reduce coupling between components, improve testability, and create more maintainable systems by allowing implementation details to evolve independently of the API contract.