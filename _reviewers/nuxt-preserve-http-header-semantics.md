---
title: Preserve HTTP header semantics
description: HTTP headers have specific semantics that must be respected when processing,
  merging, or deduplicating them. Avoid naive approaches that treat headers as simple
  key-value pairs, as this can break protocol compliance and cause unexpected behavior.
repository: nuxt/nuxt
label: Networking
language: TypeScript
comments_count: 2
repository_stars: 57769
---

HTTP headers have specific semantics that must be respected when processing, merging, or deduplicating them. Avoid naive approaches that treat headers as simple key-value pairs, as this can break protocol compliance and cause unexpected behavior.

For set-cookie headers, remember that cookies are distinct by multiple attributes (name, domain, path, secure, httpOnly, sameSite), not just their values. Simple equality checks on cookie values can incorrectly deduplicate distinct cookies that should coexist.

When handling response headers, preserve existing headers rather than flattening them. Use appropriate header manipulation functions that understand header-specific rules:

```typescript
// Good: Preserve header semantics
if (header === 'set-cookie') {
  appendResponseHeader(event, header, value)  // Preserves multiple set-cookie headers
} else {
  setResponseHeader(event, header, value)
}

// Bad: Naive deduplication that breaks cookie semantics  
if (isEqual(cookie.value, existingCookie.value)) { 
  return // This ignores domain, path, and other cookie attributes
}
```

Always use protocol-aware utilities and libraries that understand the specific rules for each header type, rather than implementing custom string manipulation logic.