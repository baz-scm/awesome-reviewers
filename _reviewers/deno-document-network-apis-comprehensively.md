---
title: Document network APIs comprehensively
description: Network APIs and interfaces should include comprehensive documentation
  with clear descriptions, practical examples, and proper configuration guidance.
  This is especially important for complex protocols like WebSockets, HTTPS, and specialized
  network transports.
repository: denoland/deno
label: Networking
language: TypeScript
comments_count: 3
repository_stars: 103714
---

Network APIs and interfaces should include comprehensive documentation with clear descriptions, practical examples, and proper configuration guidance. This is especially important for complex protocols like WebSockets, HTTPS, and specialized network transports.

When documenting network APIs:
- Provide clear descriptions of what the API does and its purpose
- Include practical code examples showing real-world usage
- Document configuration options with examples of proper setup
- Explain protocol-specific features (like WebSocket extensions) with context
- Mark unstable or experimental network interfaces appropriately

Example of comprehensive network API documentation:

```ts
/**
 * Returns the extensions selected by the server, if any.
 *
 * WebSocket extensions add optional features negotiated during the handshake via
 * the `Sec-WebSocket-Extensions` header.
 *
 * At the time of writing, there are two registered extensions:
 * - `permessage-deflate`: Enables per-message compression using DEFLATE
 * - `bbf-usp-protocol`: Used by the Broadband Forum's User Services Platform
 *
 * Example:
 * ```ts
 * const ws = new WebSocket("ws://localhost:8080");
 * console.log(ws.extensions); // e.g., "permessage-deflate"
 * ```
 */
readonly extensions: string;
```

This approach helps developers understand not just how to use network APIs, but also the underlying protocols and proper configuration patterns.