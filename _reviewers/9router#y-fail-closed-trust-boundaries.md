---
title: Fail-closed trust boundaries
description: 'At every boundary where data crosses trust levels — external input,
  upstream responses, stored credentials, or user-configured restrictions — default
  to the safest behavior and never silently degrade into something less secure. Concretely:'
repository: decolua/9router#y
label: Security
language: JavaScript
comments_count: 6
repository_stars: 31751
---

At every boundary where data crosses trust levels — external input, upstream responses, stored credentials, or user-configured restrictions — default to the safest behavior and never silently degrade into something less secure. Concretely:

1. Validate untrusted input strictly by shape and type, not just by a loose check like `.length`. Reject anything that doesn't match the expected format instead of silently coercing it (e.g. `Uint8Array.from(["data:..."])` silently produces a bogus 1-byte buffer instead of the 400 the API contract promises). When input doesn't match, throw/return an explicit error rather than letting it flow downstream.

2. Never include secrets (API keys, session tokens, refresh tokens) in any response payload, even nested ones. Strip them in a single shared serializer used by every endpoint that can emit the resource (create, list, detail, update), and keep the secret available only server-side for signing/auth:
```js
function toProviderConnectionResponse(conn) {
  const { providerSpecificData, ...rest } = conn;
  const { sessionToken, ...safeData } = providerSpecificData ?? {};
  return { ...rest, providerSpecificData: safeData };
}
```

3. Sanitize any untrusted upstream content (HTML error pages, third-party text) before reflecting it into a response or UI. Strip tags and clamp length to avoid introducing XSS through error messages or logs.

4. Treat security-relevant configuration (scope restrictions, feature toggles, disabled-by-default flags) as authoritative — never route around it. If a setting like `external_web_access: false` or an unset provider selection implies "do not do X," the code must honor that exactly, not fall back to an implicit choice (e.g. auto-picking the first credentialed provider) that silently expands access beyond what was configured.

In short: fail closed, not open — reject malformed input, withhold secrets, sanitize before display, and require explicit opt-in before expanding access or scope.</description>
</invoke>
