---
title: Consolidate related code
description: Organize code to keep related functionality together. When functions
  serve similar purposes or operate on the same data, combine them rather than creating
  separate implementations. Position validation and condition checks before execution
  to allow early returns and avoid unnecessary processing. This improves code readability,
  maintainability, and reduces...
repository: hashicorp/terraform
label: Code Style
language: Go
comments_count: 5
repository_stars: 45532
---

Organize code to keep related functionality together. When functions serve similar purposes or operate on the same data, combine them rather than creating separate implementations. Position validation and condition checks before execution to allow early returns and avoid unnecessary processing. This improves code readability, maintainability, and reduces duplication.

For example, instead of having separate validation functions:

```go
func (n *NodeAbstractResourceInstance) validateIdentity(newIdentity cty.Value) (diags tfdiags.Diagnostics) {
    // Validate marks
    // ...
    return diags
}

func (n *NodeAbstractResourceInstance) validateIdentityMatchesSchema(newIdentity cty.Value, identitySchema *configschema.Object) (diags tfdiags.Diagnostics) {
    // Validate schema
    // ...
    return diags
}
```

Prefer consolidating them into a single function:

```go
func (n *NodeAbstractResourceInstance) validateIdentity(newIdentity cty.Value, identitySchema *configschema.Object) (diags tfdiags.Diagnostics) {
    // Validate marks
    // ...
    
    // Validate schema
    // ...
    
    return diags
}
```

Similarly, perform condition checks early in functions to avoid unnecessary work, as seen in discussion 9 where condition checks were moved before execution calls.