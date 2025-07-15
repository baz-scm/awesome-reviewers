---
title: Standardize null safety patterns
description: Use modern JavaScript features and utility functions consistently for
  null/undefined checks. Prefer optional chaining (?.), nullish coalescing (??), and
  dedicated utility functions like isNil() over direct null checks or OR (||) operators.
repository: nestjs/nest
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 71766
---

Use modern JavaScript features and utility functions consistently for null/undefined checks. Prefer optional chaining (?.), nullish coalescing (??), and dedicated utility functions like isNil() over direct null checks or OR (||) operators.

Key practices:
1. Use optional chaining for potentially null properties:
```typescript
// Instead of
if (pattern && pattern.test(str))

// Use
if (pattern?.test(str))
```

2. Use nullish coalescing for default values:
```typescript
// Instead of
const ttlValueOrFactory = ttlMetadata || null;

// Use
const ttlValueOrFactory = ttlMetadata ?? null;
```

3. Use utility functions for explicit null/undefined checks:
```typescript
// Instead of
if (value === null || value === undefined)

// Use
import { isNil } from '@nestjs/common/utils';
if (isNil(value))
```

This approach improves code readability, reduces potential null reference errors, and maintains consistency across the codebase. It leverages TypeScript's type system and modern JavaScript features for better null safety.