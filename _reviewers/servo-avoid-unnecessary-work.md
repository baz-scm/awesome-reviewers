---
title: avoid unnecessary work
description: Identify and eliminate computational work that serves no purpose, particularly
  for inactive, hidden, or irrelevant elements. This includes early returns for non-visible
  components, lazy initialization of expensive resources, and preventing work during
  inappropriate timing.
repository: servo/servo
label: Performance Optimization
language: Rust
comments_count: 8
repository_stars: 32962
---

Identify and eliminate computational work that serves no purpose, particularly for inactive, hidden, or irrelevant elements. This includes early returns for non-visible components, lazy initialization of expensive resources, and preventing work during inappropriate timing.

Key strategies:
- **Early returns for inactive elements**: Skip processing for hidden webviews, unfocused components, or elements that won't affect the final result
- **Lazy resource creation**: Defer expensive object creation until actually needed, not at declaration time
- **Conditional processing**: Check visibility, focus state, or relevance before performing expensive operations
- **Timing-aware operations**: Avoid recursive or redundant work during update cycles

Example from display list processing:
```rust
// Before: Always process display lists
fn handle_display_list(&mut self, webview_id: WebViewId, display_list: DisplayList) {
    self.process_display_list(webview_id, display_list);
}

// After: Skip processing for hidden webviews
fn handle_display_list(&mut self, webview_id: WebViewId, display_list: DisplayList) {
    if !self.webview_renderers.is_shown(webview_id) {
        return debug!("Ignoring display list for hidden webview {:?}", webview_id);
    }
    self.process_display_list(webview_id, display_list);
}
```

Example from variable initialization:
```rust
// Before: Create display immediately
let display = path.display();
if some_condition {
    println!("Error with {}", display);
}

// After: Create display only when needed
if some_condition {
    let display = path.display();
    println!("Error with {}", display);
}
```

This optimization prevents wasted CPU cycles, reduces memory pressure, and improves overall application responsiveness by ensuring computational resources are only used when they contribute to meaningful work.