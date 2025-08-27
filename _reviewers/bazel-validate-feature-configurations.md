---
title: validate feature configurations
description: Always validate that required features are enabled before using feature-dependent
  functionality. Feature flags should be the primary condition for enabling code paths,
  not the presence of related data or parameters.
repository: bazelbuild/bazel
label: Configurations
language: Other
comments_count: 4
repository_stars: 24489
---

Always validate that required features are enabled before using feature-dependent functionality. Feature flags should be the primary condition for enabling code paths, not the presence of related data or parameters.

When implementing feature-dependent behavior:
1. Check feature enablement first, regardless of data availability
2. Provide clear error messages when required features are missing
3. Use feature flags to gate potentially disruptive changes
4. Fail early rather than allowing silent failures or unexpected behavior

Example of proper feature validation:
```starlark
# Good: Check feature first, regardless of data presence
if feature_configuration.is_enabled("cpp_modules"):
    _create_cc_compile_actions_with_cpp20_module(...)
    return

# Also good: Validate required features with clear error messages  
def _check_cpp20_module(ctx, feature_configuration):
    if len(ctx.files.module_interfaces) > 0 and not cc_common.is_enabled(
        feature_configuration = feature_configuration,
        feature_name = "cpp20_module",
    ):
        fail("to use C++20 Modules, the feature cpp20_module must be enabled")

# Avoid: Making feature enablement dependent on data availability
if module_interfaces_sources and feature_configuration.is_enabled("cpp_modules"):
```

This approach ensures consistent behavior, prevents silent failures, and makes feature dependencies explicit and debuggable.