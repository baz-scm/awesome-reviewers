---
title: configuration parameter handling
description: 'When working with configuration parameters and values, follow these
  best practices to ensure maintainable and correct configuration handling:


  1. **Use collections for multiple related values**: When checking against multiple
  related configuration values, use the `in` operator with a list or set rather than
  chaining multiple OR conditions. This makes the...'
repository: servo/servo
label: Configurations
language: Python
comments_count: 2
repository_stars: 32962
---

When working with configuration parameters and values, follow these best practices to ensure maintainable and correct configuration handling:

1. **Use collections for multiple related values**: When checking against multiple related configuration values, use the `in` operator with a list or set rather than chaining multiple OR conditions. This makes the code more readable and easier to maintain when adding new values.

2. **Use tool-specific parameter names**: Different tools may use different parameter names for similar concepts. Always verify and use the correct parameter names for the specific tool being invoked to avoid configuration errors.

Example from the codebase:
```python
# Good: Use 'in' operator for multiple related values
return self.is_custom() and (self.profile in ["production", "production-stripped"])

# Good: Use tool-specific parameter names
# For nextest, use --cargo-profile instead of --profile
args += ["--cargo-profile", build_type.profile]
```

This approach reduces maintenance overhead when adding new configuration values and prevents configuration mismatches when working with different tools that have similar but distinct parameter naming conventions.