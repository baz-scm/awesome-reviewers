---
title: Follow configuration conventions
description: When working with configurations, maintain consistency by following established
  conventions and proper categorization. This includes using naming patterns that
  match related tools/frameworks and organizing configuration entries in appropriate
  sections based on actual capabilities.
repository: evanw/esbuild
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 39161
---

When working with configurations, maintain consistency by following established conventions and proper categorization. This includes using naming patterns that match related tools/frameworks and organizing configuration entries in appropriate sections based on actual capabilities.

For naming conventions, prefer established patterns from related ecosystems:
```typescript
// Good: matches Webpack convention
sideEffects: false

// Avoid: creates new naming pattern
sideEffectFree: true
```

For configuration organization, ensure entries are categorized correctly based on actual support:
```typescript
// Good: placed in appropriate section
const unsupportedPlatforms = {
  'aarch64-linux-android': '@esbuild/android-arm64',
}

// Avoid: miscategorized based on assumptions
const supportedPlatforms = {
  'aarch64-linux-android': '@esbuild/android-arm64', // Not actually supported
}
```

This approach makes configurations more intuitive for users familiar with related tools and prevents confusion about actual capabilities.