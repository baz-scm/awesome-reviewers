---
title: Network data encoding
description: Ensure network-related data like URLs and IP addresses are properly encoded
  and typed to prevent validation failures and type mismatches. When working with
  network protocols, use precise types that match the actual return values and apply
  consistent encoding across all network operations.
repository: cypress-io/cypress
label: Networking
language: TypeScript
comments_count: 2
repository_stars: 48850
---

Ensure network-related data like URLs and IP addresses are properly encoded and typed to prevent validation failures and type mismatches. When working with network protocols, use precise types that match the actual return values and apply consistent encoding across all network operations.

For IP family handling, use accurate type annotations:
```typescript
// Incorrect - net.isIP returns 0 for invalid IPs
const isIP = net.isIP(host) as net.family

// Correct - includes 0 for invalid IP case  
const isIP = net.isIP(host) as net.family | 0
```

For URL operations, ensure consistent encoding:
```typescript
// Incorrect - raw path may contain unencoded characters
shouldLoad: () => document.location.pathname.includes("${file.absolute}")

// Correct - properly encode URL for comparison
shouldLoad: () => document.location.pathname.includes("${encodeURI(file.absolute)}")
```

This prevents runtime errors from type mismatches and ensures URL validation works correctly when paths contain special characters.