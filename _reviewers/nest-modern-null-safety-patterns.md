---
title: Modern null safety patterns
description: 'Leverage modern JavaScript features and utility functions for safer
  null/undefined handling. This reduces code verbosity while improving reliability.

  '
repository: nestjs/nest
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 71767
---

Leverage modern JavaScript features and utility functions for safer null/undefined handling. This reduces code verbosity while improving reliability.

Key practices:

1. Use optional chaining for nested property access:
```typescript
// Instead of
if (pattern && pattern.test(str)) { }

// Use
if (pattern?.test(str)) { }
```

2. Apply nullish coalescing for default values:
```typescript
// Instead of
const ttl = value || defaultValue;

// Use
const ttl = value ?? defaultValue;
```

3. Utilize isNil() utility for explicit null/undefined checks:
```typescript
// Instead of
if (value === null || value === undefined) { }

// Use
import { isNil } from '@nestjs/common/utils/shared.utils';
if (isNil(value)) { }
```

These patterns make code more concise while maintaining clear intent and proper null safety. They help prevent null reference errors and make null handling more consistent across the codebase.