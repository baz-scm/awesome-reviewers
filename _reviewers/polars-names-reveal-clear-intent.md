---
title: Names reveal clear intent
description: Choose names that clearly communicate intent and context, avoiding ambiguity
  or confusion. Variable and function names should be self-documenting and reflect
  their domain purpose.
repository: pola-rs/polars
label: Naming Conventions
language: Rust
comments_count: 6
repository_stars: 34296
---

Choose names that clearly communicate intent and context, avoiding ambiguity or confusion. Variable and function names should be self-documenting and reflect their domain purpose.

Key guidelines:
- Use domain-specific terminology consistently
- Prefer descriptive names over generic ones
- Make implicit context explicit in the name
- Avoid positional/numeric references in favor of semantic names

Example - Before:
```rust
fn make_categoricals_compatible(
    input: &[column],  // Uses numeric index input[1]
    array_width: usize,
) 
```

After:
```rust
fn make_rhs_categoricals_compatible(
    CategoryMapping {
        source_column,
        target_column,
    }: CategoryMapping,
    array_width_in_bytes: usize,
)
```

The improved version:
- Clarifies the function's effect on right-hand side
- Uses a semantic structure instead of array indices
- Adds context to the width parameter
- Makes the relationship between parameters explicit