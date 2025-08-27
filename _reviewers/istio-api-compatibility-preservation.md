---
title: API compatibility preservation
description: When evolving APIs, prioritize backward compatibility and avoid changing
  the semantics of existing fields. Instead of overloading existing fields with new
  meanings, introduce new fields to maintain compatibility with existing usage patterns.
repository: istio/istio
label: API
language: Go
comments_count: 5
repository_stars: 37192
---

When evolving APIs, prioritize backward compatibility and avoid changing the semantics of existing fields. Instead of overloading existing fields with new meanings, introduce new fields to maintain compatibility with existing usage patterns.

Key principles:
- Treat existing field values as opaque strings that users depend on
- Add new fields rather than changing behavior of existing ones  
- Follow API specifications precisely, especially for required vs optional fields
- Validate that implementation changes align with documented API contracts

Example from the codebase:
```go
// Instead of changing semantics of existing credentialName field:
if strings.HasSuffix(name, SdsCaSuffix) {
    // This changes behavior for existing users
}

// Better approach - add a new field:
type TLSOptions struct {
    CredentialName       string  // Keep existing semantics
    CaCertCredentialName string  // New field for CA certificates
}
```

When updating to new API versions, ensure field type changes (like `*string` to `string`) are handled correctly and check for both nil pointers and empty strings as appropriate. Always verify that changes follow the official API specification rather than making assumptions about field behavior.