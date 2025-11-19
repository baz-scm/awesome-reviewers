---
title: Cache expensive calculations
description: Avoid recalculating expensive operations in frequently called methods
  by caching results and only recalculating when necessary. This is especially important
  in rendering loops, event handlers, and other high-frequency code paths where the
  same computation may be performed repeatedly with the same inputs.
repository: nrwl/nx
label: Performance Optimization
language: Rust
comments_count: 3
repository_stars: 27518
---

Avoid recalculating expensive operations in frequently called methods by caching results and only recalculating when necessary. This is especially important in rendering loops, event handlers, and other high-frequency code paths where the same computation may be performed repeatedly with the same inputs.

Store calculated values in instance variables or state, and invalidate the cache only when the underlying data changes. This prevents performance bottlenecks from redundant computations.

Example of the problem:
```rust
fn draw(&mut self, f: &mut Frame<'_>, area: Rect) -> Result<()> {
    // Recalculates on every draw call - expensive!
    let column_visibility = self.calculate_column_visibility(area.width);
    // ... rest of drawing logic
}
```

Example of the solution:
```rust
fn draw(&mut self, f: &mut Frame<'_>, area: Rect) -> Result<()> {
    // Only recalculate if width changed or cache is invalid
    if self.column_visibility.is_none() || self.last_width != area.width {
        self.column_visibility = Some(self.calculate_column_visibility(area.width));
        self.last_width = area.width;
    }
    let column_visibility = self.column_visibility.as_ref().unwrap();
    // ... rest of drawing logic
}
```

Consider caching at initialization or on state changes rather than in performance-critical loops. When facing circular dependencies in calculations, pre-reserve space or use conservative estimates to avoid expensive recalculation cycles.