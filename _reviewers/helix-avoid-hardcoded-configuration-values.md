---
title: avoid hardcoded configuration values
description: Avoid hardcoding configuration values that affect user experience or
  behavior. Instead, make these values configurable with sensible defaults. This is
  especially important for timing values, thresholds, and user-facing constants that
  different users may want to customize.
repository: helix-editor/helix
label: Configurations
language: Rust
comments_count: 4
repository_stars: 39026
---

Avoid hardcoding configuration values that affect user experience or behavior. Instead, make these values configurable with sensible defaults. This is especially important for timing values, thresholds, and user-facing constants that different users may want to customize.

Examples of values that should be configurable rather than hardcoded:
- Completion trigger thresholds: `const MIN_WORD_LEN: usize = 7;` should be configurable for users who want completion for shorter words like "because"
- Timing values: `const DEBOUNCE: Duration = Duration::from_secs(1);` should be configurable as users may prefer faster response times like 20ms
- Default tokens: `let token = token.unwrap_or("//");` should use a configurable default comment token rather than hardcoding "//"
- Timeout values: hardcoded timeouts like 30ms should be configurable for testing and different user preferences

When making values configurable:
```rust
// Instead of:
const MIN_WORD_LEN: usize = 7;

// Do:
pub struct CompletionConfig {
    pub min_word_length: usize,
}

impl Default for CompletionConfig {
    fn default() -> Self {
        Self {
            min_word_length: 7, // Reasonable default, but configurable
        }
    }
}
```

This approach improves user experience by allowing customization while maintaining reasonable defaults for users who don't need to change the settings.