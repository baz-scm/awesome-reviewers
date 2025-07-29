---
title: Provide explicit error handling
description: Create custom, descriptive errors instead of allowing external dependencies
  or systems to fail with generic messages. Use consistent error handling utilities
  throughout the codebase rather than implementing ad-hoc error responses.
repository: remix-run/react-router
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 55270
---

Create custom, descriptive errors instead of allowing external dependencies or systems to fail with generic messages. Use consistent error handling utilities throughout the codebase rather than implementing ad-hoc error responses.

When a file or resource is missing, provide a clear custom error rather than letting the underlying system (like Vite) fail:

```typescript
// Instead of letting Vite fail when loading a missing file
if (reactRouterConfigFile) {
  try {
    let configModule = await viteNodeContext.runner.executeFile(
      reactRouterConfigFile
    );
  } catch (error) {
    // Provide our own descriptive error
    return err(`Failed to load React Router config file: ${reactRouterConfigFile}`);
  }
}

// Check for missing exports explicitly
if (typeof configModule.default !== "object") {
  return err("Config file must export a default object");
}
```

Consolidate defensive error handling into reusable utilities:

```typescript
// Instead of scattered invariant checks
function abortFetcher(key: string) {
  let controller = fetchControllers.get(key);
  // Flatten defensive check into the method itself
  if (!controller) return; // Handle gracefully
  controller.abort();
}

// Use consistent error utilities
if (!response) {
  // Use shared utility instead of ad-hoc response
  let error = new Error('Unhandled request');
  return returnLastResortErrorResponse(error, serverMode);
}
```

This approach improves debugging by providing clear error messages, reduces inconsistency across the codebase, and makes error handling more maintainable by centralizing common patterns.