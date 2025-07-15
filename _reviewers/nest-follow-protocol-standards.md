---
title: Follow protocol standards
description: When implementing networking features, strictly adhere to protocol specifications
  and standards to ensure proper interoperability. This applies to HTTP headers, status
  codes, and protocol-specific connection handling.
repository: nestjs/nest
label: Networking
language: TypeScript
comments_count: 6
repository_stars: 71767
---

When implementing networking features, strictly adhere to protocol specifications and standards to ensure proper interoperability. This applies to HTTP headers, status codes, and protocol-specific connection handling.

For HTTP responses:
1. Only use standardized status codes (avoid non-standard codes like 499) to ensure consistent client behavior
2. When setting default headers, respect existing values by checking with `!== undefined` rather than truthy checks:

```typescript
// Good practice - only set default if undefined
if (!response.getHeader('Content-Type')) {
  response.setHeader('Content-Type', 'application/octet-stream');
}

// For redirects, use standard status codes with proper defaults
const code = statusCode ? statusCode : HttpStatus.FOUND; // 302
```

3. For specialized protocols like Server-Sent Events (SSE), include all required headers for compatibility with browsers and proxies:

```typescript
response.writeHead(200, {
  'Content-Type': 'text/event-stream; charset=utf-8',
  'Cache-Control': 'no-cache',
  'X-Accel-Buffering': 'no'
  // Server will set Transfer-Encoding automatically
});
```

4. Implement proper connection cleanup during service shutdown to prevent resource leaks:

```typescript
// Close open connections on server shutdown
this.openConnections.forEach(socket => {
  socket.destroy();
});
```

Consistent adherence to protocol standards improves interoperability, simplifies debugging, and prevents subtle edge cases in network communications.