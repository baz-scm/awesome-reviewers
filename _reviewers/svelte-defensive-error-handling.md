---
title: defensive error handling
description: Add defensive checks and proper error handling to prevent crashes and
  handle edge cases gracefully. This includes using try-catch blocks around potentially
  unsafe operations, adding guard conditions to prevent infinite loops or invalid
  states, and ensuring the system can recover from unexpected inputs or conditions.
repository: sveltejs/svelte
label: Error Handling
language: JavaScript
comments_count: 5
repository_stars: 83580
---

Add defensive checks and proper error handling to prevent crashes and handle edge cases gracefully. This includes using try-catch blocks around potentially unsafe operations, adding guard conditions to prevent infinite loops or invalid states, and ensuring the system can recover from unexpected inputs or conditions.

Key practices:
- Wrap property access or function calls that might fail in try-catch blocks, especially in contexts where external factors could cause failures
- Add guard flags or conditions to prevent recursive error scenarios (e.g., preventing error handlers from triggering more errors)
- Handle unknown or future cases by logging warnings and providing fallback behavior rather than throwing fatal errors
- Add defensive resets or cleanup calls to prevent state corruption during error scenarios

Example from the codebase:
```javascript
// Add defensive try-catch around potentially unsafe operations
try {
    if ((a === b) !== (get_proxied_value(a) === get_proxied_value(b))) {
        w.state_proxy_equality_mismatch(equal ? '===' : '!==');
    }
} catch {
    // Handle case where property access might be disallowed
}

// Add guard flags to prevent recursive error handling
if (calling_on_error) {
    w.reset_misuse();
    throw error;
}

// Provide fallback for unknown cases instead of crashing
default:
    console.warn(`Unknown operator ${expression.operator}`);
    this.values.add(UNKNOWN);
```

This approach ensures the system remains stable and provides meaningful feedback even when encountering unexpected conditions or edge cases.