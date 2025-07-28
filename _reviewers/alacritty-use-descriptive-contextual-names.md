---
title: Use descriptive contextual names
description: Choose variable, function, and struct names that clearly communicate
  their purpose and content while considering their surrounding context. Avoid generic
  names like `x`, `normal`, or `data` that provide no semantic meaning. When naming
  within a specific scope or module, avoid redundant prefixes that repeat the context.
repository: alacritty/alacritty
label: Naming Conventions
language: Rust
comments_count: 13
repository_stars: 59675
---

Choose variable, function, and struct names that clearly communicate their purpose and content while considering their surrounding context. Avoid generic names like `x`, `normal`, or `data` that provide no semantic meaning. When naming within a specific scope or module, avoid redundant prefixes that repeat the context.

**Bad examples:**
```rust
// Generic, meaningless names
let x = error_result;
let normal = should_use_standard_input;
let first_line = column_count; // Misleading content

// Redundant context
struct WindowConfig {
    pub window_level: WindowLevel, // "window" is redundant
}

// Implementation-focused naming
pub fn try_from_textual(&self) -> Option<SequenceBase> // Doesn't return Self
```

**Good examples:**
```rust
// Descriptive, purpose-driven names
let err = error_result;
let use_standard_input = should_use_standard_input;
let column_count = first_line_columns;

// Context-aware naming
struct WindowConfig {
    pub level: WindowLevel, // Context is clear from struct name
}

// Semantic naming
pub fn try_build_textual(&self) -> Option<SequenceBase> // Clear about what it builds
```

Consider the scope and context when naming - a variable named `level` inside a `WindowConfig` is clearer than `window_level`. Use domain-specific terminology that your team understands, and prefer full words over abbreviations unless the abbreviation is universally recognized in your domain (like `fd` for file descriptor).