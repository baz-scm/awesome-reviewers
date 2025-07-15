---
title: Extract repeated code
description: Follow the DRY (Don't Repeat Yourself) principle by extracting repeated
  code patterns into helper functions, constants, or shared utilities. Code duplication
  leads to maintainability issues, inconsistencies, and bugs when one instance is
  updated but others are overlooked.
repository: langfuse/langfuse
label: Code Style
language: TypeScript
comments_count: 8
repository_stars: 13574
---

Follow the DRY (Don't Repeat Yourself) principle by extracting repeated code patterns into helper functions, constants, or shared utilities. Code duplication leads to maintainability issues, inconsistencies, and bugs when one instance is updated but others are overlooked.

Examples of code that should be extracted:
- Repeated string operations or formatting logic
- Duplicated validation or processing steps
- Common URL or path manipulation
- Multiple uses of the same magic numbers or strings
- Similar conditional logic across functions

```typescript
// Before: Duplicated URL endpoint replacement logic
if (this.externalEndpoint) {
  try {
    const gcsUrl = new URL(url);
    const externalUrl = new URL(this.externalEndpoint);
    gcsUrl.hostname = externalUrl.hostname;
    if (externalUrl.port) gcsUrl.port = externalUrl.port;
    gcsUrl.protocol = externalUrl.protocol;
    return gcsUrl.toString();
  } catch (err) {
    logger.warn(`Failed to replace URL with external endpoint: ${err}`);
  }
}

// After: Extract into a helper function
private replaceWithExternalEndpoint(url: string): string {
  if (!this.externalEndpoint) return url;
  
  try {
    const originalUrl = new URL(url);
    const externalUrl = new URL(this.externalEndpoint);
    originalUrl.hostname = externalUrl.hostname;
    if (externalUrl.port) originalUrl.port = externalUrl.port;
    originalUrl.protocol = externalUrl.protocol;
    return originalUrl.toString();
  } catch (err) {
    logger.warn(`Failed to replace URL with external endpoint: ${err}`);
    return url;
  }
}
```

This approach improves code maintainability, readability, and ensures consistent behavior across the application.