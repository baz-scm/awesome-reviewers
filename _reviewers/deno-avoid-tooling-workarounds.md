---
title: avoid tooling workarounds
description: Avoid code patterns that require workarounds for tooling limitations
  or create maintenance burdens. This includes using contextual keywords as identifiers
  that cause formatter edge cases, and relying on @ts-ignore comments to suppress
  type checking.
repository: denoland/deno
label: Code Style
language: JavaScript
comments_count: 2
repository_stars: 103714
---

Avoid code patterns that require workarounds for tooling limitations or create maintenance burdens. This includes using contextual keywords as identifiers that cause formatter edge cases, and relying on @ts-ignore comments to suppress type checking.

Instead of working around tooling issues, prefer patterns that work naturally with the development environment:

- Avoid using identifiers that are also contextual keywords (like "from") which can cause formatter bugs
- Replace @ts-ignore comments with proper type definitions or code restructuring
- Choose naming and code patterns that don't require special handling by formatters, linters, or type checkers

For example, instead of:
```javascript
// Workaround: rename "from" to avoid formatter issues
const renameForDefaultExport = ["from"];

// @ts-ignore Undocumented function
someUndocumentedFunction();
```

Prefer:
```javascript
// Use clear, non-conflicting names
const renameForDefaultExport = ["fromKeyword"];

// Properly type or restructure instead of ignoring
someDocumentedFunction();
```

This approach reduces technical debt, improves code maintainability, and prevents future issues when tooling is updated.