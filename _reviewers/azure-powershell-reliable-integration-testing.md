---
title: Reliable Integration Testing
description: 'Write integration/recorded tests so they are deterministic, efficient
  in playback, and self-cleaning.


  Apply these rules:

  1) Deterministic errors → unit tests with mocks'
repository: Azure/azure-powershell
label: Testing
language: Other
comments_count: 6
repository_stars: 4762
---

Write integration/recorded tests so they are deterministic, efficient in playback, and self-cleaning.

Apply these rules:
1) Deterministic errors → unit tests with mocks
- If you’re validating a specific cmdlet error code/exception path, don’t provision real VMs/consume real regional capacity.

2) Integration tests → narrow and service-focused
- Keep any end-to-end (live) scenarios narrowly focused on service integration. Avoid broad coverage that makes every recording depend on fragile infrastructure.

3) Assert the intended success and state changes
- Verify completion to the success state (or the exact expected outcome), not just “not failed”.
- Ensure your “update” test actually changes values, and assert the updated fields.

4) Always clean up in `finally`
- If the test enables protection/deployments/creation, explicitly remove/delete the created resource(s) or protected items in `finally`.

5) Keep recording/playback constants stable
- Don’t use `Get-Date` at runtime for values that are intended to remain constant across recording and playback.

6) Use playback-aware waits
- In recorded tests, prefer `Start-TestSleep -Seconds <n>` over `Start-Sleep` so playback can short-circuit.

Example patterns:
```powershell
# 1) Playback-aware wait
Start-TestSleep -Seconds 5

# 2) Strong success assertion (WhatIf)
Assert-NotNull $result
Assert-NotNull $result.Properties.ProvisioningState
Assert-AreEqual "Succeeded" $result.Properties.ProvisioningState

# 3) Cleanup in finally
try {
  Enable-AzWhatever ...
}
finally {
  # Always remove/delete/disable what you created/enabled
  Remove-AzWhatever -Name $name -ErrorAction SilentlyContinue
}

# 4) Stable recording constant (avoid runtime Now)
$env.RecordDate = (Get-Date -Year 2025 -Month 10 -Day 25 -Hour 17 -Minute 31 -Second 02).ToString('dd-MM-yyyy-h-m-s')
```
