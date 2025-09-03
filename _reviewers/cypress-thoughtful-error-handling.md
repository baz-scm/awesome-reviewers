---
title: Thoughtful error handling
description: Implement error handling that considers recoverability, appropriate logging
  levels, and prevents redundant operations. Use warnings for recoverable errors during
  retry attempts, and errors only for final failures. Avoid duplicate error logging
  when errors are already wrapped or handled elsewhere. Implement guards to prevent
  redundant error handler setup,...
repository: cypress-io/cypress
label: Error Handling
language: JavaScript
comments_count: 5
repository_stars: 48850
---

Implement error handling that considers recoverability, appropriate logging levels, and prevents redundant operations. Use warnings for recoverable errors during retry attempts, and errors only for final failures. Avoid duplicate error logging when errors are already wrapped or handled elsewhere. Implement guards to prevent redundant error handler setup, and distinguish between recoverable errors (network issues, temporary failures) and non-recoverable ones (configuration errors) to avoid unnecessary retry loops.

Example of proper retry error handling:
```javascript
async function importWithRetry(importFn) {
  try {
    return await importFn()
  } catch (error) {
    for (let i = 0; i < 3; i++) {
      console.warn(`Retrying import attempt ${i + 1}/3: ${url?.href}`) // Warning, not error
      // ... retry logic
    }
    console.error(`Final import failure after retries: ${url?.href}`) // Error only on final failure
    throw error
  }
}
```

Avoid duplicate logging:
```javascript
// Instead of logging and throwing
errors.log(err)
throw err

// Just throw the wrapped error
throw errors.get('ERROR_WRITING_FILE', dest, error)
```