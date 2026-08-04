---
title: Validated API parameters
description: Treat template parameters and embedded ARM calls as a client-facing API
  contract. Validate inputs and constrain the “request schema” so invalid values can’t
  be sent, and keep compatibility/UX aligned with how the template is consumed.
repository: Azure/azure-quickstart-templates
label: API
language: Other
comments_count: 4
repository_stars: 14846
---

Treat template parameters and embedded ARM calls as a client-facing API contract. Validate inputs and constrain the “request schema” so invalid values can’t be sent, and keep compatibility/UX aligned with how the template is consumed.

Apply:
- Prefer enumerations/allowed lists for values that map to platform-supported modes (e.g., security type).
- Avoid freeform strings for fields that must match a known set of endpoints; instead provide a selectable list (or validate/derive internally). Freeform inputs create incorrect-request failures.
- Define the portal UX contract explicitly (e.g., via uiDefinition) when you need a guided customer flow without forcing re-entry of all existing configuration.
- Pin ARM API versions to ones that work in the target environment(s) (e.g., US Gov) and use the correct intrinsic/method patterns for consistent outputs.

Example (constrained mode + dependent settings):
```bicep
@description('Security type')
@allowed([
  'Standard'
  'TrustedLaunch'
])
param securityType string = 'TrustedLaunch'

@description('Secure Boot (only valid when securityType is TrustedLaunch)')
param secureBoot bool = true
```

Example (use correct method/intrinsic for consistent outputs):
```bicep
value storageKey = storageAccount.listKeys().keys[0].value
```