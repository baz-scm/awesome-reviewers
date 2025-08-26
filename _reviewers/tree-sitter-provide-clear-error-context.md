---
title: Provide clear error context
description: Always provide meaningful, specific error messages that help users understand
  what went wrong and why. Use descriptive language that indicates what was expected
  versus what was encountered. Leverage error context tools like `with_context()`
  to add relevant information about the operation that failed, and use debug formatting
  for error display to show...
repository: tree-sitter/tree-sitter
label: Error Handling
language: Rust
comments_count: 4
repository_stars: 21799
---

Always provide meaningful, specific error messages that help users understand what went wrong and why. Use descriptive language that indicates what was expected versus what was encountered. Leverage error context tools like `with_context()` to add relevant information about the operation that failed, and use debug formatting for error display to show complete error chains.

Key practices:
- Use precise terminology: prefer "unexpected" over "invalid" when describing input that doesn't match expectations
- Add context to errors using `with_context()` to explain what operation was being performed
- Use debug formatting (`{:?}`) when printing errors to display the full error chain with "Caused by:" information
- Include relevant details like file paths, operation names, or expected values in error messages

Example:
```rust
// Instead of generic error
return Err(anyhow!("Invalid rule"));

// Provide specific context
return Err(ParseGrammarError::UnexpectedRule)?;

// Add operation context
fs::read_to_string(&location)
    .with_context(|| format!("failed to read {}", location.to_string_lossy()))?;

// Use debug format for complete error information
eprintln!("{:?}", err);
```

This approach makes debugging significantly easier by providing actionable information about what failed and why, rather than forcing developers to guess or dig through code to understand error conditions.