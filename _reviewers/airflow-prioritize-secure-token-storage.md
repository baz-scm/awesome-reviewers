---
title: Prioritize secure token storage
description: When implementing authentication token handling, prioritize more secure
  storage mechanisms over less secure ones. Specifically, prefer retrieving tokens
  from properly configured cookies (with Secure and HttpOnly flags) before falling
  back to localStorage, which is vulnerable to XSS attacks.
repository: apache/airflow
label: Security
language: TypeScript
comments_count: 1
repository_stars: 40858
---

When implementing authentication token handling, prioritize more secure storage mechanisms over less secure ones. Specifically, prefer retrieving tokens from properly configured cookies (with Secure and HttpOnly flags) before falling back to localStorage, which is vulnerable to XSS attacks.

**Why**: Cookies with proper security attributes (HttpOnly, Secure, SameSite) provide better protection against common web vulnerabilities like XSS attacks compared to localStorage or sessionStorage, which can be accessed by any JavaScript running on your page.

**Example**:
```typescript
// Insecure approach: localStorage first, cookies as fallback
const token = localStorage.getItem(TOKEN_STORAGE_KEY) ?? getTokenFromCookies();

// Secure approach: properly configured cookies first, localStorage as fallback
const token = getTokenFromCookies() ?? localStorage.getItem(TOKEN_STORAGE_KEY);
```

When using cookies for token storage, ensure they are configured with appropriate security flags (HttpOnly, Secure, SameSite) to maximize protection against common web attacks.