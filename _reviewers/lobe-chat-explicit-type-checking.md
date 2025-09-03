---
title: Explicit type checking
description: Use explicit type checks instead of just undefined checks to prevent
  null values from being passed to functions or APIs that don't expect them. Checking
  only for undefined can still allow null values to pass through, which may cause
  runtime errors.
repository: lobehub/lobe-chat
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 65138
---

Use explicit type checks instead of just undefined checks to prevent null values from being passed to functions or APIs that don't expect them. Checking only for undefined can still allow null values to pass through, which may cause runtime errors.

When dealing with optional parameters that should only be included when they have valid values, check for the specific expected type rather than just checking if the value is not undefined.

```ts
// ❌ Problematic - allows null to pass through
...(params.seed !== undefined ? { seed: params.seed } : {})

// ✅ Better - ensures only valid numbers are passed
...(typeof params.seed === 'number' ? { seed: params.seed } : {})
```

For truly optional environment variables or configuration values, avoid unnecessary fallbacks that might mask configuration issues:

```ts
// ❌ Unnecessary fallback for optional values
OPTIONAL_KEY: process.env.OPTIONAL_KEY || ''

// ✅ Let optional values remain undefined
OPTIONAL_KEY: process.env.OPTIONAL_KEY
```