---
title: validate environment variables early
description: Environment variables should be validated at startup or module initialization
  rather than at runtime usage. Use non-null assertion operators or explicit validation
  checks to fail fast when required configuration is missing, preventing delayed runtime
  errors and making configuration issues immediately apparent during development and
  deployment.
repository: firecrawl/firecrawl
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 54535
---

Environment variables should be validated at startup or module initialization rather than at runtime usage. Use non-null assertion operators or explicit validation checks to fail fast when required configuration is missing, preventing delayed runtime errors and making configuration issues immediately apparent during development and deployment.

Instead of logging errors and continuing execution:
```typescript
const url = process.env.SEARXNG_ENDPOINT as string;
if (!url) {
  console.error(`SEARXNG_ENDPOINT environment variable is not set`);
}
// Code continues and may fail later...
```

Use non-null assertion for required variables:
```typescript
const url = process.env.SEARXNG_ENDPOINT!;
```

Or implement explicit validation at module initialization:
```typescript
if (!process.env.SEARXNG_ENDPOINT) {
  throw new Error('SEARXNG_ENDPOINT environment variable is required');
}
```

This approach ensures configuration problems are caught early in the application lifecycle rather than causing mysterious runtime failures.