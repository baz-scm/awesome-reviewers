---
title: Structured, Meaningful Tests
description: 'Tests should follow consistent structure and provide high-signal coverage.


  Apply these rules:

  1) Put tests in dedicated files

  - Follow the repo convention: place unit tests in separate `*_tests.rs` (or `*_test.rs`)
  files, not inline `#[cfg(test)] mod tests { ... }` blocks.'
repository: warpdotdev/warp
label: Testing
language: Rust
comments_count: 9
repository_stars: 56893
---

Tests should follow consistent structure and provide high-signal coverage.

Apply these rules:
1) Put tests in dedicated files
- Follow the repo convention: place unit tests in separate `*_tests.rs` (or `*_test.rs`) files, not inline `#[cfg(test)] mod tests { ... }` blocks.
- Avoid inserting test modules between import statements. If you need a separate file but want to keep the module declaration local, use `#[path = "..."] mod tests;`.

Example pattern:
```rust
// in source file
#[cfg(test)]
#[path = "my_module_tests.rs"]
mod tests;
```

2) Keep tests concise and behavior-focused
- Don’t add verbose scaffolding when a test only needs to prove one meaningful behavior (e.g., “override/clear works”).

3) Consolidate related checks into regression-style tests
- When covering a previously reported bug, consolidate to a single regression test and add a comment pointing to the issue/PR (e.g., `// regression for #10139`).

4) Assert complete, observable sequences
- If logic triggers multiple events (e.g., press + release routing), the test should assert the full sequence rather than only the first effect.

5) Ensure cross-platform coverage when you condition tests
- If tests are excluded on Windows (or made platform-dependent), add Windows-specific unit tests to validate the same behavior/round-trip semantics.

These practices improve maintainability, reduce test brittleness, and ensure coverage remains accurate as behavior evolves.