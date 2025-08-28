---
title: consistent configuration handling
description: Ensure configuration options are handled uniformly across all API endpoints
  and providers. Configuration should have clear precedence rules, support dynamic
  values where appropriate, and avoid hardcoded fallbacks.
repository: better-auth/better-auth
label: API
language: TypeScript
comments_count: 10
repository_stars: 19651
---

Ensure configuration options are handled uniformly across all API endpoints and providers. Configuration should have clear precedence rules, support dynamic values where appropriate, and avoid hardcoded fallbacks.

Key principles:
1. **Clear precedence**: When multiple configuration sources exist (payload, options, defaults), document and implement a consistent precedence order
2. **Dynamic configuration**: Allow functions for configuration values that need to be determined at runtime based on context
3. **Uniform option processing**: Handle configuration options consistently across similar endpoints and providers
4. **Avoid hardcoded values**: Use configuration options instead of hardcoded paths, domains, or other values

Example of good configuration handling:
```typescript
// Bad: Unclear precedence and hardcoded fallback
const consentURI = `${options.consentPage}?client_id=${client.clientId}&scope=${requestScope.join(" ")}`;

// Good: Clear precedence and proper encoding
const url = new URL(options.consentPage);
url.searchParams.set('consent_code', encodeURIComponent(code));
url.searchParams.set('client_id', encodeURIComponent(client.clientId));
url.searchParams.set('scope', encodeURIComponent(requestScope.join(' ')));

// Bad: Static configuration only
team: string;

// Good: Dynamic configuration support  
team?: string | ((ctx: Context) => string);
```

This ensures developers have predictable behavior, proper flexibility, and consistent patterns across the entire API surface.