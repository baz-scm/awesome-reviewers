---
title: Secure credential handling
description: Treat secrets (API keys, session tokens, OAuth/LLM tokens) and client-specified
  privacy flags as security-sensitive, and centralize their handling so fixes apply
  everywhere consistently.
repository: decolua/9router#MARKER9ROUTER7
label: Security
language: JavaScript
comments_count: 3
repository_stars: 31425
---

Treat secrets (API keys, session tokens, OAuth/LLM tokens) and client-specified privacy flags as security-sensitive, and centralize their handling so fixes apply everywhere consistently.

1. Never leak raw secrets back to the client. Any field that stores a credential substitute (e.g. `providerSpecificData.sessionToken`, AWS profile data, LLM tokens) must be stripped before the object is serialized into an API response, while the server retains it internally for actual use. Route all outgoing responses through a single sanitizing serializer (e.g. `toProviderConnectionResponse()`) rather than ad hoc field removal in each route, so a new endpoint can't accidentally forget to redact a secret.

```js
// All provider routes funnel through one serializer that drops secrets
function toProviderConnectionResponse(provider) {
  const { providerSpecificData, ...safe } = provider;
  const { sessionToken, ...safeProviderData } = providerSpecificData || {};
  return { ...safe, providerSpecificData: safeProviderData };
}
```

2. Centralize credential/token-refresh logic in one service instead of duplicating HTTP calls, auth headers, and token-unwrapping logic across multiple executors/handlers. Duplication (e.g. `ZedExecutor.refreshCredentials()` reimplementing the same `/client/llm_tokens` call and token-unwrap as `refreshZedToken()`) risks a security fix landing in one copy but not the other. Extract shared logic into a single service method and have all callers delegate to it.

3. Honor explicit security/privacy flags set by the client rather than silently overriding them for convenience. If a request opts out of external access (e.g. `external_web_access:false`), do not reroute it through an external provider or service — disable the fallback entirely and pass the request through unchanged, with a test asserting the opt-out is respected.

Add regression tests that assert secrets never appear in serialized responses and that privacy opt-outs are enforced, since these issues are easy to reintroduce silently.