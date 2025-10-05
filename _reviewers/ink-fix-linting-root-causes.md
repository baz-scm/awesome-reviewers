---
title: Fix linting root causes
description: Address underlying code issues rather than disabling linting rules or
  working around auto-formatter conflicts. When linting tools flag legitimate problems,
  fix the root cause instead of suppressing the warning. When auto-formatters conflict
  with intentional code patterns, adjust project-wide configuration rather than using
  local disables.
repository: vadimdemedes/ink
label: Code Style
language: TSX
comments_count: 3
repository_stars: 31825
---

Address underlying code issues rather than disabling linting rules or working around auto-formatter conflicts. When linting tools flag legitimate problems, fix the root cause instead of suppressing the warning. When auto-formatters conflict with intentional code patterns, adjust project-wide configuration rather than using local disables.

For example, instead of:
```typescript
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
internal_static
```

Fix the underlying TypeScript issue that requires the ignore comment.

When auto-formatters incorrectly modify intentional test patterns like `A{'B'}` to `AB`, configure the formatter globally rather than disabling rules on individual lines. This maintains code quality while preserving intentional code structure.