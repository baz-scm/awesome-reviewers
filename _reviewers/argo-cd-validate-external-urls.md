---
title: validate external URLs
description: Always validate and sanitize external URLs before opening them or using
  them in navigation operations to prevent URL injection attacks. Implement domain
  allowlists to restrict which external domains are permitted, and avoid directly
  passing user-controlled or external URL data to functions like window.open() without
  proper validation.
repository: argoproj/argo-cd
label: Security
language: TSX
comments_count: 1
repository_stars: 20149
---

Always validate and sanitize external URLs before opening them or using them in navigation operations to prevent URL injection attacks. Implement domain allowlists to restrict which external domains are permitted, and avoid directly passing user-controlled or external URL data to functions like window.open() without proper validation.

Example of vulnerable code:
```typescript
// Dangerous - direct use of external URL
onClick={e => {
    e.stopPropagation();
    window.open(m.imageUrl); // Potential injection point
}}
```

Instead, implement URL validation:
```typescript
const isAllowedDomain = (url: string) => {
    const allowedDomains = ['trusted-domain.com', 'another-trusted.com'];
    try {
        const urlObj = new URL(url);
        return allowedDomains.includes(urlObj.hostname);
    } catch {
        return false;
    }
};

onClick={e => {
    e.stopPropagation();
    if (isAllowedDomain(m.imageUrl)) {
        window.open(m.imageUrl);
    }
}}
```

Consider removing external URL functionality entirely if proper validation cannot be implemented immediately, and add it back as a follow-up enhancement with appropriate security measures.