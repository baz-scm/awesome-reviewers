---
title: "Consistent method behaviors"
description: "Design API methods with predictable behavior patterns that follow common conventions. Methods that modify objects directly should not return values unless supporting method chaining. Methods that retrieve or transform data should return new objects without modifying inputs."
repository: "axios/axios"
label: "API"
language: "JavaScript"
comments_count: 5
repository_stars: 107000
---

Design API methods with predictable behavior patterns that follow common conventions. Methods that modify objects directly (`setSth()`) should not return values unless supporting method chaining. Methods that retrieve or transform data (`getSth()`) should return new objects without modifying inputs. Public class interfaces should maintain backward compatibility even if not all functionality is used internally. Ensure method signatures clearly indicate whether they accept request bodies:

```javascript
// Good - clear behavior from naming and return type
function setHeaders(config, headers) {
  config.headers = headers;
  // No return, modifies object directly
}

function getHeaders(config) {
  // Returns new object, doesn't modify input
  return {...config.headers};
}

// Support method chaining explicitly
function addHeader(config, key, value) {
  config.headers[key] = value;
  return this; // Explicitly returns for chaining
}
```

When adding features to public APIs, ensure all methods have consistent signatures, behavior, and documentation, even if some functionality isn't used in your codebase yet.