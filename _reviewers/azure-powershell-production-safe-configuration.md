---
title: Production-Safe Configuration
description: 'When changing build/test/configuration files, ensure they are (1) platform-correct
  and (2) production-safe.


  Apply this standard:

  1) Platform-correct environment/config updates'
repository: Azure/azure-powershell
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 4762
---
{% raw %}
When changing build/test/configuration files, ensure they are (1) platform-correct and (2) production-safe.

Apply this standard:
1) Platform-correct environment/config updates
- When appending to env vars that are path lists (e.g., `PSModulePath`), use the platform’s path separator rather than hard-coding `:` or `;`.

2) Gate/disable debug output in production
- Avoid enabling `debug: true` (or equivalent flags like `--debug`) in configs used to generate production artifacts. If needed, enable it only for non-production builds (or via a parameter/flag), because debug output can increase generated code size and noise.

Example (pattern):
```yaml
# Prefer parameters/env gating for debug
steps:
- powershell: |
    Install-Module -Name Pester -RequiredVersion 4.10.1 -Force
    $sep = [System.IO.Path]::PathSeparator
    $env:PSModulePath = $env:PSModulePath + $sep + (pwd).Path
  condition: eq('${{ parameters.testTarget }}', 'Test')
  continueOnError: true
```
```yaml
# In autorest/tspconfig.yaml-like configs: keep debug off unless explicitly requested
options:
  "@azure-tools/typespec-powershell":
    debug: false
```

Checklist before merging:
- Are any env/path operations using OS-specific separators? If yes, switch to a platform-aware approach.
- Are any debug/diagnostic flags enabled by default? If yes, disable or gate them for non-production only.
{% endraw %}
