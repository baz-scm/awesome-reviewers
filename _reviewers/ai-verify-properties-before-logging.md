---
title: Verify properties before logging
description: When logging object properties, always verify that the property names
  exactly match the actual structure of the object being logged. Incorrect property
  names (like 'responses' instead of 'response') or non-existent properties will result
  in undefined values in logs, reducing their usefulness for debugging and troubleshooting.
repository: vercel/ai
label: Logging
language: TypeScript
comments_count: 5
repository_stars: 15590
---

When logging object properties, always verify that the property names exactly match the actual structure of the object being logged. Incorrect property names (like 'responses' instead of 'response') or non-existent properties will result in undefined values in logs, reducing their usefulness for debugging and troubleshooting.

Example of problematic code:
```javascript
console.log('Responses:', result.responses);       // Incorrect property name
console.log('Provider Metadata:', result.providerMetadata);  // Non-existent property
```

Corrected code:
```javascript
console.log('Response:', result.response);         // Correct property name
// Don't log properties that don't exist in the object
```

Consider using optional chaining (`?.`) for nested properties or TypeScript to help catch these issues at compile time. For important logging in production code, consider adding runtime property existence checks before logging.