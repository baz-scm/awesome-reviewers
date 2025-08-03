---
title: Centralize configuration values
description: Extract and centralize configuration values instead of duplicating or
  hardcoding them throughout the codebase. This improves maintainability by ensuring
  changes only need to be made in one place and enforces consistency across the application.
repository: supabase/supabase
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 86070
---

Extract and centralize configuration values instead of duplicating or hardcoding them throughout the codebase. This improves maintainability by ensuring changes only need to be made in one place and enforces consistency across the application.

**Best practices:**
- Use shared configuration objects for common settings (like query options)
- Extract hardcoded values into named constants or environment variables
- Create structured environment checks for environment-specific configurations

**Example - Before:**
```typescript
// Hardcoded values in multiple files
Sentry.init({
  dsn: 'https://3c27c63b42048231340b7d640767ad02@o398706.ingest.us.sentry.io/4508132895096832',
})

// Duplicated configuration
{
  enabled: enabled && typeof projectRef !== 'undefined',
  refetchOnWindowFocus: false,
}

// Simple environment check
export const DEFAULT_PROVIDER: CloudProvider =
  process.env.NEXT_PUBLIC_ENVIRONMENT !== 'prod' ? 'AWS_K8S' : 'AWS'
```

**Example - After:**
```typescript
// Constants file
export const SENTRY_DSN = process.env.SENTRY_DSN || 'https://3c27c63b42048231340b7d640767ad02@o398706.ingest.us.sentry.io/4508132895096832'

// Shared configuration object
export const UNIFIED_LOGS_QUERY_OPTIONS = {
  enabled: enabled && typeof projectRef !== 'undefined',
  refetchOnWindowFocus: false,
}

// Structured environment check
export const DEFAULT_PROVIDER: CloudProvider =
  process.env.NEXT_PUBLIC_ENVIRONMENT &&
  ['staging', 'preview'].includes(process.env.NEXT_PUBLIC_ENVIRONMENT)
    ? 'AWS_K8S'
    : 'AWS'
```