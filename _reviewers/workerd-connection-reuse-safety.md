---
title: Connection reuse safety
description: When implementing network connection reuse, prioritize safety over performance
  by enforcing sequential request patterns and clear resource ownership. Connection
  reuse should be supported to avoid the overhead of creating new connections for
  each request, but must include proper safeguards to prevent concurrency issues and
  resource conflicts.
repository: cloudflare/workerd
label: Networking
language: JavaScript
comments_count: 4
repository_stars: 6989
---

When implementing network connection reuse, prioritize safety over performance by enforcing sequential request patterns and clear resource ownership. Connection reuse should be supported to avoid the overhead of creating new connections for each request, but must include proper safeguards to prevent concurrency issues and resource conflicts.

Key principles:
- Allow only sequential requests on reused connections, never concurrent ones
- Implement clear ownership semantics where HTTP clients take full control of underlying sockets
- Provide explicit error handling when connections are in invalid states
- Document the single-request-at-a-time limitation clearly for developers

Example implementation pattern:
```javascript
// Each call to fetch should:
// 1. Check if a client currently exists, if so, error
// 2. Create a new client over the stream
// 3. Perform the fetch
// 4. Release the stream when done (unless errored)

const httpClient = await internalNewHttpClient(socket);
const response1 = await httpClient.fetch('https://example.com/ping');
// Second request should fail with clear error message
await assert.rejects(httpClient.fetch('https://example.com/json'), {
  message: 'Fetcher created from internalNewHttpClient can only be used once'
});
```

This approach balances the performance benefits of connection reuse with the safety requirements of preventing undefined behavior from overlapping network operations. The connection lifecycle should be deterministic and well-documented to avoid developer confusion about resource ownership.