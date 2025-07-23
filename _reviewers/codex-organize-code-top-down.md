---
title: Organize code top down
description: Structure code files with a clear top-down organization, placing primary
  functions and important declarations at the top, followed by helper functions and
  implementation details below. This improves code readability and maintainability
  by establishing a clear hierarchy.
repository: openai/codex
label: Code Style
language: Rust
comments_count: 4
repository_stars: 31275
---

Structure code files with a clear top-down organization, placing primary functions and important declarations at the top, followed by helper functions and implementation details below. This improves code readability and maintainability by establishing a clear hierarchy.

Key principles:
1. Place core public interfaces and primary functions at the top
2. Move helper functions and implementation details to the bottom
3. Extract large code blocks into separate files when they represent distinct functionality
4. Position shared computations before their usage points

Example:
```rust
// Primary public interface first
pub fn process_event(&mut self, event: Event) {
    self.dispatch_event(event)
}

// Main implementation functions next
fn dispatch_event(&mut self, event: Event) {
    let common_data = self.prepare_common_data();  // Shared computation moved up
    match event {
        Event::A => self.handle_a(common_data),
        Event::B => self.handle_b(common_data),
    }
}

// Helper functions last
fn prepare_common_data(&self) -> Data {
    // Implementation details...
}

fn handle_a(&mut self, data: Data) {
    // Implementation details...
}

fn handle_b(&mut self, data: Data) {
    // Implementation details...
}
```