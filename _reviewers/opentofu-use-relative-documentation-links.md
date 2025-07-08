---
title: Use relative documentation links
description: When documenting error handling mechanisms, always use relative path
  references (`../path/to/file.mdx`) instead of absolute paths (`/docs/path/to/file`)
  when creating documentation links. This ensures documentation about error handling,
  assertions, validations, and error recovery patterns remains navigable even when
  documentation structures change.
repository: opentofu/opentofu
label: Error Handling
language: Other
comments_count: 2
repository_stars: 25901
---

When documenting error handling mechanisms, always use relative path references (`../path/to/file.mdx`) instead of absolute paths (`/docs/path/to/file`) when creating documentation links. This ensures documentation about error handling, assertions, validations, and error recovery patterns remains navigable even when documentation structures change.

For example, change:
```markdown
[custom conditions](/docs/language/expressions/custom-conditions)
```

To use relative paths:
```markdown
[custom conditions](../expressions/custom-conditions.mdx)
```

Properly linked documentation is essential for developers to find and implement appropriate error handling strategies. When documentation links break, developers struggle to locate crucial information about error handling techniques, potentially leading to improper implementation of validation checks, error messaging, and recovery mechanisms.