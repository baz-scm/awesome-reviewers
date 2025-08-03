---
title: Avoid code duplication
description: 'Maintain clean, maintainable code by avoiding duplication and following
  proper code organization principles:


  1. Place utility functions in dedicated utility files rather than defining them
  inline within component files'
repository: supabase/supabase
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 86070
---

Maintain clean, maintainable code by avoiding duplication and following proper code organization principles:

1. Place utility functions in dedicated utility files rather than defining them inline within component files
2. Reuse existing constants, functions, and utilities through imports rather than duplicating code
3. Maintain a single source of truth for shared logic and data

**Example - Before:**
```typescript
// In components/SomeFeature.ts
const getFileName = (path: string): string => {
  if (!path) return ''
  const cleanPath = path.split('?')[0].split('#')[0]
  const segments = cleanPath.split('/')
  return segments[segments.length - 1] || ''
}

// In another file
export const CANCELLATION_REASONS = [
  'Pricing',
  "My project isn't getting traction",
  // ... more reasons
]
```

**Example - After:**
```typescript
// In utils/fileUtils.ts
export const getFileName = (path: string): string => {
  if (!path) return ''
  const cleanPath = path.split('?')[0].split('#')[0]
  const segments = cleanPath.split('/')
  return segments[segments.length - 1] || ''
}

// In components/SomeFeature.ts
import { getFileName } from 'utils/fileUtils'

// In various files that need cancellation reasons
import { CANCELLATION_REASONS } from 'components/interfaces/Billing/Billing.constants'
```

This approach improves maintainability, reduces bugs from inconsistent implementations, and makes code easier to test and refactor.