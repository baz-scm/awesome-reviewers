---
title: Consistent error handling
description: 'Apply a single, predictable error-handling strategy across cmdlets and
  SDK wrappers:


  - **Make existence semantics consistent**: if a method supports `throwIfNotExists`
  (or callers rely on it), every related “read/modify” path must honor it the same
  way (return `null` vs throw), and callers should not silently diverge between Get/With*
  operations.'
repository: Azure/azure-powershell
label: Error Handling
language: C#
comments_count: 5
repository_stars: 4762
---

Apply a single, predictable error-handling strategy across cmdlets and SDK wrappers:

- **Make existence semantics consistent**: if a method supports `throwIfNotExists` (or callers rely on it), every related “read/modify” path must honor it the same way (return `null` vs throw), and callers should not silently diverge between Get/With* operations.
- **Align messages with cmdlet intent**: for “New” vs “Set” flows, warnings must reflect what the cmdlet is trying to do:
  - **New**: warn when the What-If already exists.
  - **Set**: warn when the What-If does *not* exist.
- **Use argument-focused exceptions for user input errors**: when inputs are invalid or mutually exclusive, validate client-side and throw **`AzPSArgumentException`** (not generic `InvalidOperationException`), with clear text (including the expected format when relevant).
- **Validate critical identifiers early + test both paths**: for parameters like `-ResourceId`, validate format upfront and add scenario tests for both success and failure.
- **Use -Force to control recovery/continuation**: if an existing resource affects behavior, query it first; if it exists/missing and `-Force` is not set, warn and stop/confirm; if `-Force` is set, proceed.

Example pattern (existence + intent + -Force + consistent throw semantics):
```csharp
PSDeploymentStackWhatIfResult existing = null;
try
{
    existing = sdk.GetResourceGroupDeploymentStackWhatIfResult(
        rgName, stackName, throwIfNotExists: false);
}
catch (Exception ex)
{
    // Only treat as non-fatal if the strategy explicitly allows graceful degradation.
    existing = null;
}

if (existing != null)
{
    // NEW cmdlet intent: warn when exists; Set cmdlet would invert this logic.
    if (!Force.IsPresent)
        throw new AzPSArgumentException($"What-If result '{stackName}' already exists. Use -Force to overwrite.");
}
else
{
    // SET cmdlet intent: warn when missing; NEW cmdlet proceeds.
    if (this.IsSetCmdlet && !Force.IsPresent)
        throw new AzPSArgumentException($"What-If result '{stackName}' not found. Use -Force to continue.");
}
```

This standard improves graceful degradation, error clarity, and reduces inconsistent behavior across cmdlets and SDK conversion layers.