---
title: Type Parameter Naming
description: Enforce a single, strict naming convention for TypeScript generic type
  parameters using ESLint, and migrate the rule to `error` after a short “warn” rollout.
repository: tanstack/query
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 49380
---

Enforce a single, strict naming convention for TypeScript generic type parameters using ESLint, and migrate the rule to `error` after a short “warn” rollout.

Rules:
- Use `PascalCase` for type parameters.
- Forbid leading/trailing underscores on type parameters.
- Use a small allowlist-style regex (e.g., allow either `T` or a PascalCase identifier such as `TUser`, `TItem2`).
- Start as `warn`, then switch to `error` once the codebase is compliant.

Example ESLint config:
```js
// .eslintrc.cjs
module.exports = {
  rules: {
    '@typescript-eslint/naming-convention': [
      'error', // start as 'warn' for gradual rollout
      {
        selector: 'typeParameter',
        format: ['PascalCase'],
        leadingUnderscore: 'forbid',
        trailingUnderscore: 'forbid',
        custom: {
          regex: '^(T|T[A-Z][A-Za-z]+[0-9]*|[A-Z][a-zA-Z]+[0-9]*)$',
          match: true,
        },
      },
    ],
  },
}
```

Apply this to every generic type parameter (`<TUser>`, `<TData2>` etc.) so the meaning of identifiers stays consistent and automatically enforced across the codebase.