---
title: eliminate code duplication
description: Actively identify and eliminate code duplication by extracting repeated
  logic into reusable functions, using loops instead of repetitive code blocks, and
  consolidating similar implementations. When you find yourself copying and pasting
  code or writing nearly identical logic multiple times, refactor it into a shared
  function or use iteration patterns.
repository: block/goose
label: Code Style
language: Rust
comments_count: 9
repository_stars: 19037
---

Actively identify and eliminate code duplication by extracting repeated logic into reusable functions, using loops instead of repetitive code blocks, and consolidating similar implementations. When you find yourself copying and pasting code or writing nearly identical logic multiple times, refactor it into a shared function or use iteration patterns.

For example, instead of repeating similar command creation logic:

```rust
// Before: Duplicated command creation
let output = if cfg!(target_os = "windows") {
    Command::new("cmd")
        .args(["/C", command])
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .stdin(Stdio::null())
        .kill_on_drop(true)
        .output()
        .await?
} else {
    Command::new("sh")
        .args(["-c", command])
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .stdin(Stdio::null())
        .kill_on_drop(true)
        .output()
        .await?
};

// After: Consolidated approach
let mut command = if cfg!(target_os = "windows") {
    Command::new("cmd").args(["/C", command])
} else {
    Command::new("sh").args(["-c", command])
};
let output = command
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .stdin(Stdio::null())
    .kill_on_drop(true)
    .output()
    .await?;
```

Similarly, replace repetitive field processing with loops, extract common validation logic into helper functions, and consolidate similar error handling patterns. This improves maintainability, reduces the chance of bugs from inconsistent implementations, and makes the codebase more readable and easier to modify.