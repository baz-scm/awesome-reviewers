---
title: Separate configuration lifecycles
description: 'Maintain clear separation between different stages of configuration
  processing by creating dedicated structures for each phase of the configuration
  lifecycle. Divide configuration handling into distinct phases:'
repository: opentofu/opentofu
label: Configurations
language: Go
comments_count: 8
repository_stars: 25901
---

Maintain clear separation between different stages of configuration processing by creating dedicated structures for each phase of the configuration lifecycle. Divide configuration handling into distinct phases:

1. **Raw configuration loading** - Parse directly from HCL/JSON without evaluation
2. **Static evaluation** - Process expressions and validate structure
3. **Runtime configuration** - Final evaluated config ready for graph processing

This separation prevents confusion, simplifies testing, and improves maintainability.

**Bad example**:
```go
// Provider represents a provider block in a module or file.
// BUT it's sometimes also used for provider instances after evaluation!
type Provider struct {
    Name       string
    NameRange  hcl.Range
    Alias      string
    AliasExpr  hcl.Expression  // nil if no alias set
    AliasRange *hcl.Range      // nil if no alias set
    ForEach    hcl.Expression
    EachValue  *cty.Value      // Only populated after evaluation
    Count      hcl.Expression
    CountIndex *cty.Value      // Only populated after evaluation
    // ...
}
```

**Good example**:
```go
// ProviderBlock represents the raw provider configuration from a file
type ProviderBlock struct {
    Name       string
    NameRange  hcl.Range
    Alias      string
    AliasExpr  hcl.Expression
    AliasRange *hcl.Range
    ForEach    hcl.Expression
    Count      hcl.Expression
    // ...
}

// Provider represents a fully evaluated provider instance
type Provider struct {
    Name        string
    Alias       string
    InstanceKey addrs.InstanceKey  // From for_each/count evaluation
    // ...
}
```

This approach also helps with tracking deprecated configuration fields, ensuring they're properly documented and validated at the appropriate phase, and prevents confusion around whether omitted fields should be represented in serialized output.