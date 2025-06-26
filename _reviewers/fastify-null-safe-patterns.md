---
title: " Null safe patterns"
description: "Use concise null checking patterns to prevent runtime errors and improve code readability when handling potentially undefined values."
repository: "fastify/fastify"
label: "Null Handling"
language: "JavaScript"
comments_count: 5
repository_stars: 34000
---

Use concise null checking patterns to prevent runtime errors and improve code readability when handling potentially undefined values. 

When checking if a value is neither null nor undefined:
```javascript
// Preferred: Concise null check
if (err != null) {
  // err is neither null nor undefined
}

// Instead of verbose explicit checks
if (err !== undefined && err !== null) {
  // Same result but more typing
}
```

Before accessing properties of objects that might be null/undefined:
```javascript
// Check before access to prevent "cannot read property of undefined" errors
if (reply.request.socket != null && !reply.request.socket.destroyed) {
  // Safe to use socket property
}
```

For default values, leverage nullish coalescing:
```javascript
// Assign default value if property is null or undefined
reply[kReplyHeaders]['content-type'] = reply[kReplyHeaders]['content-type'] ?? 'application/json; charset=utf-8'

// Or with fallback chains when appropriate
this[kRequestOriginalUrl] = this.raw.originalUrl || this.raw.url
```

These patterns ensure your code handles null and undefined values safely while remaining concise and readable.