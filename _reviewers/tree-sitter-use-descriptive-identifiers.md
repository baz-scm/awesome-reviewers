---
title: Use descriptive identifiers
description: Choose identifiers that clearly communicate their purpose, content, or
  role rather than using generic or abbreviated names. Names should be self-documenting
  and reduce the need to reference documentation or implementation details to understand
  what they represent.
repository: tree-sitter/tree-sitter
label: Naming Conventions
language: Rust
comments_count: 5
repository_stars: 21799
---

Choose identifiers that clearly communicate their purpose, content, or role rather than using generic or abbreviated names. Names should be self-documenting and reduce the need to reference documentation or implementation details to understand what they represent.

Apply this principle to:
- **Fields and variables**: Use specific names that indicate content type or purpose
- **Error variants**: Include context about what makes them invalid
- **Generic parameters**: Use descriptive names instead of single letters when the purpose isn't obvious
- **Function parameters**: Choose names that clearly indicate the expected data

Examples of improvements:
```rust
// Before: Generic field name
.supertypes = ts_supertypes,

// After: Specific field name indicating content type  
.supertype_symbols = ts_supertype_symbols,

// Before: Vague error name
ReservedWordSet,

// After: Descriptive error name with context
InvalidReservedWordSet,

// Before: Generic lifetime parameter
QueryMatches<'a, 'tree: 'a, 'b: 'a, T: TextProvider<'b>>

// After: Descriptive lifetime parameter
QueryMatches<'a, 'tree: 'a, 'text_provider: 'a, T: TextProvider<'text_provider>>

// Before: Ambiguous field name
pub expected: String,

// After: Clear field name indicating purpose
pub expected_capture_name: String,
```

This approach improves code readability and reduces cognitive load for developers who need to understand the codebase quickly.