---
title: maintain established naming conventions
description: Ensure all naming follows established patterns and conventions already
  present in the codebase. When introducing new identifiers or modifying existing
  ones, they must conform to the team's built-in expectations and standard patterns
  to maintain consistency across the system.
repository: Unstructured-IO/unstructured
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 12117
---

Ensure all naming follows established patterns and conventions already present in the codebase. When introducing new identifiers or modifying existing ones, they must conform to the team's built-in expectations and standard patterns to maintain consistency across the system.

This prevents violations of established conventions that can break compatibility or create confusion. For example, if element IDs are expected to be formatted as hashes without dashes (like "782cf07be8b3ab8f05188e479edb7f61"), then all element IDs should follow this pattern. Similarly, if certain class names violate standard output patterns used throughout the system, they should be removed or renamed to maintain consistency.

Example of applying this standard:
```json
// Bad - violates hash convention with dashes
"element_id": "897a8a47-377c-4ad6-aab8-39a929879537"

// Good - follows established hash format
"element_id": "897a8a47377c4ad6aab839a929879537"
```

Before introducing any new naming patterns, verify they align with existing conventions in the codebase and don't break established expectations that other parts of the system depend on.