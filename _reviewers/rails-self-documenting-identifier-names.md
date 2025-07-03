---
title: Self-documenting identifier names
description: "Use clear, self-documenting names for variables, methods, and classes\
  \ that express intent without exposing unnecessary implementation details. \n\n\
  **For methods and variables:**"
repository: rails/rails
label: Naming Conventions
language: Ruby
comments_count: 9
repository_stars: 57027
---

Use clear, self-documenting names for variables, methods, and classes that express intent without exposing unnecessary implementation details. 

**For methods and variables:**
- Avoid abbreviations unless universally understood (use `connection` instead of `conn`, `source_location` instead of `line`)
- Follow natural language patterns with adjectives before nouns (use `allowed_redirect_hosts` instead of `redirect_hosts_allowed`)
- Remove implementation details from public API names (use `compute_checksum` instead of `compute_checksum_in_chunks`)

**For error classes:**
- Follow the "what? kind?" pattern (e.g., `ChecksumUnsupportedError` instead of `UnsupportedChecksumError`)
- Make names descriptive enough to understand the problem (use `MissingRequiredOrderError` instead of `OrderError`)
- Match existing conventions (like `AssociationNotFoundError` for consistency with `HasManyThroughAssociationNotFoundError`)

**For method signatures:**
- Choose concise yet descriptive names for parameters and methods
- Avoid overly verbose names like `supports_disabling_use_of_index_for_queries?` when `supports_disabling_indexes?` would suffice

Remember that code is read far more often than it's written. Thoughtful naming reduces cognitive load for future readers.
