---
title: API validation consistency
description: Ensure API validation rules and type definitions remain consistent across
  all validation layers and components. When implementing validation logic, verify
  that kubebuilder annotations, manual validation functions, and API type definitions
  all enforce the same constraints and use compatible data types.
repository: volcano-sh/volcano
label: API
language: Go
comments_count: 2
repository_stars: 4899
---

Ensure API validation rules and type definitions remain consistent across all validation layers and components. When implementing validation logic, verify that kubebuilder annotations, manual validation functions, and API type definitions all enforce the same constraints and use compatible data types.

For example, if kubebuilder validation allows both HyperNode and Node member types, manual validation should also distinguish between these types consistently:

```go
// API definition should use appropriate types
type MemberType string

// Manual validation should match kubebuilder rules
func validateHyperNodeMemberSelector(selector hypernodev1alpha1.MemberSelector, fldPath *field.Path, memberType hypernodev1alpha1.MemberType) field.ErrorList {
    if memberType != hypernodev1alpha1.MemberTypeHyperNode && memberType != hypernodev1alpha1.MemberTypeNode {
        err := field.Invalid(fldPath, memberType, "hyperNode member type must be one of HyperNode or Node")
        errs = append(errs, err)
        return errs
    }
    // Validation logic should distinguish between member types consistently
    if memberType == hypernodev1alpha1.MemberTypeHyperNode {
        // HyperNode-specific validation that matches kubebuilder rules
    }
}
```

Additionally, choose appropriate data types in API definitions. Use strongly-typed fields (like int for numeric values) rather than strings when the semantic meaning is numeric, unless there's a specific need for named values that require string-to-numeric mapping.