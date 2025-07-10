---
title: Consistent API practices
description: Maintain consistency in API design, documentation, and implementation
  across all supported platforms to improve developer experience and reduce friction.
repository: maplibre/maplibre-native
label: API
language: Markdown
comments_count: 6
repository_stars: 1411
---

Maintain consistency in API design, documentation, and implementation across all supported platforms to improve developer experience and reduce friction.

**API Documentation Standards:**
- Use code formatting (backticks) when referencing API methods: `initialize`, `de_initialize`, not initialize, de_initialize
- Use correct capitalization for platform names: iOS, Android (not ios, android)
- Refer to the library consistently as "MapLibre Native" rather than variations like "maplibre-gl"

**Cross-Platform Implementation:**
- Implement new API features across all supported platforms simultaneously when possible
- When implementing features in phases, document the limitation and provide a timeline for complete implementation
- Ensure consistent behavior across platforms for identical API methods

**Example: Cross-platform implementation**
Instead of:
```
// Adding feature only for Android
// platform/android/CHANGELOG.md
* Add support for the [`slice` expression](https://maplibre.org/maplibre-style-spec/expressions/#slice) ([#1113](https://github.com/maplibre/maplibre-native/pull/1133))
```

Prefer:
```
// Implementing across platforms
// CHANGELOG.md
* Add support for the [`slice` expression](https://maplibre.org/maplibre-style-spec/expressions/#slice) across all platforms ([#1133](https://github.com/maplibre/maplibre-native/pull/1133))
```

Following these practices ensures that developers have a consistent experience regardless of which platform they are using and reduces confusion when working with MapLibre Native APIs.