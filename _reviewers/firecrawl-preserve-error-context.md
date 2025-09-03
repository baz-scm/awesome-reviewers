---
title: preserve error context
description: Always maintain complete error information when logging or re-throwing
  errors to enable effective debugging and monitoring. This includes using structured
  logging instead of console methods, chaining original errors when throwing new ones,
  and ensuring underlying errors are not masked by generic error handling.
repository: firecrawl/firecrawl
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 54535
---

Always maintain complete error information when logging or re-throwing errors to enable effective debugging and monitoring. This includes using structured logging instead of console methods, chaining original errors when throwing new ones, and ensuring underlying errors are not masked by generic error handling.

When logging errors, use structured logging with the error object:
```javascript
// Instead of
console.error(`There was an error searching for content: ${error.message}`);

// Use
logger.error(`There was an error searching for content`, { error });
```

When re-throwing errors, preserve the original error context:
```javascript
// Instead of
throw new Error("Failed to convert rawHtml to UTF-8");

// Use  
throw new Error("Failed to convert rawHtml to UTF-8", { cause: error });
```

Avoid silently continuing on failures that should be propagated - throw errors to capture the correct context rather than masking underlying issues with generic error messages or type errors.