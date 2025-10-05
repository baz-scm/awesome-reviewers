---
title: validate configuration schemas
description: Always validate configuration objects using proper schema validation
  (like Zod) before type casting or using the configuration values. Avoid unsafe type
  casting from input types to output types without validation, as this can lead to
  runtime errors when expected properties are undefined.
repository: TanStack/router
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 11590
---

Always validate configuration objects using proper schema validation (like Zod) before type casting or using the configuration values. Avoid unsafe type casting from input types to output types without validation, as this can lead to runtime errors when expected properties are undefined.

Configuration resolution should follow a clear hierarchy: file-based config → inline config → defaults. Parse and validate configurations at the appropriate boundaries, not after unsafe casting.

Example of the problem:
```typescript
// Risky - casting before validation
let userConfig = options as Config
// userConfig.routesDirectory may not be defined yet

// Better approach
const validatedConfig = configSchema.parse({
  ...fileConfig,
  ...inlineConfig,
  ...defaults
})
```

When building configuration utilities, accept optional directory parameters to avoid hardcoded paths, and leverage existing config resolution functions rather than duplicating logic. This ensures consistent behavior across different entry points and prevents configuration drift.