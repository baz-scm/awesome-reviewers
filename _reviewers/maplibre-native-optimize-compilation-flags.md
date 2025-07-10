---
title: Optimize compilation flags
description: When optimizing application performance, carefully select compiler flags
  based on your optimization goals. For size-critical applications or accurate size
  measurements, use `-Oz` to prevent aggressive inlining that can distort metrics.
  Additionally, implement compiler caching with tools like `ccache` to significantly
  improve build times in development and...
repository: maplibre/maplibre-native
label: Performance Optimization
language: Yaml
comments_count: 2
repository_stars: 1411
---

When optimizing application performance, carefully select compiler flags based on your optimization goals. For size-critical applications or accurate size measurements, use `-Oz` to prevent aggressive inlining that can distort metrics. Additionally, implement compiler caching with tools like `ccache` to significantly improve build times in development and CI environments.

For CMake-based projects, enable ccache with:
```
# For direct CMake invocation
cmake . -B build -G Ninja -DCMAKE_CXX_COMPILER_LAUNCHER=ccache -DCMAKE_BUILD_TYPE=Release

# For npm/cmake-js projects
npm config set cmake_CMAKE_CXX_COMPILER_LAUNCHER ccache
```

When analyzing binary size with tools like Bloaty, ensure you're comparing equivalent architectures by isolating specific targets:
```
# Example extracting ARM64 binary from multi-architecture framework
cp MapLibre.xcframework/ios-arm64/MapLibre.framework/MapLibre MapLibre_arm64
```

These practices ensure both efficient development cycles and optimized production artifacts.