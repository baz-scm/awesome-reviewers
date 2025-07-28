---
title: Configuration validation feedback
description: Always validate configuration options and provide clear feedback to users
  about potential issues. This includes warning about unused configuration keys, preventing
  redundant options, and ensuring cross-platform compatibility.
repository: alacritty/alacritty
label: Configurations
language: Rust
comments_count: 5
repository_stars: 59675
---

Always validate configuration options and provide clear feedback to users about potential issues. This includes warning about unused configuration keys, preventing redundant options, and ensuring cross-platform compatibility.

Key practices:
1. **Warn about unused keys**: Implement logging for configuration keys that are parsed but not used, helping users identify typos or deprecated settings
2. **Avoid redundant options**: When designing configuration structures, ensure there's no ambiguity between `None` and default enum values - choose one approach consistently
3. **Cross-platform validation**: Use `allow(unused)` instead of `cfg` attributes for configuration fields to prevent warnings on platforms where the feature isn't available
4. **Validate combinations**: Require at least one valid option when multiple configuration fields are mutually dependent

Example implementation:
```rust
// Warn about unused keys during deserialization
for key in unused.keys() {
    log::warn!(target: LOG_TARGET, "Unused config key: {}", key);
}

// Avoid redundant options - choose Option<T> OR T::Default, not both
pub struct WindowConfig {
    // Good: Clear intent
    pub window_level: WindowLevel, // with Default trait
    
    // Avoid: Ambiguous between None and WindowLevel::Normal
    // pub window_level: Option<WindowLevel>,
}

// Validate required combinations
if !content.hyperlinks && content.regex.is_none() {
    return Err("At least one of hyperlink or regex must be specified");
}
```

This approach prevents configuration errors that can be difficult to debug and improves the user experience by providing immediate feedback about configuration issues.