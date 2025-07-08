---
title: Document intent and limitations
description: Clearly document the intended purpose, scope limitations, and design
  decisions in your code. For all exported types, functions, and variables, provide
  comprehensive comments explaining their purpose, usage patterns, expected behavior,
  and any deliberate limitations.
repository: opentofu/opentofu
label: Documentation
language: Go
comments_count: 8
repository_stars: 25901
---

Clearly document the intended purpose, scope limitations, and design decisions in your code. For all exported types, functions, and variables, provide comprehensive comments explaining their purpose, usage patterns, expected behavior, and any deliberate limitations.

When documenting code:
- Explain what the code does and doesn't do
- Specify when and how it should be used
- Document any assumptions or edge cases not handled
- Include links to external specifications when referenced
- Explain platform-specific behaviors and why they exist

Always update documentation when modifying code behavior, and ensure comments accurately reflect current usage patterns. This helps prevent misunderstandings and improves maintainability.

Example:
```go
// ociImageManifestSizeLimit is the maximum size of artifact manifest (aka "image
// manifest") we'll accept. This 4MiB value matches the recommended limit for
// repositories to accept on push from the OCI Distribution v1.1 spec:
// https://github.com/opencontainers/distribution-spec/blob/v1.1.0/spec.md#pushing-manifests
const ociImageManifestSizeLimitMiB = 4

// providerIterationIdentical performs a limited comparison of HCL expressions
// to determine if they are syntactically identical. This function is intentionally
// limited to simple references and function calls with simple reference arguments.
// All other expression types will return false by default, as this function is not
// expected to handle every possible HCL expression type.
func providerIterationIdentical(a, b hcl.Expression) bool {
    // implementation...
}

// EvalContextWithParent creates an evaluation context derived from the given parent
// context. This allows the new context to inherit values from its parent while
// adding or overriding specific values. This is particularly useful for nested 
// evaluations like module calls where child contexts need access to parent variables
// but also define their own local values.
func (s *Scope) EvalContextWithParent(...) {...}

// On Windows, we use 0777 permissions instead of 0755 because Windows
// doesn't have the same permission model and these bits get ignored
if runtime.GOOS == "windows" {
    // Windows-specific behavior
}
```