---
title: Preserve sensitive data marks
description: Carefully handle data marked as sensitive throughout the codebase to
  maintain security properties. Ensure that sensitive marks are only removed when
  necessary, and be aware that operations on marked data (such as reordering from
  nested to top level) could have security implications.
repository: opentofu/opentofu
label: Security
language: Go
comments_count: 1
repository_stars: 25901
---

Carefully handle data marked as sensitive throughout the codebase to maintain security properties. Ensure that sensitive marks are only removed when necessary, and be aware that operations on marked data (such as reordering from nested to top level) could have security implications.

When modifying code that processes sensitive data:
1. Only remove sensitive marks when explicitly required
2. Validate that transformations maintain appropriate security properties
3. Consider interactions with other marking systems in your codebase

Example:
```go
// Good: Only remove marks when necessary (check if they exist first)
if n.Addr.Module.IsRoot() && marks.Contains(val, marks.Sensitive) {
    // Handle sensitive data appropriately
}

// Avoid: Unconditional operations on sensitive data that might not exist
if n.Addr.Module.IsRoot() {
    // Potentially unnecessary operations on sensitive marks
}
```