---
title: consistent localhost addressing
description: Use 127.0.0.1 instead of 'localhost' for network requests and implement
  broad localhost detection rather than specific port-based checks. This ensures consistent
  behavior across different environments and avoids issues with DNS resolution or
  host file configurations.
repository: menloresearch/jan
label: Networking
language: TypeScript
comments_count: 2
repository_stars: 37620
---

Use 127.0.0.1 instead of 'localhost' for network requests and implement broad localhost detection rather than specific port-based checks. This ensures consistent behavior across different environments and avoids issues with DNS resolution or host file configurations.

For network requests, prefer the loopback IP address:
```typescript
// Preferred
await fetch(`http://127.0.0.1:${cortexJsPort}/v1/system`, {

// Avoid
await fetch('http://localhost:1337/v1/system', {
```

For localhost detection, check the hostname broadly rather than enumerating specific ports:
```typescript
const isLocalHost = urlObj.hostname === 'localhost' ||
                   urlObj.hostname === '127.0.0.1' ||
                   urlObj.hostname === '0.0.0.0'
```

This approach is more reliable and covers all local providers rather than maintaining a list of specific ports that may become outdated as new local AI providers emerge.