---
title: Follow Generated Naming
description: 'Use naming-and-identifier rules that match what AutoRest PowerShell
  generates, and make flag-style parameter typing consistent with the name.


  Apply these rules when editing custom cmdlets:'
repository: Azure/azure-powershell
label: Naming Conventions
language: Other
comments_count: 7
repository_stars: 4762
---

Use naming-and-identifier rules that match what AutoRest PowerShell generates, and make flag-style parameter typing consistent with the name.

Apply these rules when editing custom cmdlets:
1) AutoRest v4 model namespaces are flattened
- Prefer `Microsoft.Azure.PowerShell.Cmdlets.<Product>.Models.*`.
- Do not reference removed versioned namespaces like `Microsoft.Azure.PowerShell.Cmdlets.<Product>.Models.Api<YYYYMMDD>.*`.

2) Preserve AutoRest acronym casing exactly
- Generated model type identifiers may apply lowercasing after known acronyms (example pattern: `...HCINic...` may become `...Hcinic...`).
- Copy the type names from the generated `Models/*.cs` (or use search in `generated/`) rather than guessing.

3) Flag naming implies SwitchParameter
- For parameters named like `-Enable*`, use `[System.Management.Automation.SwitchParameter]` (not `[System.Boolean]`).
- This ensures the three-state behavior: presence enables, `-EnableX:$false` disables, and omission leaves the setting untouched—consistent with existing Az cmdlet patterns.

Example (corrected flag parameter type):
```powershell
function Update-AzSomething {
  param(
    [Parameter()]
    [System.Management.Automation.SwitchParameter]$EnableSystemAssignedIdentity
  )

  if ($PSBoundParameters.ContainsKey('EnableSystemAssignedIdentity')) {
    $identityEnabled = [bool]$EnableSystemAssignedIdentity
    # ... apply enable/disable
  }
}
```