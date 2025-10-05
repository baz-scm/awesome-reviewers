---
title: Documentation quality standards
description: Ensure documentation follows proper formatting standards and provides
  complete, practical information for developers. Use JSDoc tags correctly - `@default`
  should contain actual TypeScript values, not descriptive sentences. When the default
  value is conditional or complex, use plain text descriptions instead.
repository: vadimdemedes/ink
label: Documentation
language: TypeScript
comments_count: 2
repository_stars: 31825
---

Ensure documentation follows proper formatting standards and provides complete, practical information for developers. Use JSDoc tags correctly - `@default` should contain actual TypeScript values, not descriptive sentences. When the default value is conditional or complex, use plain text descriptions instead.

Additionally, include usage examples in API documentation to make it more accessible and helpful. Synchronize examples across different documentation sources (README, inline docs, etc.) to maintain consistency.

Example of incorrect JSDoc usage:
```typescript
/**
 * Configure whether Ink should only render the last frame of non-static output.
 * @default true if in CI or stdout is not a TTY
 */
patchConsole?: boolean;
```

Example of correct approach:
```typescript
/**
 * Configure whether Ink should only render the last frame of non-static output.
 * Default: true if in CI or stdout is not a TTY
 */
patchConsole?: boolean;
```

For API documentation, include practical usage examples:
```typescript
/**
 * Hook that calls inputHandler callback with input that program received.
 * Additionally contains helpful metadata for detecting when arrow keys were pressed.
 * 
 * @example
 * ```typescript
 * useInput((input, key) => {
 *   if (key.leftArrow) {
 *     // Handle left arrow key
 *   }
 * });
 * ```
 */
```