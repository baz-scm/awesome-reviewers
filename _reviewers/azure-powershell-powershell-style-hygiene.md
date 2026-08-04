---
title: PowerShell style hygiene
description: 'Adopt consistent PowerShell coding patterns to improve correctness and
  readability, and keep project definitions clean.


  - Boolean parameter syntax: pass boolean parameters using the idiomatic form for
  the context.'
repository: Azure/azure-powershell
label: Code Style
language: Other
comments_count: 5
repository_stars: 4762
---

Adopt consistent PowerShell coding patterns to improve correctness and readability, and keep project definitions clean.

- Boolean parameter syntax: pass boolean parameters using the idiomatic form for the context.
  - Prefer plain boolean argument form (e.g., `-EnableSystemAssignedIdentity $true`) over switch-like `:$true`.
  - For passing `$false` to a boolean parameter in PowerShell test scripts, use the idiomatic `-EnableSystemAssignedIdentity:$false` form.

- Avoid redundant parameters: if a value is already present in `$PSBoundParameters`, don’t re-specify it as a separate named argument.
  - Do: `Test-AzNameAvailability -Type Site @PSBoundParameters`
  - Don’t: `Test-AzNameAvailability -Name $Name -Type Site @PSBoundParameters`

- Correct template-string interpolation: when interpolating variables adjacent to `:` in a double-quoted string, escape the `:` so the variable name is parsed correctly.
  - Do: ``throw "Failed: #$prNumber`: $($_)"``

- Project file cleanliness: don’t add SDK/package references (e.g., `<ItemGroup>` entries or SDK imports) that are not used by any code—remove or justify them.

Apply these checks during review to catch subtle correctness issues (argument binding and interpolation) and to keep scripts/projects maintainable.