---
title: Environment-aware configuration handling
description: Use environment variables to control application behavior and ensure
  configuration changes are properly synchronized between in-memory state and persistent
  storage. When configuration depends on environment context, check for relevant environment
  variables first before falling back to defaults.
repository: block/goose
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 19037
---

Use environment variables to control application behavior and ensure configuration changes are properly synchronized between in-memory state and persistent storage. When configuration depends on environment context, check for relevant environment variables first before falling back to defaults.

This prevents inconsistencies where in-memory configuration differs from persisted configuration, and allows for environment-specific behavior without hardcoding values.

Example patterns:
```typescript
// Check environment variable before generating defaults
const key = process.env.GOOSE_SERVER__SECRET_KEY || 
           (process.env.GOOSE_EXTERNAL_BACKEND ? 'test' : crypto.randomBytes(32).toString('hex'));

// Enable development features via environment
if (process.env.ENABLE_DEV_UPDATES === 'true') {
  autoUpdater.forceDevUpdateConfig = true;
}
```

When modifying configuration in memory, ensure changes are also reflected in the persistent storage layer to maintain consistency, or clearly document when temporary in-memory modifications are intentional.