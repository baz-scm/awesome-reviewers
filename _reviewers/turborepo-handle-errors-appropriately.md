---
title: Handle errors appropriately
description: Implement appropriate error handling strategies based on the criticality
  of operations. For non-critical operations that could fail (like file operations
  and JSON parsing), use try/catch blocks to handle errors gracefully and continue
  execution with proper logging. For critical operations where execution cannot reasonably
  continue, provide clear error...
repository: vercel/turborepo
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 28115
---

Implement appropriate error handling strategies based on the criticality of operations. For non-critical operations that could fail (like file operations and JSON parsing), use try/catch blocks to handle errors gracefully and continue execution with proper logging. For critical operations where execution cannot reasonably continue, provide clear error messages and abort.

**Good example:**
```typescript
// When reading files that might not exist
try {
  const config = readJsonSync(configPath);
  // Process config
} catch (error) {
  // Log the error
  debug(`Error reading config: ${error.message}`);
  // Continue with fallback or degraded functionality if appropriate
  config = defaultConfig;
}

// For critical operations
try {
  const packageJSON = readJsonSync(packageJsonPath);
  if (!packageJSON) {
    log.error("Critical error: Could not read package.json");
    return { success: false, error: "Missing required package.json" };
  }
} catch (error) {
  log.error(`Failed to parse package.json: ${error.message}`);
  return { success: false, error: "Invalid package.json" };
}
```

Be defensive with operations that might fail, but make intentional decisions about whether to continue execution based on the criticality of the error. Always provide clear error messages and sufficient context for debugging.