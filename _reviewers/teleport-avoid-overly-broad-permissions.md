---
title: Avoid overly broad permissions
description: Use specific, scoped permissions instead of wildcards to prevent unintended
  access to sensitive resources. Wildcard permissions can grant access to critical
  applications beyond the intended scope, creating security vulnerabilities.
repository: gravitational/teleport
label: Security
language: Go
comments_count: 3
repository_stars: 19109
---

Use specific, scoped permissions instead of wildcards to prevent unintended access to sensitive resources. Wildcard permissions can grant access to critical applications beyond the intended scope, creating security vulnerabilities.

When security controls like MFA or device trust must be bypassed for technical reasons, explicitly document these limitations and consider renaming functions to highlight the security implications.

Example of problematic wildcard usage:
```go
// BAD: Grants access to all applications, including sensitive ones
AppLabels: map[string]apiutils.Strings{
    types.Wildcard: []string{types.Wildcard},
}

// GOOD: Scope to specific application types using labels
AppLabels: map[string]apiutils.Strings{
    types.TeleportInternalAppType: []string{"mcp"},
}
```

When bypassing security controls, make the limitation explicit:
```go
// BAD: Unclear that MFA is bypassed
func hasAccess() bool { /* ... */ }

// GOOD: Clear about security limitations  
func canViewUncheckedMFA() bool { /* ... */ }
```

Always validate that role permissions match their intended purpose and document any security control bypasses to prevent future misuse.