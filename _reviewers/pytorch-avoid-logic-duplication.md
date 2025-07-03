---
title: Avoid logic duplication
description: Create reusable scripts or functions for common CI operations instead
  of duplicating the same logic across multiple CI files. Duplicated logic leads to
  maintenance challenges and inconsistency when one copy is updated but others aren't.
repository: pytorch/pytorch
label: CI/CD
language: Shell
comments_count: 3
repository_stars: 91169
---

Create reusable scripts or functions for common CI operations instead of duplicating the same logic across multiple CI files. Duplicated logic leads to maintenance challenges and inconsistency when one copy is updated but others aren't.

For example, instead of copying installation steps:
```bash
# Don't do this in multiple places:
export CMAKE_ARGS="-DEXECUTORCH_BUILD_PYBIND=ON -DEXECUTORCH_BUILD_XNNPACK=ON -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON"

# Instead, create a shared script that can be called from multiple places:
# shared_script.sh
setup_executorch_build() {
  export CMAKE_ARGS="-DEXECUTORCH_BUILD_PYBIND=ON -DEXECUTORCH_BUILD_XNNPACK=ON -DEXECUTORCH_BUILD_KERNELS_QUANTIZED=ON"
}
```

This approach is particularly important for installation routines, environment setup, and build configurations across Docker containers. When logic changes are needed, you only need to update in one place. Additionally, clearly document any intentional deviations or environment-specific adjustments to help reviewers understand why certain scripts may differ from the standard pattern.
