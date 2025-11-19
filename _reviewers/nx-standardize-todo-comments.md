---
title: standardize TODO comments
description: Use version-specific TODO comments with a consistent format to ensure
  actionable items are properly tracked and easily searchable across the codebase.
  Include the target version in parentheses immediately after "TODO" to make it clear
  when the item should be addressed.
repository: nrwl/nx
label: Documentation
language: TypeScript
comments_count: 2
repository_stars: 27518
---

Use version-specific TODO comments with a consistent format to ensure actionable items are properly tracked and easily searchable across the codebase. Include the target version in parentheses immediately after "TODO" to make it clear when the item should be addressed.

This practice helps prevent technical debt from accumulating by making it easy to find and address TODOs during version releases. Without version specificity, TODO comments often become stale and forgotten.

Format TODO comments like this:
```typescript
// TODO(v22): Change default value of useLegacyTypescriptPlugin to false
// TODO(v23): Remove the legacy TypeScript plugin entirely
// TODO(v22) - remove this generator
```

This format enables developers to quickly search for `TODO(v22)` when preparing for version 22 releases, ensuring nothing gets missed during major version updates.