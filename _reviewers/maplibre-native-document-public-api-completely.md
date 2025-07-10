---
title: Document public API completely
description: 'All public APIs (files in `include/`) must have comprehensive documentation
  using either Doxygen-style or triple-slash comments. Documentation should include:'
repository: maplibre/maplibre-native
label: Documentation
language: Other
comments_count: 5
repository_stars: 1411
---

All public APIs (files in `include/`) must have comprehensive documentation using either Doxygen-style or triple-slash comments. Documentation should include:

1. Class-level documentation describing purpose and usage
2. Method documentation with parameters, return values, and behavior
3. Enum documentation including individual value descriptions
4. Clear indication of public vs private API boundaries

Example:
```cpp
/// This enum defines color blending equations
enum class ColorBlendEquationType : uint8_t {
    Add,            ///< Adds source and destination colors
    Subtract,       ///< Subtracts destination from source color
    ReverseSubtract ///< Subtracts source from destination color
};

/**
 * @brief Adds a polyline to the drawable layer
 * 
 * @param coordinates Geographic coordinates of the polyline
 * @return true if polyline was successfully added, false otherwise
 */
bool addPolyline(const LineString<double>& coordinates);
```

Private implementation files (in `src/`) may have lighter documentation, focusing on complex logic or non-obvious implementations.