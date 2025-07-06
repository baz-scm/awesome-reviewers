---
title: Protect render loop performance
description: Ensure render loop operations stay within frame time budget (typically
  16.67ms for 60fps). Avoid expensive computations, traversals, and I/O operations
  during frame rendering. Instead, compute and cache results ahead of time or move
  heavy operations to background tasks.
repository: zed-industries/zed
label: Performance Optimization
language: Rust
comments_count: 4
repository_stars: 62119
---

Ensure render loop operations stay within frame time budget (typically 16.67ms for 60fps). Avoid expensive computations, traversals, and I/O operations during frame rendering. Instead, compute and cache results ahead of time or move heavy operations to background tasks.

Example of problematic code:
```rust
fn render_outline(&self, cx: &mut Context) {
    // Bad: Expensive loop during rendering
    for outline in self.outlines {
        if self.has_outline_children(outline, cx) {
            // ... rendering logic
        }
    }
}
```

Better approach:
```rust
fn render_outline(&self, cx: &mut Context) {
    // Good: Use pre-computed results during render
    for (outline, has_children) in &self.cached_outline_data {
        if *has_children {
            // ... rendering logic
        }
    }
}

// Update cache in background or on data changes
fn update_outline_cache(&mut self, cx: &mut Context) {
    let mut cached_data = Vec::new();
    for outline in self.outlines {
        cached_data.push((outline, self.has_outline_children(outline, cx)));
    }
    self.cached_outline_data = cached_data;
}
```

Key guidelines:
- Cache computed values that are expensive to calculate
- Move tree traversals, I/O operations, and heavy computations outside the render loop
- Use background tasks for expensive operations that need to update the UI
- Consider debouncing frequent updates to avoid unnecessary recalculations