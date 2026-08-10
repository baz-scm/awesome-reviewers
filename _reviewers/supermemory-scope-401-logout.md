---
title: Scope 401 Logout
description: Avoid triggering sensitive auth actions (like logout) based solely on
  a generic HTTP status (e.g., “any 401”). Instead, logout only when the 401 is clearly
  an authentication/session failure for known auth endpoints.
repository: supermemoryai/supermemory
label: Security
language: TSX
comments_count: 1
repository_stars: 28844
---

Avoid triggering sensitive auth actions (like logout) based solely on a generic HTTP status (e.g., “any 401”). Instead, logout only when the 401 is clearly an authentication/session failure for known auth endpoints.

How to apply:
- Gate logout by request target (e.g., only your `/api/auth/*` or token-refresh endpoints).
- Optionally verify server intent using headers (e.g., `WWW-Authenticate: Bearer error="invalid_token"` or a custom auth error header).
- Keep global fetch/401 interception minimal and centralized; don’t assume every 401 means the user session is invalid.

Example (gated interception):

```ts
useEffect(() => {
  const origFetch = window.fetch

  async function customFetch(input: RequestInfo | URL, init?: RequestInit) {
    const url = typeof input === 'string' ? input : input.toString()
    const response = await origFetch(input, init)

    const isAuthEndpoint = url.includes('/api/auth/') || url.includes('/api/token/refresh')
    const isAuthFailure = response.headers.get('WWW-Authenticate')?.includes('invalid_token')

    if (response.status === 401 && isAuthEndpoint && isAuthFailure) {
      router.push('/login')
      window.location.reload()
    }

    return response
  }

  window.fetch = customFetch as any
  return () => {
    window.fetch = origFetch
  }
}, [router])
```

This prevents accidental logouts from unrelated authorization checks and aligns sensitive security behavior with explicit authentication intent.