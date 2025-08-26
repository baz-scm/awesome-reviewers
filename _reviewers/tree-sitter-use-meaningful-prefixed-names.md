---
title: Use meaningful prefixed names
description: Names should be semantically meaningful and properly prefixed to prevent
  namespace conflicts. In C, enum variants and global identifiers are added to the
  top-level namespace, so prefix them with their type name even if repetitive. Choose
  names that reflect domain concepts and purpose rather than technical implementation
  details. Prioritize clarity over...
repository: tree-sitter/tree-sitter
label: Naming Conventions
language: Other
comments_count: 4
repository_stars: 21799
---

Names should be semantically meaningful and properly prefixed to prevent namespace conflicts. In C, enum variants and global identifiers are added to the top-level namespace, so prefix them with their type name even if repetitive. Choose names that reflect domain concepts and purpose rather than technical implementation details. Prioritize clarity over brevity by spelling out words fully.

Examples:
- Enum values: Use `TSQuantifierOneOrMore` instead of `OneOrMore`
- Struct fields: Use `shift` (domain-specific) instead of `status` (generic)
- Functions: Use `ts_malloc_default` instead of `ts_malloc_dflt`
- Macros: Use `SUBTREE_SIZE` (semantic) instead of `SUBTREE_4_BYTES` (technical)

This prevents naming conflicts, improves code readability, and makes the codebase more maintainable by clearly indicating the purpose and scope of each identifier.