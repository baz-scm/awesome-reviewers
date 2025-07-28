---
title: avoid version-specific documentation
description: When writing build and deployment documentation, avoid hard-coding specific
  version numbers, toolchain assumptions, or environment-specific details that will
  become outdated or may not apply to all users. Instead, use generic language that
  describes the underlying requirement or constraint.
repository: helix-editor/helix
label: CI/CD
language: Markdown
comments_count: 3
repository_stars: 39026
---

When writing build and deployment documentation, avoid hard-coding specific version numbers, toolchain assumptions, or environment-specific details that will become outdated or may not apply to all users. Instead, use generic language that describes the underlying requirement or constraint.

For example, instead of specifying exact versions like "Ubuntu 22.04" or "libc6 (>= 2.34)", explain the general compatibility concern: "The CI may use a libc version greater than what your Ubuntu/Debian/Mint version requires." Similarly, avoid assuming specific toolchain managers like rustup when providing build commands - not all users will have the same setup.

This approach ensures documentation remains accurate and useful over time, reduces maintenance burden, and provides better user experience across different development environments.

Example of brittle documentation:
```sh
# Assumes rustup is available
cargo +stable install --path helix-term --locked
```

Better approach:
```sh
# Works with any cargo installation
cargo install --path helix-term --locked
```