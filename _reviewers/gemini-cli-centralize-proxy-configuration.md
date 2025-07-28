---
title: Centralize proxy configuration
description: Avoid duplicate proxy configuration across your application by establishing
  a single point of proxy setup and leveraging built-in proxy support where available.
  Multiple proxy configurations can lead to conflicts, inconsistent behavior, and
  maintenance overhead.
repository: google-gemini/gemini-cli
label: Networking
language: TypeScript
comments_count: 4
repository_stars: 65062
---

Avoid duplicate proxy configuration across your application by establishing a single point of proxy setup and leveraging built-in proxy support where available. Multiple proxy configurations can lead to conflicts, inconsistent behavior, and maintenance overhead.

Key principles:
1. **Use global configuration**: Set up proxy handling once at the application entry point rather than in individual modules
2. **Leverage built-in support**: Many libraries automatically read proxy settings from environment variables - avoid manual configuration when this exists
3. **Avoid hardcoded network resources**: Use dynamic allocation for ports and endpoints to prevent conflicts when multiple instances run

Example from the discussions:
```typescript
// ❌ Avoid: Multiple proxy configurations
export class MCPOAuthProvider {
  private static readonly REDIRECT_PORT = 7777; // Hardcoded port causes conflicts
}

// In another file
const client = new OAuth2Client({
  transporter: new Gaxios({ proxy: proxyUrl }) // Duplicate proxy setup
});

// ❌ Avoid: Redundant proxy setup
if (config.getProxy()) {
  // setGlobalDispatcher already called in core/client.ts
}

// ✅ Better: Centralized approach
// In core/client.ts - set once globally
setGlobalDispatcher(proxyAgent);

// OAuth2Client automatically reads from environment
const client = new OAuth2Client({
  // No manual transporter needed - uses env proxy settings
});

// Use dynamic port allocation
const server = http.createServer();
server.listen(0); // Let Node.js choose available port
```

This approach ensures consistent proxy behavior across all network requests while avoiding configuration conflicts and reducing maintenance burden.