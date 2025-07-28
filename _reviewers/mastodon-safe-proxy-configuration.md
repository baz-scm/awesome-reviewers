---
title: Safe proxy configuration
description: When configuring proxy settings for network applications, always use
  proper compilation methods to prevent runtime errors and ensure consistent IP address
  handling across different connection types. Improper proxy configuration can cause
  server crashes when IP addresses are accessed, particularly when using string-based
  configurations with multiple values.
repository: mastodon/mastodon
label: Networking
language: JavaScript
comments_count: 2
repository_stars: 48691
---

When configuring proxy settings for network applications, always use proper compilation methods to prevent runtime errors and ensure consistent IP address handling across different connection types. Improper proxy configuration can cause server crashes when IP addresses are accessed, particularly when using string-based configurations with multiple values.

Use proxyaddr.compile() to safely process proxy configurations and define IP properties consistently:

```javascript
const trustProxy = proxyaddr.compile(
  process.env.TRUSTED_PROXY_IP ?
    process.env.TRUSTED_PROXY_IP.split(/(?:\s*,\s*|\s+)/) :
    ['loopback', 'uniquelocal']
);

// For websocket connections, define IP property to match Express behavior
Object.defineProperty(request, 'ip', {
  configurable: true,
  enumerable: true,
  get() {
    return proxyaddr(this, trustProxy);
  }
});
```

This approach prevents server crashes from malformed proxy configurations and ensures that IP address access works uniformly across HTTP and WebSocket connections, enabling consistent network security features like IP blocking.