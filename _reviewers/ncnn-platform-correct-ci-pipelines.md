---
title: Platform-correct CI Pipelines
description: Ensure CI/CD workflows build, test, and package artifacts in a way that
  is correct for each target platform/architecture—without running irrelevant jobs.
repository: Tencent/ncnn
label: CI/CD
language: Yaml
comments_count: 5
repository_stars: 23205
---

Ensure CI/CD workflows build, test, and package artifacts in a way that is correct for each target platform/architecture—without running irrelevant jobs.

Apply these rules:
1) Prefer dedicated toolchains; avoid hardcoded compiler/arch knobs unless the workflow explicitly documents and matches the toolchain.
2) Scope CI triggers and steps by actual feature/platform support.
   - If a feature is disabled or unsupported on a platform (e.g., Vulkan on esp32), do not trigger or build Vulkan-related paths.
3) Make dependencies explicit per arch and verify artifact completeness.
   - When packaging shared libraries (e.g., Vulkan/MoltenVK on macOS), wire the correct include/library paths for each arch and confirm the library is present during “repair/copy” steps.
4) Handle known toolchain/CI issues by gating, detecting, or temporarily disabling the failing job (and document why) so merges aren’t blocked by unrelated problems.

Concrete example (macOS per-arch Vulkan wiring):
```yaml
# x86_64
CIBW_ENVIRONMENT: |
  NCNN_VULKAN=ON
  Vulkan_INCLUDE_DIR=$GITHUB_WORKSPACE/vulkansdk-macos-1.3.236.0/MoltenVK/include
  Vulkan_LIBRARY=$GITHUB_WORKSPACE/vulkansdk-macos-1.3.236.0/MoltenVK/dylib/macOS/libMoltenVK.dylib
```

Concrete example (path-scoped CI triggering):
```yaml
# Only run when relevant; don’t trigger for Vulkan-only subtree changes if Vulkan is off
on:
  pull_request:
    paths:
      - '.github/workflows/windows-xp-clang.yml'
      - 'CMakeLists.txt'
      - 'src/*'
      # Omit 'src/layer/vulkan/**' if Vulkan support is disabled
```

Quick validation checklist for each platform/arch:
- Does the workflow use the intended toolchain settings for that target?
- Are only supported features being built/tested?
- Are all required external runtime libs correctly pointed to and included in the final artifact?
- If a toolchain job is known to fail in the CI environment, is it gated/disabled with a documented reason?