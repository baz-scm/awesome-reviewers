---
title: Add comprehensive test coverage
description: Ensure that all functionality, especially complex or quirky features,
  has corresponding unit tests. When adding new features or modifying existing code,
  proactively identify areas that lack test coverage and add appropriate tests.
repository: denoland/deno
label: Testing
language: Rust
comments_count: 3
repository_stars: 103714
---

Ensure that all functionality, especially complex or quirky features, has corresponding unit tests. When adding new features or modifying existing code, proactively identify areas that lack test coverage and add appropriate tests.

This is particularly important for:
- Complex parsing logic or edge cases ("especially that the parsing is a bit quirky")
- Utility functions that may seem simple but have important behavior
- Similar functionality that should be tested consistently

For example, when adding flag parsing functionality:
```rust
#[test]
fn test_clean_command_parsing() {
  // Test basic clean command
  let mut flags = Flags::default();
  let matches = /* create test matches */;
  clean_parse(&mut flags, &matches);
  assert_eq!(flags.subcommand, DenoSubcommand::Clean);
}

#[test] 
fn test_clean_command_with_options() {
  // Test clean command with various options
  // ...
}
```

Or for utility functions:
```rust
#[test]
fn test_url_to_uri_conversion() {
  // Test various URL formats
  assert_eq!(url_to_uri(&url).unwrap(), expected_uri);
}
```

Don't assume that functionality is "too simple" to test - utility functions, parsing logic, and similar features across a codebase should all have comprehensive test coverage to prevent regressions and ensure correctness.