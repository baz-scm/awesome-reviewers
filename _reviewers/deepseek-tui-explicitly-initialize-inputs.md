---
title: Explicitly Initialize Inputs
description: Ensure every required value is explicitly initialized/propagated across
  both configuration variants and process boundaries. Do not rely on “it will be set
  implicitly” behavior—new fields or external inputs can end up effectively undefined/empty.
repository: Hmbown/DeepSeek-TUI
label: Null Handling
language: Rust
comments_count: 2
repository_stars: 21278
---

Ensure every required value is explicitly initialized/propagated across both configuration variants and process boundaries. Do not rely on “it will be set implicitly” behavior—new fields or external inputs can end up effectively undefined/empty.

- For internal configuration (e.g., themes): when adding a new field, update *all* theme constructors/variants and provide a consistent default.
- For external commands: explicitly pass the value in the form the command expects (not just redirected stdin), and verify the command actually receives it.

Example (theme variants):
```rust
pub struct UiTheme {
    pub header_bg: Color,
    pub footer_bg: Color,
    // ...
}

impl UiTheme {
    pub fn dark() -> Self {
        Self {
            header_bg: Color::from_rgb(0,0,0),
            footer_bg: Color::from_rgb(20,20,20), // set everywhere
        }
    }

    pub fn light() -> Self {
        Self {
            header_bg: Color::from_rgb(255,255,255),
            footer_bg: Color::from_rgb(235,235,235), // set everywhere
        }
    }
}
```

Example (external input):
```rust
// Prefer passing the value in the exact parameter/variable form the command expects,
// rather than assuming redirected stdin will populate it.
let mut child = Command::new("powershell.exe")
    .args(["-NoProfile", "-Command", "Set-Clipboard -Value $input"]);
// ...then wire up $input per the intended mechanism and check the exit status.
```