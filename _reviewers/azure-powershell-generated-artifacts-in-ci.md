---
title: Generated Artifacts in CI
description: 'Treat anything under build/generated locations (including auto-generated
  test stubs and generated module mirrors) as write-protected CI outputs: update only
  the custom source files / AutoRest config / build inputs, not the generated artifacts
  themselves. When CI tests fail due to missing environment (e.g., Azure context/SubscriptionId
  in playback),...'
repository: Azure/azure-powershell
label: CI/CD
language: Other
comments_count: 5
repository_stars: 4762
---

Treat anything under build/generated locations (including auto-generated test stubs and generated module mirrors) as write-protected CI outputs: update only the custom source files / AutoRest config / build inputs, not the generated artifacts themselves. When CI tests fail due to missing environment (e.g., Azure context/SubscriptionId in playback), explicitly skip or tag the tests and document the root cause so CI stays green without masking genuine issues.

Example (Pester):
```powershell
It 'UpdateExpanded' -Skip {
    <test-body>
} # CI playback has no Azure context, so SubscriptionId is null

# Or keep the test but mark it live-only
Describe 'New-AzThing' -Tag 'LiveOnly' {
    It 'DoesRealCall' { <...> }
}
```

Example (module exports): ensure `FunctionsToExport` matches the build-generated exports scripts, and rely on the post-merge archive/build steps to populate any checked-in generated mirrors rather than editing generated scripts directly.