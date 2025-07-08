---
title: Defensive null handling
description: Always initialize data structures before use, particularly before accessing
  them in loops or conditional blocks. Check for null values before accessing their
  properties, and provide clear, contextual error messages when null values are not
  allowed.
repository: opentofu/opentofu
label: Null Handling
language: Go
comments_count: 5
repository_stars: 25901
---

Always initialize data structures before use, particularly before accessing them in loops or conditional blocks. Check for null values before accessing their properties, and provide clear, contextual error messages when null values are not allowed.

Three key practices to follow:

1. **Initialize maps and slices before they're used in loops**
```go
// Bad: May cause null pointer exception
for k, v := range instanceVariableMap {
    m.Aliases[k] = v // m.Aliases might be nil
}

// Good: Initialize first
m.Aliases = make(map[addrs.InstanceKey]string)
for k, v := range instanceVariableMap {
    m.Aliases[k] = v
}
```

2. **Validate nullability with specific error messages**
```go
// Bad: Generic or missing null validation
if val.IsNull() {
    return errors.New("invalid value")
}

// Good: Clear context about why null isn't allowed
if val.IsNull() {
    return &hcl.Diagnostic{
        Severity: hcl.DiagError,
        Summary:  "Import block 'to' address contains an invalid key",
        Detail:   "Import block contained a resource address using an index which is null. Please make sure the expression for the index is not null",
        Subject:  expr.Range().Ptr(),
    }
}
```

3. **Ensure map initialization happens even in error paths**
```go
// Bad: Variables only initialized in happy path
if len(refs) == 0 {
    ctx.Variables = make(map[string]cty.Value)
    return ctx, diags
}

// Good: Initialize early to handle all code paths
ctx := parent.NewChild()
ctx.Functions = make(map[string]function.Function)
ctx.Variables = make(map[string]cty.Value)
```

When appropriate, create helper methods (like `IsValid()` or `IsSet()`) for commonly repeated null checks to improve code readability.