---
title: HTTP protocol compliance
description: Ensure code adheres to HTTP protocol standards and handles different
  protocol versions correctly. This includes respecting protocol limitations, using
  appropriate status codes, and implementing proper fallbacks.
repository: remix-run/react-router
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 55270
---

Ensure code adheres to HTTP protocol standards and handles different protocol versions correctly. This includes respecting protocol limitations, using appropriate status codes, and implementing proper fallbacks.

Key considerations:
- HTTP/2 doesn't support status messages, so avoid setting statusMessage for HTTP/2 connections
- Use reliable endpoints for server health checks that return success status codes rather than application logic that might fail
- Handle redirect status codes appropriately with proper fallback mechanisms

Example implementation:
```javascript
// Good: Check protocol version before setting status message
export async function toNodeRequest(res: Response, nodeRes: ServerResponse) {
  nodeRes.statusCode = res.status;
  // HTTP/2 doesn't support status messages
  // https://datatracker.ietf.org/doc/html/rfc7540#section-8.1.2.4
  if (nodeRes.httpVersion !== '2.0') {
    nodeRes.statusMessage = res.statusText;
  }
}

// Good: Use reliable endpoint for health checks
await waitOn({
  resources: [
    `http://${args.host ?? "localhost"}:${args.port}${args.basename ?? "/favicon.ico"}`,
  ]
});

// Good: Handle redirect status codes with appropriate fallbacks
if (redirectStatusCodes.has(response.status)) {
  let location = response.headers.get("Location");
  let delay = response.status === 302 ? 2 : 0;
  // Implement meta refresh fallback
}
```

This ensures network communication follows established protocols and handles edge cases gracefully across different HTTP versions and scenarios.