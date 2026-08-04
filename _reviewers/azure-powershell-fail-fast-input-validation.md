---
title: Fail Fast Input Validation
description: Validate customer-supplied, security-relevant settings up front and fail
  deterministically with explicit errors when values/config combinations are invalid.
  Add tests that cover most customer-input parameters and assert the expected provisioning/result
  behavior and returned properties.
repository: Azure/azure-powershell
label: Security
language: Other
comments_count: 2
repository_stars: 4762
---

Validate customer-supplied, security-relevant settings up front and fail deterministically with explicit errors when values/config combinations are invalid. Add tests that cover most customer-input parameters and assert the expected provisioning/result behavior and returned properties.

How to apply:
- For any security/network/auth-related option, add explicit checks before proceeding.
- When an invalid configuration is detected, throw immediately with a clear, actionable message (don’t let execution continue or fail later implicitly).
- In tests, exercise the configuration surface: verify both (a) validation outcome (throw vs. success) and (b) returned properties for the parameters you accept.

Example pattern (self-contained):
```powershell
function New-SecureResource {
    param(
        [Parameter(Mandatory)]
        [ValidateSet('Enabled','Disabled')]
        [string]$PublicNetworkAccess,
        # ... other customer inputs ...
        [Parameter(Mandatory)]
        [string]$ResourceName
    )

    if ($PublicNetworkAccess -eq 'Disabled') {
        throw "Invalid configuration: PublicNetworkAccess is 'Disabled' for this operation. Enable it or adjust the request." 
    }

    # proceed with create/update
}

# Tests should assert both behavior and returned fields
# e.g., for valid config:
# $config = New-SecureResource -PublicNetworkAccess 'Enabled' -ResourceName $name
# $config.ProvisioningState | Should -Be 'Succeeded'
```