---
title: Simplify for readability
description: Prioritize code readability by using simpler and more direct expressions.
  When possible, return values directly instead of using temporary variables and explicit
  return statements. Break complex logic into intermediate variables with descriptive
  names. Structure control flow for maximum clarity, preferring Rust idioms like match
  expressions over nested...
repository: huggingface/tokenizers
label: Code Style
language: Rust
comments_count: 6
repository_stars: 9868
---

Prioritize code readability by using simpler and more direct expressions. When possible, return values directly instead of using temporary variables and explicit return statements. Break complex logic into intermediate variables with descriptive names. Structure control flow for maximum clarity, preferring Rust idioms like match expressions over nested conditionals.

Example 1 - direct returns:
```rust
// Instead of:
pub fn from_string(content: String) -> Result<Self> {
    let tokenizer = serde_json::from_str(&content)?;
    Ok(tokenizer)
}

// Prefer:
pub fn from_string(content: &str) -> Result<Self> {
    serde_json::from_str(content)
}
```

Example 2 - match expressions:
```rust
// Instead of:
if direction != "right" && direction != "left" {
    panic!("Invalid truncation direction value : {}", direction);
}

let tdir = if direction == "right" {
    TruncateDirection::Right
} else {
    TruncateDirection::Left
};

// Prefer:
let direction = match direction.as_str() {
    "left"  => Truncate::Left,
    "right" => Truncate::Right,
    other => panic!("Invalid truncation direction value : {}", other),
};
```

For complex code blocks, use intermediate variables with descriptive names to break down logic and make the code easier to follow. When implementing iterators or transformation functions, consider structuring them for readability even if it requires a few more lines of code.