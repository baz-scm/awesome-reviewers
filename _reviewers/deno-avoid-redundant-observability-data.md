---
title: avoid redundant observability data
description: When implementing observability features like tracing and monitoring,
  avoid exposing redundant information that can be inferred from existing data, and
  use appropriate abstraction levels rather than exposing internal implementation
  details through public APIs.
repository: denoland/deno
label: Observability
language: TypeScript
comments_count: 2
repository_stars: 103714
---

When implementing observability features like tracing and monitoring, avoid exposing redundant information that can be inferred from existing data, and use appropriate abstraction levels rather than exposing internal implementation details through public APIs.

For tracing spans, don't set status descriptions when the information can be derived from other attributes:

```typescript
// Avoid redundant message when status code is sufficient
if (res.status >= 400) {
  span.setAttribute("error.type", String(res.status));
  span.setStatus({
    code: 2, // Error
    // Don't set message - can be inferred from http.response.status_code
  });
}
```

For internal observability data like file descriptors, use private symbols or internal mechanisms rather than exposing them through public APIs:

```typescript
// Use internal symbols instead of public API exposure
const fd = conn[INTERNAL_FD_SYMBOL]; // Good
// Rather than: conn.fd (public API exposure)
```

This approach maintains clean public interfaces while still providing necessary observability data through appropriate channels.