---
title: Remove internal APIs
description: Delete internal system properties and APIs after use to prevent application
  code from accessing protected functionality. This security practice ensures that
  internal methods cannot be called by user code, protecting system integrity and
  preventing potential security vulnerabilities.
repository: electron/electron
label: Security
language: TypeScript
comments_count: 1
repository_stars: 117644
---

Delete internal system properties and APIs after use to prevent application code from accessing protected functionality. This security practice ensures that internal methods cannot be called by user code, protecting system integrity and preventing potential security vulnerabilities.

When internal properties are exposed temporarily (e.g., during initialization), clean them up immediately after use:

```typescript
const { appCodeLoaded } = process;
delete process.appCodeLoaded;
```

This pattern prevents application code from discovering and potentially misusing internal system APIs that should remain private to the framework or runtime environment.