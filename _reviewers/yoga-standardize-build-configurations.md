---
title: standardize build configurations
description: Ensure build configurations are consistently propagated through all build
  steps and output directories follow standardized patterns. This prevents configuration
  mismatches that can cause deployment issues and makes CI/CD pipelines more reliable.
repository: facebook/yoga
label: CI/CD
language: Other
comments_count: 4
repository_stars: 18255
---

Ensure build configurations are consistently propagated through all build steps and output directories follow standardized patterns. This prevents configuration mismatches that can cause deployment issues and makes CI/CD pipelines more reliable.

Key practices:
- Always propagate configuration parameters to native build systems (e.g., CMAKE_BUILD_TYPE)
- Use consistent output directory patterns across all project types
- Ensure native libraries and build artifacts are properly copied to expected locations
- Align MSBuild targets with the same configuration and platform structure

Example from CMake integration:
```xml
<Exec Command="cmake -S . -B build -DCMAKE_INSTALL_PREFIX=binnative -DCMAKE_BUILD_TYPE='$(Configuration)' &amp;&amp; cmake --build build --target install --config $(Configuration)" />
```

Example for consistent output directories:
```xml
<OutDir>bin\$(PlatformTarget)\$(Configuration)\</OutDir>
```

This standardization ensures that debug/release configurations are properly handled across the entire build pipeline and that all artifacts end up in predictable locations for packaging and deployment.