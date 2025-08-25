---
title: API parameter handling
description: Ensure consistent and safe handling of parameters and data across API
  endpoints. This includes using proper serialization methods, consistent parameter
  passing approaches, and context-aware processing when the same input may have different
  meanings.
repository: discourse/discourse
label: API
language: JavaScript
comments_count: 4
repository_stars: 44898
---

Ensure consistent and safe handling of parameters and data across API endpoints. This includes using proper serialization methods, consistent parameter passing approaches, and context-aware processing when the same input may have different meanings.

Key practices:
- Use proper JSON serialization instead of string concatenation for API responses to prevent injection issues with user-provided data containing quotes or backslashes
- Maintain consistent behavior patterns across related endpoints (e.g., if login stores origin URL in cookies, signup should follow the same pattern)  
- Pass parameters through appropriate channels - use hidden form fields instead of query parameters when dealing with sensitive or complex data
- Design APIs to handle context-specific interpretations where the same parameter might reference different entities based on the calling context

Example of proper JSON serialization:
```js
// Instead of string concatenation:
return JSON.stringify(this.name) + ":" + JSON.stringify(data);

// Use proper object serialization:
const object = { name: this.name, light: {...}, dark: {...} };
return JSON.stringify(object, null, 2);
```

This approach prevents security vulnerabilities, ensures predictable API behavior, and provides better developer experience through consistent interfaces.