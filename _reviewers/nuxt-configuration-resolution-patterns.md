---
title: configuration resolution patterns
description: When defining configuration schemas, use consistent patterns for safe
  property access, async resolution, and default value handling. Always use optional
  chaining with fallback values for nested configuration properties, leverage `$resolve`
  for complex async configuration logic, and ensure proper backwards compatibility.
repository: nuxt/nuxt
label: Configurations
language: TypeScript
comments_count: 10
repository_stars: 57769
---

When defining configuration schemas, use consistent patterns for safe property access, async resolution, and default value handling. Always use optional chaining with fallback values for nested configuration properties, leverage `$resolve` for complex async configuration logic, and ensure proper backwards compatibility.

Key patterns to follow:

1. **Safe property access**: Use optional chaining with fallbacks for nested config properties:
```ts
const extraKeys = nuxt.options?.experimental?.extraPageMetaExtractionKeys || []
```

2. **Async configuration resolution**: Use `$resolve` for complex configuration logic that requires async operations or cross-property dependencies:
```ts
serverDir: {
  $resolve: async (val: string | undefined, get): Promise<string> => {
    return resolve(await get('rootDir') as string, val ?? 'server')
  }
}
```

3. **Default value merging**: Use `defu` for merging configuration objects with proper defaults:
```ts
spaLoaderAttrs: {
  $resolve: (val: undefined | null | Record<string, unknown>) => {
    return defu(val, {
      id: val?.id ?? '__nuxt-spa-loader',
    })
  }
}
```

4. **Backwards compatibility**: Check for legacy configuration options when introducing new patterns:
```ts
propsDestructure: {
  $resolve: async (val, get) => {
    // Check both new and legacy locations
    return val ?? Boolean((await get('vue') as Record<string, any>).propsDestructure)
  }
}
```

5. **Runtime config handling**: Distinguish between `undefined` (not set) and `null` (explicitly set to null) values:
```ts
// Only filter out undefined, preserve null values for runtime override capability
if (typeof obj[key] === 'undefined') {
  // handle undefined case
}
```

This ensures configuration is resolved consistently, safely handles missing values, and maintains backwards compatibility while supporting complex async resolution scenarios.