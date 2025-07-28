---
title: Target documentation to audience
description: Write documentation that matches both your audience's expertise level
  and the language's conventional formats. For technical documentation, use language-specific
  conventions (like Rust's doc comments). For tutorials or learning materials, prefer
  step-by-step explanations that minimize cognitive load.
repository: helix-editor/helix
label: Documentation
language: Other
comments_count: 2
repository_stars: 39026
---

Write documentation that matches both your audience's expertise level and the language's conventional formats. For technical documentation, use language-specific conventions (like Rust's doc comments). For tutorials or learning materials, prefer step-by-step explanations that minimize cognitive load.

Example:
```rust
// Technical API documentation - uses language conventions
/// Processes the input string and returns a formatted result
/// 
/// # Arguments
/// * `input` - The string to process
pub fn process_string(input: &str) -> String { }

// Tutorial/Learning documentation - uses simpler, step-by-step format
// Step 1: First, create a new string variable
// Step 2: Add your text to the variable
// Step 3: Call the process_string function with your variable
```

Consider your audience's familiarity with the codebase and technical concepts when choosing between detailed technical documentation and simplified, step-by-step explanations. Always follow the language's documentation conventions while maintaining appropriate detail level for the target readers.