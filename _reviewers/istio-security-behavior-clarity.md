---
title: Security behavior clarity
description: When documenting or describing security-related changes, especially bug
  fixes and behavioral modifications, ensure clear and explicit communication of security
  implications. Use proper security terminology and clearly describe both the problematic
  behavior and the fix.
repository: istio/istio
label: Security
language: Yaml
comments_count: 2
repository_stars: 37192
---

When documenting or describing security-related changes, especially bug fixes and behavioral modifications, ensure clear and explicit communication of security implications. Use proper security terminology and clearly describe both the problematic behavior and the fix.

Key requirements:
- Use standard security terminology (e.g., "self-signed CA" not "selfsigned-ca")
- Explicitly state what the insecure behavior was and what the secure behavior now is
- For failure modes, clearly indicate whether the system fails open (permissive) or closed (restrictive)
- Describe the security impact in terms developers can understand

Example of unclear security communication:
```yaml
releaseNotes:
  - |
    **Fixed** For a WasmPlugin of type FAIL_CLOSE, if the wasm image fetch fails, a DENY-ALL RBAC filter will be used.
```

Example of clear security communication:
```yaml
releaseNotes:
  - |
    **Fixed** an issue where if a wasm image fetch fails, an allow all RBAC filter is used. Now if `failStrategy` is set to `FAIL_CLOSE`, a DENY-ALL RBAC filter will be used.
```

This practice helps developers understand security implications, reduces confusion about security behaviors, and ensures that security fixes are properly communicated to users who need to understand the impact on their systems.