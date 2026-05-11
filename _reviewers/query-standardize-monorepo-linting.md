---
title: Standardize monorepo linting
description: Use shared root configuration for formatting and apply consistent ESLint
  rule severities across the monorepo, allowing only narrowly scoped exceptions.
repository: tanstack/query
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 49380
---

Use shared root configuration for formatting and apply consistent ESLint rule severities across the monorepo, allowing only narrowly scoped exceptions.

- Formatting: avoid duplicating Prettier config in packages—inherit/extend the monorepo root Prettier settings.
- Linting: set intended rule severity (e.g., test-related rules) once in the root ESLint config so it applies across packages; if a package needs a deviation, disable the rule only for that package/files with an explicit override.

Example (root ESLint override pattern):

```js
export default [
  {
    files: ['**/*.spec.ts*', '**/*.test.ts*', '**/*.test-d.ts*'],
    // apply Vitest expectations consistently across packages
    rules: {
      'vitest/expect-expect': 'error',
    },
  },
  {
    // narrowly scoped exception, only where needed
    files: ['packages/query-codemods/**'],
    rules: {
      '@typescript-eslint/require-await': 'off',
    },
  },
];
```

Result: fewer configuration drifts between packages, predictable CI failures, and minimal “special case” behavior that’s easy to audit.