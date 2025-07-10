---
title: Descriptive named constants
description: Replace magic numbers and unclear variables with descriptive named constants
  using appropriate naming conventions. This improves code readability, maintainability,
  and prevents errors.
repository: maplibre/maplibre-native
label: Naming Conventions
language: C++
comments_count: 4
repository_stars: 1411
---

Replace magic numbers and unclear variables with descriptive named constants using appropriate naming conventions. This improves code readability, maintainability, and prevents errors.

Guidelines:
1. Use `constexpr` variables with descriptive names instead of raw numbers
2. Follow camelCase naming for constants (reserve ALL_CAPS for macros only)
3. Include comments explaining the origin of special values when relevant
4. Use meaningful names for array indices and limits

Example:
```cpp
// Poor readability:
resource.dataRange = std::make_pair<uint64_t, uint64_t>(0, 16383);

// Improved with named constants:
// https://github.com/protomaps/PMTiles/blob/main/spec/v3/spec.md#3-header
constexpr uint64_t pmtilesHeaderOffset = 0;
constexpr uint64_t pmtilesHeaderMaxSize = 16383;
resource.dataRange = std::make_pair(pmtilesHeaderOffset, pmtilesHeaderMaxSize);

// Array indices should have names:
bool propUpdateFlags[4] = {propertiesUpdated, propertiesUpdated, propertiesUpdated, propertiesUpdated};
// Better:
constexpr size_t linePropFlagIndex = 0;
bool propUpdateFlags[4] = {/*...*/};
if (!linePropertiesBuffer || propUpdateFlags[linePropFlagIndex]) {
    // ...
}

// Context for numeric parameters:
Context::Context(RendererBackend& backend_)
    : gfx::Context(16), // TODO
// Better:
constexpr uint32_t maximumVertexBindingCount = 16;
Context::Context(RendererBackend& backend_)
    : gfx::Context(maximumVertexBindingCount),
```

This approach makes code self-documenting, easier to maintain, and less prone to errors when numbers need to be updated.