---
title: Consistent naming conventions
description: Maintain consistent naming conventions within your codebase, even when
  external specifications or APIs use different naming patterns. Internal consistency
  should take precedence over matching external naming styles to ensure code readability
  and maintainability.
repository: ClickHouse/ClickHouse
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 42425
---

Maintain consistent naming conventions within your codebase, even when external specifications or APIs use different naming patterns. Internal consistency should take precedence over matching external naming styles to ensure code readability and maintainability.

When faced with a choice between following an external API's naming convention and maintaining internal consistency, choose internal consistency. For example, if your system uses snake_case for column names, convert external PascalCase property names to snake_case rather than mixing conventions.

Example from system table columns:
```sql
-- Inconsistent (mixing conventions)
code_point, code_point_value, Alphabetic, ASCII_Hex_Digit

-- Consistent (all snake_case)  
code_point, code_point_value, alphabetic, ascii_hex_digit
```

If external naming alignment is crucial for user experience, consider providing aliases that maintain the external naming while keeping the primary implementation consistent with your internal standards. However, in most cases, prioritize internal consistency as it benefits long-term code maintainability more than preserving external naming patterns.