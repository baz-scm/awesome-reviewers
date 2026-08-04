---
title: Explicit Null Safety Checks
description: 'Ensure null-safety is precise: guard against $null *and* empty results
  *and* blank strings (including blank entries inside arrays/hashtables). Also treat
  “omitted optional/switch parameters” as meaningful (absence != explicit value),
  and structure conditions so short-circuiting prevents null dereferences.'
repository: Azure/azure-powershell
label: Null Handling
language: Other
comments_count: 5
repository_stars: 4762
---

Ensure null-safety is precise: guard against $null *and* empty results *and* blank strings (including blank entries inside arrays/hashtables). Also treat “omitted optional/switch parameters” as meaningful (absence != explicit value), and structure conditions so short-circuiting prevents null dereferences.

Apply these rules:
- Validate strings with `-not [string]::IsNullOrWhiteSpace($x)` before using them as keys/identifiers.
- Validate collections with both `$x` (not null) and a non-zero count when “at least one” is required.
- Validate per-entry items in arrays/maps (reject `''` or whitespace entries), not only the container.
- Use short-circuit boolean logic (`$a -and $b`) so later expressions aren’t evaluated when earlier values are null/invalid.
- For generated/optional switches, understand that “not passing the switch parameter” means “no identity/config” (do not assume prior/default values remain).

Example patterns:
```powershell
# 1) Dictionary/key safety
if ($runtime -and -not [string]::IsNullOrWhiteSpace($runtime.Name)) {
    AddRuntimeToDictionary -Runtime $runtime -RuntimeToVersionDictionary ([Ref]$RuntimeToVersionLinux)
} else {
    $nullKeySafeSkip = $true
}

# 2) Assertions: non-null != useful
Assert-NotNull $crrJob
Assert-True { @($crrJob).Count -gt 0 }

# 3) Per-entry validation inside a collection
foreach ($id in $UserAssignedIdentity) {
    if ([string]::IsNullOrWhiteSpace($id)) {
        throw "At least one user-assigned identity resource ID must be provided via -UserAssignedIdentity."
    }
}

# 4) Switch/optional parameter semantics (absence means “not enabled”)
# If you need identity disabled, omit the switch; if you need it enabled, pass it.
if ($EnableSystemAssignedIdentity) {
    $functionAppDef.IdentityType = 'SystemAssigned'
}
# else: treat as None/no identity configured
```

Adopting this reduces null-key crashes, avoids false positives in tests (empty arrays), and prevents unintended behavior changes caused by omitted optional/switch parameters.