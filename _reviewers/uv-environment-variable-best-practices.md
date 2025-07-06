---
title: Environment variable best practices
description: 'When implementing environment variable configuration:


  1. Follow standard environment variable conventions:

  - Use uppercase with underscores (e.g., `NO_COLOR`, `FORCE_COLOR`)'
repository: astral-sh/uv
label: Configurations
language: Rust
comments_count: 5
repository_stars: 60322
---

When implementing environment variable configuration:

1. Follow standard environment variable conventions:
- Use uppercase with underscores (e.g., `NO_COLOR`, `FORCE_COLOR`)
- Validate non-empty values for boolean flags
- Support standard environment variables where applicable (e.g., `NO_COLOR`, `FORCE_COLOR`, `CLICOLOR_FORCE`)

2. Document environment variables clearly:
- Specify expected value formats and constraints
- Document the precedence order when multiple configuration methods exist
- Include examples of valid values

Example:
```rust
// Bad - No validation or documentation
if std::env::var_os("FORCE_COLOR").is_some() {
    ColorChoice::Always
}

// Good - Validates non-empty value and documents behavior
/// Controls color output. When set to a non-empty value, forces color output
/// regardless of terminal capabilities.
/// Takes precedence over NO_COLOR and --color settings.
if let Some(force_color) = std::env::var_os("FORCE_COLOR") {
    if !force_color.is_empty() {
        ColorChoice::Always
    }
}
```

3. Establish clear precedence rules:
- Document which settings take precedence (e.g., CLI flags vs environment variables)
- Consider standard environment variables first
- Fall back to custom environment variables before defaults

4. Provide validation and feedback:
- Validate environment variable values early
- Provide clear error messages for invalid values
- Consider warning on deprecated or conflicting configurations