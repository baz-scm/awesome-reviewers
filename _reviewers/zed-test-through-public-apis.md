---
title: Test through public APIs
description: Write comprehensive tests that validate functionality through public
  interfaces rather than testing implementation details. Tests should cover diverse
  scenarios, handle platform-specific cases, and use appropriate assertions.
repository: zed-industries/zed
label: Testing
language: Rust
comments_count: 7
repository_stars: 62119
---

Write comprehensive tests that validate functionality through public interfaces rather than testing implementation details. Tests should cover diverse scenarios, handle platform-specific cases, and use appropriate assertions.

Key principles:
1. Test public contracts instead of private methods
2. Include diverse test cases (e.g., multibyte characters, edge cases)
3. Use platform-specific configurations when needed
4. Prefer visual/structural assertions over numeric ones

Example:

```rust
// Instead of testing private implementation:
#[test]
fn test_valid_url_ending() {
    assert!(valid_url_ending("http://example.com"));
}

// Better - test through public API with comprehensive cases:
#[test]
fn test_url_regex() {
    let urls = [
        "http://example.com",
        "http://example.com/(test)",
        "http://ünicode.com",
        "[http://example.com]"
    ];
    
    for url in urls {
        let matches = find_urls(url);
        assert_eq!(matches[0], url.trim_matches(|c| c == '[' || c == ']'));
    }
}

// Handle platform-specific cases:
#[cfg_attr(target_os = "windows", ignore)]
#[test]
fn test_file_operations() {
    // Platform-specific test implementation
}
```