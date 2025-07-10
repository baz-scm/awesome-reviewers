---
title: Configure platform-specific builds
description: Ensure build and distribution configurations are properly documented
  and optimized for each target platform. For cross-platform projects, explicitly
  document which configuration flags are needed for different build scenarios and
  package manager integrations.
repository: maplibre/maplibre-native
label: Configurations
language: Markdown
comments_count: 4
repository_stars: 1411
---

Ensure build and distribution configurations are properly documented and optimized for each target platform. For cross-platform projects, explicitly document which configuration flags are needed for different build scenarios and package manager integrations.

When configuring build systems like Bazel or CMake, provide complete examples with all required flags for different contexts:

```bash
# Building application directly
bazel build //platform/ios:App --//:renderer=metal --//:use_rust

# Generating project files requires different configuration
bazel run //platform/ios:xcodeproj --@rules_xcodeproj//xcodeproj:extra_common_flags="--//:renderer=metal --//:use_rust"
```

For repository configuration, optimize for platform-specific package managers. Document the preferred distribution method (source vs. binary) for each platform, as different platforms have different requirements:

```bash
# Clone with submodules for complete source access
git clone --recurse-submodules git@github.com:maplibre/maplibre-native.git

# For Apple platforms, source distribution may be preferred for package manager integration
# "Source-only distribution is the preferred way of distribution for Apple platforms now"
```

Test all documented configurations regularly to ensure they remain valid as the codebase evolves, particularly when introducing new dependencies or build targets.