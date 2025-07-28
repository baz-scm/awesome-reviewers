---
title: Avoid unwrap on nullables
description: Never use `unwrap()` on nullable values that could reasonably be None,
  as this can cause crashes that are harder for users to work around than bugs. Instead,
  provide graceful fallbacks or proper error handling.
repository: alacritty/alacritty
label: Null Handling
language: Rust
comments_count: 5
repository_stars: 59675
---

Never use `unwrap()` on nullable values that could reasonably be None, as this can cause crashes that are harder for users to work around than bugs. Instead, provide graceful fallbacks or proper error handling.

The principle is: "We shouldn't crash here under any circumstances" and "Bugs would be easier to work around for users than crashes."

**Preferred patterns:**

```rust
// Bad - crashes on None
let country_code = locale.countryCode().unwrap();

// Good - graceful fallback
if let Some(country_code) = locale.countryCode() {
    format!("{}_{}.UTF-8", language_code, country_code)
} else {
    // Fall back to en_US in case the country code is not available.
    "en_US.UTF-8".to_string()
}

// Good - using map_or for cleaner handling
match self.hint.mouse {
    None => MouseButton::Left,
    Some(c) => c.button.0,
}
// Better as:
self.hint.mouse.map_or(MouseButton::Left, |c| c.button.0)

// Bad - empty string treated as valid due to unwrap_or(0)
let codepoint = text.chars().next().map(u32::from).unwrap_or(0);

// Good - explicit empty check
let codepoint = match text.chars().next() {
    Some(c) => u32::from(c),
    None => return false, // Handle empty case explicitly
};
```

Use `if let Some()`, `map_or()`, or explicit match statements instead of `unwrap()` to handle nullable values safely.