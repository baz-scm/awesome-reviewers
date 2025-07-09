---
title: Centralize configuration values
description: Hardcoded configuration values scattered throughout codebases create
  maintenance burdens and increase the risk of inconsistency. Define configuration
  values (like versions, paths, and feature flags) in a single location and reference
  them elsewhere.
repository: ghostty-org/ghostty
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 32864
---

Hardcoded configuration values scattered throughout codebases create maintenance burdens and increase the risk of inconsistency. Define configuration values (like versions, paths, and feature flags) in a single location and reference them elsewhere.

For build systems and CI workflows:
- Extract repeated values like dependency versions into variables at the top level
- Use environment variables or central config files rather than duplicating values
- Document the purpose and constraints of configuration variables

Example:
```yaml
# GOOD: Define version at the top level
env:
  ZIG_VERSION: "0.13.0"

jobs:
  build:
    steps:
      - name: Setup Zig
        uses: goto-bus-stop/setup-zig@v2
        with:
          version: ${{ env.ZIG_VERSION }}
          
  test:
    steps:
      - name: Build with Zig
        run: zig-${ZIG_VERSION} build test
```

This approach makes version updates simpler, reduces errors from inconsistent values, and makes configuration more maintainable. For complex configurations, consider creating a dedicated configuration module that can be imported by other components of the system.