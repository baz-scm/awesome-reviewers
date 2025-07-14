---
title: Scope security settings
description: Avoid modifying global security state in favor of connection-specific
  or context-bound security settings. Global security state changes can lead to unexpected
  security vulnerabilities when modified by dependencies without application awareness.
repository: nodejs/node
label: Security
language: Markdown
comments_count: 1
repository_stars: 112178
---

Avoid modifying global security state in favor of connection-specific or context-bound security settings. Global security state changes can lead to unexpected security vulnerabilities when modified by dependencies without application awareness.

When working with security-critical components like TLS:
1. Configure security options at the connection level rather than globally
2. Be wary of APIs that make one-way security changes affecting all connections
3. Design APIs that allow explicit security configuration for specific contexts

For example, instead of using global security state changes:
```js
// Avoid globally changing security state
tls.useSystemCA();  // Affects ALL connections

// Preferred: Scope security settings to specific connections
const connection = tls.connect({
  ca: tls.getCACertificates('system')  // Only affects this connection
});
```

This approach maintains clear security boundaries and prevents dependencies from silently weakening your application's security posture through unexpected global state mutations.