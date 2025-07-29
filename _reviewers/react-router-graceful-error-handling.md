---
title: graceful error handling
description: Implement error handling that gracefully degrades when operations fail,
  uses consistent reporting patterns, and considers security implications. Always
  wrap potentially failing operations in try-catch blocks, provide meaningful fallback
  behavior, and follow established error reporting conventions.
repository: remix-run/react-router
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 55270
---

Implement error handling that gracefully degrades when operations fail, uses consistent reporting patterns, and considers security implications. Always wrap potentially failing operations in try-catch blocks, provide meaningful fallback behavior, and follow established error reporting conventions.

Key principles:
- Use environment-aware error information disclosure (preserve debugging details in development, sanitize in production)
- Follow consistent error reporting patterns across the codebase
- Implement defensive programming against unexpected error types
- Provide graceful degradation when non-critical operations fail

Example implementation:
```ts
try {
  sessionStorage.setItem(storageKey, JSON.stringify(data));
} catch (error) {
  warning(
    false,
    `Failed to save data in sessionStorage, feature will not work properly. ${error}`
  );
  // Continue execution - don't let storage failure break the app
}

// Environment-aware error disclosure
error.stack = process.env.NODE_ENV === "development" ? val.stack : "";

// Proper error propagation with meaningful responses
if (res.status === 404) {
  throw new ErrorResponseImpl(404, "Not Found", true);
}
```

This approach ensures applications remain functional even when individual operations fail, while maintaining appropriate security boundaries and consistent user experience.