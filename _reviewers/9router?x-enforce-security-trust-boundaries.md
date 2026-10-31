---
title: Enforce security trust boundaries
description: Never let default or convenience behavior silently cross a security boundary.
  Whenever code returns data, reroutes a request, or substitutes/injects behavior
  on behalf of the caller, explicitly validate the trust and scope assumptions involved
  instead of assuming the common case is safe.
repository: decolua/9router?x
label: Security
language: JavaScript
comments_count: 4
repository_stars: 31748
---

Never let default or convenience behavior silently cross a security boundary. Whenever code returns data, reroutes a request, or substitutes/injects behavior on behalf of the caller, explicitly validate the trust and scope assumptions involved instead of assuming the common case is safe.

Concretely:
- Strip secrets/credentials from every outbound response path through one centralized serializer rather than per-endpoint logic. E.g. `toProviderConnectionResponse()` must remove fields like AWS `sessionToken` from create, list, detail, and update responses alike, while keeping the secret available server-side only where it's actually needed (e.g. request signing). A single shared helper prevents one endpoint from forgetting to redact a field another endpoint already handles correctly.
- Honor explicit security/privacy constraints set by the caller; never auto-escalate scope to make a feature work. If a client sets `external_web_access: false`, a search fallback must not reroute the request to an external provider — it must leave the request untouched (feature effectively disabled) rather than violate the stated restriction.
- Before substituting or injecting trusted system behavior under a reserved name (e.g. an internally-generated tool/function name), check it against caller-supplied/untrusted names first and bail out if there's a collision:
```js
if (!toolNames.has(RESERVED_TOOL_NAME)) {
  preservedTools.unshift(buildFallbackTool(...));
} else {
  // name is already taken by client input — skip the rewrite entirely
  return { body, fallback: disabled };
}
```
Without this check, a client-controlled name could be executed as if it were the trusted built-in mechanism.

Add regression tests asserting the sensitive field is absent from every response shape, that scoped/restricted requests are never escalated, and that name collisions disable the automatic rewrite.