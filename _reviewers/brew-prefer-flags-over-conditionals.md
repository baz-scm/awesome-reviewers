---
title: Prefer flags over conditionals
description: When implementing environment-specific or version-dependent behavior,
  use feature flags or configuration variables instead of complex conditional logic.
  This approach makes configuration management more maintainable and easier to adjust
  when requirements change.
repository: Homebrew/brew
label: Configurations
language: Other
comments_count: 2
repository_stars: 44168
---

When implementing environment-specific or version-dependent behavior, use feature flags or configuration variables instead of complex conditional logic. This approach makes configuration management more maintainable and easier to adjust when requirements change.

For example, instead of nested conditionals to handle OS version-specific behavior:

```bash
# Before: Complex conditional logic
if [[ "$OS_VERSION" -ge 10.13 && "$OS_VERSION" -lt 14 ]]; then
  # Version-specific behavior
  if [[ condition_check ]]; then
    # Do something
  fi
fi

# After: Using a configuration flag
# In initialization code:
if [[ "$OS_VERSION" -ge 10.13 && "$OS_VERSION" -lt 14 ]]; then
  append_to_cccfg "h"  # Add a feature flag
fi

# In implementation code:
if [[ "${HOMEBREW_CCCFG}" = *h* ]]; then
  # Do version-specific behavior
fi
```

This pattern:
1. Centralizes version checks and keeps implementation clean
2. Makes it obvious when the configuration can be removed
3. Prevents configuration code from running in unsupported environments
4. Creates an explicit interface between environment detection and feature behavior