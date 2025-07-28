---
title: Document configuration decisions
description: Add explanatory comments to configuration files that clarify the reasoning
  behind non-obvious choices, feature exclusions, conditional logic, and environment-specific
  settings. This helps future maintainers understand why certain configurations exist
  and prevents accidental modifications.
repository: prisma/prisma
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 42967
---

Add explanatory comments to configuration files that clarify the reasoning behind non-obvious choices, feature exclusions, conditional logic, and environment-specific settings. This helps future maintainers understand why certain configurations exist and prevents accidental modifications.

Key areas requiring documentation:
- Feature flags and their exclusions/inclusions
- Conditional logic in workflows or config files  
- Environment-specific behavior
- Default values that may not be immediately obvious

Example:
```yaml
env:
  # Driver adapters are a special feature, 
  # so in our "normal" tests, we don't enable it yet to keep things separated, 
  # also because they are tested in a separate job.
  EXCLUDED_PREVIEW_FEATURES: 'driverAdapters'
  
  # Exclude relationJoins tests with WASM because the WASM engine does not include the necessary changes yet.
  EXCLUDED_PREVIEW_FEATURES: ${{ matrix.engine-type == 'wasm' && 'relationJoins' || '' }}
```

This practice prevents confusion about configuration intent and reduces the likelihood of breaking changes when configurations are modified.