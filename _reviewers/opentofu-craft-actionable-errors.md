---
title: Craft actionable errors
description: Create error messages that provide precise context, avoid unnecessary
  details, and give users clear actions to take. Error messages should include location
  information when possible, avoid jargon, and maintain a consistent tone without
  being patronizing.
repository: opentofu/opentofu
label: Error Handling
language: Go
comments_count: 11
repository_stars: 25901
---

Create error messages that provide precise context, avoid unnecessary details, and give users clear actions to take. Error messages should include location information when possible, avoid jargon, and maintain a consistent tone without being patronizing.

When reporting errors from the UI:
1. Include relevant context like resource names or locations
2. Use source locations (`Subject` field) when available
3. Exclude technical details that don't help users solve the problem
4. Clearly state what action is needed to fix the issue

**Bad:**
```go
diags = diags.Append(tfdiags.Sourceless(
    tfdiags.Warning,
    "Output change in sensitivity",
    fmt.Sprintf("A previously sensitive output is being changed to insensitive: %q.", outputName),
))
```

**Good:**
```go
diags = diags.Append(&hcl.Diagnostic{
    Severity: hcl.DiagWarning,
    Summary:  "Output change in sensitivity",
    Detail:   fmt.Sprintf("Sensitivity of the output %q changed. By doing so, the value will not be obfuscated anymore.", oc.Name),
    Subject:  oc.DeclRange.Ptr(),
})
```

When joining multiple errors, use `errors.Join()` with a clear leading message:
```go
errs = append([]error{fmt.Errorf("decryption failed for all provided methods")}, errs...)
errMessage := errors.Join(errs...).Error()
```

For API/provider references, use a consistent style:
```go
diags = diags.Append(&hcl.Diagnostic{
    Severity: hcl.DiagError,
    Summary:  "Reference to undeclared key provider",
    Detail:   fmt.Sprintf("There is no key_provider %q %q block declared in the encryption block.", depType, depName),
})
```