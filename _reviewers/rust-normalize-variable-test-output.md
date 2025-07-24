---
title: Normalize variable test output
description: When writing tests that capture output (like UI tests, stderr, or stdout),
  ensure you normalize any variable content that might change between runs or versions
  to prevent fragile tests. This includes version numbers, debug information, instruction
  identifiers, and other implementation details that don't affect the functionality
  being tested.
repository: rust-lang/rust
label: Testing
language: Other
comments_count: 2
repository_stars: 105254
---

When writing tests that capture output (like UI tests, stderr, or stdout), ensure you normalize any variable content that might change between runs or versions to prevent fragile tests. This includes version numbers, debug information, instruction identifiers, and other implementation details that don't affect the functionality being tested.

For UI tests, use normalization directives:
```rust
//@ normalize-stderr: "!(dbg|noundef) ![0-9]+" -> "!$1 !N"
//@ normalize-stderr: "%[0-9]+" -> "%X"
//@ normalize-stdout: "current rust version: [0-9]+.[0-9]+.[0-9]+" -> "current rust version: #.#.#"
```

For complex output with potentially changing instruction ordering, consider using run-make tests with FileCheck instead of UI tests:
```rust
// In your run-make test
run(|config| {
    let filecheck = llvm_filecheck();
    filecheck
        .arg("--check-prefix=CHECK")
        .arg("--input-file=output.txt")
        .arg("expected.txt");
});
```

This approach ensures tests remain stable across version updates and implementation changes, reducing maintenance overhead and preventing false test failures.