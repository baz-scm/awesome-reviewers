---
title: Handle external operations safely
description: 'Always implement explicit error handling for external operations such
  as network requests, database queries, and API calls. When errors occur, either:'
repository: supabase/supabase
label: Error Handling
language: TypeScript
comments_count: 4
repository_stars: 86070
---

Always implement explicit error handling for external operations such as network requests, database queries, and API calls. When errors occur, either:

1. **Degrade functionality gracefully**: Implement a fallback behavior when appropriate.
2. **Propagate errors explicitly**: Use consistent error handling patterns to ensure errors bubble up properly.
3. **Use appropriate error types/codes**: Ensure error responses accurately reflect the nature of the failure.

Avoid simply logging errors without proper handling or recovery strategy.

**Example - Before:**
```typescript
async function fetchDatabaseExtensions() {
  try {
    const dbExtensions = await getDatabaseExtensions(
      { projectRef, connectionString },
      undefined,
      headers
    )
    
    effectiveAiOptInLevel = checkNetworkExtensionsAndAdjustOptInLevel(
      dbExtensions,
      effectiveAiOptInLevel
    )
  } catch (error) {
    console.error('Failed to fetch database extensions:', error)
    // No error handling strategy - neither degrading nor propagating
  }
}
```

**Example - After:**
```typescript
async function fetchDatabaseExtensions() {
  try {
    const dbExtensions = await getDatabaseExtensions(
      { projectRef, connectionString },
      undefined,
      headers
    )
    
    effectiveAiOptInLevel = checkNetworkExtensionsAndAdjustOptInLevel(
      dbExtensions,
      effectiveAiOptInLevel
    )
  } catch (error) {
    console.error('Failed to fetch database extensions:', error)
    // Option 1: Degrade functionality gracefully
    effectiveAiOptInLevel = 'restricted' // Default to restricted access on error
    
    // Option 2: Propagate the error to fail explicitly
    // throw new Error(`Database extensions check failed: ${error.message}`)
  }
}
```