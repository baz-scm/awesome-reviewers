---
title: Extract reusable components
description: Extract utilities, types, constants, and shared logic into dedicated
  modules to improve code maintainability and reduce duplication. When you find yourself
  writing similar code in multiple places, or when you have magic strings/numbers,
  inline type definitions, or mixed business logic, extract them into appropriate
  shared locations.
repository: lobehub/lobe-chat
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 65138
---

Extract utilities, types, constants, and shared logic into dedicated modules to improve code maintainability and reduce duplication. When you find yourself writing similar code in multiple places, or when you have magic strings/numbers, inline type definitions, or mixed business logic, extract them into appropriate shared locations.

Examples of what to extract:
- **Utility functions**: Move shared functions like `withTimeout`, `getDetailsToken` to utils modules
- **Type definitions**: Extract inline types like `config.$type<{...}>` to separate type files  
- **Constants**: Replace magic strings like `'Origin File Not Found'` and magic numbers with named constants
- **Duplicate implementations**: Consolidate identical code like TTS and Image file handling
- **Mixed concerns**: Separate different business logic (e.g., system agent vs embedding) into distinct modules

```typescript
// Before: Magic string and inline logic
throw new TRPCError({ code: 'BAD_REQUEST', message: 'Origin File Not Found' });

// After: Extract constant
const ERROR_MESSAGES = {
  ORIGIN_FILE_NOT_FOUND: 'Origin File Not Found'
} as const;

throw new TRPCError({ code: 'BAD_REQUEST', message: ERROR_MESSAGES.ORIGIN_FILE_NOT_FOUND });
```

This practice reduces maintenance burden, prevents inconsistencies, and makes code more testable and reusable.