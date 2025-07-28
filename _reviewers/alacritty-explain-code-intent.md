---
title: Explain code intent
description: Comments and documentation should explain WHY code exists and what purpose
  it serves, not just describe what the code does. Focus on the reasoning, motivation,
  and intent behind implementation decisions.
repository: alacritty/alacritty
label: Documentation
language: Rust
comments_count: 8
repository_stars: 59675
---

Comments and documentation should explain WHY code exists and what purpose it serves, not just describe what the code does. Focus on the reasoning, motivation, and intent behind implementation decisions.

When writing comments, ask yourself: "Would a developer understand the purpose and reasoning behind this code without additional context?" If not, add explanatory comments that clarify the intent.

**Good examples:**
```rust
// Attempt to make the context current, if it is not.
let mut was_context_reset = if is_current {
    false
} else {
    match self.context.make_current(&self.surface) {
        // ... implementation
    }
};
```

```rust
// Windows environment variables require null-terminated strings,
// with a double null at the end to mark the end of the environment block.
result.push(0);
result.push(0);
```

**Avoid comments that just restate the code:**
```rust
// This comment provides no value
// Unsafe because of Windows API calls.
unsafe { /* ... */ }
```

**Instead, explain safety or purpose:**
```rust
// Safe because we verify the handle is valid before dereferencing
unsafe { /* ... */ }
```

This is especially important for complex logic, platform-specific code, non-obvious algorithms, and any code where the implementation strategy might not be immediately clear to future maintainers.