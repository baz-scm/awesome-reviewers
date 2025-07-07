---
title: Choose semantically clear identifiers
description: 'Select parameter and method names that accurately describe their purpose
  and behavior, avoiding ambiguous terms that can lead to confusion. Consider these
  guidelines:'
repository: huggingface/tokenizers
label: Naming Conventions
language: Rust
comments_count: 4
repository_stars: 9868
---

Select parameter and method names that accurately describe their purpose and behavior, avoiding ambiguous terms that can lead to confusion. Consider these guidelines:

1. Use descriptive names that reflect the actual behavior:
   ```rust
   // AVOID: Parameter name doesn't clearly indicate truncation behavior
   pub fn truncate(&mut self, max_len: usize, stride: usize, left: bool) {
      // ...
   }
   
   // BETTER: Use an enum with meaningful names
   pub fn truncate(&mut self, max_len: usize, stride: usize, direction: TruncationDirection) {
      // ...
   }
   ```

2. Follow language-specific naming conventions:
   - In Python interfaces, use lowercase for enum values (`"first"` instead of `"First"`)
   - In Rust, avoid leading underscores for public functions (`from_string` not `_from_string`)

3. Choose names that prevent confusion between related but different concepts:
   ```rust
   // AVOID: Similar method names with different behaviors
   fn add_tokens(&mut self) { /* ... */ }
   fn num_added_tokens(&self) { /* ... */ }
   
   // BETTER: Clear distinction in naming
   fn add_tokens(&mut self) { /* ... */ }
   fn num_special_tokens_to_add(&self) { /* ... */ }
   ```

When choosing identifiers, always ask: "Would another developer immediately understand what this name represents without looking at its implementation?"