---
title: Centralize configuration settings
description: Place configuration settings in centralized, appropriate locations rather
  than duplicating them across multiple files. This improves maintainability by ensuring
  changes only need to be made in one place.
repository: tensorflow/tensorflow
label: Configurations
language: Other
comments_count: 4
repository_stars: 190625
---

Place configuration settings in centralized, appropriate locations rather than duplicating them across multiple files. This improves maintainability by ensuring changes only need to be made in one place.

For build configurations:
- Use the root `.bazelrc` file for settings that apply across multiple configurations
- Place platform-specific configurations in dedicated locations (e.g., platform targets in `tools/toolchains`)
- Use existing configuration hierarchies like `release_base` or `release_cpu_linux` for settings that apply to groups of configurations

For code configurations:
- Consolidate common configuration options into shared variables/lists
- Avoid duplicating the same settings in multiple places

Example:
```python
# Bad: Duplicating settings in multiple environment-specific files
# ci/official/envs/continuous_linux_x86_cpu_py310
# ci/official/envs/continuous_linux_arm64_cpu_py310
# ...

# Good: Single definition in .bazelrc
# .bazelrc
build:release_base --define=some_feature=enabled
build:release_cpu_linux --config=release_base --some_other_setting=value
```

Similarly, for code:
```python
# Bad: Duplicating settings across multiple configuration sets
_DNNL_RUNTIME_THREADPOOL = {
    "#cmakedefine01 DNNL_WITH_SYCL": "#define DNNL_WITH_SYCL 0",
    "#cmakedefine01 DNNL_WITH_LEVEL_ZERO": "#define DNNL_WITH_LEVEL_ZERO 0",
}

_DNNL_RUNTIME_OMP = {
    "#cmakedefine01 DNNL_WITH_SYCL": "#define DNNL_WITH_SYCL 0",
    "#cmakedefine01 DNNL_WITH_LEVEL_ZERO": "#define DNNL_WITH_LEVEL_ZERO 0",
}

# Good: Define common settings once
_CMAKE_COMMON_LIST = {
    "#cmakedefine01 DNNL_WITH_SYCL": "#define DNNL_WITH_SYCL 0",
    "#cmakedefine01 DNNL_WITH_LEVEL_ZERO": "#define DNNL_WITH_LEVEL_ZERO 0",
}

_DNNL_RUNTIME_THREADPOOL = dict(_CMAKE_COMMON_LIST)
_DNNL_RUNTIME_OMP = dict(_CMAKE_COMMON_LIST)
```

This approach reduces maintenance burden and helps prevent inconsistencies that arise when settings are updated in some places but not others.