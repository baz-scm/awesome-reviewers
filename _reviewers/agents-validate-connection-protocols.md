---
title: validate connection protocols
description: Always validate network connection types, required parameters, and protocol-specific
  headers before processing requests. This prevents runtime errors and ensures proper
  connection handling across different network protocols.
repository: cloudflare/agents
label: Networking
language: TypeScript
comments_count: 2
repository_stars: 2312
---

Always validate network connection types, required parameters, and protocol-specific headers before processing requests. This prevents runtime errors and ensures proper connection handling across different network protocols.

For WebSocket connections, verify the Upgrade header and required parameters:
```typescript
// Validate WebSocket upgrade request
if (request.headers.get("Upgrade") !== "websocket") {
  return new Response("Expected WebSocket Upgrade request", {
    status: 400,
  });
}

// Validate required parameters
const url = new URL(request.url);
const sessionId = url.searchParams.get("sessionId");
if (!sessionId) {
  return new Response("Missing sessionId", { status: 400 });
}
```

Use URL paths to distinguish between different protocols and route accordingly:
```typescript
const path = url.pathname;
switch (path) {
  case "/sse": {
    // Handle SSE protocol
    break;
  }
  case "/websocket": {
    // Handle WebSocket protocol
    break;
  }
}
```

Consider implementing connection limits and state management to prevent issues with multiple concurrent connections when your system expects only one active connection per session.