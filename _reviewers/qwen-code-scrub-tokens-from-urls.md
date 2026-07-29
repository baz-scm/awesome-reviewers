---
title: Scrub Tokens From URLs
description: Sensitive authentication tokens must not remain in the browser URL after
  they are consumed. Tokens in query parameters (`?token=`) will leak via browser
  history, server access logs, and `Referer` headers when users navigate away; removing
  URL fragments alone is insufficient if `?token=` is supported.
repository: QwenLM/qwen-code
label: Security
language: TSX
comments_count: 1
repository_stars: 26407
---

Sensitive authentication tokens must not remain in the browser URL after they are consumed. Tokens in query parameters (`?token=`) will leak via browser history, server access logs, and `Referer` headers when users navigate away; removing URL fragments alone is insufficient if `?token=` is supported.

Apply this standard by:
- Deleting any token-bearing query params immediately after reading/consuming them.
- Relying on safer storage (e.g., `sessionStorage`) or internal state for refresh/reload behavior.
- Ensuring the cleanup covers the actual supported token path(s) (query params, not only `#fragment`).

Example pattern:
```ts
function replaceStandaloneSessionUrl(url: URL) {
  // ... logic that extracts token from url.searchParams

  // After token is consumed, remove it from the address bar
  if (!import.meta.env.DEV) {
    url.searchParams.delete('token');
    url.searchParams.delete('daemon');
  }

  // ... continue with navigation/state update
}
```