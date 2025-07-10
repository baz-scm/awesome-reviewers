---
title: Accurate documentation references
description: Ensure all code documentation includes appropriate reference links that
  are current and accurate. When porting code or migrating between frameworks, preserve
  all documentation comments with their external references. For API documentation,
  verify that links point to the correct and up-to-date specification documentation.
repository: maplibre/maplibre-native
label: Documentation
language: Kotlin
comments_count: 2
repository_stars: 1411
---

Ensure all code documentation includes appropriate reference links that are current and accurate. When porting code or migrating between frameworks, preserve all documentation comments with their external references. For API documentation, verify that links point to the correct and up-to-date specification documentation.

Example:
```kotlin
/**
 * The circle manager allows to add circles to a map.
 * 
 * Learn more about circle properties in the 
 * [Style specification](https://maplibre.org/maplibre-style-spec/).
 * 
 * For implementation details, see the 
 * [KhronosGroup repository](https://github.com/KhronosGroup/...)
 */
class CircleManager {
    // Implementation
}
```

Maintaining accurate documentation references helps developers find the correct information quickly and prevents them from following outdated or incorrect links. This is especially important when migrating code between frameworks (like Mapbox to MapLibre) or when porting from one language to another (like Groovy to Kotlin).