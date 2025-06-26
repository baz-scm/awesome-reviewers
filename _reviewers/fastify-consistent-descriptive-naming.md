---
title: " Consistent descriptive naming"
description: "Use precise, consistent, and descriptive naming conventions throughout your code to enhance readability and maintainability. This includes using past participle forms for variables storing processed data, choosing function names that clearly describe their purpose, using consistent naming patterns for related parameters, and naming properties to clearly indicate their relationships."
repository: "fastify/fastify"
label: "Naming Conventions"
language: "JavaScript"
comments_count: 4
repository_stars: 34000
---

Use precise, consistent, and descriptive naming conventions throughout your code to enhance readability and maintainability. This includes:

1. Use past participle (adjective form) for variables storing processed data:
```javascript
// ✅ Good
const normalizedMethod = options.method?.toUpperCase() ?? ''

// ❌ Bad
const normalizeMethod = options.method?.toUpperCase() ?? ''
```

2. Choose function names that clearly describe their purpose without ambiguity:
```javascript
// ✅ Good
function addHTTPMethod(method, { acceptBody = true } = {}) {
  // Implementation
}

// ❌ Bad (confusing with HTTP Accept header)
function acceptHTTPMethod(method, { hasBody = false } = {}) {
  // Implementation
}
```

3. Use consistent naming patterns for related parameters and properties:
```javascript
// ✅ Good - consistent terminology
contentTypeSchemas[contentType] = compile({ schema: contentSchema, method, url, httpPart: 'body', contentType })

// ❌ Bad - inconsistent terminology
contentTypeSchemas[mediaName] = compile({ schema: contentSchema, method, url, httpPart: 'body' })
```

4. Name properties to clearly indicate their relationships:
```javascript
// ✅ Good - clear relationship between host and hostname
host: {
  get() { return this.raw.headers.host || this.raw.headers[':authority'] }
},
hostname: {
  get() { return this.host.split(':')[0] }
},
port: {
  get() { return this.host.split(':')[1] }
}
```

These conventions improve code understandability and reduce cognitive load for developers working in the codebase.