---
title: Environment-specific configuration values
description: Avoid hardcoding configuration values that should vary between different
  deployment environments (testnet, mainnet, development). Instead, use environment
  variables, configuration files, or conditional logic to handle environment-specific
  settings.
repository: unionlabs/union
label: Configurations
language: Go
comments_count: 2
repository_stars: 74800
---

Avoid hardcoding configuration values that should vary between different deployment environments (testnet, mainnet, development). Instead, use environment variables, configuration files, or conditional logic to handle environment-specific settings.

Hardcoded values like network addresses, token supplies, or feature flags create deployment issues and require code changes for different environments. Use environment variables for optional features and implement proper branching logic for environment-specific constants.

Example of problematic hardcoded values:
```go
const U_BASE_DENOM = "au"
const ONE_U = 1000000000000000000
const UNION_FOUNDATION_MULTI_SIG = "union1cpz5fhesgjcv2q0640uxtyur5ju65av6r8fem0"
```

Better approach using environment variables:
```go
if depinjectOutPath, ok := os.LookupEnv("DEPINJECT_OUT_PATH"); ok {
    os.WriteFile(depinjectOutPath, []byte(dotGraph), 0644)
}
```

Consider implementing environment detection logic or configuration files to manage different settings for testnet versus mainnet deployments.