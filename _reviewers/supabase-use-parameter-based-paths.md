---
title: Use parameter-based paths
description: When designing API routes and interfaces, always use parameter-based
  path syntax instead of hardcoded literals. This approach provides better flexibility,
  improved type safety, and allows for more reusable code. Additionally, always validate
  parameters before using them in routes or API calls to prevent undefined reference
  errors.
repository: supabase/supabase
label: API
language: TSX
comments_count: 3
repository_stars: 86070
---

When designing API routes and interfaces, always use parameter-based path syntax instead of hardcoded literals. This approach provides better flexibility, improved type safety, and allows for more reusable code. Additionally, always validate parameters before using them in routes or API calls to prevent undefined reference errors.

Example of proper path parameterization:
```typescript
// Incorrect - using literal values
path: '/platform/projects/default/analytics/endpoints/logs.all'

// Correct - using parameter syntax
path: '/platform/projects/:ref/analytics/endpoints/logs.all'
```

Example of proper parameter validation:
```typescript
// Incorrect - not validating parameter before use
if (slug === 'last-visited-org') {
  router.replace(`/new/${lastVisitedOrganization}`)
}

// Correct - validating parameter existence
if (slug === 'last-visited-org' && !!lastVisitedOrganization) {
  router.replace(`/new/${lastVisitedOrganization}`)
}
```

This approach also enhances API flexibility by supporting optional parameters, allowing consumers to provide only what they need. When designing component APIs, consider parameterizing inputs to increase reusability across different contexts.