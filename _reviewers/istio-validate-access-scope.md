---
title: validate access scope
description: When implementing security features that involve access control, authentication,
  or authorization, carefully validate that the changes don't inadvertently grant
  broader access than intended. This is particularly critical when dealing with secret
  access, trust domains, or credential handling.
repository: istio/istio
label: Security
language: Go
comments_count: 2
repository_stars: 37192
---

When implementing security features that involve access control, authentication, or authorization, carefully validate that the changes don't inadvertently grant broader access than intended. This is particularly critical when dealing with secret access, trust domains, or credential handling.

Key areas to scrutinize:
- **Secret Access**: Ensure clients can only access secrets for resources that actually apply to them, not arbitrary secrets they request
- **Trust Domain Expansion**: When expanding trust domains or SANs, verify that generated identities correspond to legitimate, existing service accounts
- **Privilege Escalation**: Check that security policy changes don't allow bypassing intended access restrictions

Example from the codebase:
```go
// PROBLEMATIC: Allows proxy to access secrets for any WasmPlugin they request
wasmPlugins := push.WasmPluginsByName(proxy, core.ParseExtensionName(resourceNames))

// BETTER: Only allow access to WasmPlugins that actually apply to the proxy  
wasmPlugins := push.WasmPlugins(proxy)
```

Always ask: "Could this change allow a client to access resources they shouldn't have access to?" If the answer is unclear, implement additional validation or use more restrictive approaches like RBAC-style permission checks.