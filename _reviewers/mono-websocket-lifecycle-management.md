---
title: WebSocket lifecycle management
description: Ensure proper WebSocket connection lifecycle management by using `once()`
  instead of `on()` for cleanup operations and separating initialization from construction
  to avoid race conditions.
repository: rocicorp/mono
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 2091
---

Ensure proper WebSocket connection lifecycle management by using `once()` instead of `on()` for cleanup operations and separating initialization from construction to avoid race conditions.

When setting up WebSocket connections, use `once()` for events that should only happen once, particularly for cleanup operations:

```typescript
// Good: Use once() for cleanup events
ws.once('open', () => startHeartBeats());
ws.once('close', () => clearInterval(heartbeatTimer));
ws.once('close', () => clearTimeout(missedPingTimer));

// Avoid: Using on() for one-time cleanup
ws.on('close', () => clearInterval(heartbeatTimer)); // Could fire multiple times
```

Separate connection initialization from construction to prevent race conditions where close handlers might execute before the connection is properly registered:

```typescript
// Good: Two-phase initialization
const connection = new Connection(..., onCloseHandler);
this.connections.set(clientID, connection);
connection.init(); // Now safe to close if needed

// Avoid: Initialization in constructor that might close immediately
```

This pattern prevents resource leaks, ensures cleanup operations execute exactly once, and avoids timing issues where connections might be closed before being properly tracked.