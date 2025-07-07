---
title: Use explicit permission notations
description: When setting file permissions through system calls like `chmod`, always
  use explicit octal notation (with the `0o` prefix) rather than decimal integers.
  Decimal integers in permission contexts can lead to unintended access rights, creating
  security vulnerabilities through incorrect file permissions.
repository: astral-sh/ruff
label: Security
language: Rust
comments_count: 1
repository_stars: 40619
---

When setting file permissions through system calls like `chmod`, always use explicit octal notation (with the `0o` prefix) rather than decimal integers. Decimal integers in permission contexts can lead to unintended access rights, creating security vulnerabilities through incorrect file permissions.

For example, instead of:
```python
os.chmod("foo", 644)  # Incorrect - decimal integer
```

Use:
```python
os.chmod("foo", 0o644)  # Correct - explicit octal notation
```

The decimal value `644` is not equivalent to the octal value `0o644`, and this mismatch can lead to improper permission settings that may expose sensitive files to unauthorized access. Always verify permission values in security-sensitive operations.