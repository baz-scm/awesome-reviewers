---
title: synchronize declared versions
description: Ensure that version declarations in configuration files accurately reflect
  the versions actually being used in runtime environments. Configuration drift occurs
  when declared versions diverge from deployed versions, leading to inconsistent environments
  and potential deployment issues.
repository: nrwl/nx
label: Configurations
language: Toml
comments_count: 2
repository_stars: 27518
---

Ensure that version declarations in configuration files accurately reflect the versions actually being used in runtime environments. Configuration drift occurs when declared versions diverge from deployed versions, leading to inconsistent environments and potential deployment issues.

When updating configuration files, verify that the specified versions match what's currently deployed or intended for deployment. Avoid situations where configuration declares one version while the system runs another.

Example from mise.toml:
```toml
# Bad: Config says node 24, but runtime uses 20.19
node = "24"  # Actually running 20.19

# Good: Config matches runtime
node = "20.19"  # Matches actual deployed version
```

Before committing configuration changes, validate that:
- Declared versions match intended deployment versions
- Manual installations are replaced with proper configuration management
- Version specifications are consistent across all environment configuration files