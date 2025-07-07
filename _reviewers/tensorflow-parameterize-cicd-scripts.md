---
title: Parameterize ci/cd scripts
description: Avoid duplicating CI/CD scripts by leveraging configuration files and
  parameterization instead of creating multiple similar scripts for different platforms
  or build scenarios. Use platform-specific configuration options in shared config
  files (like .bazelrc) or make scripts accept parameters for variant behaviors.
repository: tensorflow/tensorflow
label: CI/CD
language: Shell
comments_count: 2
repository_stars: 190625
---

Avoid duplicating CI/CD scripts by leveraging configuration files and parameterization instead of creating multiple similar scripts for different platforms or build scenarios. Use platform-specific configuration options in shared config files (like .bazelrc) or make scripts accept parameters for variant behaviors.

For example, instead of having separate build scripts for different compilers:
```bash
# Bad: Multiple nearly-identical scripts
build_tf_windows.sh      # For MSVC
build_tf_windows_clang.sh  # For Clang

# Good: Single script with parameters
build_tf_windows.sh --compiler=clang
# Or use configuration files
bazel build --config=win_clang
```

Similarly, for build parameters like job counts, prefer configurable variables with defaults instead of hard-coding:
```bash
# Bad: Hard-coded value
cmake --build . --verbose -j $(nproc)

# Good: Configurable with default
: ${BUILD_NUM_JOBS:=$(nproc)}  # Default to nproc if not set
cmake --build . --verbose -j ${BUILD_NUM_JOBS}
```

This approach improves maintainability, reduces errors from out-of-sync scripts, and provides flexibility for different build environments and debugging scenarios.