---
title: descriptive naming patterns
description: Use descriptive names that clearly indicate the expected format, convention,
  or constraints. This applies to template variables, configuration keys, and validation
  patterns. Names should communicate not just what something is, but how it should
  be formatted or what rules it follows.
repository: tree-sitter/tree-sitter
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 21799
---

Use descriptive names that clearly indicate the expected format, convention, or constraints. This applies to template variables, configuration keys, and validation patterns. Names should communicate not just what something is, but how it should be formatted or what rules it follows.

For template variables, include format hints in the name:
```json
{
  "description": "CAMEL_PARSER_NAME grammar for tree-sitter"
}
```

For validation patterns, ensure they accommodate all valid naming conventions:
```json
{
  "pattern": "^(source|text)(\\.[\\w\\-]+)+$"
}
```

This approach reduces ambiguity and helps developers understand naming requirements without consulting additional documentation.