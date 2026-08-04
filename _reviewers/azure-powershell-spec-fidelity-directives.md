---
title: Spec fidelity directives
description: When using AutoRest (or similar) to generate PowerShell/SDK surfaces,
  enforce that the generated cmdlets and types preserve the intended REST API contract—especially
  around nullability, required parameters, and unintended extra parameter-set variants.
repository: Azure/azure-powershell
label: API
language: Markdown
comments_count: 7
repository_stars: 4762
---

When using AutoRest (or similar) to generate PowerShell/SDK surfaces, enforce that the generated cmdlets and types preserve the intended REST API contract—especially around nullability, required parameters, and unintended extra parameter-set variants.

Apply this standard:
1) Verify intent with spec/API diffs
- If a generated type changes (e.g., non-nullable -> nullable), confirm whether the REST spec truly changed.
- If the change is unintended, correct it with an explicit directive (e.g., restore non-nullability) rather than patching generated code.

2) Fix via generation directives; regenerate outputs
- Avoid manual edits to generated cmdlets/models/help files.
- Update README/directives (or typespec/swagger inputs) and then regenerate so the same rule is consistently applied.

3) Suppress unwanted generated surface for API-correct behavior
- Don’t allow generic command behaviors that don’t make sense for the underlying HTTP action.
- Example: for Get- commands, suppress -Confirm/-WhatIf if the generator adds ShouldProcess due to non-GET transport behavior.

4) Keep required parameters required; don’t hide breaking changes without basis
- Ensure path/route parameters remain mandatory in cmdlet signatures.
- If generation introduces “new” parameter sets/variants, only include/unhide those that are part of the intended backward-compatible surface; otherwise filter them.

Example (directive-driven contract correction):
```yaml
# Force non-nullable primitive array elements to preserve released contract
# (addresses unintended IList<int?> generation)
- from: swagger-document
  where: $.definitions["SomeResource"].properties["rules"].items
  transform: $['x-nullable'] = false

# Suppress ShouldProcess for Get- commands that don't benefit from -Confirm/-WhatIf
# (exact directive syntax depends on the repo’s directive framework)
- where:
    subject: ^Get-.*
  suppress-shouldprocess: true
```

5) Resource-scope correctness in documentation/examples
- For examples, ensure the stated scope (resource group vs subscription-level proxy resources) matches how the API actually creates/targets the resource.

Checklist for PRs in this area:
- Show old vs new generated type signature (and where it came from in spec).
- Confirm whether the spec change is intentional.
- If not intentional: add/adjust a generation directive.
- Regenerate SDK/docs and confirm the only diffs are the intended ones.
- Validate cmdlet signature correctness (mandatory path params, filtering of unwanted variants, and suppression of misleading -Confirm/-WhatIf on Get where applicable).