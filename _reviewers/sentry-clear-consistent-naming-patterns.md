---
title: Clear consistent naming patterns
description: Use clear, consistent naming patterns for variables and event handlers.
  Avoid abbreviations unless they are widely understood standards. For event handlers,
  follow the pattern 'on' + 'action' + 'object'.
repository: getsentry/sentry
label: Naming Conventions
language: TSX
comments_count: 3
repository_stars: 41297
---

Use clear, consistent naming patterns for variables and event handlers. Avoid abbreviations unless they are widely understood standards. For event handlers, follow the pattern 'on' + 'action' + 'object'.

Good examples:
```typescript
// Event handler naming
onSortChange: (sort: Sort) => void;     // ✓ Clear and follows pattern
onColumnSortChange: () => void;         // ✗ Redundant, object implied

// Variable naming
const currentSort = useState<Sort>();    // ✓ Clear and explicit
const curSort = useState<Sort>();        // ✗ Unnecessary abbreviation

// Event handler pattern
onChangePassword()                      // ✓ on + action + object
onPasswordChange()                      // ✗ Inconsistent pattern
```

This promotes code readability and maintains consistency across the codebase. When multiple developers follow the same naming patterns, it becomes easier to understand and maintain the code.